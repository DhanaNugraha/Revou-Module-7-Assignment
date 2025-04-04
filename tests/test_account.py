from models.account import AccountsModel

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_account.py -v -s --cov=.

def test_register_account(client, mock_token_data, mock_account_data, users_data_inject, db):
    response = client.post("/accounts",headers=mock_token_data, json=mock_account_data)

    assert response.status_code == 200
    assert response.json["success"] is True

    account = db.session.execute(
        db.select(AccountsModel).filter_by(id=1)
    ).scalar_one()

    assert account.currency == "USD"
    assert account.account_type == "savings"
    assert account.user_id == 1

def test_register_account_missing_field(client, mock_token_data, mock_account_data, users_data_inject):
    mock_account_data.pop("currency")
    response = client.post("/accounts",headers=mock_token_data, json=mock_account_data)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["location"] == "account data validation"

def test_register_account_repo_error(client, mock_token_data, mock_account_data, users_data_inject):
    mock_account_data.pop("testing")
    response = client.post("/accounts",headers=mock_token_data, json=mock_account_data)

    assert response.status_code == 409
    assert response.json["success"] is False
    assert response.json["location"] == "create account repo"

def test_update_account_details(client, mock_token_data, mock_account_id, mock_update_account_data, users_data_inject, account_data_inject, db):
    response = client.put(f"/accounts/{mock_account_id}", headers=mock_token_data, json=mock_update_account_data)

    assert response.status_code == 200
    assert response.json["success"] is True

    account = db.session.execute(
        db.select(AccountsModel).filter_by(id=1)
    ).scalar_one()

    assert account.currency == "IDR"
    assert account.user_id == 1

def test_update_account_details_missing_field(client, mock_token_data, mock_account_id, mock_update_account_data, users_data_inject, account_data_inject):
    mock_update_account_data.pop("currency")
    response = client.put(f"/accounts/{mock_account_id}", headers=mock_token_data, json=mock_update_account_data)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["location"] == "account data validation"

def test_update_account_details_repo_error(client, mock_token_data, mock_account_id, mock_update_account_data, users_data_inject, account_data_inject):
    mock_update_account_data.pop("testing")
    response = client.put(f"/accounts/{mock_account_id}", headers=mock_token_data, json=mock_update_account_data)
    print(response.json)

    assert response.status_code == 409
    assert response.json["success"] is False
    assert response.json["location"] == "update account repo"

def test_delete_account(client, mock_token_data, mock_account_id, users_data_inject, account_data_inject):
    response = client.delete(f"/accounts/{mock_account_id}", headers=mock_token_data)

    assert response.status_code == 200
    assert response.json["success"] is True

def test_get_account_details(client, mock_token_data, mock_account_id, users_data_inject, account_data_inject):
    response = client.get(f"/accounts/{mock_account_id}", headers=mock_token_data)

    assert response.status_code == 200
    assert response.json["success"] is True

def test_get_user_accounts(client, mock_token_data, users_data_inject, account_data_inject):
    response = client.get("/accounts", headers=mock_token_data)

    assert response.status_code == 200
    assert response.json["success"] is True





# def test_get_user_accounts(client, mock_token_data):
#     with client.application.test_request_context(
#         "/accounts", method="GET", headers=mock_token_data):

#         app.preprocess_request()
#         print(flask.request.user)

#         response = accounts_api()[0]
#         print(response)
#         assert response.json["success"] is True
#         assert len(response.json["data"]) == 2

# def test_register_account(client, mock_token_data, mock_account_data):
#     with client.application.test_request_context(
#         "/accounts", method="POST", headers=mock_token_data, json=mock_account_data):

#         app.preprocess_request()
#         print(flask.request.user)

#         # idk why status code is always 200
#         response = accounts_api()[0]
 
#         assert response.json["success"] is True
#         assert len(response.json["data"]) == 1


# def test_get_account_details(client, mock_token_data, mock_account_id):
#     with client.application.test_request_context(
#         f"/accounts/{mock_account_id}", method="GET", headers=mock_token_data):

#         app.preprocess_request()
#         print(flask.request.user)

#         response = accounts_by_id(mock_account_id)[0]
#         print(response)

#         assert response.json["success"] is True
#         assert len(response.json["data"]) == 8


# def test_update_account_details(client, mock_token_data, mock_account_id, mock_update_account_data):
#     with client.application.test_request_context(
#         f"/accounts/{mock_account_id}", method="PUT", headers=mock_token_data, json=mock_update_account_data):

#         app.preprocess_request()
#         print(flask.request.user)

#         response = accounts_by_id(mock_account_id)[0]
#         print(response)

#         assert response.json["success"] is True
#         assert response.json["message"] == "account updated successfully"

# def test_delete_account(client, mock_token_data, mock_account_id):
#     with client.application.test_request_context(
#         f"/accounts/{mock_account_id}", method="DELETE", headers=mock_token_data):

#         app.preprocess_request()
#         print(flask.request.user)

#         response = accounts_by_id(mock_account_id)[0]
#         print(response)

#         assert response.json["success"] is True
#         assert response.json["message"] == "account deleted successfully"

