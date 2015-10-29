from flask.views import MethodView
from flask.ext.login import login_required, current_user

from ..blog.forms import TagForm


class TagAPI(MethodView):

    def post(self):
        form = TagForm()
