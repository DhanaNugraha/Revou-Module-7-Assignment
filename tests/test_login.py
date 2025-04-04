from app import app

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_login.py -v -s --cov=.

def test_login_user(client, mock_login_data, mock_token_data, users_data_inject):
    login_user = client.post("/login", json=mock_login_data)
    # print(login_user)
    # print(login_user.json)

    assert login_user.status_code == 200
    assert login_user.json["success"] is True
    assert login_user.json["data"]["token"] == mock_token_data["Authorization"]

def test_before_request_handler(client, mock_token_data, users_data_inject):

    # Make a request to any endpoint (you might need to create a test endpoint)
    response = client.get("/users/me", headers=mock_token_data)
    print(response.json)

    # Verify that request.user was set (you'll need a way to check this)
    # This depends on how you can verify the user was set - maybe through a response?
    assert response.status_code == 200
    # Add more assertions based on your implementation

    # Test without a token
    response = client.get("/users/me")
    assert response.status_code == 401  # Or whatever your app returns for unauthorized


# def test_login_user(client, mock_login_data, mock_token_data):
#     login_user = client.post("/login", json=mock_login_data)
#     print(login_user)

#     assert login_user.status_code == 200
#     assert login_user.json["success"] is True
#     assert login_user.json["data"]["token"] == mock_token_data["Authorization"]

# def test_incorrect_login_user(client, mock_incorrect_login_data, mock_token_data):
#     login_user = client.post("/login", json=mock_incorrect_login_data)
#     print(login_user)

#     assert login_user.status_code == 400
#     assert login_user.json["success"] is False
#     assert login_user.json["message"] == "Incorrect password"

