from flask import render_template, session, redirect, url_for, request, jsonify
from models import get_accounts_by_user, transfer_money
import math


def handle_transfer():
    """Handle money transfer page"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    accounts = get_accounts_by_user(user_id)

    # Filter out credit accounts for source (can't transfer from credit)
    source_accounts = [acc for acc in accounts if acc["account_type"] != "credit"]

    if request.method == "POST":
        from_account_id = request.form.get("from_account")
        to_account_id = request.form.get("to_account")
        amount = request.form.get("amount")
        description = request.form.get("description", "Transfer")

        # Validation
        if not from_account_id or not to_account_id or not amount:
            return render_template(
                "transfer.html",
                accounts=source_accounts,
                all_accounts=accounts,
                error="All fields are required",
            )

        if from_account_id == to_account_id:
            return render_template(
                "transfer.html",
                accounts=source_accounts,
                all_accounts=accounts,
                error="Cannot transfer to the same account",
            )

        try:
            amount_str = str(amount).strip().lower()
            if amount_str in {
                "nan",
                "+nan",
                "-nan",
                "inf",
                "+inf",
                "-inf",
                "infinity",
                "+infinity",
                "-infinity",
            }:
                raise ValueError()
            amount = float(amount_str)
            if amount <= 0 or not math.isfinite(amount):
                raise ValueError()
        except ValueError:
            return render_template(
                "transfer.html",
                accounts=source_accounts,
                all_accounts=accounts,
                error="Invalid amount",
            )

        # Perform transfer
        success, message = transfer_money(
            int(from_account_id),
            int(to_account_id),
            amount,
            description,
            acting_user_id=user_id,
        )

        if success:
            return render_template(
                "transfer.html",
                accounts=source_accounts,
                all_accounts=accounts,
                success=message,
            )
        else:
            status = 403 if message == "Forbidden" else 200
            return (
                render_template(
                    "transfer.html",
                    accounts=source_accounts,
                    all_accounts=accounts,
                    error=message,
                ),
                status,
            )

    return render_template(
        "transfer.html", accounts=source_accounts, all_accounts=accounts
    )


def handle_api_transfer():
    """Handle API transfer endpoint"""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    data = request.get_json()

    from_account_id = data.get("from_account_id")
    to_account_id = data.get("to_account_id")
    amount = data.get("amount")
    description = data.get("description", "Transfer")

    if not from_account_id or not to_account_id or not amount:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    try:
        amount_str = str(amount).strip().lower()
        if amount_str in {
            "nan",
            "+nan",
            "-nan",
            "inf",
            "+inf",
            "-inf",
            "infinity",
            "+infinity",
            "-infinity",
        }:
            raise ValueError()
        amount = float(amount_str)
        if amount <= 0 or not math.isfinite(amount):
            raise ValueError()
    except ValueError:
        return jsonify({"success": False, "message": "Invalid amount"}), 400

    success, message = transfer_money(
        int(from_account_id),
        int(to_account_id),
        amount,
        description,
        acting_user_id=session["user_id"],
    )

    if success:
        return jsonify({"success": True, "message": message})
    else:
        status = 403 if message == "Forbidden" else 400
        return jsonify({"success": False, "message": message}), status
