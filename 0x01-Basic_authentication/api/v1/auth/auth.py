#!/usr/bin/env python3
from flask import request
"""Creates the auth class """


class Auth:
    """
    Hadles authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check the require paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Check if the header is authorized"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        return None
