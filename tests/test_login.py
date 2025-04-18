# uv run pytest -v -s --cov=.
# uv run pytest tests/test_login.py -v -s --cov=.

def test_login_user(client, mock_login_data, mock_token_data, users_data_inject):
    login_user = client.post("/login", json=mock_login_data)

    # print(login_user.json)

    assert login_user.status_code == 200
    assert login_user.json["success"] is True
    assert login_user.json["data"]["token"] is not None

def test_incorrect_login_user(client, mock_incorrect_login_data, users_data_inject):
    login_user = client.post("/login", json=mock_incorrect_login_data)

    assert login_user.status_code == 400
    assert login_user.json["success"] is False
    assert login_user.json["message"] == "Invalid credentials"

# make login for admin
def test_login_admin(client, mock_admin_login_data, mock_token_data, users_data_inject):
    login_user = client.post("/login", json=mock_admin_login_data)

    # print(login_user.json)

    assert login_user.status_code == 200
    assert login_user.json["success"] is True
    assert login_user.json["data"]["token"] is not None

