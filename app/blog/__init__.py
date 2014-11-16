"""
(c) 2014 by Brijesh Bittu
"""
from flask import Blueprint

blog_blueprint = Blueprint('blog',__name__)

@blog_blueprint.route('/')
def index():
    return 'blog index'