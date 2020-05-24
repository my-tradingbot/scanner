#!/usr/bin/python3

from flask import Flask, Response, jsonify, Request
import argparse
import pytest

# Scanner Imports
from scanner import scan


class DefaultResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(DefaultResponse, cls).force_type(rv, environ)


app = Flask(__name__)
app.response_class = DefaultResponse


class ValidationError(ValueError):
    pass


@app.errorhandler(ValidationError)
def bad_request(e):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': e.args[0]})
    response.status_code = 400
    return response


@app.errorhandler(404)
def not_found(e):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': 'invalid resource URI'})
    response.status_code = 404
    return response


@app.errorhandler(405)
def method_not_supported(e):
    response = jsonify({'status': 405, 'error': 'method not supported',
                        'message': 'the method is not supported'})
    response.status_code = 405
    return response


@app.errorhandler(500)
def internal_server_error(e):
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': e.args[0]})
    response.status_code = 500
    return response


@app.route('/test')
def test_json():
    return {'code': 1, 'message': 'Server is a live', 'status': 200}


# Blueprints registration
app.register_blueprint(scan)


def create_app(host, port, debug):
    flask_app = Flask(__name__)
    flask_app.run(host=host, port=port, debug=debug, ssl_context='adhoc')
    flask_app.app_context().push()
    return flask_app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Trading Listener Parameters")
    parser.add_argument('-host', dest='host', help='Listener IP')
    parser.add_argument('-port', dest='port', help='Listener IP')
    parser.add_argument('-debug', dest='debug', help='True to Enable Debug')
    args = parser.parse_args()
    app = create_app(host=args.host, port=args.port, debug=args.debug)

