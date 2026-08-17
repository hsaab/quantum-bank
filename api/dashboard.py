from flask import render_template, session, redirect, url_for
from models import (
    get_accounts_by_user,
    get_all_transactions_by_user,
    get_rewards_points_for_user,
)


def handle_dashboard():
    """Handle dashboard page"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    full_name = session.get("full_name", "User")

    # Get user's accounts
    accounts = get_accounts_by_user(user_id)

    # Calculate total balance (excluding credit cards which have negative balance)
    total_balance = sum(
        acc["balance"] for acc in accounts if acc["account_type"] != "credit"
    )

    # Get recent transactions
    recent_transactions = get_all_transactions_by_user(user_id, limit=5)
    rewards_points, rewards_banner_kind = get_rewards_points_for_user(user_id)

    return render_template(
        "dashboard.html",
        full_name=full_name,
        accounts=accounts,
        total_balance=total_balance,
        recent_transactions=recent_transactions,
        rewards_points=rewards_points,
        rewards_banner_kind=rewards_banner_kind,
    )
