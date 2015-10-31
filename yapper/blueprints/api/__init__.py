from flask import Blueprint

from .decorators import has_access_token
from .tag import TagAPI
from .category import CategoryAPI
from .blog import PostAPI


api = Blueprint('api', __name__)


@api.before_request
@has_access_token('hello')
def before_request():
    """
    Check every request to this blueprint for a valid Access Token.
    """
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
