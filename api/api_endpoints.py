from flask import jsonify, session
from models import get_accounts_by_user, get_all_transactions_by_user, get_account_by_id


def handle_api_accounts():
    """API endpoint for accounts"""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    user_id = session["user_id"]
    accounts = get_accounts_by_user(user_id)

    return jsonify({"accounts": accounts})


def handle_api_transactions():
    """API endpoint for transactions"""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    user_id = session["user_id"]
    transactions = get_all_transactions_by_user(user_id, limit=50)

    return jsonify({"transactions": transactions})


def handle_api_account_detail(account_id):
    """API endpoint for account detail"""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    account = get_account_by_id(account_id)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({"account": account})
