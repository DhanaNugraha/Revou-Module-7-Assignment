from models.transaction import transactions_db
from models.account import accounts_db
from repo.account import get_all_accounts
import copy

def get_all_transactions():
    return copy.deepcopy(transactions_db["transactions"])

def get_account_transactions_repository(account_id):
    all_transactions = get_all_transactions()
    return all_transactions.get(account_id)

def get_specific_transaction_repository(account_id, transaction_id):
    return get_all_transactions()[account_id].get(transaction_id)

def create_transaction_id(account_id):
    account_transactions = get_all_transactions().get(account_id)

    if account_transactions is None:
        transaction_number = 1

    else:
        transaction_number = max(int(account_transactions.keys().split("t")[1])) + 1

    return f"{account_id}t{transaction_number}"

def modify_user_balance_repository(transaction_data):
    transaction_type = transaction_data.get("type")
    transaction_amount = transaction_data.get("amount")
    account_id = transaction_data.get("account_id")
    old_balance = get_all_accounts()[account_id].get("balance")

    if transaction_type == "deposit":
        accounts_db["accounts"][account_id].update({"balance": old_balance + transaction_amount})

    # transfer or withdraw
    else:
        accounts_db["accounts"][account_id].update({"balance": old_balance - transaction_amount})

def register_transaction_repository(user_id, transaction_data):
    account_id = transaction_data.get("account_id")
    transaction_id = transaction_data.get("transaction_id")
    
    transactions_db["transactions"][account_id].update({transaction_id: transaction_data})

    