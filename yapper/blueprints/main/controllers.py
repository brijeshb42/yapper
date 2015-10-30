import os

from flask import render_template, send_from_directory

from . import main_blueprint
from config import basedir

TEMPLATE_DIR = os.path.join(basedir, 'templates')
STATIC_DIR = os.path.join(TEMPLATE_DIR, 'static')


@main_blueprint.route('/')
def index():
    return render_template('main/index.html')


@main_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(
        STATIC_DIR,
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
