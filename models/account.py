from instance.database import db
from shared import time


class AccountsModel(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(20))
    account_number = db.Column(db.String(10), unique=True)
    balance = db.Column(db.Float(precision=2), default=0.00)
    currency = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=time.now)
    updated_at = db.Column(db.DateTime, default=time.now, onupdate=time.now)
    status = db.Column(db.String(10), default="active")

    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # user = db.relationship('UsersModel', back_populates='accounts')

    source_transactions = db.relationship(
        "TransactionsModel",
        foreign_keys="TransactionsModel.from_account_id",
        backref="from_account",
        lazy="dynamic",
    )

    target_transactions = db.relationship(
        "TransactionsModel",
        foreign_keys="TransactionsModel.to_account_id",
        backref="to_account",
        lazy="dynamic",
    )

    def __repr__(self):
        return f"id = {self.id} | account_type = {self.account_type} | account_number = {self.account_number} | balance = {self.balance} |  created_at = {self.created_at} | updated_at = {self.updated_at} | status = {self.status} | user_id = {self.user_id}"


# accounts_db = {
#     "accounts": {
#         "a1": {
#             "account_id": "a1",
#             "user_id": "u1",
#             "account_type": "checking",
#             "account_number": "1234567890",
#             "balance": 1500.50,
#             "currency": "USD",
#             "opened_date": "01-01-2023",
#             "status": "active",
#         },
#         "a2": {
#             "account_id": "a2",
#             "user_id": "u1",
#             "account_type": "savings",
#             "account_number": "1234567891",
#             "balance": 5000.00,
#             "currency": "USD",
#             "opened_date": "30-09-2023",
#             "status": "active",
#         },
#         "a3": {
#             "account_id": "a3",
#             "user_id": "u2",
#             "account_type": "checking",
#             "account_number": "1234567892",
#             "balance": 2500.75,
#             "currency": "USD",
#             "opened_date": "15-02-2023",
#             "status": "active",
#         },
#     }
# }
