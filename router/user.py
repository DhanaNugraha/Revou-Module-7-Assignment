from flask import Blueprint, request, jsonify

from views.user import register_user

users_router = Blueprint("users_router", __name__, url_prefix="/users")


@users_router.route("", methods=["POST"])
def users_api():
    return register_user(request.json)

@users_router.route("/me", methods=["GET", "PUT"])
def current_user():
    match request.method.lower():
        # give list of all users users (list in users db)
        case "get":
            pass
        # update users
        case "put":
            pass
