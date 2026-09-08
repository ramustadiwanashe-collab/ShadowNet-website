import os
import secrets
import sqlite3
import json

import urllib.request
import urllib.error
from functools import wraps

from flask import Flask, abort, flash, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "shadownet.db")

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "change-me-in-production"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1",
    MAX_CONTENT_LENGTH=1 * 1024 * 1024,
)

LANGUAGES = {
    "python": {
        "name": "Python",
        "icon": "🐍",
        "description": "Automation, web development, scripting, data and AI foundations.",
        "color": "cyan",
    },
    "html": {
        "name": "HTML",
        "icon": "🌐",
        "description": "Build the structure and semantics of modern websites.",
        "color": "orange",
    },
    "css": {
        "name": "CSS",
        "icon": "🎨",
        "description": "Create responsive, accessible and polished interfaces.",
        "color": "blue",
    },
    "javascript": {
        "name": "JavaScript",
        "icon": "⚡",
        "description": "Add behavior, interactivity and full-stack web capabilities.",
        "color": "yellow",
    },
    "cpp": {
        "name": "C++",
        "icon": "⚙️",
        "description": "Systems programming, performance, algorithms and game development.",
        "color": "purple",
    },
    "java": {
        "name": "Java",
        "icon": "☕",
        "description": "Object-oriented programming, backend systems and enterprise apps.",
        "color": "red",
    },
    "sql": {
        "name": "SQL",
        "icon": "🗄️",
        "description": "Query, model and manage relational data.",
        "color": "green",
    },
    "bash": {
        "name": "Bash / Linux",
        "icon": "🐧",
        "description": "Terminal workflows, automation, scripting and Linux fundamentals.",
        "color": "pink",
    },
}

TOPICS = {
    "python": {
        "beginner": ["What Python is", "Variables and data types", "Operators", "Conditionals", "Loops", "Functions", "Lists, tuples and dictionaries", "Files and exceptions"],
        "intermediate": ["Modules and packages", "Object-oriented programming", "Virtual environments", "Decorators", "Iterators and generators", "Testing with pytest", "APIs with requests", "Flask fundamentals"],
        "semipro": ["Project architecture", "Async programming", "Type hints", "Database integration", "Authentication patterns", "Performance profiling", "Production deployment", "Secure Python practices"],
        "premium": ["Advanced concurrency patterns", "Production-grade architecture", "Advanced security engineering", "Distributed Python systems", "Performance optimization case studies"],
    },
    "html": {
        "beginner": ["Document structure", "Headings and paragraphs", "Links and images", "Lists and tables", "Forms", "Semantic HTML", "Accessibility basics", "HTML validation"],
        "intermediate": ["Advanced forms", "Media elements", "Metadata and SEO", "ARIA patterns", "Templates", "Web components basics", "Performance-friendly markup", "Progressive enhancement"],
        "semipro": ["Accessible design systems", "Component architecture", "SEO strategy", "Security-focused markup", "Complex forms and validation", "Web platform APIs"],
        "premium": ["Enterprise component systems", "Advanced accessibility audits", "High-performance document architecture", "Complex web platform integration"],
    },
    "css": {
        "beginner": ["Selectors", "Colors and typography", "Box model", "Display and positioning", "Flexbox", "Grid", "Responsive design", "Transitions"],
        "intermediate": ["Custom properties", "Advanced Grid", "Animations", "Container queries", "Responsive component patterns", "Layering and stacking contexts", "Accessibility in CSS", "Modern reset strategies"],
        "semipro": ["Design tokens", "Scalable CSS architecture", "Advanced layout systems", "Performance", "Theming", "Complex motion systems", "Component isolation"],
        "premium": ["Design-system architecture", "Advanced rendering performance", "Large-scale theming", "Production UI architecture"],
    },
    "javascript": {
        "beginner": ["Syntax and variables", "Functions", "Arrays and objects", "DOM basics", "Events", "Forms", "Fetch basics", "Modules"],
        "intermediate": ["Promises and async/await", "Classes", "Closures", "Error handling", "Local storage", "REST APIs", "Tooling with npm", "Testing"],
        "semipro": ["Architecture patterns", "State management", "Web performance", "Security", "WebSockets", "Node.js backend", "TypeScript transition", "Production debugging"],
        "premium": ["Large-scale frontend architecture", "Advanced Node.js systems", "Performance engineering", "Security engineering case studies"],
    },
    "cpp": {
        "beginner": ["Syntax and compilation", "Variables and types", "Control flow", "Functions", "Arrays and strings", "References", "Classes", "STL basics"],
        "intermediate": ["Templates", "RAII", "Smart pointers", "Move semantics", "STL algorithms", "Exception safety", "File I/O", "Build systems"],
        "semipro": ["Modern C++ patterns", "Concurrency", "Memory models", "Profiling", "CMake architecture", "Systems design", "Low-level optimization"],
        "premium": ["Advanced concurrency", "Lock-free programming", "ABI and binary compatibility", "High-performance systems architecture"],
    },
    "java": {
        "beginner": ["Java syntax", "Types and operators", "Control flow", "Methods", "Arrays", "Classes and objects", "Exceptions", "Collections"],
        "intermediate": ["Generics", "Streams", "Lambdas", "Concurrency", "JVM basics", "Maven/Gradle", "REST APIs", "Testing"],
        "semipro": ["Spring Boot architecture", "JVM profiling", "Distributed systems", "Security", "Database tuning", "Caching", "Production observability"],
        "premium": ["Advanced JVM tuning", "Distributed transaction design", "Enterprise security architecture", "High-scale backend systems"],
    },
    "sql": {
        "beginner": ["Tables and rows", "SELECT", "WHERE", "ORDER BY", "INSERT", "UPDATE", "DELETE", "Basic joins"],
        "intermediate": ["Aggregations", "Subqueries", "Indexes", "Constraints", "Views", "Transactions", "Window functions", "Query plans"],
        "semipro": ["Schema architecture", "Advanced indexing", "Performance tuning", "Concurrency", "Partitioning", "Data integrity", "Production migrations"],
        "premium": ["Large-scale query optimization", "Advanced relational architecture", "High-availability strategies", "Data platform case studies"],
    },
    "bash": {
        "beginner": ["Terminal navigation", "Files and directories", "Permissions", "Pipes and redirection", "Variables", "Shell scripts", "Package management", "Processes"],
        "intermediate": ["Text processing", "Functions", "Cron jobs", "SSH", "Environment management", "Networking commands", "Logs", "Shell safety"],
        "semipro": ["Automation architecture", "Hardening", "Deployment scripts", "CI/CD shell workflows", "System diagnostics", "Container workflows"],
        "premium": ["Advanced Linux automation", "Production hardening", "Infrastructure scripting patterns", "Incident-response tooling"],
    },
}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS premium_access (
            user_id INTEGER PRIMARY KEY,
            active INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )
    db.commit()
    db.close()


