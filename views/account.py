# from flask import jsonify
# from repo.account import (
#     delete_account_repository,
#     get_account_by_account_id,
#     get_all_accounts,
#     register_account_in_user_repository,
#     register_account_repository,
#     update_account_repository,
#     get_accounts_by_user_id
# )
# from datetime import datetime, timezone
# from views.data_checker import missing_data_checker

from flask import jsonify
from repo.account import account_number_checker_repo, create_account_repo, update_account_repo, delete_account_repo, account_by_account_id_repo, account_by_user_id_repo
from pydantic import BaseModel, ValidationError
import random

class AccountRequest(BaseModel):
    currency: str
    account_type: str   

def register_account(account_data_request, user_auth_data):
    try:
        account_data_validated = AccountRequest.model_validate(account_data_request)

    except ValidationError as e:
        return jsonify({"message": str(e), "success": False}), 400
    
    # make account number
    account_number = str(random.randint(1000000000, 9999999999))
    while account_number_checker_repo(account_number):
        account_number = str(random.randint(1000000000, 9999999999))
    
    # insert acc number and user id
    user_id = user_auth_data.get("id")

    try:
        create_account_repo(account_data_validated, user_id, account_number)

    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 400

    return jsonify({"message": f"account created successfully with account number {account_number}", "success": True}), 200


def update_account_details(account_id, account_data_request):
    # data checker
    try:
        account_data_validated = AccountRequest.model_validate(account_data_request)

    except ValidationError as e:
        return jsonify({"message": str(e), "success": False}), 400
    
    try:
        account_number = update_account_repo(account_data_validated, account_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 401

    return jsonify({"message": f"account {account_number} updated successfully", "success": True}), 200

def delete_account(account_id, user_auth_data):
    try:
        delete_account_repo(account_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 401

    return jsonify({"message": "account deleted successfully", "success": True}), 200

def get_account_details(account_id):
    try:
        account_data = account_by_account_id_repo(account_id)

    except Exception as e:
        print(e)
        return jsonify({"message": str(e), "success": False}), 401

    converted_account = {
        "id": account_data.id,
        "account_type": account_data.account_type,
        "account_number": account_data.account_number,
        "balance": account_data.balance,
        "currency": account_data.currency,
        "created_at": account_data.created_at,
        "updated_at": account_data.updated_at,
        "status": account_data.status,
        "user_id": account_data.user_id,
    }

    return jsonify({"data": converted_account, "success": True}), 200

def get_user_accounts(user_auth_data):
    user_id = user_auth_data.get("id")
    try:
        user_accounts = account_by_user_id_repo(user_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 400

    return jsonify({"data": user_accounts, "success": True}), 200







# account_key_fields = {"currency", "account_type"}


# def register_account(account_data, user_auth_data):
#     # data checker
#     (incomplete, missing_key, missing_value) = missing_data_checker(
#         account_data, account_key_fields
#     )

#     if incomplete:
#         return jsonify(
#             {
#                 "message": {
#                     "missing key": f"{missing_key}",
#                     "missing value": f"{missing_value}",
#                 },
#                 "success": False,
#             }
#         ), 400

#     # inject stuff to request
#     # add account id to user repo as well
#     accounts = get_all_accounts()
#     current_max_account_id = 0
#     current_max_account_number = 0

#     for account_id, account_data in accounts.items():
#         account_id_number = int(account_id.replace("a", ""))

#         current_max_account_id = max(current_max_account_id, account_id_number)

#         current_max_account_number = max(
#             current_max_account_number, int(account_data["account_number"])
#         )

#     formatted_account_id = f"a{current_max_account_id + 1}"
#     formatted_account_number = f"{current_max_account_number + 1}"

#     # get current time in utc
#     now_utc = datetime.now(timezone.utc).isoformat()

#     # inject acc_id, user_id, accounts, create time
#     account_data.update(
#         {
#             "account_id": formatted_account_id,
#             "user_id": user_auth_data["user_id"],
#             "account_number": formatted_account_number,
#             "balance": 0,
#             "opened_date": now_utc,
#             "status": "active",
#         }
#     )

#     # register account
#     register_account_repository(formatted_account_id, account_data)

#     # register account in user repo
#     register_account_in_user_repository(user_auth_data["user_id"], formatted_account_id)

#     return jsonify(
#         {
#             "data": {
#                 "message": f"account registered successfully! with account id {formatted_account_id} and account number {formatted_account_number}"
#             },
#             "success": True,
#         }
#     ), 201


# def get_user_accounts(user_auth_data):
#     user_id = user_auth_data["user_id"]
#     user_accounts = list(get_accounts_by_user_id(user_id).values())

#     return jsonify({"data": user_accounts, "success": True}), 200


# def update_account_details(account_id, account_request_data):
#     # data checker
#     (incomplete, missing_key, missing_value) = missing_data_checker(
#         account_request_data, account_key_fields
#     )

#     if incomplete:
#         return jsonify(
#             {
#                 "message": {
#                     "missing key": f"{missing_key}",
#                     "missing value": f"{missing_value}",
#                 },
#                 "success": False,
#             }
#         ), 400

#     try:
#         update_account_repository(account_id, account_request_data)
    
#     except Exception as e:
#         return jsonify({"message": str(e), "success": False}), 401

#     return jsonify({"message": "account updated successfully", "success": True}), 200


# def get_account_details(account_id):
#     try:
#         account_data = get_account_by_account_id(account_id)
    
#     except Exception as e:
#         print(e)
#         return jsonify({"message": str(e), "success": False}), 401
    
#     return jsonify({"data": account_data, "success": True}), 200

# (delete from user list as well)
# def delete_account(account_id, user_auth_data):
#     try: 
#         delete_account_repository(account_id, user_auth_data["user_id"])

#     except Exception as e:
#         return jsonify({"message": str(e), "success": False}), 401
    
#     return jsonify({"message": "account deleted successfully", "success": True}), 200