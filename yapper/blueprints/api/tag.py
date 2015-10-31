from sqlalchemy.exc import IntegrityError

from yapper.lib.response import json_success, json_error
from yapper import db
from vomitter import LOGGER as L
from ..blog.models import Tag
from ..blog.forms import TagForm
from .blog import PostAPI
from .decorators import validate_form_data


class TagAPI(PostAPI):
    MODEL = Tag
    FORM = TagForm

    @validate_form_data(FORM)
    def post(self, form=None, *args, **kwargs):
        L.d(form.name.data)
        try:
            item = self.MODEL(name=form.name.data.lower())
            item.save()
        except IntegrityError, e:
            L.ex(e)
            db.session.rollback()
            return json_error(data='This item already exists.', code=406)
        return json_success(data=item.to_json())
