from flask import render_template, session, redirect, url_for
from models import get_all_transactions_by_user


def handle_transactions():
    """Handle transactions page"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    transactions = get_all_transactions_by_user(user_id, limit=100)

    return render_template("transactions.html", transactions=transactions)
