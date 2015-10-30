import os

from flask import (
    url_for,
    send_from_directory,
    redirect,
    Blueprint
)

from ..user.models import Permission
from config import basedir

BP_NM = 'main'

main = Blueprint(BP_NM, __name__, template_folder='views')

TEMPLATE_DIR = os.path.join(basedir, 'templates')
STATIC_DIR = os.path.join(TEMPLATE_DIR, 'static')


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main.route('/')
def index():
    return redirect(url_for('blog.index'))
    # return render_template('main/index.html')


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(
        STATIC_DIR,
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
