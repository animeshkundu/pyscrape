"""Tests for pyscrape.js_driver.

The Playwright tests are separated into a dedicated file so they can be run
in a separate CI job that installs Playwright + Chromium.

Tests that verify the import guard (missing playwright → clear error) run
unconditionally as part of the normal test suite.
"""

from __future__ import annotations

import pytest

import pyscrape.js_driver as js_driver_module
from pyscrape.js_driver import PlaywrightDriver, _require_playwright

# ---------------------------------------------------------------------------
# Import-guard tests — run unconditionally (no playwright required)
# ---------------------------------------------------------------------------


def test_require_playwright_raises_when_unavailable() -> None:
    """_require_playwright() raises ImportError with pip install hint."""
    original = js_driver_module._PLAYWRIGHT_AVAILABLE
    js_driver_module._PLAYWRIGHT_AVAILABLE = False
    try:
        with pytest.raises(ImportError, match=r"pyscrape\[js\]"):
            _require_playwright()
    finally:
        js_driver_module._PLAYWRIGHT_AVAILABLE = original


def test_playwright_driver_init_raises_when_unavailable() -> None:
    """PlaywrightDriver() raises ImportError when playwright is absent."""
    original = js_driver_module._PLAYWRIGHT_AVAILABLE
    js_driver_module._PLAYWRIGHT_AVAILABLE = False
    try:
        with pytest.raises(ImportError, match=r"pyscrape\[js\]"):
            PlaywrightDriver()
    finally:
        js_driver_module._PLAYWRIGHT_AVAILABLE = original


def test_playwright_driver_visit_outside_context_raises() -> None:
    """Calling visit() outside a context manager raises RuntimeError."""
    driver = object.__new__(PlaywrightDriver)
    driver._page = None
    with pytest.raises(RuntimeError, match="context manager"):
        driver.visit("http://example.com")


def test_playwright_driver_body_outside_context_raises() -> None:
    """Calling body() outside a context manager raises RuntimeError."""
    driver = object.__new__(PlaywrightDriver)
    driver._page = None
    with pytest.raises(RuntimeError, match="context manager"):
        driver.body()


# ---------------------------------------------------------------------------
# Full Playwright tests — skipped if playwright is not installed
# ---------------------------------------------------------------------------


def test_playwright_driver_fetches_fixture(fixture_server: str) -> None:
    pytest.importorskip("playwright")
    with PlaywrightDriver() as driver:
        driver.visit(fixture_server)
        html = driver.body()
    assert "Hello, pyscrape!" in html
