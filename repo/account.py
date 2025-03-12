from models.account import accounts_db
from models.user import users_db
import copy

from repo.user import get_all_users

def get_all_accounts():
    return copy.deepcopy(accounts_db["accounts"])

def get_account_by_user_id(user_id):
    all_accounts = get_all_accounts()

    for account_id, account_data in all_accounts.items():
        if account_data["user_id"] == user_id:
            return account_data

    return None


def register_account_repository(account_id, account_data):
    accounts_db["accounts"].update({account_id: account_data})

def register_account_in_user_repository(user_id, account_id):
    user_account_data = get_all_users()[user_id]["accounts"]

    if user_account_data == {}:
        account_number = 1
    else:
        account_number = max(user_account_data.keys()) + 1

    # update in main user db
    users_db["users"][user_id]["accounts"][account_number] = account_id

def update_account_repository(account_id, account_data):
    accounts_db["accounts"].update({account_id: account_data})