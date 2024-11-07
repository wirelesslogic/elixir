from functools import wraps
from flask import request, abort


def htmx_view(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not request.headers.get("HX-Request"):
            abort(404)
        return view_func(*args, **kwargs)

    return wrapped_view
