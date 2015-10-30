from functools import wraps

from flask import request, abort


def has_access_token(tkn):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Access-Token', '')
            if token != tkn:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# def add_error_hanlder(app=None, code=400):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if app:
#                 @app.error_handler(code):
#                 def handler_xxx()
