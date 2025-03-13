from models.transaction import transactions_db
from models.account import accounts_db
from repo.account import get_all_accounts
import copy


def get_all_transactions():
    return copy.deepcopy(transactions_db["transactions"])


def get_account_transactions_repository(account_id):
    account_transactions = get_all_transactions().get(account_id)
    print("+"*30)
    print(account_transactions, account_id)

    if account_transactions:
        return account_transactions


def get_specific_transaction_repository(account_id, transaction_id):
    account_transactions = get_all_transactions().get(account_id)
    # print(account_transaction)

    if account_transactions:
        transaction = account_transactions.get(transaction_id)

        if transaction:
            return transaction


def create_transaction_id(account_id):
    account_transactions = get_all_transactions().get(account_id)

    if account_transactions is None:
        transaction_number = 1

    else:
        # obtains in id form
        current_max_transaction_id = max(
            account_transactions.keys(), key=lambda x: int(x.split("t")[1])
        )

        # obtains in number form
        transaction_number = int(current_max_transaction_id.split("t")[1]) + 1

    return f"{account_id}t{transaction_number}"


def modify_user_balance_repository(transaction_data):
    transaction_type = transaction_data.get("type").lower()
    transaction_amount = transaction_data.get("amount")
    account_id = transaction_data.get("account_id")
    old_balance = get_all_accounts()[account_id].get("balance")

    if transaction_type == "deposit":
        accounts_db["accounts"][account_id].update(
            {"balance": old_balance + transaction_amount}
        )

    # transfer or withdraw
    else:
        accounts_db["accounts"][account_id].update(
            {"balance": old_balance - transaction_amount}
        )


def register_transaction_repository(user_id, transaction_data):
    account_id = transaction_data.get("account_id")
    transaction_id = transaction_data.get("transaction_id")
    account_transactions = get_all_transactions().get(account_id)

    if account_transactions:
        transactions_db["transactions"][account_id].update(
            {transaction_id: transaction_data}
        )

    else:
        transactions_db["transactions"].update(
            {account_id: {transaction_id: transaction_data}}
        )

    # print(transactions_db["transactions"])
