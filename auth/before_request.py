from flask import request
from auth.auth import claim_user_from_token

def register_auth_middleware(app):
    @app.before_request
    def before_request():
        token = request.headers.get("Authorization")
        if token:
            request.user = claim_user_from_token(token)

