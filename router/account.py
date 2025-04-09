from flask import Blueprint, request
from auth.auth import admin_required, login_required
from views.account import delete_account, get_account_details, get_user_accounts, register_account, update_account_details


accounts_router = Blueprint("accounts_router", __name__, url_prefix="/accounts")

@accounts_router.route("", methods=["GET"])
@login_required
def accounts_api():
    match request.method.lower():
        # give list of all user accounts (list in user db)
        case "get":
            return get_user_accounts(request.user)

@accounts_router.route("", methods=["POST"])
@login_required
@admin_required
def accounts_api_admin():
    match request.method.lower():
        # create new accounts (add to user db and accounts db)
        case "post":
            return register_account(request.json, request.user)

@accounts_router.route("/<account_id>", methods=["GET"])
@login_required
def accounts_by_id(account_id):
    match request.method.lower():
        # give list of all user accounts (list in user db)
        case "get":
            return get_account_details(account_id)
        
@accounts_router.route("/<account_id>", methods=["PUT", "DELETE"])
@login_required
@admin_required
def accounts_by_id_admin(account_id):
    match request.method.lower():
        # update accounts
        case "put":
            return update_account_details(account_id, request.json)
        # delete accounts (transaction will still exist)
        case "delete":
            return delete_account(account_id)
