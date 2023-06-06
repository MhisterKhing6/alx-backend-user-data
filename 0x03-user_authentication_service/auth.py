#!/usr/bin/env python3
""" authentication """
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user in a database """
        val1 = self._db._session.query(User).where(
            User.email == email
            ).one()
        if val1 is None:
            hase = _hash_password(password)
            return self._db.add_user(email, hase)
        else:
            raise ValueError("User {} already exists".format(val1.email))


def _hash_password(password: str) -> bytes:
    """encrypt password using bcrypt """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
