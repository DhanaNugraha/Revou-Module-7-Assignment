from models.account import AccountsModel
from models.transaction import TransactionsModel

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_transaction.py -v -s --cov=.


def test_initiate_transaction_transfer(client, mock_token_data, mock_transfer_data, users_data_inject, account_data_inject, transaction_data_inject, db):
    response = client.post("/transactions", headers=mock_token_data, json=mock_transfer_data)

    assert response.status_code == 201
    assert response.json["success"] is True

    transaction = db.session.execute(
        db.select(TransactionsModel).filter_by(id=2)
    ).scalar_one()

    assert transaction.currency == "USD"
    assert transaction.type == "transfer"
    assert transaction.amount == 100

    account_from = db.session.execute(
        db.select(AccountsModel).filter_by(id=1)
    ).scalar_one()

    assert account_from.balance == 900

    account_to = db.session.execute(
        db.select(AccountsModel).filter_by(id=2)
    ).scalar_one()

    assert account_to.balance == 2100.50
    

def test_initiate_transaction_deposit(
    client,
    mock_token_data,
    mock_deposit_data,
    users_data_inject,
    account_data_inject,
    transaction_data_inject,
    db,
):
    response = client.post(
        "/transactions", headers=mock_token_data, json=mock_deposit_data
    )

    assert response.status_code == 201
    assert response.json["success"] is True

    transaction = db.session.execute(
        db.select(TransactionsModel).filter_by(id=2)
    ).scalar_one()

    assert transaction.currency == "USD"
    assert transaction.type == "deposit"
    assert transaction.amount == 400

    account_from = db.session.execute(
        db.select(AccountsModel).filter_by(id=1)
    ).scalar_one()

    assert account_from.balance == 1400


def test_initiate_transaction_transfer_missing_data(
    client,
    mock_token_data,
    mock_transfer_data,
    users_data_inject,
    account_data_inject,
    transaction_data_inject,
    db,
):
    mock_transfer_data.pop("amount")
    response = client.post(
        "/transactions", headers=mock_token_data, json=mock_transfer_data
    )

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["location"] == "transaction data validation"

def test_transaction_transfer_no_to_account(client, mock_token_data, mock_transfer_data, users_data_inject, account_data_inject, transaction_data_inject, db):
    mock_transfer_data.pop("to_account_id")
    response = client.post("/transactions", headers=mock_token_data, json=mock_transfer_data)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "To account id is required"

def test_transaction_transfer_insufficient_balance(client, mock_token_data, mock_transfer_data, users_data_inject, account_data_inject, transaction_data_inject, db):
    mock_transfer_data["amount"] = 20000
    response = client.post("/transactions", headers=mock_token_data, json=mock_transfer_data)

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "Insufficient balance"

def test_transaction_transfer_repo_error(client, mock_token_data, mock_transfer_data, users_data_inject, account_data_inject, transaction_data_inject, db):
    mock_transfer_data.pop("testing")
    response = client.post("/transactions", headers=mock_token_data, json=mock_transfer_data)

    assert response.status_code == 409
    assert response.json["success"] is False
    assert response.json["location"] == "transaction modify account balance repo"

def test_transaction_deposit_repo_error(
    client,
    mock_token_data,
    mock_deposit_data,
    users_data_inject,
    account_data_inject,
    transaction_data_inject,
    db,
):
    mock_deposit_data.pop("testing")
    response = client.post(
        "/transactions", headers=mock_token_data, json=mock_deposit_data
    )

    assert response.status_code == 409
    assert response.json["success"] is False
    assert response.json["location"] == "transaction modify account balance repo"

def test_invalid_transaction_type(client, mock_token_data, mock_deposit_data, users_data_inject, account_data_inject, transaction_data_inject, db):
    mock_deposit_data["type"] = "wrong"
    response = client.post(
        "/transactions", headers=mock_token_data, json=mock_deposit_data
    )

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "Invalid transaction type"

def test_get_user__account_transactions(client, mock_token_data, mock_transaction_id, users_data_inject, account_data_inject, transaction_data_inject, db):
    response = client.get("/transactions", headers=mock_token_data)
    print(response.json)

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"][0] == 1

def test_get_transaction_details(client, mock_token_data, mock_transaction_id, users_data_inject, account_data_inject, transaction_data_inject, db):
    response = client.get(f"/transactions/{mock_transaction_id}", headers=mock_token_data)

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"].get("id") == 1
    assert response.json["data"].get("type") == "transfer"
    assert response.json["data"].get("payment_method") == "card"
    assert response.json["data"].get("amount") == 100





# def test_get_user_account_transactions(client, mock_token_data, mock_transaction_id):
#     with client.application.test_request_context(
#         f"/transactions/{mock_transaction_id}", method="GET", headers=mock_token_data
#     ):
#         app.preprocess_request()
#         print(flask.request.user)

#         response = transactions_api()[0]
#         print(response)

#         assert response.json["success"] is True

# def test_initiate_transaction(client, mock_token_data, mock_transaction_data):
#     with client.application.test_request_context(
#         "/transactions",
#         method="POST",
#         headers=mock_token_data,
#         json=mock_transaction_data,
#     ):
#         app.preprocess_request()
#         print(flask.request.user)

#         response = transactions_api()[0]
#         print(response)

#         assert response.json["success"] is True
#         assert len(response.json["data"]) == 1

# def test_get_transaction_details(client, mock_token_data, mock_transaction_id):
#     with client.application.test_request_context(
#         f"/transactions/{mock_transaction_id}", method="GET", headers=mock_token_data
#     ):
#         app.preprocess_request()
#         print(flask.request.user)

#         response = transactions_by_id(mock_transaction_id)[0]
#         print(response)

#         assert response.json["success"] is True
#         assert len(response.json["data"]) == 9



