from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

def init_db(app):
    """Inicializa la base de datos y crea tablas si no existen."""
    with app.app_context():
        db.create_all()

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=True)
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today)

    # CREATE
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    # READ
    @staticmethod
    def find(account_id):
        return Account.query.get(account_id)

    # LIST
    @staticmethod
    def all():
        return Account.query.all()

    # UPDATE
    def update(self):
        db.session.commit()
        return self

    # DELETE
    def delete(self):
        db.session.delete(self)
        db.session.commit()
