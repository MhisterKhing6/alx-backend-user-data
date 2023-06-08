#!/usr/bin/env python3
""" authentication """
import bcrypt
from db import DB
from user import User
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user in a database """
        val1 = self._db.check_for_user(email)
        if not val1:
            hase = _hash_password(password)
            return self._db.add_user(email, hase)
        else:
            raise ValueError("User {} already exists".format(val1.email))

    def valid_login(self, email: str, password: str) -> bool:
        """ Check if user password is valid """
        user = self._db.find_user_by(email=email)
        if user:
            return True if bcrypt.checkpw(
                    password.encode(),
                    user.hashed_password) else False
        else:
            return False
    
    def get_reset_password_token(self, email: str) -> str:
        user = self._db.find_user_by(email=email)
        if user:
            token = _generate_uuid()
            user.reset_password_token = token
            return token
        else:
            raise ValueError()

    def get_user_from_session_id(self, session_id):
        """ Get user by session id """
        user = self._db.find_user_by(session_id=session_id)
        return user

    def create_session(self, email: str) -> str:
        """ create a session """
        user = self._db.find_user_by(email=email)
        if user:
            user.session_id = _generate_uuid()
            return user.session_id
        else:
            return None
    
    def update_password(self, reset_token: str, password: str) -> str:
        """ update password """
        user = self._db.find_user_by(reset_token=reset_token)
        if user:
            user.password = _hash_password(password)
            user.reset_token = None
        else:
            raise ValueError("")


    def destroy_session(self, user_id):
        user = self._db.find_user_by(id=user_id)
        user.session_id = None


def _hash_password(password: str) -> bytes:
    """encrypt password using bcrypt """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generate a unique uuid """
    return str(uuid.uuid4())
