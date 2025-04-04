from flask import request, g
import flask
from app import app
from views.user import get_user, update_user
from router.user import users_api, current_user

# uv run pytest -v -s --cov=.






# def test_register_user(client, mock_user_data):
#     register_user = client.post("/users", json=mock_user_data)
#     print(register_user)

#     assert register_user.status_code == 201
#     assert register_user.json["success"] is True


# def test_get_user(client, mock_auth_user_data, mock_token_data):
#     with client.application.test_request_context(
#         "/users/me", method="GET", headers=mock_token_data
#     ):  
#         app.preprocess_request()
#         print(flask.request.user) 

#         response = current_user()[0]
#         print(response)
#         assert response.status_code == 200
#         assert response.json["success"] is True
#         assert len(response.json["data"]) == 9


# def test_update_user(client, mock_update_user_data, mock_token_data):
#     with client.application.test_request_context(
#         "/users/me", method="PUT", headers= mock_token_data, json= mock_update_user_data
#     ):  
#         app.preprocess_request()
#         print(flask.request.user) 

#         response = current_user()[0]
#         print(response)
#         assert response.status_code == 200
#         assert response.json["success"] is True
#         assert response.json["message"] == "user updated successfully"


