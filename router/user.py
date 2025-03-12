from flask import Blueprint, request, jsonify
from auth.auth import login_required
from views.user import get_users, register_user

users_router = Blueprint("users_router", __name__, url_prefix="/users")


@users_router.route("", methods=["POST"])
def users_api():
    return register_user(request.json)


@users_router.route("/me", methods=["GET", "PUT"])
@login_required
def current_user():
    match request.method.lower():
        # give list of all users users (list in users db)
        case "get":
            return get_users(request.user)

        # update users
        case "put":
            pass
