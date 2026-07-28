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

    # CREATE como método de instancia
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    # READ con nombre esperado por los tests
    @staticmethod
    def find(account_id):
        return Account.query.get(account_id)

    # LIST
    @staticmethod
    def all():
        return Account.query.all()

    # UPDATE como método de instancia sin argumentos
    def update(self):
        db.session.commit()
        return self

    # DELETE como método de instancia
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

def init_db(app):
    with app.app_context():
        db.create_all()
