from flask import jsonify
from flask_jwt_extended import create_access_token
from repo.user import user_by_email_repo

def login(login_request_data):
    email = login_request_data.get("email")
    password =login_request_data.get("password")

    try:
        user_data = user_by_email_repo(email)
    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "login repo access"}), 400
 
    if user_data:
        if user_data.authenticate_password(password):

            token = create_access_token(identity=str(user_data.id))

            return jsonify({"data": {"token": token}, "success": True}), 200
        
        else:
            return jsonify({"message": "Invalid credentials", "success": False}), 400