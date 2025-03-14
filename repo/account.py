from models.account import accounts_db
from models.user import users_db
import copy

from repo.user import get_all_users

def get_all_accounts():
    return copy.deepcopy(accounts_db["accounts"])

def get_accounts_by_user_id(user_id):
    user = get_all_users()[user_id]
    return user["accounts"]

def get_account_by_account_id(account_id):
    account = get_all_accounts().get(account_id)
    # make sure account not None
    assert account, "account does not exist"
    return account

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

def update_account_repository(account_id, account_request_data):
    # get old data
    account_data = get_all_accounts().get(account_id)

    # make sure account not None
    assert account_data, "account does not exist"                   

    # replace data
    account_data.update(account_request_data)

    # inject to db
    accounts_db["accounts"].update({account_id: account_data})

def delete_account_repository(account_id, user_id):
    user_account_data = get_all_users()[user_id]["accounts"]

    # check if account exist
    assert account_id in user_account_data.values(), "account does not exist"

    updated_account_data = {key:val for key, val in user_account_data.items() if val != account_id}

    # update accounts in user db
    users_db["users"][user_id].update({"accounts" : updated_account_data})

    # delete account from account db
    accounts_db["accounts"].pop(account_id)
