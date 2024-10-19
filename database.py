from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    is_hr = db.Column(db.Boolean, default=False)
    is_candidate = db.Column(db.Boolean, default=False)

    def verify_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)
