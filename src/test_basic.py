from flask import Flask,request
import json
from .routes import configure_routes

ALPACA_URL = 'https://paper-api.alpaca.markets'


def load_test_data(json_path):
    with open(json_path) as f:
        return json.load(f)


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/test'
    expected_response = load_test_data('./src/test_data/test.json')
    response = client.get(url)
    assert json.loads(response.data) == expected_response
