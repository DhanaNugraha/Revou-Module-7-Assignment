from flask import Blueprint, request, jsonify

transactions_router = Blueprint("transactions_router", __name__, url_prefix="/transactions")


@transactions_router.route("", methods=["GET", "POST"])
def transactions_api():
    match request.method:
        # give list of all user transactions (list in user db)
        case "get":
            pass
        # create new transaction (add to user db and transactions db)
        case "post":
            pass


@transactions_router.route("/<transaction_id>", methods=["GET"])
def transactions_by_id():
    match request.method:
        # give list of user transaction by id
        case "get":
            pass

