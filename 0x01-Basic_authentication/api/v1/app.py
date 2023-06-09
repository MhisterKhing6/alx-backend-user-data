#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if os.environ.get("AUTH_TYPE"):
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


def beforet():
    """
    Handles operations before request
    """
    if auth:
        if auth.require_auth(
            request.path, [
                '/api/v1/status/',
                '/api/v1/unauthorized/', '/api/v1/forbidden/'
                ]
                            ):
            if not auth.authorization_header(request):
                abort(401)
            if not auth.current_user(request):
                abort(403)


app.before_request(beforet)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def error_401(error):
    """
    Handles 401 error unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def error_403(error):
    """
    Handles 403 error unauthorized
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
