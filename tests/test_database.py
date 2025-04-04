from models.user import UsersModel

# users_data is called to inject to db
def test_user_query (db, users_data_inject):
    user = db.one_or_404(
        db.select(UsersModel).filter_by(email="john.doe@example.com"),
        description="No user with email 'john.doe@example.com'.",
    )
    print(user)

    assert user.password == "password123"
    assert user.id == 1
    assert user.first_name == "John"