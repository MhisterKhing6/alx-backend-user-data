#!/usr/bin/env python3
"""Basic authentication for a class """
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
from flask import request


class SessionAuth(Auth):
    """ Instantiate a basic authentication """
