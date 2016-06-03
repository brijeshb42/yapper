from functools import wraps
import time

from vomitter import LOGGER as L

from .response import json_error


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


def profile(f):
    """
    Decorate a function with this to know its running time.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        strt = time.time()
        L.i('Calling function %s @ %f' % (f.func_name, strt))
        res = f(*args, **kwargs)
        end = time.time()
        L.i('Finished function %s @ %f' % (f.func_name, end))
        L.i('Time taken : %f ms' % (end - strt))
        return res
    return decorated_function
