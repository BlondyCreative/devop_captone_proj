import os
from flask import Flask
from flask_cors import CORS
from .models import db, init_db


def create_app():
    app = Flask(__name__)
    CORS(app)

    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "..", "instance", "accounts.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    init_db(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app


app = create_app()
