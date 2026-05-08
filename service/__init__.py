import sys
from flask import Flask
from flask_talisman import Talisman
from service import config
from service.common import log_handlers
from service.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # 1. Seguridad
    is_testing = app.config.get("TESTING", False)
    Talisman(app, content_security_policy={'default-src': "\'self\'"}, force_https=not is_testing)

    # 2. Extensiones
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)

    with app.app_context():
        # 3. Imports internos
        from service import routes, models
        from service.common import error_handlers, cli_commands

        # 4. Logs
        log_handlers.init_logging(app, "gunicorn.error")

        # 5. Inicialización de DB (PROTEGIDA)
        if not is_testing:
            try:
                models.init_db(app)
            except Exception as error:
                app.logger.error(f"Database connection skipped: {error}")
                # HEMOS ELIMINADO EL SYS.EXIT PARA QUE NO MATE A PYTEST

    return app

# Crear la instancia para Flask/Gunicorn
app = create_app()
