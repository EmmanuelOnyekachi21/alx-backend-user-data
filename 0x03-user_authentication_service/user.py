#!/usr/bin/env python3
"""Defining the user class linked wth sqlite DB."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User base model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __init__(self, email: str, hashed_password: str,
                 session_id: str = None, reset_token: str = None) -> None:
        """ initializes the class. """
        self.email = email
        self.hashed_password = hashed_password
        if session_id:
            self.session_id = session_id
        if reset_token:
            self.reset_token = reset_token
