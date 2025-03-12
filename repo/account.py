from models.account import accounts_db
import copy

def get_all_accounts():
    return copy.deepcopy(accounts_db["accounts"])