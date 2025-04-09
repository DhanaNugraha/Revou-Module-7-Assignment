import pytest
from middleware.before_request import auth_middleware
from config.settings import create_app
from models.account import AccountsModel
from models.transaction import TransactionsModel
from models.user import UsersModel
from instance.database import db as _db
from shared.time import now_testing, testing_datetime
import os

@pytest.fixture
def test_app():
    config_module = os.environ["FLASK_CONFIG"] = "config.testing"
    app = create_app(config_module)
    auth_middleware(app)
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
            "_password_hash": "$2b$12$FCOwMdBOK8A6bon2tuDN.e/ZC1D9AMCORv/HrR/pjxsWA8/szTYCW",
            "phone_number": "+1234567890",
            "address": "123 Main St New York NY 10001 USA",
            "date_of_birth": testing_datetime(str(now_testing())),
            "created_at": testing_datetime(str(now_testing())),
            "updated_at": testing_datetime(str(now_testing())),
            "role": "user",
        },
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "_password_hash": "$2b$12$FCOwMdBOK8A6bon2tuDN.e/ZC1D9AMCORv/HrR/pjxsWA8/szTYCW",
            "phone_number": "+0987654321",
            "address": "456 Elm St Los Angeles CA 90001 USA",
            "date_of_birth": testing_datetime(str(now_testing())),
            "created_at": testing_datetime(str(now_testing())),
            "updated_at": testing_datetime(str(now_testing())),
            "role": "admin",
        },
    ]
    with test_app.app_context():
        users_list = []
        for user in users_data:
            user_model = UsersModel(**user)
            users_list.append(user_model)
        print("inserting user data to db")
        _db.session.add_all(users_list)
        _db.session.commit()
        print("user data inserted")
        return users_list
    
@pytest.fixture
def account_data_inject(test_app):
    account_data = [
        {
            "id": 1,
            "user_id": 1,
            "account_type": "checking",
            "account_number": "1234567890",
            "balance": 1000.00,
            "currency": "USD",
            "status": "active",
            "created_at": testing_datetime(str(now_testing())),
            "updated_at": testing_datetime(str(now_testing())),
        },
        {
            "id": 2,
            "user_id": 1,
            "account_type": "checking",
            "account_number": "1234567891",
            "balance": 2000.50,
            "currency": "USD",
            "status": "active",
            "created_at": testing_datetime(str(now_testing())),
            "updated_at": testing_datetime(str(now_testing())),
        },
        {
            "id": 3,
            "user_id": 2,
            "account_type": "checking",
            "account_number": "1234567892",
            "balance": 2100.50,
            "currency": "USD",
            "status": "active",
            "created_at": testing_datetime(str(now_testing())),
            "updated_at": testing_datetime(str(now_testing())),
        },
    ]
    with test_app.app_context():
        accounts_list = []
        for account in account_data:
            account_model = AccountsModel(**account)
            accounts_list.append(account_model)
        print("inserting account data to db")
        _db.session.add_all(accounts_list)
        _db.session.commit()
        print("account data inserted")
        return accounts_list
    
@pytest.fixture
def transaction_data_inject(test_app):
    transaction_data = [
        {
            "id": 1,
            "from_account_id": 1,
            "to_account_id": 2,
            "type": "transfer",
            "payment_method": "card",
            "amount": 100.00,
            "currency": "USD",
            "description": "Grocery store purchase",
            "status": "completed",
            "created_at": testing_datetime(str(now_testing())),
        }
    ]
    with test_app.app_context():
        transactions_list = []
        for transaction in transaction_data:
            transaction_model = TransactionsModel(**transaction)
            transactions_list.append(transaction_model)
        print("inserting transaction data to db")
        _db.session.add_all(transactions_list)
        _db.session.commit()
        print("transaction data inserted")
        return transactions_list


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client  
    print("Tearing down the test client")


@pytest.fixture
def mock_admin_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe.100@example.com",
        "password": "password123",
        "phone_number": "+1234567890",
        "address": "tess",
        "date_of_birth": testing_datetime(str(now_testing())),
        "testing": "true",
        "admin_token": "admin-token-testing",
    }

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
        "testing": "true",
    }

@pytest.fixture
def mock_auth_user_data():
    return {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "+1234567890",
        "address": "123 Main St New York NY 10001 USA",
        "date_of_birth": testing_datetime(str(now_testing())),
        "created_at": testing_datetime(str(now_testing())),
        "updated_at": testing_datetime(str(now_testing())),
        "role": "user",
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
        "date_of_birth": testing_datetime(str(now_testing())),
        "testing": "true",
    }

@pytest.fixture
def mock_update_user_to_admin_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password1234556",
        "phone_number": "+1234567890",
        "address": "tess",
        "date_of_birth": testing_datetime(str(now_testing())),
        "testing": "true",
        "admin_token": "admin-token-testing",
    }


@pytest.fixture
def mock_login_data():
    return {
        "email": "john.doe@example.com",
        "password": "password123",
    }

@pytest.fixture
def mock_admin_login_data():
    return {
        "email": "jane.smith@example.com",
        "password": "password123",
        "admin_token": "admin-token-testing",
    }

@pytest.fixture
def mock_incorrect_login_data():
    return {
        "email": "john.doe@example.com",
        "password": "password123456",
    }

@pytest.fixture
def mock_token_data():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MzkyODY3NywianRpIjoiZjUwYzllNGMtNmFjMi00ZjMzLTlhZGYtMjg4YjQ5YmRlYmRjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDM5Mjg2NzcsImNzcmYiOiJmNTBkMDUwYi0wZTU2LTRhNTktYWY3OS1iZjA2M2QyOWRjNmMifQ.HYJUuhTStjw94k_UsiVQML7SF9byxh_f_RNAisiM3Kw"
    }

@pytest.fixture
def mock_admin_token_data():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDIxNTU4MywianRpIjoiYzkzODQ1NGMtNjM3NS00NDY5LWE3NTgtYTJkZThkM2JkOGE1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE3NDQyMTU1ODMsImNzcmYiOiI4OTcwYTJhZC0zNzRlLTQyYWEtYTg1OS00Zjc3NWVkYzM5MzIifQ.hl9vNYiQSzqMyU-txUc1kc7-s2h6WIeV3aiZn0Lhp_c"
    }

@pytest.fixture
def mock_account_data():
    return {"currency": "USD", "account_type": "savings", "testing": "true"}

@pytest.fixture
def mock_account_id():
    return 1

@pytest.fixture
def mock_admin_account_id():
    return 3

@pytest.fixture
def mock_update_account_data():
    return {"currency": "IDR", "account_type": "savings", "testing": "true"}

@pytest.fixture
def mock_transfer_data():
    return {
        "from_account_id": 1,
        "to_account_id": 2,
        "type": "transfer",
        "payment_method": "card",
        "amount": 100.00,
        "currency": "USD",
        "description": "Grocery store purchase",
        "testing": "true",
    }

@pytest.fixture
def mock_deposit_data():
    return {
        "from_account_id": 1,
        "type": "deposit",
        "payment_method": "card",
        "amount": 400.00,
        "currency": "USD",
        "testing": "true",
    }

@pytest.fixture
def mock_transaction_id():
    return 1





