from config import config
from .lib.response import json_error


def add_error_handlers(app=None):
    if not app:
        return

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


def mount_blueprints(app, config_name):
    if not app:
        return
    from yapper.blueprints.api import api
    from yapper.blueprints.main import main
    from yapper.blueprints.user import user
    from yapper.blueprints.blog import blog

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
