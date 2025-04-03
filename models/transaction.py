from instance.database import db
from shared import time

class TransactionsModel(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    payment_method = db.Column(db.String(20))
    amount = db.Column(db.Float(precision=2))
    currency = db.Column(db.String(10))
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=time.now)
    status = db.Column(db.String(10))

    # relationships
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    # accounts = db.relationship("AccountsModel", back_populates="transactions")

transactions_db = {
    "transactions": {
        "a1": {
            "a1t1": {
                "transaction_id": "a1t1",
                "account_id": "a1",
                "type": "transfer",
                "payment_method": "card",
                "amount": 100.00,
                "currency": "USD",
                "description": "Grocery store purchase",
                "transaction_date": "01-02-2023",
                "status": "completed",
            },
            "a1t2": {
                "transaction_id": "a1t2",
                "account_id": "a1",
                "type": "deposit",
                "payment_method": "credit",
                "amount": 500.00,
                "currency": "USD",
                "description": "Salary deposit",
                "transaction_date": "05-10-2023",
                "status": "completed",
            },
        },
        "a2": {
            "a2t1": {
                "transaction_id": "a2t1",
                "account_id": "a2",
                "type": "withdrawal",
                "payment_method": "debit",
                "amount": 200.00,
                "currency": "USD",
                "description": "Utility bill payment",
                "transaction_date": "02-11-2023",
                "status": "completed",
            },
        },
    }
}