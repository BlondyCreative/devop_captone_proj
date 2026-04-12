from flask import Flask, jsonify
app = Flask(__name__)

# Example in-memory data (replace with DB later)
accounts = [
    {"id": 1, "name": "John Doe", "address": "123 Main St"},
    {"id": 2, "name": "Jane Smith", "address": "456 Oak Ave"}
]

@app.route('/accounts', methods=['GET'])
def list_accounts():
    return jsonify(accounts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
