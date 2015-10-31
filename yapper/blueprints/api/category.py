from ..blog.models import Category
from ..blog.forms import TagForm
from .tag import TagAPI


class CategoryAPI(TagAPI):
    MODEL = Category
