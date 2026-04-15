# Spec: Registration

## Overview
Implement user registration so new visitors can create a Spendly account. This step adds the `POST /register` handler that validates form input, hashes the password, inserts a new row into the `users` table, starts a session, and redirects to the dashboard. It is the first authenticated flow in the app and gates all future logged-in features.

## Depends on
- Step 1 — Database setup (`get_db()`, `users` table must exist)

## Routes
- `GET  /register` — render the registration form — public (already exists as stub)
- `POST /register` — process form submission, create user, start session — public

## Database changes
No new tables or columns. The `users` table created in Step 1 is sufficient.

## Templates
- **Modify:** `templates/register.html` — already contains the form; add `{{ error }}` rendering (already present) and ensure `value="{{ name }}"` and `value="{{ email }}"` are re-populated on validation failure so the user doesn't retype everything.

## Files to change
- `app.py` — replace the `GET /register` stub with a combined GET/POST handler; add `secret_key`, import `session`, `redirect`, `url_for`, `request` from Flask and `check_password_hash` / `generate_password_hash` from werkzeug
- `templates/register.html` — add `value` attributes to name and email inputs for sticky form behaviour

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- `app.secret_key` must be set (use a hard-coded dev string for now, e.g. `"dev-secret"`)
- On successful registration store `session["user_id"]` and `session["user_name"]`
- On failure re-render the form with the original `name` and `email` values and a human-readable `error` message
- Validation rules:
  - All three fields (name, email, password) are required — reject blanks
  - Password must be at least 8 characters
  - If email already exists in `users`, return a specific error ("An account with that email already exists")
- After successful registration redirect to `/expenses` (dashboard stub) — do not redirect to `/login`

## Definition of done
- [ ] `GET /register` renders `register.html` with an empty form
- [ ] Submitting with all fields blank shows a validation error
- [ ] Submitting with a password shorter than 8 characters shows a validation error
- [ ] Submitting with a duplicate email shows "An account with that email already exists"
- [ ] On any error the name and email fields are pre-filled with what the user typed
- [ ] Submitting valid data inserts a new row in `users` with a hashed (not plain-text) password
- [ ] After successful registration `session["user_id"]` is set
- [ ] Browser is redirected to `/expenses` after registration
- [ ] Registering twice with the same email is rejected even after a page refresh
