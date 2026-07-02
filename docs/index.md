# pyscrape

A lightweight Python 3 web scraping library.

**Default mode** (`pip install pyscrape`) uses **requests + lxml** — fast, zero-browser-dependency scraping.

**JS mode** (`pip install 'pyscrape[js]'`) adds **Playwright (Chromium)** for full JavaScript rendering.

---

## Quick start

### Default mode

```python
from pyscrape import Session

s = Session()
s.visit("https://example.com")
print(s.body())
```

### JS mode

```python
from pyscrape.js_driver import PlaywrightDriver

with PlaywrightDriver() as driver:
    driver.visit("https://example.com")
    print(driver.body())
```

### CLI

```bash
# Default (requests + lxml)
pyscrape https://example.com

# JS rendering
pyscrape --js https://example.com
```

### HTTP server

```bash
# Start
pyrun --port 1234

# Scrape
curl "http://localhost:1234/scrape?url=https://example.com"
curl -X POST http://localhost:1234/scrape -d "url=https://example.com"
```

---

## Installation

```bash
# Default (no browser required)
pip install pyscrape

# With JS rendering
pip install 'pyscrape[js]'
playwright install chromium
```
