from instance.database import db
from models.transaction import TransactionsModel

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
    db.session.add(new_transaction)
    db.session.commit()

def account_transactions_repo(from_account_id):
    transactions = db.session.execute(db.select(TransactionsModel.id).filter_by(from_account_id=from_account_id)).scalars()
    
    return transactions.all()

def transaction_by_id_repo(transaction_id):
    transaction = db.one_or_404(
        db.select(TransactionsModel).filter_by(id=transaction_id),
        description=f"No transaction with id '{transaction_id}'.",
    )
    return transaction

