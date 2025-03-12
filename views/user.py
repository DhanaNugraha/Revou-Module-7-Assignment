from flask import jsonify
from repo.user import get_all_users, register_user_repository
from datetime import datetime, timezone


user_key_fields = {
    "first_name",
    "last_name",
    "email",
    "password",
    "phone_number",
    "address",
    "date_of_birth",
}

empty_field_check = {"", None}

# check for empty value


def register_user(user_data):
    user_data_keys = user_data.keys()
    user_data_values = user_data.values()

    missing_key = user_key_fields.difference(user_data_keys)

    empty_value = empty_field_check.intersection(user_data_values)

    # data checker
    if missing_key or empty_value:
        return jsonify(
            {
                "message": {
                    "missing key": f"{list(missing_key)}",
                    "missing value": f"{list(empty_value)}",
                },
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
    current_max_user_id = max(users.keys(), key=lambda x: int(x.replace("u", "")))

    # format register id
    user_id = f"u{int(current_max_user_id.replace('u', '')) + 1}"

    # get current time in utc
    now_utc = datetime.now(timezone.utc).isoformat()

    # inject user_id, accounts, create time
    user_data.update({"user_id": user_id, "accounts": {}, "created_at": now_utc})

    # register user
    register_user_repository(user_id, user_data)

    return jsonify(
        {
            "data": {
                "message": f"{request_email} registered successfully! with user id {user_id}"
            },
            "success": True,
        }
    ), 201

# test -> no key, no value, duplicate email, 
# error if key or value in dict type

def get_users(user):
    return jsonify({"data": user, "success": True}), 200


