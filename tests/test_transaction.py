import flask
from app import app
from router.transaction import transactions_api, transactions_by_id

# uv run pytest -v -s --cov=.




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



