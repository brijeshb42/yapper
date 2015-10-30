from ..blog.models import Category
from .blog import PostAPI


class CategoryAPI(PostAPI):
    MODEL = Category
