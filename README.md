# ShadowNet

ShadowNet is a Flask-based coding learning website concept for a brand founded in 2017.

## Included

- Sign in and account creation.
- Password hashing with Werkzeug.
- Session-based authentication.
- CSRF protection on form actions.
- Five-second welcome loading screen after sign-in.
- Coding paths for Python, HTML, CSS, JavaScript, C++, Java, SQL and Bash/Linux.
- Beginner, intermediate and semi-pro topic tracks.
- Premium professional notes with a payment integration placeholder.
- ShadowBot assistant UI and a simple local assistant API fallback.
- Privacy Policy and Terms & Conditions pages.
- Responsive cyber-tech visual design inspired by the supplied reference image.

## Deployment

See `DEPLOYMENT.md` for the complete local, GitHub, Render, AI, database, and production checklist.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Production

Set `SECRET_KEY` to a long random value. Set `COOKIE_SECURE=1`. Run behind HTTPS. The default database is SQLite, which is convenient for a prototype or low-traffic deployment. For higher traffic, move users and premium state to PostgreSQL.

## Premium payments

The Professional button is intentionally a safe integration placeholder. Connect a provider such as Stripe Checkout, verify payment events server-side, then set `premium_access.active=1` for the user. Do not store card details in this app.

## AI assistant

The included `/api/assistant` route is a local rule-based fallback so the demo works without an API key. To use a real model, replace that route with your chosen provider, keep the API key on the server, and add request limits and abuse protection.

## Brand

Company name: ShadowNet.
Founded: 2017.


## ShadowBot AI

Set `OPENAI_API_KEY` as a server environment variable. The assistant sends requests through the OpenAI Responses API. Set `OPENAI_MODEL` to the model ID available to your API project. The default is `gpt-5.0` as requested. If that model is not enabled for your API project, set `OPENAI_MODEL` to an available model ID. Do not expose the API key in browser JavaScript.