@app.context_processor
def inject_globals():
    return {"languages": LANGUAGES, "current_user": current_user()}


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return get_db().execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,)).fetchone()


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Please sign in to access ShadowNet.", "error")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapper


def csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


app.jinja_env.globals["csrf_token"] = csrf_token


def validate_csrf():
    token = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token")
    expected = session.get("csrf_token")
    if not token or not expected or not secrets.compare_digest(token, expected):
        abort(400, description="Invalid CSRF token")


@app.route("/")
def index():
    if current_user():
        return redirect(url_for("welcome"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user():
        return redirect(url_for("welcome"))
    if request.method == "POST":
        validate_csrf()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if len(username) < 2 or len(username) > 50:
            flash("Use a username between 2 and 50 characters.", "error")
        elif "@" not in email or len(email) > 160:
            flash("Enter a valid email address.", "error")
        elif len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        else:
            db = get_db()
            try:
                cur = db.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)),
                )
                db.execute("INSERT INTO premium_access (user_id, active) VALUES (?, 0)", (cur.lastrowid,))
                db.commit()
                flash("Account created. Welcome to ShadowNet.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("That email is already registered.", "error")
    return render_template("auth.html", mode="register", title="Create account")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user():
        return redirect(url_for("welcome"))
    if request.method == "POST":
        validate_csrf()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["csrf_token"] = secrets.token_urlsafe(32)
            return redirect(url_for("welcome"))
    return render_template("auth.html", mode="login", title="Sign in")


@app.post("/logout")
@login_required
def logout():
    validate_csrf()
    session.clear()
    return redirect(url_for("login"))


@app.route("/welcome")
@login_required
def welcome():
    return render_template("welcome.html")


@app.route("/app")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/language/<slug>")
@login_required
def language(slug):
    if slug not in LANGUAGES:
        abort(404)
    return render_template("language.html", language=LANGUAGES[slug], slug=slug, topic_data=TOPICS[slug])


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.0")
OPENAI_API_URL = os.environ.get("OPENAI_API_URL", "https://api.openai.com/v1/responses")


def call_openai(message, username):
    if not OPENAI_API_KEY:
        return None

    system_prompt = (
        "You are ShadowBot, the official AI coding assistant inside ShadowNet, a learning platform founded in 2017. "
        "Teach programming clearly from beginner through professional level. Support Python, HTML, CSS, JavaScript, "
        "C++, Java, SQL, Bash/Linux and general software engineering. Give practical explanations and safe code examples. "
        "For cybersecurity, stay within authorized defensive education, secure coding, CTF and lab contexts. "
        "Do not claim that premium ShadowNet notes are included unless the user has premium access. "
        f"The learner's account name is {username}."
    )
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    }
    req = urllib.request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            body = json.loads(response.read().decode("utf-8"))
        output_text = body.get("output_text")
        if output_text:
            return output_text.strip()
        for item in body.get("output", []):
            for content in item.get("content", []):
                if content.get("type") == "output_text" and content.get("text"):
                    return content["text"].strip()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    return None


@app.post("/api/assistant")
@login_required
def assistant():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message or len(message) > 2000:
        return jsonify({"reply": "Send a coding question up to 2,000 characters."}), 400

    user = current_user()
    reply = call_openai(message, user["username"]) if user else None
    if reply:
        return jsonify({"reply": reply, "model": OPENAI_MODEL})

    return jsonify({
        "reply": "ShadowBot is not connected to the AI service yet. Add OPENAI_API_KEY to the server environment, then restart ShadowNet.",
        "model": OPENAI_MODEL,
        "configured": bool(OPENAI_API_KEY),
    })


@app.route("/privacy")
def privacy():
    return render_template("legal.html", page="privacy", title="Privacy Policy")


@app.route("/terms")
def terms():
    return render_template("legal.html", page="terms", title="Terms & Conditions")


@app.errorhandler(400)
def bad_request(e):
    return render_template("error.html", code=400, message=e.description), 400


@app.errorhandler(404)
def not_found(_e):
    return render_template("error.html", code=404, message="Page not found."), 404


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("FLASK_DEBUG") == "1")
else:
    init_db()
