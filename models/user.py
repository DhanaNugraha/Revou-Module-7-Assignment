from instance.database import db
from shared import time

class UsersModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=time.now)
    updated_at = db.Column(db.DateTime, default=time.now, onupdate=time.now)
    # relationships
    accounts = db.relationship("AccountsModel", backref="user")

    def __repr__(self):
        return f"id = {self.id} | first_name = {self.first_name} | last_name = {self.last_name} | email = {self.email} |  password = {self.password} | phone_number = {self.phone_number} | address = {self.address} | date_of_birth = {self.date_of_birth} | created_at = {self.created_at} | updated_at = {self.updated_at}"


# users_db = {
#     "users": {
#         "u1": {
#             "user_id": "u1",
#             "first_name": "John",
#             "last_name": "Doe",
#             "email": "john.doe@example.com",
#             "password": "password123",
#             "phone_number": "+1234567890",
#             "address": "123 Main St New York NY 10001 USA",
#             "date_of_birth": "1990-01-01",
#             "created_at": "01-01-2023",
#             "accounts": {1: "a1", 2: "a2"},
#         },
#         "u2": {
#             "user_id": "u2",
#             "first_name": "Jane",
#             "last_name": "Smith",
#             "email": "jane.smith@example.com",
#             "password": "password1234",
#             "phone_number": "+0987654321",
#             "address": "456 Elm St Los Angeles CA 90001 USA",
#             "date_of_birth": "1985-05-15",
#             "created_at": "15-02-2023",
#             "accounts": {
#                 1: "a3",
#             },
#         },
#     }
# }
