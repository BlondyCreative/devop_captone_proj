from flask import jsonify
from service.routes import app
from service.common import status

@app.route("/", methods=["GET"])
def index():
    """Página de inicio"""
    return jsonify(name="Account Rest API Service", version="1.0"), status.HTTP_200_OK

@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Listar todas las cuentas"""
    return jsonify([]), status.HTTP_200_OK
