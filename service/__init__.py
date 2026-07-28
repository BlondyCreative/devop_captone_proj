from flask import Flask
from flask_cors import CORS
from .models import db, init_db

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/accounts.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    init_db(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app

# ESTA LÍNEA ES CLAVE PARA LOS TESTS
app = create_app()
