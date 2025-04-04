# uv run pytest -v -s --cov=.
# uv run pytest tests/test_request_handler.py -v -s --cov=.

def test_before_request_handler(client, mock_token_data, users_data_inject):
    response = client.get("/users/me", headers=mock_token_data)

    assert response.status_code == 200

def test_no_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401  