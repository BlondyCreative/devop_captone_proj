from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=True)
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today)

    # CREATE
    @staticmethod
    def create(data):
        account = Account(**data)
        db.session.add(account)
        db.session.commit()
        return account

    # READ
    @staticmethod
    def read(account_id):
        return Account.query.get(account_id)

    # LIST
    @staticmethod
    def list_all():
        return Account.query.all()

    # UPDATE
    @staticmethod
    def update(account_id, data):
        account = Account.query.get(account_id)
        if account:
            for key, value in data.items():
                setattr(account, key, value)
            db.session.commit()
        return account

    # DELETE
    @staticmethod
    def delete(account_id):
        account = Account.query.get(account_id)
        if account:
            db.session.delete(account)
            db.session.commit()
        return account

def init_db(app):
    with app.app_context():
        db.create_all()
