"""Main flask module"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({"id": 1, "text": "hi young ejecta"})


if __name__ == '__main__':
    app.run()
