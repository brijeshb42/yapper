from sqlalchemy.exc import IntegrityError

from yapper.lib.response import json_success, json_error
from yapper.lib.decorators import validate_form_data
from yapper import db
from ..blog.models import Tag
from ..blog.forms import TagForm
from .blog import PostAPI


class TagAPI(PostAPI):
    MODEL = Tag
    FORM = TagForm

    @validate_form_data(FORM)
    def post(self, form=None, *args, **kwargs):
        try:
            item = self.MODEL(name=form.name.data.lower())
            item.save()
        except IntegrityError:
            db.session.rollback()
            return json_error(data='This item already exists.', code=406)
        return json_success(data=item.to_json())
