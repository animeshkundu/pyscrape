"""Unit tests for pyscrape.session.Session."""

from __future__ import annotations

from pyscrape.session import Session


def test_session_visit_and_body(fixture_server: str) -> None:
    s = Session()
    s.visit(fixture_server)
    assert "Hello, pyscrape!" in s.body()


def test_session_with_base_url(fixture_server: str) -> None:
    s = Session(base_url=fixture_server)
    s.visit("/")  # resolved relative to base_url
    assert "Hello, pyscrape!" in s.body()


def test_session_proxies_driver_status_code(fixture_server: str) -> None:
    s = Session()
    s.visit(fixture_server)
    # Session should proxy status_code() through to the driver
    assert s.status_code() == 200


def test_session_complete_url_no_base() -> None:
    s = Session()
    assert s._complete_url("https://example.com/path") == "https://example.com/path"


def test_session_complete_url_with_base(fixture_server: str) -> None:
    s = Session(base_url=fixture_server)
    result = s._complete_url("/page")
    assert result == f"{fixture_server}/page"
