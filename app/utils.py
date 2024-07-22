from functools import wraps
from flask import session, request, redirect, url_for, flash


def login_required(role):
    def wrapper(original):
        @wraps(original)
        def inner(*args, **kwargs):
            if session.get("username") and session.get("role") == role:
                return original(*args, **kwargs)
            else:
                flash(f"You need to login as {role}", "warning")
                return redirect(url_for("auth.login"))

        return inner

    return wrapper
