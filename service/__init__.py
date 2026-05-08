import sys
from flask import Flask
from flask_talisman import Talisman
from service import config
from service.common import log_handlers
# Importamos la instancia de SQLAlchemy desde models
from service.models import db

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config)

    # 1. Configurar Seguridad (Talisman)
    csp = {
        'default-src': '\'self\'',
        'script-src': ['\'self\'', 'trusted-scripts.com']
    }

    # Detectamos si estamos en modo de prueba
    is_testing = app.config.get("TESTING", False)
    
    # Inicializamos Talisman
    Talisman(app, content_security_policy=csp, force_https=not is_testing)

    # 2. Inicializar extensiones
    # Solo inicializamos si no ha sido registrada previamente (evita el RuntimeError)
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)

    # 3. Importar rutas y handlers (dentro del contexto para evitar ciclos)
    with app.app_context():
        # pylint: disable=import-outside-toplevel
        from service import routes, models
        from service.common import error_handlers, cli_commands

        # 4. Configurar Logging
        log_handlers.init_logging(app, "gunicorn.error")

        app.logger.info(70 * "*")
        app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
        app.logger.info(70 * "*")

        # 5. Inicializar Base de Datos (Solo si no estamos en TESTING)
        if not is_testing:
            try:
                models.init_db(app)
                app.logger.info("Database initialized!")
            except Exception as error:
                app.logger.critical("%s: Cannot continue", error)
                sys.exit(4)

    app.logger.info("Service initialized!")
    return app

# Creamos la instancia global para que Gunicorn la encuentre
app = create_app()
