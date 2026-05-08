from flask import jsonify, request, url_for, make_response, abort
from flask import current_app as app  # <--- Cambia esto
from service.models import Account
from service.common import status
# Elimina: from . import app (esto suele causar errores en los tests)

######################################################################
# GET INDEX
######################################################################
@app.route("/", methods=["GET"])
def index():
    """Página de inicio del microservicio"""
    return jsonify(
        name="Account RESTful Service",
        version="1.0",
        # Asegúrate de que el nombre coincida con la función de abajo
        paths=url_for("list_accounts", _external=True),
    ), status.HTTP_200_OK

######################################################################
# LIST ALL ACCOUNTS
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Lista todas las cuentas disponibles"""
    app.logger.info("Request to list all accounts")
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    return make_response(jsonify(results), status.HTTP_200_OK)
######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Lee una cuenta basado en su ID"""
    app.logger.info("Request to read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return make_response(jsonify(account.serialize()), status.HTTP_200_OK)

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Actualiza una cuenta existente"""
    app.logger.info("Request to update Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    
    account.deserialize(request.get_json())
    account.update()
    return make_response(jsonify(account.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Elimina una cuenta"""
    app.logger.info("Request to delete Account with id: %s", account_id)
    account = Account.find(account_id)
    if account:
        account.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)
