from flask import Flask
from flask_cors import CORS
from service.models import db, init_db

def create_app():
    app = Flask(__name__)

    # CONFIGURACIÓN DE LA BASE DE DATOS
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accounts.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # INICIALIZAR SQLALCHEMY
    db.init_app(app)

    # CREAR TABLAS
    init_db(app)

    # CORS
    CORS(app)

    # REGISTRAR RUTAS
    from .routes import bp
    app.register_blueprint(bp)

    return app


app = create_app()