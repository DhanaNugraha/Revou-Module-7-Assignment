from flask import Blueprint, request
from auth.auth import login_required


transactions_router = Blueprint("transactions_router", __name__, url_prefix="/transactions")


@transactions_router.route("", methods=["GET", "POST"])
@login_required
def transactions_api():
    match request.method.lower():
        # give list of all user transactions (list in user db)
        case "get":
            pass
        # create new transaction (add to user db and transactions db)
        case "post":
            pass


@transactions_router.route("/<transaction_id>", methods=["GET"])
@login_required
def transactions_by_id():
    match request.method.lower():
        # give list of user transaction by id
        case "get":
            pass

