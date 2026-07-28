import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")
db = SQLAlchemy()


def init_db(app):
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)
    with app.app_context():
        db.create_all()


class DataValidationError(Exception):
    pass


class PersistentBase:
    def create(self):
        logger.info("Creating record")
        db.session.add(self)
        db.session.commit()

    def update(self):
        logger.info("Updating record")
        db.session.commit()

    def delete(self):
        logger.info("Deleting record")
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, by_id):
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def all(cls):
        logger.info("Processing all records")
        return cls.query.all()


class Account(db.Model, PersistentBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=True)
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today)

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat(),
        }

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")
            date_joined = data.get("date_joined")
            if date_joined:
                self.date_joined = date.fromisoformat(date_joined)
            else:
                self.date_joined = date.today()
        except KeyError as error:
            msg = "Invalid Account: missing " + error.args[0]
            raise DataValidationError(msg) from error
        except TypeError as error:
            msg = (
                "Invalid Account: body contained bad or no data - "
                + str(error)
            )
            raise DataValidationError(msg) from error
        return self
