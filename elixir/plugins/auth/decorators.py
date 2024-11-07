from functools import wraps

from flask import abort
from flask_login import current_user


def permission_required(scope=""):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            nonlocal scope
            scope = scope.replace(" ", "")

            if ":" in scope:
                resource, action_str = scope.split(":", 1)
                actions = action_str.split(",") if "," in action_str else [action_str]

                # Retrieve current user's permissions
                user_permissions = current_user.permissions

                # Check if the user has the required permission
                if resource not in user_permissions or not set(actions).issubset(
                    user_permissions[resource]
                ):
                    abort(403)

            return fn(*args, **kwargs)

        return decorated

    return wrapper
