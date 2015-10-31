from functools import wraps

from flask import request, abort


def has_access_token(tkn):

    """
    Checks only for a fixed Access-Token in header data.
    Will update after figuring out how to generate tokens.

    Used as a decorator in the before_request part of the
    API Blueprint.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Access-Token', '')
            if token != tkn:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
