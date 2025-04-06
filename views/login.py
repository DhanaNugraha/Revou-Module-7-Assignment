from flask import jsonify
from auth.auth import get_token
from models.user import UsersModel
from repo.user import user_by_email_repo

def login(login_request_data):
    email = login_request_data.get("email")
    password =login_request_data.get("password")

    try:
        user_data = user_by_email_repo(email)
    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "login repo access"}), 400
    
    # user = UsersModel.query.filter(UsersModel.email == email).first()
    
    if user_data:
        if user_data.authenticate_password(password):
            token = get_token(email, user_data.id)   

            return jsonify({"data": {"token": token}, "success": True}), 200
        
        else:
            return jsonify({"message": "Invalid credentials", "success": False}), 400