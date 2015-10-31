from functools import wraps

from flask import request, abort

from yapper.lib.response import json_error


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


def validate_form_data(FORM_Class):

    """
    Validates the passed form/json data to a request and passes the
    form to the called function.
    If form data is not valid, return a 406 response.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            form = FORM_Class(csrf_enabled=False)
            if not form.validate():
                return json_error(code=406, data=form.errors)
            kwargs['form'] = form
            return f(*args, **kwargs)
        return decorated_function
    return decorator
