from flask import Blueprint

BP_NM = 'blog'

blog_blueprint = Blueprint(BP_NM, __name__)

from . import controllers
