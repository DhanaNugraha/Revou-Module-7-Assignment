from models.user import UsersModel

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_user.py -v -s --cov=.

def test_register_user(client, mock_user_data, users_data_inject, db):
    register_user = client.post("/users", json=mock_user_data)
    # print(register_user.json)
    assert register_user.status_code == 201
    assert register_user.json["success"] is True

    user = db.session.execute(
        db.select(UsersModel).filter_by(email="john.doe.100@example.com")
    ).scalar_one()
    
    assert user.id == 3
    assert user.first_name == "John"


def test_register_user_missing_field(client, mock_user_data, users_data_inject):
    mock_user_data.pop("email")
    register_user = client.post("/users", json=mock_user_data)
    # print(register_user.json)
    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "user data validation"

def test_register_repo_error(client, mock_user_data, users_data_inject):
    mock_user_data.pop("testing")
    register_user = client.post("/users", json=mock_user_data)
    # print(register_user.json)
    assert register_user.status_code == 409
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "create user repo"

def test_get_user(client, mock_token_data, users_data_inject):
    response = client.get("/users/me", headers=mock_token_data)

    assert response.status_code == 200
    assert response.json["success"] is True

def test_update_user(client, mock_update_user_data, mock_token_data, users_data_inject, db):
    response = client.put("/users/me", headers=mock_token_data, json=mock_update_user_data)

    assert response.status_code == 200
    assert response.json["success"] is True

    user = db.session.execute(
        db.select(UsersModel).filter_by(email="john.doe@example.com")
    ).scalar_one()
    
    assert user.id == 1
    assert user.address == "tess"

def test_update_user_missing_field(client, mock_update_user_data, mock_token_data, users_data_inject):
    mock_update_user_data.pop("email")
    response = client.put(
        "/users/me", headers=mock_token_data, json=mock_update_user_data
    )

    assert response.status_code == 400
    assert response.json["success"] is False

def test_update_user_wrong_email(
    client, mock_update_user_data, mock_token_data, users_data_inject
):
    mock_update_user_data["email"] = "wrong@example.com"
    response = client.put(
        "/users/me", headers=mock_token_data, json=mock_update_user_data
    )

    assert response.status_code == 400
    assert response.json["success"] is False
    assert (
        response.json["message"]
        == "You are not authorized to update this user. Make sure you input your registered email."
    )

def test_update_user_repo_error(
    client, mock_update_user_data, mock_token_data, users_data_inject
):
    mock_update_user_data.pop("testing")
    response = client.put(
        "/users/me", headers=mock_token_data, json=mock_update_user_data
    )

    assert response.status_code == 409
    assert response.json["success"] is False
    assert response.json["location"] == "update user repo"





# def test_get_user(client, mock_auth_user_data, mock_token_data, users_data_inject, ):
#     with client.application.test_request_context(
#         "/users/me", method="GET", headers=mock_token_data
#     ):
#         app.preprocess_request()
#         print(flask.request.user)

#         response = current_user()[0]
#         print(response)
#         assert response.status_code == 200
#         assert response.json["success"] is True
#         assert len(response.json["data"]) == 9



# def test_register_user(client, mock_user_data):
#     register_user = client.post("/users", json=mock_user_data)
#     print(register_user)

#     assert register_user.status_code == 201
#     assert register_user.json["success"] is True


# def test_get_user(client, mock_auth_user_data, mock_token_data):
#     with client.application.test_request_context(
#         "/users/me", method="GET", headers=mock_token_data
#     ):  
#         app.preprocess_request()
#         print(flask.request.user) 

#         response = current_user()[0]
#         print(response)
#         assert response.status_code == 200
#         assert response.json["success"] is True
#         assert len(response.json["data"]) == 9


# def test_update_user(client, mock_update_user_data, mock_token_data):
#     with client.application.test_request_context(
#         "/users/me", method="PUT", headers= mock_token_data, json= mock_update_user_data
#     ):  
#         app.preprocess_request()
#         print(flask.request.user) 

#         response = current_user()[0]
#         print(response)
#         assert response.status_code == 200
#         assert response.json["success"] is True
#         assert response.json["message"] == "user updated successfully"


