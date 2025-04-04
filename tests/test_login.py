from app import app



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

