from instance.database import db
from models.account import AccountsModel

def account_number_checker_repo(account_number):
    exist = db.session.execute(
        db.select(AccountsModel).filter_by(account_number=account_number)
    ).scalar_one_or_none()

    # true if exist, false otherwise
    return exist is not None

def create_account_repo(account_data, user_id, account_number):
    # print(user_id)
    # print(type(user_id))
    new_account = AccountsModel(
        account_type = account_data.account_type,
        account_number = account_number,
        currency = account_data.currency,
        user_id = user_id
    )
    db.session.add(new_account)
    db.session.commit()

def update_account_repo(account_data, account_id):
    account = account_by_account_id_repo(account_id)

    account.account_type = account_data.account_type
    account.currency = account_data.currency

    db.session.commit()
    return account.account_number

def delete_account_repo(account_id):
    account = db.one_or_404(
        db.select(AccountsModel).filter_by(id=account_id),
        description=f"No user with id'{account_id}'.",
    )
    db.session.delete(account)
    db.session.commit()

def account_by_account_id_repo(account_id):
    account = db.one_or_404(
        db.select(AccountsModel).filter_by(id=account_id),
        description=f"No user with account id '{account_id}'.",
    )

    return account

def account_by_user_id_repo(user_id):
    accounts = db.session.execute(db.select(AccountsModel.id).filter_by(user_id=user_id)).scalars()

    # .all() returns in list form
    return accounts.all()

def modify_account_balance_repo(account_id, new_amount):
    account = db.one_or_404(
        db.select(AccountsModel).filter_by(id=account_id),
        description=f"No user with account id '{account_id}'.",
    )

    account.balance = new_amount
    db.session.commit()



