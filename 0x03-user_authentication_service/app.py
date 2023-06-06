#!/usr/bin/env python3
""" simple flask view for the api """

from flask import Flask, jsonify, request
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def js():
    """ Return the firsts view """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def reg():
    """ Register user """
    email = request.form.get('email')
    password = request.form.get('password')
    value = AUTH._db.check_for_user(email)
    if not value:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    else:
        return jsonify({"message": "email already registered"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
