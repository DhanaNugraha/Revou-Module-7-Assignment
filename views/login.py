from flask import jsonify
from auth.auth import get_token
from repo.user import user_by_email_repo

def login(login_request_data):
    email = login_request_data.get("email")
    password =login_request_data.get("password")
    user_data = user_by_email_repo(email)
    print("login view -> user data", user_data)
    # assert user_data, "User does not exist"

    assert user_data.password == password, "Incorrect password"

    token = get_token(email, user_data.id)
    print("login view -> token", token)
    return jsonify({"data": {"token": token}, "success": True}), 200