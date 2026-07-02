"""Lightweight Flask-based HTTP scraping server.

Start it with the ``pyrun`` CLI or call :func:`run_server` directly::

    pyrun --port 1234
    curl "http://localhost:1234/scrape?url=https://example.com"
"""

from __future__ import annotations

import logging
import time

from flask import Flask, jsonify, request

from .session import Session

log = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/ping", methods=["GET", "POST"])
def ping():  # type: ignore[return]
    """Health-check endpoint."""
    return "OK"


@app.route("/scrape", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def scrape():  # type: ignore[return]
    """Scrape a URL and return its HTML body.

    GET  /scrape?url=<url>
    POST /scrape  body: url=<url>  (form or JSON)
    """
    if request.method == "POST":
        url = request.form.get("url")
        if url is None:
            json_body = request.get_json(force=False, silent=True) or {}
            url = json_body.get("url")
    else:
        url = request.args.get("url")

    if not url:
        return jsonify({"error": "Missing required parameter 'url'"}), 400

    t = time.time()
    s = Session()
    s.visit(url)
    body = s.body()
    elapsed = time.time() - t
    log.info("%s | %d chars | %.3fs", url, len(body), elapsed)
    return body, 200, {"Content-Type": "text/html; charset=utf-8"}


def run_server(port: int = 1234, debug: bool = False) -> None:
    """Start the HTTP scraping server on *port*."""
    app.run(host="0.0.0.0", port=port, debug=debug)
