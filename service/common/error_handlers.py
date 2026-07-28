from flask import jsonify
from service import app


@app.errorhandler(404)
def not_found(error):
    message = {"error": "Not found"}
    return jsonify(message), 404


@app.errorhandler(500)
def internal_error(error):
    message = {"error": "Internal server error"}
    return jsonify(message), 500
