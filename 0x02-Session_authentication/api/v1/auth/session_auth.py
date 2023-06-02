#!/usr/bin/env python3
"""Basic authentication for a class """
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
from flask import request
import uuid


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
