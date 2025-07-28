from datetime import datetime
from webapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    ts = db.Column(db.DateTime, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(5), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #session = db.Column(db.String(100), nullable=True)
    #is_active = db.Column(db.Boolean, default=True, nullable=False) or is_paid ?
    #subscription_level = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

