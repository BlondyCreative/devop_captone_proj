from flask import Blueprint, request, jsonify

bp = Blueprint("api", __name__)

# CREATE
@bp.route("/account", methods=["POST"])
def create_account():
    data = request.json
    return jsonify({"message": "Account created", "data": data}), 201

# LIST
@bp.route("/account", methods=["GET"])
def list_accounts():
    return jsonify({"accounts": []})

# READ
@bp.route("/account/<id>", methods=["GET"])
def read_account(id):
    return jsonify({"account_id": id})

# UPDATE
@bp.route("/account/<id>", methods=["PUT"])
def update_account(id):
    data = request.json
    return jsonify({"message": "Account updated", "id": id, "data": data})

# DELETE
@bp.route("/account/<id>", methods=["DELETE"])
def delete_account(id):
    return jsonify({"message": "Account deleted", "id": id})
