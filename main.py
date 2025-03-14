from flask import request
from auth.auth import claim_user_from_token
from config.settings import create_app

app = create_app()

@app.before_request
def before_request():
    print("hereeeeeeeeeee")
    token = request.headers.get("Authorization")
    print("Thosssss",token)
    if token:
        request.user = claim_user_from_token(token)


