"""Default requests + lxml driver for pyscrape.

No browser dependency — works out of the box with a plain ``pip install pyscrape``.
For JavaScript rendering see :mod:`pyscrape.js_driver` (requires the ``[js]`` extra).
"""

from __future__ import annotations

import lxml.html
import requests


class FetchError(Exception):
    """Raised when a URL cannot be fetched."""


class RequestsDriver:
    """Lightweight HTTP driver backed by *requests* + *lxml* (no browser required).

    Parameters
    ----------
    timeout:
        Request timeout in seconds.
    headers:
        Additional headers to send with every request.
    """

    DEFAULT_TIMEOUT: int = 30
    DEFAULT_USER_AGENT: str = (
        "Mozilla/5.0 (compatible; pyscrape/2.0; +https://github.com/animeshkundu/pyscrape)"
    )

    def __init__(
        self,
        timeout: int = DEFAULT_TIMEOUT,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": self.DEFAULT_USER_AGENT})
        if headers:
            self._session.headers.update(headers)
        self.timeout = timeout
        self._response: requests.Response | None = None

    # -- navigation ----------------------------------------------------------

    def visit(self, url: str) -> None:
        """Fetch *url* and store the response."""
        try:
            self._response = self._session.get(url, timeout=self.timeout)
            self._response.raise_for_status()
        except requests.RequestException as exc:
            raise FetchError(f"Failed to fetch {url!r}: {exc}") from exc

    # -- response accessors --------------------------------------------------

    def body(self) -> str:
        """Return the response body as a string."""
        if self._response is None:
            raise RuntimeError("No page loaded — call visit() first.")
        return self._response.text

    def status_code(self) -> int:
        """Return the HTTP status code of the last response."""
        if self._response is None:
            raise RuntimeError("No page loaded — call visit() first.")
        return self._response.status_code

    def document(self) -> lxml.html.HtmlElement:
        """Return the parsed lxml HTML document."""
        return lxml.html.document_fromstring(self.body())

    # -- configuration -------------------------------------------------------

    def set_header(self, name: str, value: str) -> None:
        """Set a persistent request header."""
        self._session.headers[name] = value

    def set_timeout(self, timeout: int) -> None:
        """Set the request timeout in seconds."""
        self.timeout = timeout

    # -- lifecycle -----------------------------------------------------------

    def reset(self) -> None:
        """Clear the stored response."""
        self._response = None
