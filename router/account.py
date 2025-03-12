from flask import Blueprint, request, jsonify

accounts_router = Blueprint("accounts_router", __name__, url_prefix="/accounts")

@accounts_router.route("", methods=["GET", "POST"])
def accounts_api():
    match request.method:
        # give list of all user accounts (list in user db)
        case "get":
            pass
        # create new accounts (add to user db and accounts db)
        case "post":
            pass

@accounts_router.route("/<account_id>", methods=["GET", "PUT", "DELETE"])
def accounts_by_id():
    match request.method:
        # give list of all user accounts (list in user db)
        case "get":
            pass
        # update accounts
        case "put":
            pass
        # delete accounts (transaction will still exist)
        case "delete":
            pass
