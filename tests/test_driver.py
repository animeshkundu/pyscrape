"""Unit tests for pyscrape.driver.RequestsDriver."""

from __future__ import annotations

import pytest

from pyscrape.driver import FetchError, RequestsDriver


def test_fetch_and_body(fixture_server: str) -> None:
    driver = RequestsDriver()
    driver.visit(fixture_server)
    assert "Hello, pyscrape!" in driver.body()


def test_status_code(fixture_server: str) -> None:
    driver = RequestsDriver()
    driver.visit(fixture_server)
    assert driver.status_code() == 200


def test_document_parsing(fixture_server: str) -> None:
    driver = RequestsDriver()
    driver.visit(fixture_server)
    doc = driver.document()
    h1_elements = doc.cssselect("h1")
    assert h1_elements, "Expected at least one <h1> element"
    assert h1_elements[0].text_content().strip() == "Hello, pyscrape!"


def test_body_before_visit_raises() -> None:
    driver = RequestsDriver()
    with pytest.raises(RuntimeError, match="visit()"):
        driver.body()


def test_status_code_before_visit_raises() -> None:
    driver = RequestsDriver()
    with pytest.raises(RuntimeError, match="visit()"):
        driver.status_code()


def test_fetch_error_on_unreachable_url() -> None:
    driver = RequestsDriver(timeout=2)
    with pytest.raises(FetchError):
        driver.visit("http://127.0.0.1:1")  # nothing listening on port 1


def test_set_header_does_not_crash(fixture_server: str) -> None:
    driver = RequestsDriver()
    driver.set_header("X-Test", "pyscrape")
    driver.visit(fixture_server)
    assert driver.body()


def test_set_timeout() -> None:
    driver = RequestsDriver()
    driver.set_timeout(5)
    assert driver.timeout == 5


def test_reset_clears_response(fixture_server: str) -> None:
    driver = RequestsDriver()
    driver.visit(fixture_server)
    assert driver.body()
    driver.reset()
    with pytest.raises(RuntimeError):
        driver.body()
