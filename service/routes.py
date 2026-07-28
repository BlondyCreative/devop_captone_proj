from flask import Blueprint, request, jsonify
from .models import Account

bp = Blueprint("api", __name__)

@bp.route("/")
def index():
    return jsonify({"message": "Service is running"}), 200

# CREATE
@bp.route("/account", methods=["POST"])
def create_account():
    data = request.json
    account = Account(**data).create()
    return jsonify({"message": "Account created", "id": account.id}), 201

# LIST
@bp.route("/account", methods=["GET"])
def list_accounts():
    accounts = Account.all()
    return jsonify([{"id": a.id, "name": a.name, "email": a.email} for a in accounts]), 200

# READ
@bp.route("/account/<int:id>", methods=["GET"])
def read_account(id):
    account = Account.find(id)
    if account:
        return jsonify({"id": account.id, "name": account.name, "email": account.email}), 200
    return jsonify({"error": "Not found"}), 404

# UPDATE
@bp.route("/account/<int:id>", methods=["PUT"])
def update_account(id):
    account = Account.find(id)
    if account:
        data = request.json
        for key, value in data.items():
            setattr(account, key, value)
        account.update()
        return jsonify({"message": "Account updated", "id": account.id}), 200
    return jsonify({"error": "Not found"}), 404

# DELETE
@bp.route("/account/<int:id>", methods=["DELETE"])
def delete_account(id):
    account = Account.find(id)
    if account:
        account.delete()
        return jsonify({"message": "Account deleted", "id": id}), 200
    return jsonify({"error": "Not found"}), 404
