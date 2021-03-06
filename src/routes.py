#!/usr/bin/python3

from flask import Flask, Response, jsonify

# Route Imports
from .blueprints.scanner import scan


def configure_routes(app):

    class ValidationError(ValueError):
        pass

    class DefaultResponse(Response):
        @classmethod
        def force_type(cls, rv, environ=None):
            if isinstance(rv, dict):
                rv = jsonify(rv)
            return super(DefaultResponse, cls).force_type(rv, environ)

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
        return jsonify({"code": 1, "message": "Server is a live", "status": 200})

    # Blueprints registration
    app.register_blueprint(scan)

