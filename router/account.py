from flask import Blueprint, request
from auth.auth import login_required
from views.account import register_account


accounts_router = Blueprint("accounts_router", __name__, url_prefix="/accounts")

@accounts_router.route("", methods=["GET", "POST"])
@login_required
def accounts_api():
    match request.method.lower():
        # give list of all user accounts (list in user db)
        case "get":
            pass
        # create new accounts (add to user db and accounts db)
        case "post":
            return register_account(request.json, request.user)

@accounts_router.route("/<account_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def accounts_by_id():
    match request.method.lower():
        # give list of all user accounts (list in user db)
        case "get":
            pass
        # update accounts
        case "put":
            pass
        # delete accounts (transaction will still exist)
        case "delete":
            pass
