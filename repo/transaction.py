from models.transaction import transactions_db
import copy

def get_all_transactions():
    return copy.deepcopy(transactions_db["transactions"])