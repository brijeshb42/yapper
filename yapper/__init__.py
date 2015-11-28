"""Flask application creation factory."""
import logging
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_wtf import CsrfProtect

from werkzeug.contrib.fixers import ProxyFix

from config import config
from vomitter import get_mail_handler, get_file_handler
from .extension import mount_blueprints, add_error_handlers

db = SQLAlchemy()
# csrf = CsrfProtect()
login_manager = LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'


def setdefaultencoding():
    if sys.version[0] == '2':
        reload(sys)
        sys.setdefaultencoding('utf-8')


def create_app(config_name, set_utf=True):
    """App creation factory based on the FLASK_CONFIG env var."""
    if set_utf:
        setdefaultencoding()
    app = Flask(
        __name__,
        template_folder="../templates/",
        static_url_path="/static",
        static_folder="../templates/static/"
    )
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    mount_blueprints(app, config_name)
    add_error_handlers(app)

    if not app.debug:
        app.logger.addHandler(
            get_mail_handler(name=config['default'].APP_NAME,
                             level=logging.ERROR))
    else:
        app.logger.addHandler(get_file_handler())
    return app
