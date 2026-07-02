# API Reference

## `pyscrape.Session`

High-level scraping session backed by a driver.

```python
from pyscrape import Session

s = Session()
s.visit("https://example.com")
html = s.body()
doc  = s.document()  # lxml HtmlElement
```

**Constructor parameters**

| Parameter  | Type                | Default              | Description                                       |
|------------|---------------------|----------------------|---------------------------------------------------|
| `driver`   | driver instance     | `RequestsDriver()`   | Underlying driver (requests or Playwright)        |
| `base_url` | `str \| None`       | `None`               | Base URL — relative URLs in `visit()` are resolved against it |

---

## `pyscrape.driver.RequestsDriver`

```python
from pyscrape.driver import RequestsDriver

driver = RequestsDriver(timeout=30)
driver.visit("https://example.com")
print(driver.body())
print(driver.status_code())
doc = driver.document()  # lxml HtmlElement
```

| Method                        | Description                                    |
|-------------------------------|------------------------------------------------|
| `visit(url)`                  | Fetch the URL                                  |
| `body() → str`                | Return the response HTML as a string           |
| `status_code() → int`         | Return the HTTP status code                    |
| `document() → HtmlElement`    | Return the parsed lxml document                |
| `set_header(name, value)`     | Set a persistent request header                |
| `set_timeout(seconds)`        | Set the request timeout                        |
| `reset()`                     | Clear the stored response                      |

---

## `pyscrape.js_driver.PlaywrightDriver`

Requires `pip install 'pyscrape[js]'` + `playwright install chromium`.

```python
from pyscrape.js_driver import PlaywrightDriver

with PlaywrightDriver(headless=True) as driver:
    driver.visit("https://example.com")
    html = driver.body()
```

A clear `ImportError` is raised if Playwright is not installed.

---

## HTTP Server

```
GET  /scrape?url=<url>
POST /scrape          body: url=<url>  (form-encoded or JSON)
GET  /ping            → "OK"
```

Start with `pyrun --port 1234` or call `pyscrape.server.run_server(port)`.
