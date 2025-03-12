from flask import Flask, request
from router.user import users_router
from router.transaction import transactions_router
from router.account import accounts_router
from auth.auth import claim_user_from_token


app = Flask(__name__)
app.register_blueprint(users_router)
app.register_blueprint(transactions_router)
app.register_blueprint(accounts_router)

@app.before_request
def before_request():
    token = request.headers.get("Authorization")
    if token:
        request.user = claim_user_from_token(token)

