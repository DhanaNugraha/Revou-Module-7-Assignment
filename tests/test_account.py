from models.account import AccountsModel
from views.account import register_account, update_account_details, delete_account, get_account_details, get_user_accounts

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_account.py -v -s --cov=.

def test_register_account(test_app, mock_account_data, mock_auth_user_data, db):

    with test_app.app_context():
        response = register_account(mock_account_data, mock_auth_user_data)
        print(response[1])

        assert response[1] == 200

        account = db.session.execute(
            db.select(AccountsModel).filter_by(id=1)
        ).scalar_one()

        assert account.currency == "USD"
        assert account.account_type == "savings"
        assert account.id == 1


def test_register_account_missing_field(test_app, mock_auth_user_data, mock_account_data):

    with test_app.app_context():
        mock_account_data.pop("currency")
        response = register_account(mock_account_data, mock_auth_user_data)
        print(response)

        assert response[1] == 400

def test_register_account_repo_error(test_app, mock_auth_user_data, mock_account_data):
        
    with test_app.app_context():
        mock_account_data.pop("testing")
        response = register_account(mock_account_data, mock_auth_user_data)

        assert response[1] == 409

def test_update_account_details(test_app, mock_account_id, mock_update_account_data, users_data_inject, account_data_inject, db):
    with test_app.app_context():
        response = update_account_details(mock_account_id, mock_update_account_data)

        assert response[1] == 200

        account = db.session.execute(
            db.select(AccountsModel).filter_by(id=1)
        ).scalar_one()

        assert account.currency == "IDR"
        assert account.id == 1

def test_update_account_details_missing_field(test_app, mock_account_id, mock_update_account_data):
    with test_app.app_context():
        mock_update_account_data.pop("currency")
        response = update_account_details(mock_account_id, mock_update_account_data)

        assert response[1] == 400

def test_update_account_details_repo_error(test_app, mock_account_id, mock_update_account_data):
    with test_app.app_context():
        mock_update_account_data.pop("testing")
        response = update_account_details(mock_account_id, mock_update_account_data)

        assert response[1] == 409
       

def test_delete_account(test_app, mock_account_id, users_data_inject, account_data_inject):
    with test_app.app_context():
        response = delete_account(mock_account_id)

        assert response[1] == 200

def test_get_account_details(test_app, mock_account_id, account_data_inject):
    with test_app.app_context():
        response = get_account_details(mock_account_id)

        assert response[1] == 200
       

def test_get_user_accounts(test_app, mock_user_data,users_data_inject, account_data_inject):
    with test_app.app_context():
        response = get_user_accounts(mock_user_data)

        assert response[1] == 200
      


