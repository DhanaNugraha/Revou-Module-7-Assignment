from models.user import users_db
import copy

def get_all_users():
    return copy.deepcopy(users_db["users"])

def get_user_by_email(email):
    all_users = get_all_users()

    for user_id, user_data in all_users.items():
        if user_data["email"] == email:
            return user_data
        
    return None

def register_user_repository(user_id, user_data):
    users_db["users"].update({user_id: user_data})