#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add user to the database """
        user1 = User()
        user1.email = email
        user1.hashed_password = hashed_password
        self._session.add(user1)
        self._session.commit()
        return user1

    def find_user_by(self, **kwargs) -> User:
        """ Find user base on datainputed """
        return self._session.query(User).filter_by(**kwargs).one()

    def update_user(self, Id: str, **kwargs: dict) -> User:
        """ Update user """
        try:
            user = self.find_user_by(id=Id)
            for key, value in kwargs.items():
                if key not in User.__dict__:
                    raise ValueError
                else:
                    setattr(user, key, value)
            return None
        except Exception:
            return None


        