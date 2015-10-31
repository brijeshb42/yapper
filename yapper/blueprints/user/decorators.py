from functools import wraps
from flask import abort
from flask_login import current_user

from .models import Permission


def permission_required(permission):
    """
    Checks for a specific permission the current_user has or not.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Like `permission required`, but specific to admin."""
    return permission_required(Permission.ADMIN)(f)
