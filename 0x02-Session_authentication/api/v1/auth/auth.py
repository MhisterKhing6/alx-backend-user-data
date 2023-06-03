#!/usr/bin/env python3
"""
Creates the auth class
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Hadles authentication
    return headers
    """

    user_id_by_session_id = {}

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check the require paths
        return headers
        """
        if path:
            if excluded_paths:
                if path in excluded_paths or (path + "/") in excluded_paths:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        Check if the header is authorized
        and returns headers
        """
        if request:
            auth = request.headers.get('Authorization')
            return auth
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        the user
        """
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get id by session """
        if session_id and type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
        return None

    def session_cookie(self, request=None):
        """ Set a session cookie """
        if request:
            key = os.environ.get('SESSION_NAME')
            return request.cookies.get(key)

    def create_session(self, user_id: str = None) -> str:
        """ Create a session """
        if user_id is None or type(user_id) is not str:
            return None
        else:
            sess_id = str(uuid.uuid4())
            self.user_id_by_session_id[sess_id] = user_id
            return sess_id
