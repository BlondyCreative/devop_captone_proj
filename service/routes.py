from flask import jsonify, request, abort, url_for, current_app as app
from service.models import Account
from service.common import status

######################################################################
# INDEX
######################################################################
@app.route("/", methods=["GET"])
def index():
    return jsonify(
        name="Account REST API Service",
        version="1.0",
        paths={
            "list": url_for("list_accounts", _external=True),
            "create": url_for("create_account", _external=True),
            "read": url_for("get_account", account_id=1, _external=True),
            "update": url_for("update_account", account_id=1, _external=True),
            "delete": url_for("delete_account", account_id=1, _external=True),
        }
    ), status.HTTP_200_OK

######################################################################
# LIST ACCOUNTS
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    app.logger.info("Request for account list")
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    return jsonify(results), status.HTTP_200_OK

######################################################################
# CREATE ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_account():
    app.logger.info("Request to create an account")
    data = request.get_json()

    if not data:
        abort(status.HTTP_400_BAD_REQUEST)

    account = Account()
    account.deserialize(data)
    account.create()

    return jsonify(account.serialize()), status.HTTP_201_CREATED

######################################################################
# READ ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    app.logger.info(f"Request for account {account_id}")
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND)
    return jsonify(account.serialize()), status.HTTP_200_OK

######################################################################
# UPDATE ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    app.logger.info(f"Request to update account {account_id}")
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND)

    data = request.get_json()
    account.deserialize(data)
    account.update()

    return jsonify(account.serialize()), status.HTTP_200_OK

######################################################################
# DELETE ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    app.logger.info(f"Request to delete account {account_id}")
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND)

    account.delete()
    return "", status.HTTP_204_NO_CONTENT