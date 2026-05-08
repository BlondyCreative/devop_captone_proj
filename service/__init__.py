import sys
from flask import Flask
from flask_talisman import Talisman
from service import config
from service.common import log_handlers

# 1. Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(config)

def init_db(app):
    """Inicializa SQLAlchemy de forma segura"""
    # Importamos db aquí o usamos models.db
    from service.models import db 
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)
# 2. Configurar Seguridad (Talisman)
# Definimos la política de seguridad
csp = {
    'default-src': '\'self\'',
    'script-src': ['\'self\'', 'trusted-scripts.com']
}

# Detectamos si estamos en modo de prueba para no forzar HTTPS localmente
is_testing = app.config.get("TESTING", False)

# Inicializamos Talisman UNA SOLA VEZ con toda la configuración
Talisman(app, content_security_policy=csp, force_https=not is_testing)

# 3. Importar rutas y modelos (DESPUÉS de configurar la app)
# pylint: disable=wrong-import-position, cyclic-import, wrong-import-order
from service import routes, models  # noqa: F401 E402
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# 4. Configurar Logging
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

# 5. Inicializar Base de Datos (Solo si no estamos en modo TESTING)
# Los tests inicializan su propia base de datos en setUpClass
if not is_testing:
    try:
        models.init_db(app)
        app.logger.info("Database initialized!")
    except Exception as error:
        app.logger.critical("%s: Cannot continue", error)
        # Gunicorn requiere código 4 para detenerse si los workers mueren
        sys.exit(4)

app.logger.info("Service initialized!")
