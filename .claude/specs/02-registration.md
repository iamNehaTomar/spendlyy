# Spec: Registration

## Overview

Implement user registration and login so visitors can create a Spendly account and sign in. This step wires up the POST handlers for `/register` and `/login`, introduces Flask sessions so the app knows who is logged in, creates a minimal dashboard page that authenticated users land on, and wires up the `/logout` stub. The templates already exist and expect an `error` variable — this step makes those forms actually work.

---

## Depends on

- Step 01 — Database setup (`database/db.py` fully implemented with `users` table)

---

## Routes

| Method | Path | Description | Access |
|--------|------|-------------|--------|
| GET | `/register` | Render registration form | Public |
| POST | `/register` | Handle registration form submission | Public |
| GET | `/login` | Render login form | Public |
| POST | `/login` | Handle login form submission | Public |
| GET | `/logout` | Clear session and redirect to landing | Logged-in |
| GET | `/dashboard` | Main page for authenticated users | Logged-in |

---

## Database changes

No new tables or columns. The `users` table created in Step 01 already has all required fields (`id`, `name`, `email`, `password_hash`, `created_at`).

---

## Templates

**Create:**
- `templates/dashboard.html` — minimal logged-in home page showing the user's name and a placeholder for expenses

**Modify:**
- `templates/base.html` — update navbar links to show "Dashboard" + "Logout" when `session.user_id` is set, and "Register" + "Login" when it is not

---

## Files to change

- `app.py` — add `secret_key`, import `request`, `redirect`, `url_for`, `session`; implement POST `/register`, POST `/login`, GET `/logout`; add GET `/dashboard` route
- `templates/base.html` — conditional navbar based on session

---

## Files to create

- `templates/dashboard.html`

---

## New dependencies

No new dependencies. `werkzeug.security` (already installed) provides `generate_password_hash` and `check_password_hash`.

---

## Rules for implementation

- Set `app.secret_key` to a hard-coded dev string (e.g. `"spendly-dev-secret"`) — note in a comment that it must be replaced with an env var before production
- Use parameterised queries only — never string-format SQL
- Hash passwords with `werkzeug.security.generate_password_hash`; verify with `check_password_hash`
- Session stores only `user_id` (integer) — never store the password or hash in the session
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- On duplicate email at registration, re-render `register.html` with `error="An account with that email already exists."`
- On bad credentials at login, re-render `login.html` with `error="Invalid email or password."`
- After successful registration, log the user in immediately (set `session["user_id"]`) and redirect to `/dashboard`
- After successful login, redirect to `/dashboard`
- `/logout` clears the session with `session.clear()` and redirects to `/`
- `/dashboard` must redirect to `/login` if `session.get("user_id")` is not set

### Registration validation (server-side)
- Name: required, strip whitespace, min 1 character after strip
- Email: required (browser `type="email"` handles format)
- Password: required, minimum 8 characters

---

## Definition of done

- [ ] Visiting `/register` and submitting the form with a new email creates a user row in the database
- [ ] After successful registration the browser is on `/dashboard` and shows the new user's name
- [ ] Submitting `/register` with an already-used email stays on `/register` and shows the duplicate-email error message
- [ ] Submitting `/register` with a password shorter than 8 characters shows a validation error
- [ ] Visiting `/login` and submitting correct credentials redirects to `/dashboard`
- [ ] Submitting `/login` with a wrong password shows the invalid-credentials error message
- [ ] Visiting `/logout` clears the session and redirects to the landing page
- [ ] Visiting `/dashboard` while logged out redirects to `/login`
- [ ] The navbar shows "Dashboard" and "Logout" links when logged in, and "Register" and "Login" when logged out
- [ ] Passwords are stored as hashes — the plain-text password is never persisted
