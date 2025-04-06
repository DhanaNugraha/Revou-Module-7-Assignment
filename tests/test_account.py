from models.account import AccountsModel
from models.user import UsersModel

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_account.py -v -s --cov=.

def test_register_account(client, mock_token_data, mock_account_data, users_data_inject, db):
    user = db.session.execute(
        db.select(UsersModel).filter_by(id=1)
    ).scalar_one()
    print(user)


    response = client.post("/accounts",headers=mock_token_data, json=mock_account_data)

    print(response.json)

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


