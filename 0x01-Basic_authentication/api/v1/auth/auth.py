#!/usr/bin/env python3
"""
Creates the auth class
"""
from flask import request
from typing import List, TypeVar


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
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        the user
        """
        return None
