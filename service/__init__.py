from flask import Flask
from flask_cors import CORS
from service.models import db, init_db
from service.routes import bp


def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accounts.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Crear tablas
    init_db(app)

    # CORS
    CORS(app)

    # Registrar rutas (Blueprint)
    app.register_blueprint(bp)

    return app


app = create_app()