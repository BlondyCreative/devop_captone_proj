import sys
from flask import Flask
from service import config
from service.models import db
from service import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # 1. Inicializar la base de datos (Solo una vez)
    db.init_app(app)

    with app.app_context():
        # 2. Registro de rutas y manejadores
        from service import routes
        from service.common import error_handlers

        # 3. Inicialización de la DB (Solo si no es para tests)
        if not app.config.get("TESTING"):
            try:
                models.init_db(app) 
                app.logger.info("Database initialized!")
            except Exception as error:
                app.logger.error(f"Database error: {error}")
                # Solo cerramos si es producción y NO estamos testeando
                if app.config.get("ENV") == "production" and "pytest" not in sys.modules:
                    sys.exit(4)
                else:
                    app.logger.info("Continuando a pesar del error de DB...")
    
    return app
app = create_app() 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
