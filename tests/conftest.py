"""Shared pytest fixtures for pyscrape tests."""

from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

FIXTURE_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head><title>Test Page</title></head>
<body>
  <h1>Hello, pyscrape!</h1>
  <p id="content">This is a test fixture page.</p>
  <a href="/other">Other page</a>
</body>
</html>
"""


class _FixtureHandler(BaseHTTPRequestHandler):
    """Minimal handler that always returns FIXTURE_HTML."""

    def log_message(self, *args: object) -> None:  # suppress access logs in tests
        pass

    def do_GET(self) -> None:  # noqa: N802
        body = FIXTURE_HTML.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


@pytest.fixture(scope="session")
def fixture_server() -> str:
    """Start a local HTTP server serving the fixture HTML; return its base URL."""
    server = HTTPServer(("127.0.0.1", 0), _FixtureHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()
