#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar
"""Creates the auth class """


class Auth:
    """
    Hadles authentication
    return headers
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check the require paths
        return headers
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ 
        Check if the header is authorized
        and returns headers
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ 
        current user 
        the user
        """
        return None
