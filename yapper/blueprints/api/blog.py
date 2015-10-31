from flask.views import MethodView

from yapper.lib.response import json_success
from ..blog.models import Post


class PostAPI(MethodView):

    MODEL = Post

    def get(self, m_id=None):
        if m_id:
            item = self.MODEL.query.get_or_404(m_id)
            return json_success(data=item.to_json())
        items = self.MODEL.query.order_by(
            self.MODEL.created_at.desc()).limit(10)
        resp = []
        for item in items:
            resp.append(item.to_json())
        return json_success(data=resp)
