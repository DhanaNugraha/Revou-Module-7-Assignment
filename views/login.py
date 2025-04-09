import os
from typing import Optional
from flask import jsonify
from flask_jwt_extended import create_access_token
from repo.user import user_by_email_repo
from pydantic import BaseModel, ValidationError

class LoginRequest(BaseModel):
    email: str
    password: str
    admin_token: Optional[str] = None

def login(login_request_data):
    # data checker
    try:
        login_data_validated = LoginRequest.model_validate(login_request_data)

    except ValidationError as e:
        return jsonify(
            {"message": str(e), "success": False, "location": "login data validation"}
        ), 400

    try:
        user_data = user_by_email_repo(login_data_validated.email)
    except Exception as e:
        return jsonify({"message": str(e), "success": False, "location": "login repo access"}), 400
    
    # admin check
    if user_data.role == "admin":
        admin_token = os.getenv("ADMIN_TOKEN")

        if admin_token != login_data_validated.admin_token:
            return jsonify({"message": "Unauthorized", "success": False, "location": "login admin"}), 401
 

    if user_data.authenticate_password(login_data_validated.password):

        token = create_access_token(identity=str(user_data.id))

        return jsonify({"data": {"token": token}, "success": True}), 200
    
    else:
        return jsonify({"message": "Invalid credentials", "success": False}), 400