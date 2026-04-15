# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** is a personal expense tracker web app built with Flask + SQLite. It is a step-by-step student tutorial project (Campus X course) where features are implemented incrementally across numbered steps.

## Commands

```bash
# Set up virtual environment (first time)
python -m venv .venv
source .venv/Scripts/activate   # Windows bash
pip install -r requirements.txt

# Run the dev server
python app.py                    # runs on http://localhost:5001

# Run all tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run a single test by name
pytest -k "test_login"
```

## Architecture

**Stack:** Python/Flask · SQLite (raw `sqlite3`, no ORM) · Werkzeug (password hashing) · Jinja2 templates · Vanilla CSS/JS · pytest + pytest-flask

**Key files:**
- `app.py` — all Flask routes; currently has stubs for most endpoints
- `database/db.py` — students implement `get_db()`, `init_db()`, `seed_db()` here (Step 1)
- `templates/base.html` — shared layout with navbar and footer; all pages extend this
- `static/css/style.css` — global styles; `static/css/landing.css` — landing page only
- `static/js/main.js` — vanilla JS added incrementally

**Template structure:** All pages `{% extends "base.html" %}` and fill `{% block title %}`, `{% block content %}`, and optionally `{% block scripts %}`.

**Database pattern:** `get_db()` should return a `sqlite3.Connection` with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`. No connection pooling — connections are opened per-request.

## Step-by-step build plan

The app is built in numbered steps; existing route stubs indicate what's coming:
1. Database setup (`database/db.py`)
2. Auth — register / login (POST handlers + session)
3. Logout
4. Profile page
5–6. Expense listing / dashboard
7. Add expense
8. Edit expense
9. Delete expense

Most routes in `app.py` currently return placeholder strings. When implementing a step, replace the stub return value with real logic.
