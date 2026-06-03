import sqlite3

from flask import Flask, flash, render_template, request, redirect, session, url_for, abort
from werkzeug.security import check_password_hash

from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id, get_monthly_summary

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"  # dev only — replace with env var before production


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect(url_for("profile"))
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Name is required.")
    if not email:
        return render_template("register.html", error="Email is required.")
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.")

    try:
        user_id = create_user(name, email, password)
    except sqlite3.IntegrityError:
        return render_template("register.html", error="An account with that email already exists.")

    session["user_id"] = user_id
    return redirect(url_for("profile"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect(url_for("profile"))
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = get_user_by_id(session["user_id"])
    if user is None:
        session.clear()
        return redirect(url_for("login"))
    summary = get_monthly_summary(session["user_id"])
    return render_template("dashboard.html", user=user, **summary)


@app.route("/logout")
def logout():
    flash("You've been signed out.", "info")
    session.clear()
    return redirect(url_for("landing"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db_user = get_user_by_id(session["user_id"])
    if db_user is None:
        session.clear()
        return redirect(url_for("login"))

    from datetime import datetime
    try:
        member_since = datetime.strptime(db_user["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y")
    except (ValueError, TypeError):
        member_since = db_user["created_at"]

    user = {
        "name": db_user["name"],
        "email": db_user["email"],
        "member_since": member_since,
    }

    stats = {
        "total_spent": 364.24,
        "transaction_count": 8,
        "top_category": "Bills",
    }

    transactions = [
        {"date": "May 19, 2026", "description": "Grocery run",   "category": "Food",          "amount": 22.75},
        {"date": "May 16, 2026", "description": "Miscellaneous", "category": "Other",         "amount": 15.00},
        {"date": "May 13, 2026", "description": "New shoes",     "category": "Shopping",      "amount": 89.99},
        {"date": "May 10, 2026", "description": "Movie tickets", "category": "Entertainment", "amount": 25.00},
        {"date": "May 08, 2026", "description": "Pharmacy",      "category": "Health",        "amount": 35.00},
    ]

    categories = [
        {"name": "Bills",         "total": 120.00, "pct": 33},
        {"name": "Shopping",      "total":  89.99, "pct": 25},
        {"name": "Transport",     "total":  45.00, "pct": 12},
        {"name": "Health",        "total":  35.00, "pct": 10},
        {"name": "Food",          "total":  35.25, "pct":  9},
        {"name": "Entertainment", "total":  25.00, "pct":  7},
        {"name": "Other",         "total":  15.00, "pct":  4},
    ]

    return render_template("profile.html", user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
