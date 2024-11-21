"""test the various endpoints"""
import requests


def register_user(email: str, password: str) -> None:
    """Register a user"""
    resp = requests.post("http://127.0.0.1:5000/users",
                         {"email": email, "password": password})
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Checks a wrong log in attempt"""
    resp = requests.post("http://127.0.0.1:5000/sessions",
                         {"email": email, "password": password})
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """Logs the user in creating a session"""
    resp = requests.post("http://127.0.0.1:5000/sessions",
                         {"email": email, "password": password})
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    assert resp.cookies
    return resp.cookies.get("session_id")


def profile_unlogged() -> None:
    """Retrieves profile of email without a session"""
    resp = requests.get("http://127.0.0.1:5000/profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """retireves profile of a logged in user"""
    resp = requests.get("http://127.0.0.1:5000/profile",
                        cookies={"session_id": session_id})
    assert resp.status_code == 200


def log_out(session_id: str) -> None:
    """Logs out a user"""
    resp = requests.delete("http://127.0.0.1:5000/sessions",
                           cookies={"session_id": session_id})
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """Request a reset password and stores token"""
    resp = requests.post("http://127.0.0.1:5000/reset_password",
                         {"email": email})
    assert resp.status_code == 200
    data = resp.json()
    assert data
    return data.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Changes passwor using received token"""
    param = {"email": email,
             "reset_token": reset_token,
             "new_password": new_password}
    resp = requests.put("http://127.0.0.1:5000/reset_password", param)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
