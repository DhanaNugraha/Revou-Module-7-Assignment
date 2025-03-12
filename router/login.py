from flask import Blueprint, request, jsonify
from views.login import login

login_router = Blueprint("login_router", __name__, url_prefix="/login")


@login_router.route("", methods=["POST"])
def login_api():
    return login(request.json)