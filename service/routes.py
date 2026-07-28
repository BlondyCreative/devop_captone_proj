from flask import Blueprint, request, jsonify
from .models import Account

bp = Blueprint("api", __name__)

# CREATE
@bp.route("/account", methods=["POST"])
def create_account():
    data = request.json
    account = Account.create(data)
    return jsonify({"message": "Account created", "id": account.id}), 201

# LIST
@bp.route("/account", methods=["GET"])
def list_accounts():
    accounts = Account.list_all()
    return jsonify([{"id": a.id, "name": a.name, "email": a.email} for a in accounts])

# READ
@bp.route("/account/<int:id>", methods=["GET"])
def read_account(id):
    account = Account.read(id)
    if account:
        return jsonify({"id": account.id, "name": account.name, "email": account.email})
    return jsonify({"error": "Not found"}), 404

# UPDATE
@bp.route("/account/<int:id>", methods=["PUT"])
def update_account(id):
    data = request.json
    account = Account.update(id, data)
    if account:
        return jsonify({"message": "Account updated", "id": account.id})
    return jsonify({"error": "Not found"}), 404

# DELETE
@bp.route("/account/<int:id>", methods=["DELETE"])
def delete_account(id):
    account = Account.delete(id)
    if account:
        return jsonify({"message": "Account deleted", "id": id})
    return jsonify({"error": "Not found"}), 404
