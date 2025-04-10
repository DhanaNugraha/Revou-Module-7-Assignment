from typing import Optional
from flask import jsonify
from repo.account import account_by_account_id_repo, account_by_user_id_repo, modify_account_balance_repo
from repo.transaction import (
    create_transaction_repo,
    account_transactions_repo,
    transaction_by_id_repo,
)
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from instance.database import db

class TransactionRequest(BaseModel):
    type: str
    payment_method: str
    amount: float
    currency: str
    description: Optional[str] = None
    from_account_id: int
    to_account_id: Optional[int] = None
    testing: Optional[str] = None


def substract_balance_calculator(account_id, amount):
    try:
        account = account_by_account_id_repo(account_id)

    except Exception as e:  
        return jsonify({"message": str(e), "success": False, "location": "substract balance repo"}), 409

    return account.balance - amount
    
# def add_balance_calculator(account_id, amount):
#     try:
#         account = account_by_account_id_repo(account_id)

#     except Exception as e:
#         return jsonify({"message": str(e), "success": False, "location": "add balance repo"}), 409

#     return account.balance + amount

def currency_check(transaction_data_request):
    request_currency = transaction_data_request.currency.lower()

    try:
        account_data = account_by_account_id_repo(transaction_data_request.from_account_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "currency check repo"}), 409
    

    account_currency = account_data.currency.lower() 

    if request_currency.lower() != account_currency:
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
        return jsonify({"message": str(e), "success": False, "location": "transaction data validation"}), 400

    transaction_type = transaction_data_validated.type
    from_account_id = transaction_data_validated.from_account_id
    to_account_id = transaction_data_validated.to_account_id
    amount = transaction_data_validated.amount

    # check currency
    currency_check(transaction_data_validated)

    # check account
    account_checker(user_auth_data.get("id"), from_account_id, to_account_id=None)

    # case 1
    if transaction_type == "transfer":
        if to_account_id is None:
            return jsonify(
                {
                    "message": "To account id is required",
                    "success": False,
                }
            ), 400

        try:
            source_final_balance = substract_balance_calculator(from_account_id, amount)

            if source_final_balance < 0:
                return jsonify(
                    {
                        "message": "Insufficient balance",
                        "success": False,
                    }
                ), 400

            # modify source account balance
            modify_account_balance_repo(from_account_id, amount, "-", transaction_data_validated)

        
            # modify target account balance
            modify_account_balance_repo(to_account_id, amount, "+", transaction_data_validated)

            # register transaction
            create_transaction_repo(transaction_data_validated)

            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()

            return jsonify({"message": str(e), "success": False, "location": "transfer modify account balance repo"}), 409

        
    # case 2
    elif transaction_type == "withdraw":
        try:
            source_final_balance = substract_balance_calculator(from_account_id, amount)

            if source_final_balance < 0:
                return jsonify(
                    {
                        "message": "Insufficient balance",
                        "success": False,
                    }
                ), 400
            
            # modify source account balance
            modify_account_balance_repo(from_account_id, amount, "-", transaction_data_validated)

            # register transaction
            create_transaction_repo(transaction_data_validated)

            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()

            return jsonify({"message": str(e), "success": False, "location": "withdraw modify account balance repo"}), 409
        

    # case 3
    elif transaction_type == "deposit":
        try:
            # modify account balance
            modify_account_balance_repo(
                from_account_id, amount, "+", transaction_data_validated
            )

            # register transaction
            create_transaction_repo(transaction_data_validated)

            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()

            return jsonify(
                {
                    "message": str(e),
                    "success": False,
                    "location": "deposit modify account balance repo",
                }
            ), 409


    # case 4
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
        return jsonify({"message": str(e), "success": False, "location": "get user accounts repo"}), 400

    transactions = []

    for from_account_id in user_accounts:
        try:
            account_transactions = account_transactions_repo(from_account_id)

        except Exception as e:
            return jsonify({"message": str(e), "success": False, "location": "get account transactions repo"}), 409

        transactions.extend(account_transactions)

    return jsonify({"data": transactions, "success": True}), 200

def get_transaction_details(transaction_id):
    try:
        transaction_data = transaction_by_id_repo(transaction_id)

    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "get transaction details repo"}), 409
    
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

