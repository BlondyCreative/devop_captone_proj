import sys
from flask import Flask
from service import config
from service.models import db
from service import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    models.db.init_app(app)

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
                models.init_db(app) # <--- Ahora sí funcionará
                app.logger.info("Database initialized!")
            except Exception as error:
                app.logger.error(f"Database error: {error}")
                
                # Esto es lo que mataba tus tests:
                if app.config.get("ENV") == "production" and "pytest" not in sys.modules:
                    sys.exit(4)

    return app
if __name__ == "__main__" or "gunicorn" in sys.argv[0]:
    app = create_app()
