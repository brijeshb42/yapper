from flask import render_template
from . import main_blueprint


@main_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main_blueprint.app_errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403
