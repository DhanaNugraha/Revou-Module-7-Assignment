from typing import Optional
from flask import jsonify
from repo.account import account_number_checker_repo, create_account_repo, update_account_repo, delete_account_repo, account_by_account_id_repo, account_by_user_id_repo
from pydantic import BaseModel, ValidationError
import random

class AccountRequest(BaseModel):
    currency: str
    account_type: str   
    testing: Optional[str] = None

def register_account(account_data_request, user_id):
    try:
        account_data_validated = AccountRequest.model_validate(account_data_request)

    except ValidationError as e:
        return jsonify({"message": str(e), "success": False, "location": "account data validation"}), 400
    
    # make account number
    account_number = str(random.randint(1000000000, 9999999999))
    try:
        while account_number_checker_repo(account_number):
            account_number = str(random.randint(1000000000, 9999999999))

    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "account number checker"}), 409

    try:
        create_account_repo(account_data_validated, user_id, account_number)

    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "create account repo"}), 409

    return jsonify({"message": f"account created successfully with account number {account_number}", "success": True}), 200


def update_account_details(account_id, account_data_request):
    # data checker
    try:
        account_data_validated = AccountRequest.model_validate(account_data_request)

    except ValidationError as e:
        return jsonify({"message": str(e), "success": False, "location": "account data validation"}), 400
    
    try:
        account_number = update_account_repo(account_data_validated, account_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "update account repo"}), 409

    return jsonify({"message": f"account {account_number} updated successfully", "success": True}), 200

def delete_account(account_id):
    try:
        delete_account_repo(account_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "delete account repo"}), 409

    return jsonify({"message": "account deleted successfully", "success": True}), 200

def get_account_details(account_id):
    try:
        account_data = account_by_account_id_repo(account_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "get account details repo"}), 409

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
        return jsonify({"message": str(e), "success": False, "location": "get user accounts repo"}), 400

    return jsonify({"data": user_accounts, "success": True}), 200

