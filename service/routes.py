from flask import Blueprint, request, jsonify
from service.models import Account

bp = Blueprint("api", __name__)


@bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Accounts Service"}), 200


@bp.route("/account", methods=["GET"])
def list_accounts():
    accounts = Account.all()
    results = [acct.serialize() for acct in accounts]
    return jsonify(results), 200


@bp.route("/account/<int:account_id>", methods=["GET"])
def read_account(account_id):
    account = Account.find(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account.serialize()), 200


@bp.route("/account/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = Account.find(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    data = request.json
    account.deserialize(data)
    account.update()
    return jsonify(account.serialize()), 200
