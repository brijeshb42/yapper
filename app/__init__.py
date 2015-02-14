"""
(c) 2014 by Brijesh Bittu
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
# from flask_wtf import CsrfProtect
from config import config

db = SQLAlchemy()
# csrf = CsrfProtect()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'


class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    from .main import main_blueprint
    from .user import user_blueprint
    from .blog import blog_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(
        user_blueprint,
        url_prefix=config[config_name].USER_PREFIX
    )
    app.register_blueprint(
        blog_blueprint,
        url_prefix=config[config_name].BLOG_PREFIX
    )

    # if app.config['DEBUG']:
    #     #app.jinja_options['trim_blocks'] = True
    #     #app.jinja_options['lstrip_blocks'] = True
    #     app.jinja_env.trim_blocks = True
    #     app.jinja_env.lstrip_blocks = True

    return app
