#!/usr/bin/env python3
""" authentication """
import bcrypt


def hash_password(password: str) -> bytes:
    """encrypt password using bcrypt """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
