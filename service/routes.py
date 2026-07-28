from flask import Blueprint, request, jsonify, url_for, make_response, abort
from service.models import Account, db
from service.common import status

bp = Blueprint("accounts", __name__)

######################################################################
# GET INDEX
######################################################################
@bp.route("/", methods=["GET"])
def index():
    """Página de inicio del microservicio"""
    return jsonify(
        name="Account RESTful Service",
        version="1.0",
        paths=url_for("accounts.list_accounts", _external=True),
    ), status.HTTP_200_OK


######################################################################
# LIST ALL ACCOUNTS
######################################################################
@bp.route("/accounts", methods=["GET"])
def list_accounts():
    """Lista todas las cuentas disponibles"""
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# READ AN ACCOUNT
######################################################################
@bp.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """Lee una cuenta basado en su ID"""
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return make_response(jsonify(account.serialize()), status.HTTP_200_OK)


######################################################################
# CREATE AN ACCOUNT
######################################################################
@bp.route("/accounts", methods=["POST"])
def create_account():
    """Crea una nueva cuenta"""
    data = request.get_json()

    # Asegurar que address exista para evitar IntegrityError
    if "address" not in data or data["address"] is None:
        data["address"] = "N/A"

    account = Account()
    account.deserialize(data)
    account.create()
    return make_response(jsonify(account.serialize()), status.HTTP_201_CREATED)


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################
@bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Actualiza una cuenta existente"""
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    data = request.get_json()

    # Asegurar que address exista
    if "address" not in data or data["address"] is None:
        data["address"] = "N/A"

    account.deserialize(data)
    account.update()
    return make_response(jsonify(account.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN ACCOUNT
######################################################################
@bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Elimina una cuenta"""
    account = Account.find(account_id)
    if account:
        account.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)