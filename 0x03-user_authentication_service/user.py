#!/usr/bin/env python3
""" Authentication users """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer


Base = declarative_base()


class User(Base):
    """ user model for the project """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(Integer, nullable=True)
    reset_token = Column(String, nullable=True)
