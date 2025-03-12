from functools import wraps
from flask import jsonify, request
import base64

from repo.user import get_user_by_email
# from repo.universal import get_user_by_email

# used by login
def get_token(email, id):
    token = base64.b64encode(f"{email}:{id}".encode()).decode()
    return token

# used by middleware
# return user data except password
def claim_user_from_token(token):
    token_user_data = base64.b64decode(token).decode().split(":")

    email = token_user_data[0]
    user = get_user_by_email(email)
    user.pop("password")

    if user is None:
        return jsonify({"message": "Unauthorized", "success": False}), 401

    return user

# used by any function as wrapper
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = getattr(request, "user", None)
        if user is None:
            return jsonify({"message": "Unauthorized", "success": False}), 401
        return f(*args, **kwargs)

    return decorated_function