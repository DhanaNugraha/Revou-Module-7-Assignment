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


def register_user(user_data_request):
    # data checker
    try:
        user_data_validated = userRequest.model_validate(user_data_request)

    except ValidationError as e:
        return jsonify({"message": str(e), "success": False, "location": "user data validation"}), 400

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
    
    try:
        user_update_repo(user_data_validated)

    except Exception as e:
        return jsonify(
            {"message": str(e), "success": False, "location": "update user repo"}
        ), 409

    return jsonify(
        {
            "message": f"user {user_data_validated.email} updated successfully",
            "success": True,
        }
    ), 200


