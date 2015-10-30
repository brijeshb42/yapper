from flask import Blueprint

BP_NM = 'user'
user_blueprint = Blueprint(BP_NM, __name__)

from . import controllers
