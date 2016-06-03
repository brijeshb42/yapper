import os

from werkzeug.contrib.cache import RedisCache, NullCache

from config import config


typ = os.environ.get('FLASK_CONFIG')
if typ and typ in ['dev', 'test', 'prod']:
    Config = config[typ]
else:
    Config = config['default']

if Config.CACHE:
    cache = RedisCache(default_timeout=3000)
    cache.key_prefix = Config.APP_NAME
else:
    cache = NullCache()
