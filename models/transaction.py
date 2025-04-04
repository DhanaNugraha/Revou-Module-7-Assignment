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


