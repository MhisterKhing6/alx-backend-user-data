#!/usr/bin/env python3
"""Basic authentication for a class """
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
from flask import request


class BasicAuth(Auth):
    """ Instantiate a basic authentication """

    def extract_base64_authorization_header(
        self, authorization_header: str
                                            ) -> str:
        """Extrat base64 authorization header """
        if authorization_header and type(authorization_header) is str:
            if not authorization_header.startswith("Basic "):
                return None
            else:
                return authorization_header.split(" ")[-1]
        else:
            return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
                                            ) -> str:
        """ Return a decoded base64 message """
        if (base64_authorization_header) and  (type(base64_authorization_header) is str):
            try:
                encoded_str = base64_authorization_header.encode()
                base = base64.b64decode(encoded_str)
                return base.decode("utf-8")
            except Exception as e:
                return None
        else:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Returns email and password """
        if decoded_base64_authorization_header:
            if type(decoded_base64_authorization_header) is str:
                if ":" in decoded_base64_authorization_header:
                    value = decoded_base64_authorization_header.split(":")
                    return (value[0], value[1])
                else:
                    return (None, None)
            else:
                return (None, None)
        else:
            return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar(User):
        """ Returns the user object from credentials """
        if user_email and user_pwd and type(user_pwd) is str and type(user_email) is str:
            users = User.search({"email": user_email})
            if users is None or len(users) == 0:
                return None
            else:
                for user in users:
                    if user.is_valid_password(user_pwd):
                        return user
                return None
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user"""
        auth = self.authorization_header(request)
        base = self.extract_base64_authorization_header(auth)
        cedientials = self.decode_base64_authorization_header(base)
        cedientials = self.extract_user_credentials(cedientials)
        user = self.user_object_from_credentials(cedientials[0], cedientials[1])
        return user
