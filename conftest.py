import pytest
from config.settings import create_app


@pytest.fixture
def test_app():
    app = create_app()

    app.config.update({
        "TESTING": True
    })
    yield app

@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
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
        "date_of_birth": "1990-01-01",
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
    return {"Authorization": "am9obi5kb2VAZXhhbXBsZS5jb206dTE="}

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

