"""E2E tests for pyscrape.server (Flask HTTP scraping API).

The Flask test client is used so no background thread is required.
Actual HTTP scraping calls go to the local fixture server, making this
a true end-to-end test of the scrape pipeline.
"""

from __future__ import annotations

import pytest

from pyscrape.driver import FetchError
from pyscrape.server import app as flask_app
from pyscrape.server import run_server


@pytest.fixture(scope="module")
def client(fixture_server: str):  # noqa: ANN201
    """Flask test client for the scraping server."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# /ping
# ---------------------------------------------------------------------------


def test_ping_get(client) -> None:  # noqa: ANN001
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.data == b"OK"


def test_ping_post(client) -> None:  # noqa: ANN001
    r = client.post("/ping")
    assert r.status_code == 200


# ---------------------------------------------------------------------------
# /scrape — GET
# ---------------------------------------------------------------------------


def test_scrape_get(client, fixture_server: str) -> None:  # noqa: ANN001
    r = client.get("/scrape", query_string={"url": fixture_server})
    assert r.status_code == 200
    assert b"Hello, pyscrape!" in r.data


def test_scrape_root_get(client, fixture_server: str) -> None:  # noqa: ANN001
    r = client.get("/", query_string={"url": fixture_server})
    assert r.status_code == 200
    assert b"Hello, pyscrape!" in r.data


def test_scrape_get_missing_url_returns_400(client) -> None:  # noqa: ANN001
    r = client.get("/scrape")
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# /scrape — POST (form)
# ---------------------------------------------------------------------------


def test_scrape_post_form(client, fixture_server: str) -> None:  # noqa: ANN001
    r = client.post("/scrape", data={"url": fixture_server})
    assert r.status_code == 200
    assert b"Hello, pyscrape!" in r.data


# ---------------------------------------------------------------------------
# /scrape — POST (JSON)
# ---------------------------------------------------------------------------


def test_scrape_post_json(client, fixture_server: str) -> None:  # noqa: ANN001
    r = client.post(
        "/scrape",
        json={"url": fixture_server},
        content_type="application/json",
    )
    assert r.status_code == 200
    assert b"Hello, pyscrape!" in r.data


def test_scrape_post_missing_url_returns_400(client) -> None:  # noqa: ANN001
    r = client.post("/scrape", data={})
    assert r.status_code == 400


def test_scrape_get_fetch_error_returns_502(client, monkeypatch) -> None:  # noqa: ANN001
    def _raise_fetch_error(_self, _url: str) -> None:
        raise FetchError("network down")

    monkeypatch.setattr("pyscrape.session.Session.visit", _raise_fetch_error)
    r = client.get("/scrape", query_string={"url": "http://example.invalid"})
    assert r.status_code == 502
    assert r.get_json()["error"] == "Failed to fetch URL"


def test_run_server_defaults_to_localhost(monkeypatch) -> None:  # noqa: ANN001
    called = {}

    def _fake_run(**kwargs):  # noqa: ANN003
        called.update(kwargs)

    monkeypatch.setattr("pyscrape.server.app.run", _fake_run)
    run_server()
    assert called["host"] == "127.0.0.1"
