from typing import Optional
from flask import jsonify
from repo.account import account_by_account_id_repo, account_by_user_id_repo, modify_account_balance_repo
from repo.transaction import (
    create_transaction_repo,
    account_transactions_repo,
    transaction_by_id_repo,
)
from pydantic import BaseModel, ValidationError

class TransactionRequest(BaseModel):
    type: str
    payment_method: str
    amount: float
    currency: str
    description: Optional[str] = None
    from_account_id: int
    to_account_id: Optional[int] = None


def substract_balance(account_id, amount):
    try:
        account = account_by_account_id_repo(account_id)

    except Exception as e:  
        return jsonify({"message": str(e), "success": False}), 400

    if account.balance < amount:
        return False
    else:
        return account.balance - amount
    
def add_balance(account_id, amount):
    try:
        account = account_by_account_id_repo(account_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 400

    return account.balance + amount

def currency_check(transaction_data_request):
    request_currency = transaction_data_request.currency.lower()

    try:
        account_data = account_by_account_id_repo(transaction_data_request.from_account_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 400
    
    account_currency = account_data.currency.lower() 

    if request_currency != account_currency:
        return jsonify(
            {
                "message": "Currency does not match to your account's currency",
                "success": False,
            }
        ), 400
    
def account_checker(user_id, from_account_id, to_account_id=None):
    user_accounts = account_by_user_id_repo(user_id)

    if from_account_id not in user_accounts:    
        return jsonify(
            {
                "message": "From account does not exist in user accounts",
                "success": False,
            }
        ), 400

    if from_account_id == to_account_id:
        return jsonify(
            {
                "message": "You cannot transfer to the same account",
                "success": False,
            }
        ), 400


def initiate_transaction(transaction_data_request, user_auth_data):
    try:
        transaction_data_validated = TransactionRequest.model_validate(transaction_data_request)

    except ValidationError as e:
        return jsonify({"message": str(e), "success": False}), 400

    transaction_type = transaction_data_validated.type
    from_account_id = transaction_data_validated.from_account_id
    to_account_id = transaction_data_validated.to_account_id
    amount = transaction_data_validated.amount

    # check currency
    currency_check(transaction_data_validated)

    # check account
    account_checker(user_auth_data.get("id"), from_account_id, to_account_id=None)

    # case 1
    if transaction_type == "transfer" or transaction_type == "withdrawal":

        if not to_account_id:
            return jsonify(
                {
                    "message": "To account id is required",
                    "success": False,
                }
            ), 400

        source_new_balance = substract_balance(from_account_id, amount)

        if source_new_balance is False:
            return jsonify(
                {
                    "message": "Insufficient balance",
                    "success": False,
                }
            ), 400
        
        # update account balance
        try:
            modify_account_balance_repo(from_account_id, source_new_balance)

        except Exception as e:
            return jsonify({"message": str(e), "success": False}), 400
        
        if to_account_id:
            target_new_balance = add_balance(to_account_id, amount)

            try:
                modify_account_balance_repo(to_account_id, target_new_balance)

            except Exception as e:
                return jsonify({"message": str(e), "success": False}), 400

        # register transaction
        create_transaction_repo(transaction_data_validated)

    # case 2
    elif transaction_type == "deposit":

        target_new_balance = add_balance(from_account_id, amount)

        try:
            modify_account_balance_repo(from_account_id, target_new_balance)

        except Exception as e:
            return jsonify({"message": str(e), "success": False}), 400
        
        # register transaction
        create_transaction_repo(transaction_data_validated)


    # case 3
    else:
        return jsonify(
            {
                "message": "Invalid transaction type",
                "success": False,
            }
        ), 400

    # success message
    return jsonify(
        {
            "data": {
                "message": f"{transaction_type} initiated successfully!"
            },
            "success": True,
        }
    ), 201

def get_user_account_transactions(user_auth_data):
    user_id = user_auth_data.get("id")

    try:
        user_accounts = account_by_user_id_repo(user_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 400

    transactions = []

    for from_account_id in user_accounts:
        try:
            account_transactions = account_transactions_repo(from_account_id)

        except Exception as e:
            return jsonify({"message": str(e), "success": False}), 400

        transactions.extend(account_transactions)

    return jsonify({"data": transactions, "success": True}), 200

def get_transaction_details(transaction_id):
    try:
        transaction_data = transaction_by_id_repo(transaction_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 400
    
    format_transaction_data = {
        "id": transaction_data.id,
        "from_account_id": transaction_data.from_account_id,
        "to_account_id": transaction_data.to_account_id,
        "type": transaction_data.type,
        "payment_method": transaction_data.payment_method,
        "amount": transaction_data.amount,
        "currency": transaction_data.currency,
        "description": transaction_data.description,
        "created_at": transaction_data.created_at,
        "status": transaction_data.status
    }
    
    return jsonify({"data": format_transaction_data, "success": True}), 200

