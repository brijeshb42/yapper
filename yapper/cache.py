from functools import wraps
import inspect

from werkzeug.contrib.cache import RedisCache

from vomitter import LOGGER as L

cache = RedisCache()


def get_cache_key(func):
    key = 'func-'
    key += func.func_name
    func_dict = func.func_dict
    argspec = inspect.getargspec(func)
    L.i(argspec)
    if func_dict == {}:
        if not argspec.defaults and len(argspec.args) < 1:
            key += ''
        elif len(argspec.args) > 0:
            if argspec.defaults:
                key += ''
    return key


def layer():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            L.i(get_cache_key(f))
            L.i(args)
            L.i(kwargs)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
