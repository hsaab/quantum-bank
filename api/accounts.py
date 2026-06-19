from flask import render_template, session, redirect, url_for, request
from models import get_account_by_id, get_transactions_by_account, get_cards_by_account


def handle_account_detail():
    """Handle account detail page"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    account_id = request.args.get("id")

    if not account_id:
        return redirect(url_for("dashboard"))

    account = get_account_by_id(account_id)

    if not account or str(account.get("user_id")) != str(user_id):
        return redirect(url_for("dashboard"))

    # Get transactions for this account
    transactions = get_transactions_by_account(account_id, limit=20)

    # Get cards for this account
    cards = get_cards_by_account(account_id)

    return render_template(
        "account_detail.html", account=account, transactions=transactions, cards=cards
    )
