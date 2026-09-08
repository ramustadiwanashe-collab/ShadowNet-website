# Auto-generated learning notes helpers for ShadowNet.
# Topic lists remain in app.py; this module adds a useful note for every topic.

LANGUAGE_FOUNDATIONS = {
    'python': {
        'focus': 'Python emphasizes readable syntax, dynamic typing, a large standard library, and rapid iteration.',
        'example': 'def greet(name):\n    return f"Hello, {name}"\n\nprint(greet("ShadowNet"))',
    },
    'html': {
        'focus': 'HTML defines document structure and meaning. Good HTML is semantic, accessible, valid, and easy for browsers and assistive technology to interpret.',
        'example': '<main>\n  <h1>ShadowNet</h1>\n  <p>Learn to build software.</p>\n</main>',
    },
    'css': {
        'focus': 'CSS controls presentation and layout. Prefer predictable layout primitives, reusable values, responsive rules, and accessible contrast.',
        'example': '.card {\n  display: grid;\n  gap: 1rem;\n  padding: 1.25rem;\n  border-radius: 1rem;\n}',
    },
    'javascript': {
        'focus': 'JavaScript provides behavior in the browser and can also run on servers. Modern code relies heavily on modules, promises, events, and explicit state.',
        'example': 'const button = document.querySelector("button");\nbutton.addEventListener("click", () => {\n  console.log("Clicked");\n});',
    },
    'cpp': {
        'focus': 'Modern C++ combines low-level control with high-level abstractions. Ownership, lifetime, value semantics, and the standard library are central concepts.',
        'example': '#include <iostream>\n#include <string>\n\nint main() {\n    std::string name = "ShadowNet";\n    std::cout << name << "\\n";\n}',
    },
    'java': {
        'focus': 'Java is statically typed and object-oriented, with automatic memory management and a mature JVM ecosystem.',
        'example': 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("ShadowNet");\n    }\n}',
    },
    'sql': {
        'focus': 'SQL describes operations on relational data. Think in terms of sets, keys, constraints, joins, transactions, and query plans.',
        'example': 'SELECT name, email\nFROM users\nWHERE active = TRUE\nORDER BY name;',
    },
    'bash': {
        'focus': 'Bash is a command interpreter and scripting environment. Robust scripts validate inputs, quote variables, check exit status, and make side effects explicit.',
        'example': '#!/usr/bin/env bash\nset -euo pipefail\nname="ShadowNet"\nprintf "Hello %s\\n" "$name"',
    },
}

LEVEL_ADVICE = {
    'beginner': 'Build the mental model first. Trace small examples by hand, then change one thing at a time and observe the result.',
    'intermediate': 'Connect the concept to real programs. Pay attention to interfaces, errors, testing, and maintainability rather than only syntax.',
    'semipro': 'Think like an engineer: define constraints, measure behavior, choose abstractions deliberately, and consider security, performance, and operations.',
    'premium': 'Professional work requires trade-offs, observability, failure handling, security boundaries, and architecture that remains maintainable as the system grows.',
}

