from flask import jsonify, request, abort, url_for, current_app as app
from service.models import Account
from service.common import status

@app.route("/", methods=["GET"])
def index():
    return jsonify(
        name="Account REST API Service",
        version="1.0",
        paths={
            "list": url_for("list_accounts", _external=True)
        }
    ), status.HTTP_200_OK


@app.route("/accounts", methods=["GET"])
def list_accounts():
    app.logger.info("Request for account list")
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    return jsonify(results), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    app.logger.info(f"Request for account {account_id}")
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND)
    return jsonify(account.serialize()), status.HTTP_200_OK
