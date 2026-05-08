import sys
from flask import Flask
from service import config
from service.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # 1. Inicializar la base de datos (evitando el RuntimeError)
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)

    with app.app_context():
        # 2. IMPORTANTE: Aquí es donde incluyes routes.py
        from service import routes  # <--- Esto registra tus rutas
        from service.common import error_handlers

        # 3. Inicialización segura de la DB para tests
        if not app.config.get("TESTING"):
            try:
                models.init_db(app)
            except Exception as error:
                app.logger.error(f"Error de base de datos: {error}")
                # No uses sys.exit(4) aquí para que pytest no muera
                if app.config.get("ENV") == "production":
                    sys.exit(4)

    return app
