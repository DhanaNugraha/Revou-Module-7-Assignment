from instance.database import db, bcrypt
from shared import time
from sqlalchemy.ext.hybrid import hybrid_property

class UsersModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    _password_hash = db.Column(db.String)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=time.now)
    updated_at = db.Column(db.DateTime, default=time.now, onupdate=time.now)
    # relationships
    accounts = db.relationship("AccountsModel", backref="user")

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hash may not be viewed. It is not a readable attribute.")
    
    @password_hash.setter
    def password_hash(self, password):
        # hash a password in byte form
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        # convert byte to string and inject to db
        self._password_hash = password_hash.decode("utf-8")

    # check_pass_hash input is byte, string. change pass into byte because stored pass is string.
    def authenticate_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    def __repr__(self):
        return f"id = {self.id} | first_name = {self.first_name} | last_name = {self.last_name} | email = {self.email} |  _password_hash = {self._password_hash} | phone_number = {self.phone_number} | address = {self.address} | date_of_birth = {self.date_of_birth} | created_at = {self.created_at} | updated_at = {self.updated_at}"

