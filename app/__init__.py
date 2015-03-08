"""Flask application creation factory."""
import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
# from flask_wtf import CsrfProtect

from werkzeug.contrib.fixers import ProxyFix

from config import config

db = SQLAlchemy()
# csrf = CsrfProtect()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'


def create_app(config_name):
    """App creation factory based on the FLASK_CONFIG env var."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    @app.before_first_request
    def setup_logging():
        if not app.debug:
            # In production mode, add log handler to sys.stderr.
            app.logger.addHandler(logging.StreamHandler())
            app.logger.setLevel(logging.INFO)

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

    return app
