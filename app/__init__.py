"""
(c) 2014 by Brijesh Bittu
"""
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import config


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from main import main as main_blueprint
    from user import user_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/u')

    return app
