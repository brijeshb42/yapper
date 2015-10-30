from flask import Blueprint

from yapper.lib.response import json_error
from vomitter import LOGGER as L
from .decorators import has_access_token
from .tag import TagAPI
from .category import CategoryAPI
from .blog import PostAPI


api = Blueprint('api', __name__)


@api.app_errorhandler(403)
def handle_403(e):
    return json_error(403, 'You are not allowed here!')


@api.app_errorhandler(500)
def handle_500(e):
    L.ex(e)
    return json_error(500, 'Internal server error!')


@api.app_errorhandler(404)
def handle_404(e):
    return json_error(404, "What you were looking for is not here!")


@api.before_request
@has_access_token('hello')
def before_request():
    pass

post_api = PostAPI.as_view('post_api')
api.add_url_rule('/blog/', defaults={'m_id': None},
                 view_func=post_api, methods=['GET'])

tag_api = TagAPI.as_view('tag_api')
api.add_url_rule('/tags/', defaults={'m_id': None},
                 view_func=tag_api, methods=['GET'])

category_api = CategoryAPI.as_view('category_api')
api.add_url_rule('/categories/', defaults={'m_id': None},
                 view_func=category_api, methods=['GET'])
