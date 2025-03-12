from flask import Blueprint, request, jsonify

users_router = Blueprint("users_router", __name__, url_prefix="/users")


@users_router.route("", methods=["POST"])
def users_api():
    match request.method:
        case "post":
            pass

@users_router.route("/me", methods=["GET", "PUT"])
def current_user():
    match request.method:
        # give list of all users users (list in users db)
        case "get":
            pass
        # update users
        case "put":
            pass
