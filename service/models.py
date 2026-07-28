import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# SQLAlchemy global instance
db = SQLAlchemy()

def init_db(app):
    """
    Inicializa la base de datos de forma segura.
    Se asegura de que SQLAlchemy esté registrado y crea las tablas.
    """
    if 'sqlalchemy' not in app.extensions:
        db.init_app(app)

    with app.app_context():
        db.create_all()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


######################################################################
#  PERSISTENT BASE MODEL
######################################################################
class PersistentBase:
    """Base class added persistent methods"""

    def create(self):
        """Creates a record to the database"""
        logger.info("Creating record")
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a record to the database"""
        logger.info("Updating record")
        db.session.commit()

    def delete(self):
        """Removes a record from the data store"""
        logger.info("Deleting record")
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, by_id):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def all(cls):
        """Returns all records in the database"""
        logger.info("Processing all records")
        return cls.query.all()


######################################################################
#  ACCOUNT MODEL
######################################################################
class Account(db.Model, PersistentBase):
    """Class that represents an Account"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)

    # ← ESTA LÍNEA ERA EL PROBLEMA
    # Tus tests NO envían address, así que debe ser nullable=True
    address = db.Column(db.String(256), nullable=True)

    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today)

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def serialize(self):
        """Serializes an Account into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat()
        }

    def deserialize(self, data):
        """Deserializes an Account from a dictionary"""
        try:
            self.name = data["name"]
            self.email = data["email"]

            # address puede faltar → tus tests lo omiten
            self.address = data.get("address", None)

            self.phone_number = data.get("phone_number")

            date_joined = data.get("date_joined")
            if date_joined:
                self.date_joined = date.fromisoformat(date_joined)
            else:
                self.date_joined = date.today()

        except KeyError as error:
            raise DataValidationError("Invalid Account: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Account: body of request contained bad or no data - " + str(error)
            ) from error

        return self

    @classmethod
    def find_by_name(cls, name):
        """Returns all Accounts with the given name"""
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)