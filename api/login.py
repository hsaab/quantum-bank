from flask import render_template, request, session, redirect, url_for
from models import get_user_by_username


def handle_login():
    """Handle login page"""
    if request.method == "POST":
        username = request.form.get("username")

        if not username:
            return render_template("login.html", error="Username is required")

        user = get_user_by_username(username)

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["full_name"] = user["full_name"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="User not found")

    return render_template("login.html")


def handle_logout():
    """Handle logout"""
    session.clear()
    return redirect(url_for("login"))
