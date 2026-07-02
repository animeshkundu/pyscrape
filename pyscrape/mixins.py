"""Mixin classes for CSS/XPath selection and wait helpers."""

from __future__ import annotations

import time


class SelectionMixin:
    def css(self, css):
        return self.css(css)

    def at_css(self, css):
        return self._first_or_none(self.css(css))

    def at_xpath(self, xpath):
        return self._first_or_none(self.xpath(xpath))

    def parent(self):
        return self.at_xpath("..")

    def children(self):
        return self.xpath("*")

    def form(self):
        return self.at_xpath("ancestor::form")

    def _first_or_none(self, lst):
        return lst[0] if lst else None


class AttributeMixin:
    def __getitem__(self, attr):
        return self.get_attr(attr)

    def __setitem__(self, attr, value):
        self.set_attr(attr, value)


class HtmlParsingMixin:
    def document(self):
        import lxml.html

        return lxml.html.document_fromstring(self.body())


# default timeout values
DEFAULT_WAIT_INTERVAL = 0.5
DEFAULT_WAIT_TIMEOUT = 10
DEFAULT_AT_TIMEOUT = 1


class WaitTimeoutError(Exception):
    """Raised when a wait times out"""


class WaitMixin(SelectionMixin):
    def wait_for(
        self,
        condition,
        interval=DEFAULT_WAIT_INTERVAL,
        timeout=DEFAULT_WAIT_TIMEOUT,
    ):
        start = time.time()

        # at least execute the check once!
        while True:
            res = condition()
            if res:
                return res

            # timeout?
            if time.time() - start > timeout:
                break

            # wait a bit
            time.sleep(interval)

        # timeout occurred
        raise WaitTimeoutError("wait_for timed out")

    def wait_for_safe(self, *args, **kw):
        try:
            return self.wait_for(*args, **kw)
        except WaitTimeoutError:
            return None

    def wait_while(self, condition, *args, **kw):
        return self.wait_for(lambda: not condition(), *args, **kw)

    def at_css(self, css, timeout=DEFAULT_AT_TIMEOUT, **kw):
        return self.wait_for_safe(
            lambda: super().at_css(css),
            timeout=timeout,
            **kw,
        )

    def at_xpath(self, xpath, timeout=DEFAULT_AT_TIMEOUT, **kw):
        return self.wait_for_safe(
            lambda: super().at_xpath(xpath),
            timeout=timeout,
            **kw,
        )
