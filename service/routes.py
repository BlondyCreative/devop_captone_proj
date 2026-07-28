from flask import Blueprint, request, jsonify
from service.models import Account

bp = Blueprint("api", __name__)


# CREATE
@bp.route("/account", methods=["POST"])
def create_account():
    data = request.json
    account = Account()
    account.deserialize(data)
    account.create()
    return jsonify(account.serialize()), 201


# LIST
@bp.route("/account", methods=["GET"])
def list_accounts():
    accounts = Account.all()
    results = [acct.serialize() for acct in accounts]
    return jsonify(results), 200


# READ
@bp.route("/account/<int:account_id>", methods=["GET"])
def read_account(account_id):
    account = Account.find(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account.serialize()), 200


# UPDATE
@bp.route("/account/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = Account.find(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    data = request.json
    account.deserialize(data)
    account.update()
    return jsonify(account.serialize()), 200


# DELETE
@bp.route("/account/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    account = Account.find(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    account.delete()
    return jsonify({"message": "Account deleted"}), 200
