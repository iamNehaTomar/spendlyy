impl# Spec: Login and Logout

## Overview

Polish and complete the login, logout, and dashboard flows that were scaffolded in Step 02. The routes and templates already exist and the core logic works, but several UX gaps remain: authenticated users can still reach `/login` and `/register` without being redirected, there is no feedback message after logout, and the dashboard shows only a placeholder. This step closes those gaps and delivers a fully usable auth loop for Spendly.

---

## Depends on

- Step 01 — Database setup (`database/db.py` with `users` and `expenses` tables)
- Step 02 — Registration (`/register` POST, `/login` POST, `/dashboard`, `templates/login.html`, `templates/dashboard.html`)

---

## Routes

| Method | Path | Description | Access |
|--------|------|-------------|--------|
| GET | `/login` | Render login form — redirect to `/dashboard` if already logged in | Public |
| GET | `/register` | Render registration form — redirect to `/dashboard` if already logged in | Public |
| GET | `/logout` | Clear session, flash "You've been signed out." message, redirect to landing | Logged-in |
| GET | `/dashboard` | Show authenticated user's name and basic expense summary | Logged-in |

No new routes are needed — all four exist already.

---

## Database changes

No new tables or columns. The `users` and `expenses` tables from Step 01 are sufficient.

---

## Templates

**Modify:**
- `templates/login.html` — render the `get_flashed_messages()` block so logout confirmation message is visible on this page
- `templates/dashboard.html` — replace the "coming soon" placeholder with a real summary section: total expenses this month, total amount this month, a breakdown by category (count + sum), and a "No expenses yet" empty state

**No new templates.**

---

## Files to change

- `app.py`
  - `/login` GET: add `if session.get("user_id"): return redirect(url_for("dashboard"))`
  - `/register` GET: same already-authenticated guard
  - `/logout`: use `flask.flash("You've been signed out.", "info")` before `session.clear()` and redirect
  - `/dashboard`: query the `expenses` table to build a summary dict passed to the template
- `templates/login.html` — render flashed messages above the form
- `templates/dashboard.html` — replace placeholder with summary UI

---

## Files to create

None.

---

## New dependencies

No new dependencies. `flask.flash` and `flask.get_flashed_messages` are part of Flask (already installed).

---

## Rules for implementation

- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — never string-format SQL
- Passwords are never read or re-hashed in this step
- Session stores only `user_id` (integer)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Flash messages use the `"info"` category; render them using `get_flashed_messages(with_categories=true)`
- The already-authenticated guard must appear in the GET branch only — never block a POST from redirecting

### Dashboard query requirements
- Filter expenses by `user_id = session["user_id"]`
- "This month" means `strftime('%Y-%m', date) = strftime('%Y-%m', 'now')`
- Pass to the template:
  - `user` — Row with at least `name`
  - `monthly_total` — `SUM(amount)` for current month (default `0.0` if NULL)
  - `monthly_count` — `COUNT(*)` for current month
  - `by_category` — list of `(category, count, total)` rows for current month, ordered by total DESC
- If `by_category` is empty, the template must show an "Add your first expense" empty state

---

## Definition of done

- [ ] Visiting `/login` while already logged in redirects to `/dashboard` without showing the login form
- [ ] Visiting `/register` while already logged in redirects to `/dashboard` without showing the form
- [ ] Clicking "Logout" shows the landing page with a flash message "You've been signed out."
- [ ] The flash message disappears on the next page load (not persistent)
- [ ] The dashboard shows the logged-in user's name in the heading
- [ ] The dashboard shows total amount and count of expenses for the current month
- [ ] The dashboard shows a per-category breakdown for the current month
- [ ] When the user has no expenses, the dashboard shows an empty-state message instead of the breakdown
- [ ] Visiting `/dashboard` while logged out redirects to `/login` (unchanged from Step 02)
- [ ] No plain-text hex colours are introduced in any template or CSS changes
