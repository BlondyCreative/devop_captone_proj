import sys
from flask import Flask
# Importaciones corregidas usando rutas relativas
import config
from models import db
import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # 1. Inicializar la base de datos
    db.init_app(app)

    with app.app_context():
        # 2. Registro de rutas y manejadores (Corregido)
        import routes
        from common import error_handlers

        # 3. Inicialización de la DB
        if not app.config.get("TESTING"):
            try:
                models.init_db(app) 
                app.logger.info("Database initialized!")
            except Exception as error:
                app.logger.error(f"Database error: {error}")
                if app.config.get("ENV") == "production" and "pytest" not in sys.modules:
                    sys.exit(4)
                else:
                    app.logger.info("Continuando a pesar del error de DB...")
    
    return app

app = create_app()
