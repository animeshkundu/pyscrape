"""pyscrape — lightweight Python 3 web scraping library.

Default mode (``pip install pyscrape``) uses *requests* + *lxml* with no
browser dependency.  For JavaScript rendering install the ``[js]`` extra::

    pip install 'pyscrape[js]'
    playwright install chromium
"""

from __future__ import annotations

import argparse

from .driver import FetchError, RequestsDriver
from .session import Session


def cli() -> None:
    """Command-line entry point: fetch a URL and print the HTML to stdout."""
    parser = argparse.ArgumentParser(
        description="Download (optionally JS-rendered) web pages",
    )
    parser.add_argument("url", help="The URL to download")
    parser.add_argument(
        "--js",
        action="store_true",
        help="Use Playwright JS rendering (requires pyscrape[js] extra)",
    )
    args = parser.parse_args()

    if args.js:
        from .js_driver import PlaywrightDriver

        with PlaywrightDriver() as driver:
            driver.visit(args.url)
            print(driver.body())
    else:
        s = Session()
        s.visit(args.url)
        print(s.body())


def http() -> None:
    """HTTP server entry point (``pyrun``)."""
    from .server import run_server

    parser = argparse.ArgumentParser(
        description="Run the pyscrape HTTP scraping server",
    )
    parser.add_argument(
        "--port",
        "-p",
        default=1234,
        type=int,
        help="Port to listen on (default: 1234)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    args = parser.parse_args()
    run_server(args.port, args.debug)


__all__ = ["FetchError", "RequestsDriver", "Session", "cli", "http"]
