from models.user import users_db
import copy

from instance.database import db
from models.user import UsersModel
from shared import time

def create_user_repo(user_data):
    print(user_data.first_name)
    new_user = UsersModel(
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        email = user_data.email,
        password = user_data.password,
        phone_number = user_data.phone_number,
        address = user_data.address,
        date_of_birth = user_data.date_of_birth,
    )
    db.session.add(new_user)
    db.session.commit()

def user_by_email_repo(email):
    user = db.one_or_404(
        db.select(UsersModel).filter_by(email=email),
        description=f"No user with email '{email}'.",
    )
    return user

def user_update_repo(user_data):
    updated_user = UsersModel(
        email=user_data.email,
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        password = user_data.password,
        phone_number = user_data.phone_number,
        address = user_data.address,
        date_of_birth = user_data.date_of_birth,
        updated_at = time.now,
    )
    db.session.add(updated_user)
    db.session.commit()






def get_all_users():
    return copy.deepcopy(users_db["users"])

# def get_user_by_email(email):
#     all_users = get_all_users()

#     for user_id, user_data in all_users.items():
#         if user_data["email"] == email:
#             return user_data
               
#     return None

# def register_user_repository(user_id, user_data):
#     users_db["users"].update({user_id: user_data})
#     # print(users_db["users"])

# def update_user_repository(user_id, user_data):
#     users_db["users"].update({user_id: user_data})




