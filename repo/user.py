from models.user import users_db
import copy

def get_all_users():
    return copy.deepcopy(users_db["users"])

