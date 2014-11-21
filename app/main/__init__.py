"""
(c) 2014 by Brijesh Bittu
"""
from flask import Blueprint

BP_NM = 'main'

main_blueprint = Blueprint(BP_NM, __name__, template_folder='views')

from . import controller
from . import errors