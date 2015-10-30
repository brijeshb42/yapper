from flask.views import MethodView

from yapper.lib.response import json_success
from ..blog.models import Post


class PostAPI(MethodView):

    MODEL = Post

    def get(self, m_id=None):
        items = self.MODEL.query.order_by(
            self.MODEL.created_at.desc()).limit(10)
        resp = []
        for item in items:
            resp.append(item.to_json())
        return json_success(data=resp)
