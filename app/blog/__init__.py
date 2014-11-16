"""
(c) 2014 by Brijesh Bittu
"""
from flask import Blueprint

BP_NM = 'blog'

blog_blueprint = Blueprint(BP_NM,__name__)

@blog_blueprint.route('/')
def index():
    return 'blog index'