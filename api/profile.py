from flask import render_template, session, redirect, url_for
from models import get_user_profile


def handle_profile():
    """Handle profile page — session-scoped, read-only, no URL parameter."""
    if "user_id" not in session:
        return redirect(url_for("login"))

    profile = get_user_profile(session["user_id"])

    if profile is None:
        return redirect(url_for("login"))

    return render_template("profile.html", profile=profile)
