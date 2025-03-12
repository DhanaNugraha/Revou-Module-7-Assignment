from flask import jsonify
from repo.account import (
    get_account_by_account_id,
    get_all_accounts,
    register_account_in_user_repository,
    register_account_repository,
    update_account_repository,
    get_accounts_by_user_id
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


def get_user_accounts(user_auth_data):
    user_id = user_auth_data["user_id"]
    user_accounts = list(get_accounts_by_user_id(user_id).values())

    return jsonify({"data": user_accounts, "success": True}), 200


def update_account_details(account_id, account_request_data):
    # data checker
    (incomplete, missing_key, missing_value) = missing_data_checker(
        account_request_data, account_key_fields
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

    update_account_repository(account_id, account_request_data)

    return jsonify({"message": "account updated succesfully", "success": True}), 200

def get_account_details(account_id):
    account_data = get_account_by_account_id(account_id)
    return jsonify({"data": account_data, "success": True}), 200

# (delete from user list as well)
def delete_account(account_id, user_auth_data):
    pass