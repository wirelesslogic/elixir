from flask import session, redirect, url_for
from functools import wraps


def guarded(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("guard.login"))
        return f(*args, **kwargs)

    return decorated
