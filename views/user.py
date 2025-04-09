import os
from typing import Optional
from flask import jsonify
from repo.user import create_user_repo, user_update_repo
from pydantic import BaseModel, ValidationError

class userRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    address: str
    date_of_birth: str
    testing: Optional[str] = None
    admin_token: Optional[str] = None


def register_user(user_data_request):
    # data checker
    try:
        user_data_validated = userRequest.model_validate(user_data_request)

    except ValidationError as e:
        return jsonify({"message": str(e), "success": False, "location": "user data validation"}), 400
    
    if user_data_validated.admin_token:
        admin_token = os.getenv("ADMIN_TOKEN")

        if admin_token == user_data_validated.admin_token:
            try:
                create_user_repo(user_data_validated, admin_token)

            except Exception as e:  
                return jsonify(
                    {"message": str(e), "success": False, "location": "create admin repo"},
                ), 409
        else:
            return jsonify({"message": "Unauthorized", "success": False, "location": "register admin"}), 401

    else:
        try:
            create_user_repo(user_data_validated)

        except Exception as e:  
            return jsonify(
                {"message": str(e), "success": False, "location": "create user repo"},
            ), 409

    return jsonify(
        {
            "data": {
                "message": f"{user_data_validated.email} registered successfully!"
            },
            "success": True,
        }
    ), 201

    
def get_user(user_auth_data):
    user_auth_data.pop("role")
    return jsonify({"data": user_auth_data, "success": True}), 200

def update_user(user_data_request, user_auth_data):
    # data checker
    try:
        user_data_validated =userRequest.model_validate(user_data_request)

    except ValidationError as e:
        return jsonify(
            {"message": str(e), "success": False, "location": "user data validation"}
        ), 400

    if user_auth_data.get("email") != user_data_validated.email:
        return jsonify(
            {
                "message": "You are not authorized to update this user. Make sure you input your registered email.",
                "success": False,
            }
        ), 400
    
    if user_data_validated.admin_token:
        admin_token = os.getenv("ADMIN_TOKEN")
        print(admin_token)

        if admin_token == user_data_validated.admin_token:
            try:
                user_update_repo(user_data_validated, admin_token)

            except Exception as e:  
                return jsonify(
                    {"message": str(e), "success": False, "location": "update admin repo"},
                ), 409
        else:
            return jsonify({"message": "Unauthorized", "success": False, "location": "update user admin"}), 401
    
    else:
        try:
            user_update_repo(user_data_validated)

        except Exception as e:
            return jsonify(
                {"message": str(e), "success": False, "location": "update user repo"}
            ), 409

    return jsonify(
        {
            "message": f"{user_data_validated.email} updated successfully",
            "success": True,
        }
    ), 200


