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
                app.logger.info("Database initialized!")
            except Exception as error:
                app.logger.error(f"Database error: {error}")
                
                # SOLO cerramos el proceso si es PRODUCCIÓN real 
                # y NO estamos ejecutando un comando de pytest
                if app.config.get("ENV") == "production" and "pytest" not in sys.modules:
                    sys.exit(4)
                else:
                    # En desarrollo o tests, solo imprimimos el error pero NO matamos el proceso
                    app.logger.info("Skipping SystemExit: Development or Test environment detected.")

    return app
if __name__ == "__main__" or "gunicorn" in sys.argv[0]:
    app = create_app()