# Focused explanations for common concepts. Topics not listed here still receive a
# tailored note using the language and topic name instead of an empty placeholder.
CONCEPTS = {
    'variables and data types': 'A variable binds a name to a value. Learn the language\'s primitive types, collection types, mutability rules, conversions, and how type errors appear.',
    'conditionals': 'Conditionals choose a path based on a boolean expression. Keep branches simple, handle boundary cases, and avoid duplicating large blocks of logic.',
    'loops': 'Loops repeat work over a sequence or while a condition remains true. Understand initialization, termination, iteration state, and how to avoid infinite loops.',
    'functions': 'Functions package behavior behind a name and interface. Prefer small functions with clear inputs, outputs, and one responsibility.',
    'classes and objects': 'A class describes state and behavior while an object is a concrete instance. Keep responsibilities cohesive and expose only the interface callers need.',
    'object-oriented programming': 'OOP organizes behavior around objects and their responsibilities. Learn encapsulation, composition, inheritance, and polymorphism, but prefer composition when it reduces coupling.',
    'exceptions': 'Exceptions represent failures that should be handled separately from the normal path. Catch only what you can handle and preserve useful error context.',
    'files and exceptions': 'File I/O crosses a resource boundary, so handle missing files, permissions, encoding, and cleanup. Pair file operations with explicit error handling.',
    'semantic html': 'Semantic elements such as main, nav, article, section, header, and footer communicate document meaning. They improve accessibility and maintainability.',
    'accessibility basics': 'Accessible interfaces work with keyboards, screen readers, zoom, and different input methods. Use semantic controls, labels, focus states, and sufficient contrast.',
    'selectors': 'Selectors determine which elements receive CSS declarations. Prefer simple, maintainable selectors and avoid unnecessary specificity.',
    'box model': 'Every element has content, padding, border, and margin. box-sizing: border-box usually makes width calculations easier to reason about.',
    'flexbox': 'Flexbox lays out items along one primary axis. Use it for rows, columns, alignment, spacing, and components whose size can adapt to available space.',
    'grid': 'CSS Grid handles two-dimensional layouts. Define columns and rows intentionally, then use gaps and responsive tracks rather than brittle pixel positioning.',
    'responsive design': 'Responsive design adapts layout to viewport and content constraints. Use flexible units, media or container queries, and test intermediate widths.',
    'promises and async/await': 'Promises represent future completion or failure. async/await makes asynchronous control flow easier to read, but errors still need explicit handling.',
    'dom basics': 'The DOM is the browser\'s object representation of the document. Query elements, change properties deliberately, and keep DOM work separate from application state where possible.',
    'templates': 'Templates combine reusable structure with data. Keep presentation logic simple and validate or escape untrusted values before rendering.',
    'rest apis': 'A REST-style API exposes resources through HTTP methods and status codes. Design predictable request and response shapes and validate inputs at the boundary.',
    'smart pointers': 'Smart pointers express ownership and automate resource cleanup. unique_ptr is the default ownership tool; shared_ptr is for genuinely shared ownership.',
    'raii': 'RAII ties resource lifetime to object lifetime. Constructors acquire resources and destructors release them, making cleanup deterministic.',
    'move semantics': 'Move semantics transfers resources instead of copying them when an object can safely give up its state. Understand rvalues, std::move, and moved-from object validity.',
    'generics': 'Generics let Java code work with types while retaining compile-time checking. Use bounded type parameters when an algorithm needs specific capabilities.',
    'streams': 'Streams model data-processing pipelines with operations such as filter, map, and collect. Use them for clarity, not simply to make code shorter.',
    'lambdas': 'Lambdas create small function values inline. Keep captured state minimal and make the lambda readable enough that its behavior is obvious.',
    'select': 'SELECT reads rows and expressions from one or more sources. Select only the columns you need and add a clear WHERE clause when filtering is required.',
    'where': 'WHERE filters rows before grouping. Use precise predicates, understand NULL semantics, and parameterize values in application code.',
    'joins': 'Joins combine related rows using matching keys or conditions. Start with the relationship you need, then verify cardinality so a join does not unexpectedly multiply rows.',
    'indexes': 'Indexes accelerate specific access patterns at the cost of storage and write overhead. Index columns used by real filters, joins, and ordering patterns, then verify with a query plan.',
    'transactions': 'Transactions group related database operations into an atomic unit. Understand commit, rollback, isolation, and what concurrency behavior your database provides.',
    'terminal navigation': 'Learn pwd, ls, cd, and tab completion first. A strong command-line workflow comes from combining small commands rather than memorizing huge commands.',
    'permissions': 'Linux permissions separate owner, group, and other access. Understand read, write, execute, chmod, chown, and least privilege before automating changes.',
    'pipes and redirection': 'Pipes send one command\'s output to another command. Redirection controls standard input, output, and errors; always quote paths and inspect destructive commands before running them.',
    'shell scripts': 'Shell scripts automate repeatable command sequences. Use a clear interpreter line, quote variables, check failures, and keep complex business logic in a language better suited to it.',
    'ssh': 'SSH provides authenticated encrypted remote access. Use keys, verify host identity, restrict accounts, and avoid exposing unnecessary services.',
}


def make_note(slug, topic, level):
    foundation = LANGUAGE_FOUNDATIONS[slug]
    key = topic.lower()
    concept = CONCEPTS.get(key)
    if concept:
        core = concept
    else:
        core = f'{topic} is a {level}-level {foundation["focus"].split(".")[0].lower()} concept. Study what the concept does, what inputs and outputs it has, common failure cases, and how it fits into a complete program.'
    practice = f'Practice: build a tiny {slug} exercise that uses “{topic}”, test the normal case and at least two edge cases, then refactor it once.'
    return {
        'title': topic,
        'level': level,
        'summary': core,
        'key_points': [
            foundation['focus'],
            LEVEL_ADVICE[level],
            'Do not memorize syntax in isolation. Trace the data or control flow and verify the result with a small test.',
        ],
        'example': foundation['example'],
        'practice': practice,
    }
