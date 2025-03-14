from flask import Blueprint, request
from auth.auth import login_required
from views.transaction import get_transaction_details, get_user_account_transactions, initiate_transaction


transactions_router = Blueprint("transactions_router", __name__, url_prefix="/transactions")


@transactions_router.route("", methods=["GET", "POST"])
@login_required
def transactions_api():
    match request.method.lower():
        # give list of all user transactions (list in user db)
        case "get":
            return get_user_account_transactions(request.user)
        # create new transaction (add to user db and transactions db)
        case "post":
            try:
                return initiate_transaction(request.json, request.user)
            except Exception as e:
                return {"success": False, "message": str(e)}, 400


@transactions_router.route("/<transaction_id>", methods=["GET"])
@login_required
def transactions_by_id(transaction_id):
    return get_transaction_details(transaction_id)

