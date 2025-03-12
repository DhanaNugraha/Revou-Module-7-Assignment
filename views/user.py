from flask import jsonify
from repo.user import get_all_users, register_user_repository


user_key_fields = {
    "first_name",
    "last_name",
    "email",
    "password",
    "phone_number",
    "address",
    "date_of_birth",
    "created_at",
}

empty_check = {"", None}


def register_user(user_data):
    user_data_keys = user_data.keys()

    # data checker
    if user_data_keys != user_key_fields:
        missing_data = user_key_fields.difference(user_data_keys)

        return jsonify(
            {
                "message": {"missing data": f"{list(missing_data)}"},
                "success": False,
            }
        ), 400

    request_email = user_data.get("email")

    # check for duplicate in db
    # dont loop db directly, create a copy
    users = get_all_users()
    for _id, registered_user in users.items():
        if registered_user["email"] == request_email:
            return jsonify(
                {
                    "message": "This user already exists. Please register with a different email",
                    "success": False,
                }
            ), 400

    # get the highest current registerd id "uxx"
    current_max_user_id = max(users.keys(), key = lambda x: int(x.replace("u", "")))
    
    # format register id 
    user_id = f"u{int(current_max_user_id.replace('u', '')) + 1}"

    # inject user_id and accounts
    user_data.update({"user_id": user_id, "accounts": {}})

    # register user
    register_user_repository(user_id, user_data)

    # print(all_users_repository())
    return jsonify(
        {"data": {"message": f"{request_email} registered successfully! with user id {user_id}"}, "success": True}
    ), 201
