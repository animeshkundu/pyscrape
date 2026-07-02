# AGENTS.md — pyscrape agentic-dev context

See [CLAUDE.md](CLAUDE.md) for the full architecture and design rules.
This file surfaces the most important constraints for any AI coding agent.

## Constraints every agent must follow

### 1. Default mode stays browser-free
`pyscrape.driver` and `pyscrape.session` must never import `playwright` or any
browser package. All browser code lives exclusively in `pyscrape.js_driver`.

### 2. PlaywrightDriver import guard
If a user calls `PlaywrightDriver()` without `pyscrape[js]` installed, it **must**
raise `ImportError` with this exact pip install hint:

```
pip install 'pyscrape[js]'
playwright install chromium
```

### 3. No unilateral license changes
There is no LICENSE file. Do **not** add or change a license without explicit
instruction from the repository owner.

### 4. Never trigger release or Pages
`.github/workflows/release.yml` and `.github/workflows/docs.yml` are PREPARED
but must not be triggered, published to PyPI, or deployed to Pages without
human approval.

### 5. Test separation
- `tests/test_js_driver.py` is excluded from the default `pytest` run.
- It is exercised only in the `test-js` CI job (which installs Playwright).
- The `playwright = pytest.importorskip(...)` guard must remain in place.

## Development quick-start

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check .
pytest tests/ --ignore=tests/test_js_driver.py -v
```

## Accepting human decisions

Surface the following to the repository owner before acting:
- Any changes to the package version in `pyproject.toml`
- Any change to the `[js]` extra's Playwright version pin
- Choosing / adding a LICENSE
- Enabling GitHub Pages or triggering a PyPI release
