from flask import Flask
from router.user import users_router
from router.transaction import transactions_router
from router.account import accounts_router
from router.login import login_router


def create_app(config_module = "config.local"):
    app = Flask(__name__)
    app.config.from_object(config_module)
    app.register_blueprint(users_router)
    app.register_blueprint(transactions_router)
    app.register_blueprint(accounts_router)
    app.register_blueprint(login_router)
    return app