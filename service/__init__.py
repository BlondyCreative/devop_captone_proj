from flask import Flask
from service import config
from service.models import db
import sys

def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)

    db.init_app(flask_app)

    with flask_app.app_context():
        from service import routes
        from service.common import error_handlers

        if not flask_app.config.get("TESTING"):
            try:
                from service import models
                models.init_db(flask_app)
                flask_app.logger.info("Database initialized!")
            except Exception as error:
                flask_app.logger.error(f"Database error: {error}")
                if flask_app.config.get("ENV") == "production" and "pytest" not in sys.argv:
                    sys.exit(4)
                else:
                    flask_app.logger.info("Continuando a pesar del error de DB")

    return flask_app
