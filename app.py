from flask import Flask, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm_password:
        return render_template("register.html", error="All fields are required.", name=name, email=email)

    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)

    if password != confirm_password:
        return render_template("register.html", error="Passwords do not match.", name=name, email=email)

    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return render_template("register.html", error="An account with that email already exists.", name=name, email=email)

    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password))
    )
    conn.commit()
    conn.close()

    flash("Account created successfully! Please sign in.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("expenses"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="All fields are required.")

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]

    return redirect(url_for("expenses"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/expenses")
def expenses():
    return "Dashboard — coming in Step 5"


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "April 1, 2026",
        "initials": "DU",
    }
    stats = [
        {"label": "Total Spent",  "value": "₹392.50", "icon": "credit-card"},
        {"label": "Transactions", "value": "8",        "icon": "list"},
        {"label": "Top Category", "value": "Food",     "icon": "tag"},
    ]
    transactions = [
        {"date": "Apr 15, 2026", "description": "Restaurant dinner",  "category": "Food",          "amount": "₹60.00"},
        {"date": "Apr 12, 2026", "description": "New shoes",          "category": "Shopping",      "amount": "₹80.00"},
        {"date": "Apr 10, 2026", "description": "Movie night",        "category": "Entertainment", "amount": "₹25.00"},
        {"date": "Apr 07, 2026", "description": "Pharmacy",           "category": "Health",        "amount": "₹35.00"},
        {"date": "Apr 05, 2026", "description": "Electricity bill",   "category": "Bills",         "amount": "₹120.00"},
        {"date": "Apr 03, 2026", "description": "Bus pass",           "category": "Transport",     "amount": "₹12.00"},
        {"date": "Apr 01, 2026", "description": "Grocery shopping",   "category": "Food",          "amount": "₹45.50"},
    ]
    categories = [
        {"name": "Bills",         "amount": "₹120.00", "pct": 85},
        {"name": "Food",          "amount": "₹105.50", "pct": 75},
        {"name": "Shopping",      "amount": "₹80.00",  "pct": 57},
        {"name": "Health",        "amount": "₹35.00",  "pct": 25},
        {"name": "Entertainment", "amount": "₹25.00",  "pct": 18},
        {"name": "Other",         "amount": "₹15.00",  "pct": 11},
        {"name": "Transport",     "amount": "₹12.00",  "pct": 9},
    ]
    return render_template("profile.html",
                           user=user, stats=stats,
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


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
