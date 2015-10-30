from ..blog.models import Tag
from .blog import PostAPI


class TagAPI(PostAPI):
    MODEL = Tag
