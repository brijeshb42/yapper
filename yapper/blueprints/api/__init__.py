from flask import Blueprint

from yapper.lib.response import json_error

from .decorators import has_access_token
from .tag import TagAPI
from .category import CategoryAPI
from .blog import PostAPI


api = Blueprint('api', __name__)


# @api.errorhandler(403)
# def handle_403(e):
#     return json_error(403, 'You are not allowed here!')


# @api.errorhandler(406)
# def handle_406(e):
#     return json_error(406, 'Data not acceptable!')


# @api.errorhandler(400)
# def handle_400(e):
#     return json_error(400, ('You sent a request that this'
#                             ' server could not understand!'))


# @api.errorhandler(500)
# def handle_500(e):
#     L.ex(e)
#     return json_error(500, 'Internal server error!')


@api.errorhandler(404)
def handle_404(e):
    return json_error(404, "What you were looking for is not here!")


@api.before_request
@has_access_token('hello')
def before_request():
    pass

post_api = PostAPI.as_view('post_api')
tag_api = TagAPI.as_view('tag_api')
category_api = CategoryAPI.as_view('category_api')

api.add_url_rule('/posts/', defaults={'m_id': None},
                 view_func=post_api, methods=['GET', 'POST'])
api.add_url_rule('/posts/<int:m_id>', view_func=post_api, methods=['GET'])
api.add_url_rule('/tags/', defaults={'m_id': None},
                 view_func=tag_api, methods=['GET', 'POST'])
api.add_url_rule('/tags/<int:m_id>', view_func=tag_api, methods=['GET'])
api.add_url_rule('/categories/', defaults={'m_id': None},
                 view_func=category_api, methods=['GET', 'POST'])
api.add_url_rule('/categories/<int:m_id>',
                 view_func=category_api, methods=['GET'])
