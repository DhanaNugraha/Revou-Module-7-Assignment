from flask import jsonify
from datetime import datetime, timezone
from repo.account import get_account_by_account_id
from repo.transaction import create_transaction_id, get_account_transactions_repository, get_specific_transaction_repository, modify_user_balance_repository, register_transaction_repository
from views.data_checker import missing_data_checker


transaction_key_fields = {
    "account_id",
    "type",
    "payment_method",
    "amount",
    "currency",
    "description"
}


def initiate_transaction(transaction_data, user_auth_data):
    # data checker
    (incomplete, missing_key, missing_value) = missing_data_checker(
        transaction_data, transaction_key_fields
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
    
    # prelim check
    account_id = transaction_data.get("account_id")
    account_data = get_account_by_account_id(account_id)

    # check currency
    if transaction_data.get("currency").lower() != account_data.get("currency").lower():
        return jsonify(
            {
                "message": "Currency does not match to your account's currency",
                "success": False,
            }
        ), 400
    
    # store required data for use
    user_id = user_auth_data.get("user_id")
    transaction_id = create_transaction_id(account_id)
    transaction_date = datetime.now(timezone.utc).isoformat()
    transaction_type = transaction_data.get("type").lower()

    # inject transaction_id, transaction_date, status
    transaction_data.update(
        {
            "transaction_id": transaction_id,
            "transaction_date": transaction_date,
            "status": "completed",
        }
    )
    
    # check balance and proceed with transaction
    if transaction_type == "transfer" or transaction_type == "withdrawal":
        if transaction_data.get("amount") > account_data.get("balance"):
            return jsonify({"message": "Insufficient balance", "success": False}), 400
        
        else:
            modify_user_balance_repository(transaction_data)
            register_transaction_repository(user_id, transaction_data)
    
    elif transaction_type == "deposit":
        modify_user_balance_repository(transaction_data)
        register_transaction_repository(user_id, transaction_data)

    else:
        return jsonify({"message": "Invalid transaction type", "success": False}), 400

    return jsonify(
        {
            "data": {
                "message": f"transaction initiated successfully! with account id {account_id} and transaction id {transaction_id}"
            },
            "success": True,
        }
    ), 201


def get_user_account_transactions(user_auth_data):
    user_accounts = user_auth_data.get("accounts")
    if user_accounts is None:
        transaction_data = {}

    else:
        transaction_data = {}

        for account_id in user_accounts.values():
            account_transactions = get_account_transactions_repository(account_id)

            if account_transactions:
                transaction_data.update(
                    {account_id: account_transactions}
                )

    return jsonify({"data": transaction_data, "success": True}), 200


def get_transaction_details(transaction_id):
    account_id= transaction_id.split("t")[0]

    transaction_data = get_specific_transaction_repository(account_id, transaction_id)

    if transaction_data is None:
        transaction_data = {}

    return jsonify({"data": transaction_data, "success": True}), 200
