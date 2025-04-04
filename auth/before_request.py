# app.py
from flask import request
from auth.auth import claim_user_from_token
# from config.settings import create_app


def register_auth_middleware(app):
    @app.before_request
    def before_request():
        token = request.headers.get("Authorization")
        if token:
            request.user = claim_user_from_token(token)


# app = create_app("config.local")
# register_auth_middleware(app)  # Register middleware
