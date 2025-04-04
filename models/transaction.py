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
    status = db.Column(db.String(10), default="completed")

    # relationships
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __repr__(self):
        return f"id = {self.id} | type = {self.type} | payment_method = {self.payment_method} | amount = {self.amount} |  currency = {self.currency} | description = {self.description} | created_at = {self.created_at} | status = {self.status} | from_account_id = {self.from_account_id} | to_account_id = {self.to_account_id}"






# transactions_db = {
#     "transactions": {
#         "a1": {
#             "a1t1": {
#                 "transaction_id": "a1t1",
#                 "account_id": "a1",
#                 "type": "transfer",
#                 "payment_method": "card",
#                 "amount": 100.00,
#                 "currency": "USD",
#                 "description": "Grocery store purchase",
#                 "transaction_date": "01-02-2023",
#                 "status": "completed",
#             },
#             "a1t2": {
#                 "transaction_id": "a1t2",
#                 "account_id": "a1",
#                 "type": "deposit",
#                 "payment_method": "credit",
#                 "amount": 500.00,
#                 "currency": "USD",
#                 "description": "Salary deposit",
#                 "transaction_date": "05-10-2023",
#                 "status": "completed",
#             },
#         },
#         "a2": {
#             "a2t1": {
#                 "transaction_id": "a2t1",
#                 "account_id": "a2",
#                 "type": "withdrawal",
#                 "payment_method": "debit",
#                 "amount": 200.00,
#                 "currency": "USD",
#                 "description": "Utility bill payment",
#                 "transaction_date": "02-11-2023",
#                 "status": "completed",
#             },
#         },
#     }
# }