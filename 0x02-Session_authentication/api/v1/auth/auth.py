#!/usr/bin/env python3
"""
Authentication class for the API
"""

from flask import request
from typing import TypeVar, List
from os import getenv


class Auth():
    """
    Base class definition for the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if the path requires authentication"""
        if not path or not excluded_paths:
            return True
        if path[(len(path) - 1)] == '/':
            if path in excluded_paths:
                return False
            elif path[:-1] in excluded_paths:
                return False
        else:
            if path in excluded_paths:
                return False
            elif (path + '/') in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Check if the authorization object is present."""
        if not request:
            return None
        if not request.headers.get('Authorization', None):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user who sent the request."""
        return None

    def session_cookie(self, request=None):
        """Retrieves the cookie sent by the client for authentication."""
        if request is None:
            return None
        cookie_key = getenv("SESSION_NAME")
        if not cookie_key:
            return None
        return request.cookies.get(cookie_key)
