#!/usr/bin/env python3
""" Module of Session views (login/logout)
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Logs the user in and set session cookie."""
    from models.user import User
    from api.v1.app import auth
    user_obj = None
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        search_results = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not search_results:
        return jsonify({"error": "no user found for this email"}), 404
    for obj in search_results:
        if obj.is_valid_password(password):
            user_obj = obj
            break
    if user_obj is None:
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user_obj.id)
    resp = jsonify(user_obj.to_json())
    resp.set_cookie(getenv('SESSION_NAME'), session_id)
    return resp


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Logouts a user. """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
