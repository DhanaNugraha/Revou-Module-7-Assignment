from instance.database import db
from models.user import UsersModel
from shared.time import now_testing, testing_datetime

def create_user_repo(user_data):
    print(user_data, "-"*30)
    new_user = UsersModel(
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        email = user_data.email,
        password = user_data.password,
        phone_number = user_data.phone_number,
        address = user_data.address,
        date_of_birth = user_data.date_of_birth,
    )

    if user_data.testing:
       new_user.date_of_birth = testing_datetime(str(now_testing()))
       new_user.created_at = testing_datetime(str(now_testing()))
       new_user.updated_at = testing_datetime(str(now_testing()))

    db.session.add(new_user)
    db.session.commit()

def user_by_email_repo(email):
    user = db.one_or_404(
        db.select(UsersModel).filter_by(email=email),
        description=f"No user with email '{email}'.",
    )
    return user

def user_update_repo(user_data):

    user = user_by_email_repo(user_data.email)

    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.password = user_data.password
    user.phone_number = user_data.phone_number
    user.address = user_data.address
    user.date_of_birth = user_data.date_of_birth
    # updated at ada di model

    if user_data.testing:
       user.date_of_birth = testing_datetime(str(now_testing()))
       user.created_at = testing_datetime(str(now_testing()))
       user.updated_at = testing_datetime(str(now_testing()))

    db.session.commit()

