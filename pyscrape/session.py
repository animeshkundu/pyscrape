"""Session: high-level scraping session backed by a driver."""

from __future__ import annotations

from itertools import chain
from urllib.parse import urljoin

from .driver import RequestsDriver


class Session:
    """A scraping session.

    Parameters
    ----------
    driver:
        The underlying driver instance.  Defaults to
        :class:`~pyscrape.driver.RequestsDriver` (requests + lxml, no browser).
    base_url:
        Optional base URL.  Relative URLs passed to :meth:`visit` are resolved
        against it via :func:`urllib.parse.urljoin`.
    """

    def __init__(self, driver=None, base_url: str | None = None) -> None:
        self.driver = driver or RequestsDriver()
        self.base_url = base_url

    # -- proxy pattern -------------------------------------------------------

    def __getattr__(self, attr: str):  # noqa: ANN204
        return getattr(self.driver, attr)

    def __dir__(self) -> list[str]:
        return list(set(chain(dir(type(self)), dir(self.driver))))

    # -- navigation ----------------------------------------------------------

    def visit(self, url: str) -> None:
        """Fetch *url* (resolved against :attr:`base_url` when set)."""
        self.driver.visit(self._complete_url(url))

    def _complete_url(self, url: str) -> str:
        if self.base_url:
            return urljoin(self.base_url, url)
        return url
