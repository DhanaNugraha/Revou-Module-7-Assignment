from flask import jsonify
from auth.auth import get_token
from repo.user import get_user_by_email

def login(login_request_data):
    email = login_request_data.get("email")
    password =login_request_data.get("password")
    user_data = get_user_by_email(email)
    
    assert user_data, "User does not exist"

    assert user_data.get("password") == password, "Incorrect password"

    token = get_token(email, user_data["user_id"])

    return jsonify({"data": {"token": token}, "success": True}), 200