import os
from flask import Flask
from flask_cors import CORS
from .models import db, init_db


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Cargar configuración desde config.py
    app.config.from_object("service.config")

    # Si la base de datos es SQLite, asegurar que el archivo exista
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]

    if db_uri.startswith("sqlite:///"):
        # Obtener ruta absoluta del archivo SQLite
        db_file = db_uri.replace("sqlite:///", "")
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), db_file))

        # Crear carpeta si no existe
        db_dir = os.path.dirname(db_path)
        os.makedirs(db_dir, exist_ok=True)

        # Crear archivo vacío si no existe
        if not os.path.exists(db_path):
            open(db_path, "a").close()

        # Reasignar la ruta absoluta
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    db.init_app(app)
    init_db(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app


app = create_app()
