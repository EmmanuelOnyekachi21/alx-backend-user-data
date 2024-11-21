#!/usr/bin/env python3
'''DB'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """ Creates a User object stored in the DB."""
        if not email or not hashed_password:
            return None
        new_user = User(email, hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Finds User with passed characteristics."""
        arg_list = ["id", "email", "hashed_password", "session_id",
                    "reset_token"]
        if kwargs:
            for key, value in kwargs.items():
                if key in arg_list:
                    for user in self._session.query(User).all():
                        if getattr(user, key) == value:
                            return user
                    raise NoResultFound
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a given user details."""
        arg_list = ["id", "email", "hashed_password", "session_id",
                    "reset_token"]
        if type(user_id) is not int:
            raise ValueError
        user = self.find_user_by(id=user_id)
        for attr, value in kwargs.items():
            if attr not in arg_list:
                raise ValueError
            setattr(user, attr, value)
        self._session.add(user)
        self._session.commit()
