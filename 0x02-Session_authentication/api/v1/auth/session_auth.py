#!/usr/bin/env python3
"""
Session Authentication class for the API
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """ Session Management class for the API. """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates the session id for a given user."""
        if not user_id or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns the user id associated with the session id. """
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns Current user based on cookie."""
        from models.user import User
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes a user session. """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
