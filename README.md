# pyscrape

[![CI](https://github.com/animeshkundu/pyscrape/actions/workflows/ci.yml/badge.svg)](https://github.com/animeshkundu/pyscrape/actions/workflows/ci.yml)

A lightweight **Python 3** web scraping library with an optional Playwright backend for
JavaScript rendering.

| Mode | Dependency | Install |
|---|---|---|
| **Default** (requests + lxml) | No browser | `pip install pyscrape` |
| **JS** (Playwright / Chromium) | Chromium browser | `pip install 'pyscrape[js]'` then `playwright install chromium` |

> **⚠️ Disposition note — revive vs preserve vs archive**
>
> The original pyscrape relied on `webkit-server` + `xvfbwrapper` (both abandoned) and
> the Python 2 `futures` backport. Those are **removed** in v2. The rendering engine has
> been replaced with a **PLAYWRIGHT-OPTIONAL** design: the default path is pure
> `requests + lxml`; JS rendering is an opt-in `[js]` extra backed by Playwright
> (Chromium). This is the **revive** disposition — the repo is kept alive and useful
> on modern Python. An alternative **archive** disposition (freeze at last working
> commit with a tombstone README) remains available if the owner prefers.
>
> **License**: no `LICENSE` file exists in this repository. The old `setup.py`
> mentioned "Apache 2.0" but no file was ever committed. **The repository owner must
> choose and commit a license before the package can be published to PyPI.**

---

## Installation

```bash
# Default — no browser dependency
pip install pyscrape

# With JavaScript rendering (Playwright / Chromium)
pip install 'pyscrape[js]'
playwright install chromium
```

## Python API

### Default mode (requests + lxml)

```python
from pyscrape import Session

s = Session()
s.visit("https://example.com")
print(s.body())                   # raw HTML string
doc = s.document()                # lxml HtmlElement
links = doc.cssselect("a[href]")
```

### JS mode (Playwright)

```python
from pyscrape.js_driver import PlaywrightDriver

with PlaywrightDriver(headless=True) as driver:
    driver.visit("https://example.com")
    print(driver.body())          # fully JS-rendered HTML
```

A clear `ImportError` with pip install instructions is raised if you use
`PlaywrightDriver` without the `[js]` extra.

## CLI

```bash
# Default mode
pyscrape https://example.com

# JS rendering (requires pyscrape[js])
pyscrape --js https://example.com
```

## HTTP server

```bash
# Start the scraping API server (default port 1234)
pyrun --port 1234

# Health check
curl http://localhost:1234/ping

# Scrape via GET
curl "http://localhost:1234/scrape?url=https://example.com"

# Scrape via POST (form)
curl -X POST http://localhost:1234/scrape -d "url=https://example.com"

# Scrape via POST (JSON)
curl -X POST http://localhost:1234/scrape \
     -H "Content-Type: application/json" \
     -d '{"url":"https://example.com"}'
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Lint
ruff check .
ruff format --check .

# Unit + E2E tests (no browser required)
pytest tests/ --ignore=tests/test_js_driver.py -v

# Full test suite including Playwright (requires pyscrape[js])
pip install -e ".[dev,js]" && playwright install chromium
pytest tests/ -v
```

## Architecture

```
pyscrape/
├── __init__.py      — public API + CLI entry points
├── driver.py        — RequestsDriver  (requests + lxml, default)
├── js_driver.py     — PlaywrightDriver (optional [js] extra, import-guarded)
├── session.py       — Session          (high-level, driver-agnostic)
├── server.py        — Flask HTTP scraping server
└── mixins.py        — SelectionMixin / WaitMixin helpers

tests/
├── conftest.py      — shared fixtures (local fixture HTTP server)
├── test_driver.py   — RequestsDriver unit tests
├── test_session.py  — Session unit tests
├── test_server.py   — Flask server E2E tests (fixture page → scrape API)
└── test_js_driver.py — Playwright tests (skipped if [js] not installed)
```

## Legacy dependencies — disposition

| Package | Status | v2 disposition |
|---|---|---|
| `webkit-server` | Dead (PyPI 404) | **Removed** → replaced by Playwright (optional) |
| `xvfbwrapper` | Dead / abandoned | **Removed** → no longer needed |
| `futures` | Python 2 backport | **Removed** → `concurrent.futures` is built-in on Python 3 |
| `tornado` | Alive | **Removed** → replaced by Flask for the HTTP server |
| `fake-useragent` | Alive | **Removed** → fixed UA string in RequestsDriver |

---

Improvements are welcome — open an issue or PR.
