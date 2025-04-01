import flask
from app import app
from router.account import accounts_api, accounts_by_id

# uv run pytest -v -s --cov=.

def test_get_user_accounts(client, mock_token_data):
    with client.application.test_request_context(
        "/accounts", method="GET", headers=mock_token_data):

        app.preprocess_request()
        print(flask.request.user)

        response = accounts_api()[0]
        print(response)
        assert response.json["success"] is True
        assert len(response.json["data"]) == 2

def test_register_account(client, mock_token_data, mock_account_data):
    with client.application.test_request_context(
        "/accounts", method="POST", headers=mock_token_data, json=mock_account_data):

        app.preprocess_request()
        print(flask.request.user)

        # idk why status code is always 200
        response = accounts_api()[0]
 
        assert response.json["success"] is True
        assert len(response.json["data"]) == 1


def test_get_account_details(client, mock_token_data, mock_account_id):
    with client.application.test_request_context(
        f"/accounts/{mock_account_id}", method="GET", headers=mock_token_data):

        app.preprocess_request()
        print(flask.request.user)

        response = accounts_by_id(mock_account_id)[0]
        print(response)

        assert response.json["success"] is True
        assert len(response.json["data"]) == 8


def test_update_account_details(client, mock_token_data, mock_account_id, mock_update_account_data):
    with client.application.test_request_context(
        f"/accounts/{mock_account_id}", method="PUT", headers=mock_token_data, json=mock_update_account_data):

        app.preprocess_request()
        print(flask.request.user)

        response = accounts_by_id(mock_account_id)[0]
        print(response)

        assert response.json["success"] is True
        assert response.json["message"] == "account updated successfully"

def test_delete_account(client, mock_token_data, mock_account_id):
    with client.application.test_request_context(
        f"/accounts/{mock_account_id}", method="DELETE", headers=mock_token_data):

        app.preprocess_request()
        print(flask.request.user)

        response = accounts_by_id(mock_account_id)[0]
        print(response)

        assert response.json["success"] is True
        assert response.json["message"] == "account deleted successfully"

