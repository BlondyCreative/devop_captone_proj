from flask import Blueprint, request, jsonify, abort
from .models import Account


bp = Blueprint("accounts", __name__, url_prefix="/accounts")


@bp.route("/", methods=["GET"])
def list_accounts():
    accounts = Account.all()
    result = []

    for account in accounts:
        result.append(
            {
                "id": account.id,
                "name": account.name,
                "email": account.email,
                "address": account.address,
                "phone_number": account.phone_number,
                "date_joined": account.date_joined.isoformat(),
            }
        )

    return jsonify(result), 200


@bp.route("/", methods=["POST"])
def create_account():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        abort(400, "Missing required fields")

    account = Account(
        name=data["name"],
        email=data["email"],
        address=data.get("address"),
        phone_number=data.get("phone_number"),
    )
    account.create()

    return jsonify({"id": account.id}), 201


@bp.route("/<int:account_id>", methods=["GET"])
def get_account(account_id):
    account = Account.find(account_id)

    if not account:
        abort(404)

    return jsonify(
        {
            "id": account.id,
            "name": account.name,
            "email": account.email,
            "address": account.address,
            "phone_number": account.phone_number,
            "date_joined": account.date_joined.isoformat(),
        }
    ), 200


@bp.route("/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = Account.find(account_id)

    if not account:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400)

    account.name = data.get("name", account.name)
    account.email = data.get("email", account.email)
    account.address = data.get("address", account.address)
    account.phone_number = data.get(
        "phone_number",
        account.phone_number,
    )

    account.update()

    return jsonify({"message": "updated"}), 200


@bp.route("/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    account = Account.find(account_id)

    if not account:
        abort(404)

    account.delete()

    return jsonify({"message": "deleted"}), 204
