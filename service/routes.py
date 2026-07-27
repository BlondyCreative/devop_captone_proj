from flask import jsonify, request, abort, url_for
from service.models import Account
from service.common import status  # Importante para los códigos de estado
from . import app  # Importa la instancia de Flask creada en __init__.py

######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(status="OK"), status.HTTP_200_OK

######################################################################
# GET INDEX
######################################################################
@app.route("/", methods=["GET"])
def index():
    """Root URL response"""
    return jsonify(
        name="Account Rest API Service",
        version="1.0",
        paths=url_for("list_accounts", _external=True),
        health=url_for("health", _external=True)
    ), status.HTTP_200_OK

######################################################################
# LIST ALL ACCOUNTS
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Listar todas las cuentas"""
    app.logger.info("Request to list Accounts")
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    return jsonify(results), status.HTTP_200_OK

######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Leer una cuenta específica"""
    app.logger.info("Request to read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return jsonify(account.serialize()), status.HTTP_200_OK
