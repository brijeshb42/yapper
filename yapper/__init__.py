"""Flask application creation factory."""
import logging
import sys

from flask import Flask  # , request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_wtf import CsrfProtect

from werkzeug.contrib.fixers import ProxyFix

from config import config
from vomitter import get_mail_handler, get_file_handler
# from vomitter import LOGGER as L
from .lib.response import json_error

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

    from yapper.blueprints.api import api
    from yapper.blueprints.main import main
    from yapper.blueprints.user import user
    from yapper.blueprints.blog import blog

    # @app.before_request
    # def before_request():
    #     L.i(request.blueprint)
    #     L.i(request.endpoint)
    #     L.i(request.headers)

    app.register_blueprint(main, url_prefix='')
    app.register_blueprint(api, url_prefix='/api/v1')
    app.register_blueprint(
        user,
        url_prefix=config[config_name].USER_PREFIX
    )
    app.register_blueprint(
        blog,
        url_prefix=config[config_name].BLOG_PREFIX
    )

    @app.errorhandler(403)
    def handle_403(e):
        return json_error(403, 'You are not allowed here!')

    @app.errorhandler(406)
    def handle_406(e):
        return json_error(406, 'Data not acceptable!')

    @app.errorhandler(400)
    def handle_400(e):
        return json_error(400, ('You sent a request that this'
                                ' server could not understand!'))

    @app.errorhandler(404)
    def handle_404(e):
        return json_error(404, 'What you were looking for isn\'t here!')

    if not app.debug:
        app.logger.addHandler(
            get_mail_handler(name=config['default'].APP_NAME,
                             level=logging.ERROR))
    else:
        app.logger.addHandler(get_file_handler())
    return app
