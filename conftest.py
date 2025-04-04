from flask import request
import pytest
from auth.auth import claim_user_from_token
from auth.before_request import register_auth_middleware
from config.settings import create_app
from models.account import AccountsModel
from models.transaction import TransactionsModel
from models.user import UsersModel
from instance.database import db as _db
from shared.time import now_testing, testing_datetime

@pytest.fixture
def test_app():
    app = create_app("config.testing")
    register_auth_middleware(app)
    with app.app_context():
        _db.create_all()

    yield app

    with app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(test_app):
    with test_app.app_context():
        yield _db

@pytest.fixture
def users_data_inject(test_app):
    users_data = [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone_number": "+1234567890",
            "address": "123 Main St New York NY 10001 USA",
            "date_of_birth": testing_datetime(str(now_testing())),
            "created_at": testing_datetime(str(now_testing())),
            "updated_at": testing_datetime(str(now_testing())),
        },
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "password": "password1234",
            "phone_number": "+0987654321",
            "address": "456 Elm St Los Angeles CA 90001 USA",
            "date_of_birth": testing_datetime(str(now_testing())),
            "created_at": testing_datetime(str(now_testing())),
            "updated_at": testing_datetime(str(now_testing())),
        },
    ]
    with test_app.app_context():
        users_list = []
        for user in users_data:
            user_model = UsersModel(**user)
            users_list.append(user_model)
        print("inserting user data to db")
        # print(type(users_list[0].date_of_birth))
        # print(users_list)
        # print(30*"-")
        _db.session.add_all(users_list)
        _db.session.flush()
        _db.session.commit()
        print("user data inserted")
        return users_list



@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        with test_app.app_context():
            yield client  # This is where the testing happens
    print("Tearing down the test client")
    # yield test_app.test_client()


@pytest.fixture
def mock_user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe.100@example.com",
        "password": "password123",
        "phone_number": "+1234567890",
        "address": "tess",
        "date_of_birth": testing_datetime(str(now_testing())),
        "created_at": testing_datetime(str(now_testing())),
        "updated_at": testing_datetime(str(now_testing())),
        "testing": "true",
    }

@pytest.fixture
def mock_update_user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password1234556",
        "phone_number": "+1234567890",
        "address": "tess",
        "date_of_birth": "1990-01-01",
    }

@pytest.fixture
def mock_auth_user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "+1234567890",
        "address": "tess",
        "date_of_birth": "1990-01-01",
    }

@pytest.fixture
def mock_login_data():
    return {
        "email": "john.doe@example.com",
        "password": "password123",
    }

@pytest.fixture
def mock_incorrect_login_data():
    return {
        "email": "john.doe@example.com",
        "password": "password123456",
    }

@pytest.fixture
def mock_token_data():
    return {"Authorization": "am9obi5kb2VAZXhhbXBsZS5jb206MQ=="}

@pytest.fixture
def mock_account_data():
    return {"currency": "USD", "account_type": "savings"}

@pytest.fixture
def mock_account_id():
    return "a1"

@pytest.fixture
def mock_update_account_data():
    return {"currency": "IDR", "account_type": "savings"}

@pytest.fixture
def mock_transaction_data():
    return {
        "account_id": "a4",
        "type": "deposit",
        "payment_method": "card",
        "amount": 400,
        "currency": "USD",
        "description": "Grocery store purchase",
    }

@pytest.fixture
def mock_transaction_id():
    return "a1t1"

# @pytest.fixture
# def mock_token_data2():
#     return {"Authorization": "am9obi5kb2UuMTAwQGV4YW1wbGUuY29tOnUz"}

