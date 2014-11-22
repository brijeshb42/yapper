"""
(c) 2014 by Brijesh Bittu
"""
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
#from flask_wtf import CsrfProtect
from config import config

db = SQLAlchemy()
#csrf = CsrfProtect()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main_blueprint
    from .user import user_blueprint
    from .blog import blog_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix=config[config_name].USER_PREFIX)
    app.register_blueprint(blog_blueprint, url_prefix=config[config_name].BLOG_PREFIX)

    return app
