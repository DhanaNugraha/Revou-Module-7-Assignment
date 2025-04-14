from instance.database import db
from models.user import UsersModel
from shared.time import now, date_from_string, datetime_from_string

def create_user_repo(user_data, admin_token=None):
    new_user = UsersModel(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        address=user_data.address,
        date_of_birth=date_from_string(user_data.date_of_birth),
        created_at=datetime_from_string(str(now())),
        updated_at=datetime_from_string(str(now())),
    )

    new_user.password_hash = user_data.password

    if admin_token:
        new_user.role = "admin"
       
    db.session.add(new_user)
    db.session.commit()

def user_update_repo(user_data, admin_token=None):

    user = user_by_email_repo(user_data.email)

    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.phone_number = user_data.phone_number
    user.address = user_data.address
    user.date_of_birth = (date_from_string(user_data.date_of_birth))
    user.created_at = (datetime_from_string(str(now())))
    user.updated_at = (datetime_from_string(str(now())))

    user.password_hash = user_data.password

    if admin_token:
        user.role = "admin"

    db.session.commit()

def user_by_email_repo(email):
    user = db.one_or_404(
        db.select(UsersModel).filter_by(email=email),
        description=f"No user with email '{email}'.",
    )
    return user

def user_by_id_repo(user_id):
    user = db.one_or_404(
        db.select(UsersModel).filter_by(id=user_id),
        description=f"No user with id '{user_id}'.",
    )
    return user

