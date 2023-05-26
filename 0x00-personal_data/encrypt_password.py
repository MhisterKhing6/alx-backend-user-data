#!/usr/bin/env python3
""" bycrypting a password """
import bcrypt

def hash_password(password : str) -> bytes:
    """encrypt password using bcrypt """
    return bcrypt.hashpw(password, bcrypt.gensalt())

def is_valid(hashed_password: bytes, password : str) -> bool:
    """Check for validity of a password"""
    return True if bcrypt.checkpw(password, hashed_password) else False
