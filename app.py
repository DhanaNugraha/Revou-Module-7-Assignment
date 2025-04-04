from flask import request
from auth.auth import claim_user_from_token
from auth.before_request import register_auth_middleware
from config.settings import create_app

app = create_app("config.local")

register_auth_middleware(app)  # Register middleware


# @app.before_request
# def before_request():
#     print("Before request" *10)
#     token = request.headers.get("Authorization")
#     if token:
#         request.user = claim_user_from_token(token)




