from flask import Blueprint, request
from views.login import login

login_router = Blueprint("login_router", __name__, url_prefix="/login")


@login_router.route("", methods=["POST"])
def login_api():
    try:
        return login(request.json)
    except Exception as e:
        return {"success": False, "message": str(e)}, 400
