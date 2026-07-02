"""Optional Playwright-backed JS-rendering driver for pyscrape.

Requires the ``[js]`` extra::

    pip install 'pyscrape[js]'
    playwright install chromium

A clear :exc:`ImportError` is raised if you instantiate :class:`PlaywrightDriver`
without that extra installed, so the default ``pip install pyscrape`` path is
never burdened by a browser dependency.
"""

from __future__ import annotations

try:
    from playwright.sync_api import sync_playwright as _sync_playwright

    _PLAYWRIGHT_AVAILABLE = True
except ImportError:
    _sync_playwright = None  # type: ignore[assignment]
    _PLAYWRIGHT_AVAILABLE = False

_INSTALL_HINT = (
    "Playwright is not installed.\n"
    "Install the JS extra:  pip install 'pyscrape[js]'\n"
    "Then install the browser:  playwright install chromium"
)


def _require_playwright() -> None:
    """Raise :exc:`ImportError` with an actionable message when playwright is absent."""
    if not _PLAYWRIGHT_AVAILABLE:
        raise ImportError(_INSTALL_HINT)


class PlaywrightDriver:
    """JS-capable driver using Playwright (Chromium).

    Use as a context manager::

        with PlaywrightDriver() as driver:
            driver.visit("https://example.com")
            html = driver.body()

    Raises :exc:`ImportError` on construction if *playwright* is not installed.
    """

    def __init__(self, headless: bool = True) -> None:
        _require_playwright()
        self._headless = headless
        self._pw = None
        self._browser = None
        self._page = None

    def __enter__(self) -> PlaywrightDriver:
        self._pw = _sync_playwright().start()  # type: ignore[misc]
        self._browser = self._pw.chromium.launch(headless=self._headless)
        self._page = self._browser.new_page()
        return self

    def __exit__(self, *_: object) -> None:
        if self._browser:
            self._browser.close()
        if self._pw:
            self._pw.stop()
        self._page = None
        self._browser = None
        self._pw = None

    def visit(self, url: str) -> None:
        """Navigate to *url* and wait until the network is idle."""
        if self._page is None:
            raise RuntimeError(
                "Use PlaywrightDriver as a context manager (with PlaywrightDriver() as d:)."
            )
        self._page.goto(url)
        self._page.wait_for_load_state("networkidle")

    def body(self) -> str:
        """Return the fully-rendered HTML content of the current page."""
        if self._page is None:
            raise RuntimeError(
                "Use PlaywrightDriver as a context manager (with PlaywrightDriver() as d:)."
            )
        return self._page.content()
