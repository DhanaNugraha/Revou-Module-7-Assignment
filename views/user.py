from flask import jsonify
from repo.user import get_all_users, register_user_repository, update_user_repository
from datetime import datetime, timezone
from views.data_checker import missing_data_checker


user_key_fields = {
    "first_name",
    "last_name",
    "email",
    "password",
    "phone_number",
    "address",
    "date_of_birth",
}
   
def register_user(user_data):
    # data checker
    (incomplete, missing_key, missing_value) = missing_data_checker(user_data, user_key_fields)

    if incomplete:
        return jsonify(
            {
                "message": {
                    "missing key": f"{missing_key}",
                    "missing value": f"{missing_value}",
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


def get_user(user_data):
    return jsonify({"data": user_data, "success": True}), 200

def update_user(user_request_data, user_auth_data):
    # data checker
    (incomplete, missing_key, missing_value) = missing_data_checker(user_request_data, user_key_fields)

    if incomplete:
        return jsonify(
            {
                "message": {
                    "missing key": f"{missing_key}",
                    "missing value": f"{missing_value}",
                },
                "success": False,
            }
        ), 400
    
    # check email with auth
    authorized_email = user_auth_data.get("email")
    requested_email = user_request_data.get("email")

    if authorized_email != requested_email:
        return jsonify({"message": "You are not authorized to update this user. Make sure you input your registered email.", "success": False}), 400
    
    # inject user_id, accounts, create_time
    user_request_data.update(
        {
            "user_id" : user_auth_data["user_id"],
            "accounts" : user_auth_data["accounts"],
            "created_at" : user_auth_data["created_at"]   
        }
    )

    update_user_repository(user_auth_data["user_id"], user_request_data)

    return jsonify({"message": "user updated successfully", "success": True}), 200

# test -> no key, no value, wrong email
# error if key or value in dict type