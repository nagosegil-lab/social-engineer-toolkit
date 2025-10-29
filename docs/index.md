## Social-Engineer Toolkit (SET) — API and Usage Documentation

- **Audience**: security engineers, red-teamers, and developers working on SET
- **Scope**: comprehensive, auto-generated API docs for Python modules under `src`, plus human-written guides with safe examples
- **Legal & ethical notice**: Use SET only on systems you own or are explicitly authorized to assess. Misuse may be illegal. All examples here are designed for safe, non-destructive, and educational purposes.

## What’s included
- **API Reference (HTML)**: browse modules, classes, and functions extracted from the codebase
  - Open: [HTML API Reference](./api/index.html) — optional, requires generator
- **API Reference (static Markdown)**: import-free AST docs for all Python modules
  - Open: [Static API Reference](./api_md/index.md)
- **Guides**
  - [Usage Guide](./usage.md): install, run, and maintain SET responsibly
  - [Examples](./examples.md): safe, copy-pasteable snippets for common utilities

## Getting started (quick)
- Python 3.8+
- Install runtime deps:
  ```bash
  pip3 install -r requirements.txt
  ```
- Run the interactive console (requires elevated privileges on POSIX):
  ```bash
  sudo ./setoolkit
  ```

## Generating API docs locally (HTML)
- Install doc tooling:
  ```bash
  pip3 install -r docs/requirements.txt
  ```
- Generate HTML docs to `docs/api/`:
  ```bash
  ./docs/generate_api_docs.sh
  ```
- Then open `docs/api/index.html` in a browser.

## Repo structure (high-level)
- `src/core/`: core utilities, menus, helpers, web server/bootstrap logic
- `src/webattack/`, `src/phishing/`, `src/html/`: feature modules and helpers
- `src/payloads/`: payload preparation helpers and artifacts
- `seautomate`, `seproxy`, `seupdate`, `setoolkit`: top-level CLI entry points

## How to read the API reference
- Navigate by module (e.g., `src.core.setcore`).
- Each module page lists public functions and classes with signatures. Where docstrings exist, descriptions are shown. When not present, use names, parameters, and call sites in the codebase as a guide.

## Contributing documentation
- Prefer adding or improving docstrings next to code. The API pages are regenerated from source, so improvements appear automatically.
- Keep examples safe, reproducible, and scoped to authorized/test environments only.
