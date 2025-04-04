from models.user import UsersModel

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_database.py -v -s --cov=.

# users_data is called to inject to db
def test_user_query (db, users_data_inject):
    user = db.session.execute(
        db.select(UsersModel).filter_by(email="john.doe@example.com")
    ).scalar_one()
    
    assert user.password == "password123"
    assert user.id == 1
    assert user.first_name == "John"

