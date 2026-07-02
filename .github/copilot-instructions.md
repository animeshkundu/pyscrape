# GitHub Copilot Instructions — pyscrape

## Project overview
pyscrape is a Python 3 web scraping library. Default mode uses `requests + lxml`
(no browser). JS rendering is optional via `pyscrape[js]` (Playwright / Chromium).

## Coding conventions
- Python 3.9+; use `from __future__ import annotations` in every module.
- `ruff` for linting and formatting (line-length 100, target py39).
- Type hints on all public methods.

## Critical design rules

### Browser-free default
`pyscrape.driver` and `pyscrape.session` must **never** import `playwright`.
All Playwright code is isolated in `pyscrape.js_driver`.

### Import guard for PlaywrightDriver
`PlaywrightDriver.__init__` raises `ImportError` (with a pip install hint)
when the `playwright` package is absent. Do not bypass this guard.

### Test structure
- Default tests: `tests/test_driver.py`, `tests/test_session.py`, `tests/test_server.py`
  — run with `pytest tests/ --ignore=tests/test_js_driver.py`.
- Playwright tests: `tests/test_js_driver.py` — separate CI job only.

### Release / Pages workflows
`release.yml` and `docs.yml` are **prepared but must not be triggered**
without explicit owner instruction.

### License
No LICENSE file exists. **Do not add one** without explicit approval.

## Build and test

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check .
pytest tests/ --ignore=tests/test_js_driver.py -v
```
