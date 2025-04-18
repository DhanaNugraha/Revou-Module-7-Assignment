from sqlalchemy import or_
from instance.database import db
from models.transaction import TransactionsModel
from shared.time import now_testing, testing_datetime

def create_transaction_repo(transaction_data):
    new_transaction = TransactionsModel(    
        type = transaction_data.type,
        payment_method = transaction_data.payment_method,
        amount = transaction_data.amount,
        currency = transaction_data.currency,
        description = transaction_data.description, 
        from_account_id = transaction_data.from_account_id,
        to_account_id = transaction_data.to_account_id
    )

    if transaction_data.testing:
        new_transaction.created_at = testing_datetime(str(now_testing()))

    db.session.add(new_transaction)
    # db.session.commit()

def account_transactions_repo(account_ids_list):
    transactions = db.session.execute(
        db.select(TransactionsModel.id).where(
            or_(
                TransactionsModel.to_account_id.in_(account_ids_list),
                TransactionsModel.from_account_id.in_(account_ids_list),
            )
        )
    ).scalars()
    
    return transactions.all()

def transaction_by_id_repo(transaction_id):
    transaction = db.one_or_404(
        db.select(TransactionsModel).filter_by(id=transaction_id),
        description=f"No transaction with id '{transaction_id}'.",
    )
    return transaction

