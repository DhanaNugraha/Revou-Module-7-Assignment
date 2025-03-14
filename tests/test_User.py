from flask import request


def test_register_user(client, mock_user_data):
    register_user = client.post("/users", json=mock_user_data)
    print(register_user)

    assert register_user.status_code == 201
    assert register_user.json["success"] is True

def test_login_user(client, mock_login_data, mock_token_data):
    login_user = client.post("/login", json= mock_login_data)
    print(login_user)

    assert login_user.status_code == 200
    assert login_user.json["success"] is True
    assert login_user.json["data"]["token"] == mock_token_data["Authorization"]



# def test_middleware(client, mock_token_data,mock_auth_user_data):
#     print(mock_token_data)
#     response = client.get("/users/me", headers=mock_token_data)

#     with client.application.test_request_context(
#         "/users/me", method="GET", headers=mock_token_data
#     ):  
#         client.preprocess_request()
#         print("testttt")
#         print(request)
#         print(request.headers)
#         assert response.status_code == 200
        # assert response.json["data"]["email"] == "john.doe@example.com"
        # assert response.json["data"].get("password") is None

# def test_get_user(client, mock_auth_user_data):
#     get_user = client.get("/users/me", user= mock_auth_user_data)
#     print(get_user)

#     assert get_user.status_code == 200
#     assert get_user.json["success"] is True
#     assert get_user.json["data"]["email"] == "john.doe@example.com"
#     assert get_user.json["data"].get("password") is None


# def test_middleware(client, mock_token_data):
#     with client.test_request_context(headers=mock_token_data):
#         client.preprocess_request()
#         print(request.user)
#         assert request.user["email"] == "john.doe@example.com"



