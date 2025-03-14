from flask import request
from auth.auth import claim_user_from_token
from config.settings import create_app

app = create_app()

@app.before_request
def before_request():
    token = request.headers.get("Authorization")
    if token:
        request.user = claim_user_from_token(token)


