# Spec: Login and Logout

## Overview
Implement login and logout so users can authenticate into Spendly and end their session. The `POST /login` handler and `GET /login` template already exist; this step wires up the `/logout` route, adds a session guard to `/login` so already-authenticated users are bounced to the dashboard, and updates `base.html` so the navbar reflects the current session state (showing "Sign out" when logged in, and "Sign in / Get started" when logged out).

## Depends on
- Step 1 — Database setup (`get_db()`, `users` table must exist)
- Step 2 — Registration (user rows in `users`; `session` and `flash` already imported)

## Routes
- `GET  /login`  — render the login form; redirect to `/expenses` if already logged in — public
- `POST /login`  — validate credentials, set session, redirect to `/expenses` — public *(already implemented; add the already-logged-in guard only)*
- `GET  /logout` — clear session, flash a goodbye message, redirect to landing — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `templates/base.html` — replace the static nav links with a conditional block:
  - When `session.user_id` is set: show a greeting (e.g. "Hi, {{ session.user_name }}") and a "Sign out" link pointing to `url_for('logout')`
  - When no session: show the existing "Sign in" and "Get started" links

## Files to change
- `app.py` — implement `GET /logout` (clear session, flash success, redirect to landing); add already-logged-in guard to `GET /login`
- `templates/base.html` — conditional navbar based on `session.user_id`

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.check_password_hash` (already used in login)
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Logout must call `session.clear()` (not just pop individual keys) to wipe the entire session
- After logout, flash a success message (e.g. "You have been signed out.") before redirecting
- The already-logged-in guard on `GET /login` must redirect to `url_for('expenses')`
- Navbar conditional must use `{% if session.user_id %}` — do not rely on `session.get`

## Definition of done
- [ ] `GET /login` when already logged in redirects to `/expenses` instead of showing the form
- [ ] `POST /login` with valid credentials sets `session["user_id"]` and `session["user_name"]` and redirects to `/expenses`
- [ ] `POST /login` with wrong password re-renders the form with an error and does not set a session
- [ ] `POST /login` with an unknown email re-renders the form with an error
- [ ] `GET /logout` clears the session and redirects to the landing page
- [ ] After logout a flash message "You have been signed out." (or similar) is visible on the landing page
- [ ] Navbar shows "Sign in" and "Get started" when logged out
- [ ] Navbar shows the user's name and a "Sign out" link when logged in
- [ ] Visiting `/logout` when not logged in does not raise an error (graceful redirect)
