from flask import Blueprint

BP_NM = 'user'
user_blueprint = Blueprint(BP_NM, __name__, template_folder='templates')

from . import controller
