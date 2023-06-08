#!/usr/bin/env python3
""" simple flask view for the api """

from flask import Flask, jsonify, request, abort, redirect, url_for
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

@app.route('/sessions', methods=['POST', 'DELETE'])
def login():
    """ Login User """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email is None or password is None:
            abort(401)
        else:
            if AUTH.valid_login(email, password):
                ses = AUTH.create_session(email)
                response = jsonify({"email": f"{email}", "message": "logged in"})
                response.set_cookie('session_id', ses)
                return response
            else:
                abort(401)
    else:
        ses_Id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('Main.js'))
        else:
            abort(403)

@app.route('/profile', methods=['GET'])
def profile():
    sees = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(sees)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    else:
        return str(None)

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """ Get response """
    email = request.form.get(email)
    results = AUTH.get_reset_password_token(email)
    if results:
        return jsonify({"email": f"{email}", "reset_token": f"{results}"}), 200
    else:
        abort(403)
@app.route('/reset_password', methods=['PUT'])
def update_password():
    """ update password """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": f"{email}", "message": "Password updated"})
    except ValueError:
        abort(403)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
