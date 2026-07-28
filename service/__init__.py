import os
from flask import Flask
from flask_cors import CORS
from .models import db, init_db


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Cargar configuración desde config.py
    app.config.from_object("service.config")

    # Obtener URI
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]

    # Si es SQLite, preparar archivo
    if db_uri.startswith("sqlite:///"):
        db_file = db_uri.replace("sqlite:///", "")
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, db_file)

        # Crear archivo si no existe
        if not os.path.exists(db_path):
            open(db_path, "a").close()

        # Reasignar ruta absoluta (dividida para evitar E501)
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = f"sqlite:///{db_path}"

    db.init_app(app)
    init_db(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app


app = create_app()
