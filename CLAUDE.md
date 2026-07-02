# CLAUDE.md — pyscrape agentic-dev context

## Project overview

**pyscrape** is a lightweight Python 3 web scraping library.

- **Default mode**: `requests` + `lxml` — no browser dependency.
- **JS mode** (`pyscrape[js]` extra): Playwright (Chromium) — full JS rendering.
- HTTP scraping server (`pyrun`) built with Flask.

## Repository layout

```
pyscrape/
├── __init__.py      Public API + CLI entry points (cli, http)
├── driver.py        RequestsDriver  — default HTTP driver (requests + lxml)
├── js_driver.py     PlaywrightDriver — optional JS driver (import-guarded)
├── session.py       Session          — high-level, driver-agnostic
├── server.py        Flask HTTP scraping server
└── mixins.py        SelectionMixin / WaitMixin helpers

tests/
├── conftest.py      Fixtures (local fixture HTTP server)
├── test_driver.py   RequestsDriver unit tests
├── test_session.py  Session unit tests
├── test_server.py   Flask server E2E tests
└── test_js_driver.py Playwright tests (skipped without [js])

.github/workflows/
├── ci.yml           Lint + unit/E2E + Playwright CI
├── release.yml      PREPARED: tag-triggered PyPI release (not triggered)
└── docs.yml         PREPARED: manual Pages deploy (not enabled)
```

## Build and test commands

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Lint
ruff check .
ruff format --check .

# Tests (no browser)
pytest tests/ --ignore=tests/test_js_driver.py -v

# Tests (with Playwright)
pip install -e ".[dev,js]" && playwright install chromium
pytest tests/ -v
```

## Key design rules

1. **Default mode must NOT import playwright**. The `pyscrape.driver` and
   `pyscrape.session` modules must remain import-clean without any optional extras.
2. **PlaywrightDriver raises `ImportError`** with a clear pip install hint when
   `playwright` is not installed. Never let it fail with a bare `ModuleNotFoundError`.
3. **No LICENSE file** — do not add one without explicit owner approval.
   Note in PRs when this blocks PyPI publishing.
4. **Release and Pages workflows are PREPARED but not triggered** — they require
   human activation (add license, configure PyPI env, enable Pages).
5. Keep the Flask server stateless; each request creates a fresh `Session`.

## Dependency disposition (v2)

| Package | Status | Disposition |
|---|---|---|
| `webkit-server` | Dead | Removed → Playwright (optional) |
| `xvfbwrapper` | Dead | Removed |
| `futures` | Py2 backport | Removed (`concurrent.futures` is built-in) |
| `tornado` | Alive | Replaced by Flask |
| `fake-useragent` | Alive | Removed (fixed UA in RequestsDriver) |
