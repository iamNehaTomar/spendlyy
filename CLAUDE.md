# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the dev server (http://localhost:5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

**Single-file Flask app** — all routes live in `app.py`. The app runs on port 5001 with `debug=True`.

**Templates** all extend `base.html`, which provides the navbar, footer (with Terms/Privacy links), and three overridable blocks: `{% block head %}` (per-page CSS), `{% block content %}`, and `{% block scripts %}` (per-page JS).

**CSS is split in two layers:**
- `static/css/style.css` — global styles, CSS variables, all shared components (navbar, buttons, auth forms, footer, `.terms-*` page styles)
- `static/css/landing.css` — landing-page-only overrides, loaded via `{% block head %}` in `landing.html`. Overrides the `.hero` grid from `style.css` into a centered single-column flex layout, and defines the browser mockup, stat tiles, bar chart, and video modal

**Database** (`database/db.py`) is a stub — not yet implemented. It will expose `get_db()`, `init_db()`, and `seed_db()` using SQLite with `row_factory` and foreign keys enabled.

**Several routes in `app.py` are placeholder stubs** (logout, profile, add/edit/delete expense) returning plain strings — they are meant to be implemented incrementally.

## Conventions

- New pages: add a route in `app.py` + create `templates/<name>.html` extending `base.html`. Legal/info pages (terms, privacy) reuse `.terms-*` CSS classes already in `style.css`.
- Per-page JavaScript goes in `{% block scripts %}` as a vanilla JS IIFE — no JS framework is used. The video modal in `landing.html` is the reference pattern.
- The video modal stops playback by clearing `iframe.src = ''` on close and restoring it from `data-src` on open — no YouTube iframe API needed.
- CSS variables are defined in `:root` in `style.css`: `--ink`, `--accent` (dark green `#1a472a`), `--accent-2` (amber), `--paper`, `--font-display` (DM Serif Display), `--font-body` (DM Sans).
