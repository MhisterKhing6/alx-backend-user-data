#!/usr/bin/env python3
"""Basic authentication for a class """
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
from flask import request, jsonify
import uuid
import os
from api.v1.views import app_views


class SessionAuth(Auth):
    """ Instantiate a basic authentication """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session """
        if user_id is None or type(user_id) is not str:
            return None
        else:
            sess_id = str(uuid.uuid4())
            self.user_id_by_session_id[sess_id] = user_id
            return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get id by session """
        if session_id and type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
        return None

    def session_cookie(self, request=None) -> str:
        """ Set a session cookie """
        if request:
            key = os.environ.get('SESSION_NAME')
            return request.cookies.get(key)

    def current_user(self, request=None) -> str:
        """ Get the current user """
        if request is None:
            return None
        else:
            key = self.session_cookie(request)
            id = self.current_user(key)
            return id

    @app_views.route(
        "/auth_session/login", methods=["POST"], strict_slashes=False
        )
    def sess_login():
        """ This doucemthe the app """
        from api.v1.auth.auth import Auth
        """ View for session login """
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or email == "":
            return jsonify({"error": "email missing"}), 400
        if not password or password == "":
            return jsonify({"password": "email missing"}), 400
        user = User.search({"email": email})
        if user is None or len(user) == 0:
            return jsonify({"error": "no user found for this email"}), 404
        else:
            user = user[0]
            if user.is_valid_password(password):
                ses = Auth.create_session(user.id)
                ses_key = os.environ.get('SESSION_NAME')
                out = jsonify(user.to_json())
                out.set_cookie(ses_key, ses)
                return out
            else:
                return jsonify({"error": "wrong password"})
