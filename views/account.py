from flask import jsonify
from repo.account import (
    get_all_accounts,
    register_account_in_user_repository,
    register_account_repository,
    update_account_repository,
)
from datetime import datetime, timezone

from views.data_checker import missing_data_checker

account_key_fields = {"currency", "account_type"}


def register_account(account_data, user_auth_data):
    # data checker
    (incomplete, missing_key, missing_value) = missing_data_checker(
        account_data, account_key_fields
    )

    if incomplete:
        return jsonify(
            {
                "message": {
                    "missing key": f"{missing_key}",
                    "missing value": f"{missing_value}",
                },
                "success": False,
            }
        ), 400

    # inject stuff to request
    # add account id to user repo as well
    accounts = get_all_accounts()
    current_max_account_id = 0
    current_max_account_number = 0

    for account_id, account_data in accounts.items():
        account_id_number = int(account_id.replace("a", ""))

        current_max_account_id = max(current_max_account_id, account_id_number)

        current_max_account_number = max(
            current_max_account_number, int(account_data["account_number"])
        )

    formatted_account_id = f"a{current_max_account_id + 1}"
    formatted_account_number = f"{current_max_account_number + 1}"

    # get current time in utc
    now_utc = datetime.now(timezone.utc).isoformat()

    # inject acc_id, user_id, accounts, create time
    account_data.update(
        {
            "account_id": formatted_account_id,
            "user_id": user_auth_data["user_id"],
            "account_number": formatted_account_number,
            "balance": 0,
            "opened_date": now_utc,
            "status": "active",
        }
    )


    # register account
    register_account_repository(formatted_account_id, account_data)

    # register account in user repo
    register_account_in_user_repository(user_auth_data["user_id"], formatted_account_id)

    return jsonify(
        {
            "data": {
                "message": f"account registered successfully! with account id {formatted_account_id} and account number {formatted_account_number}"
            },
            "success": True,
        }
    ), 201
