"""
(c) 2014 by Brijesh Bittu
"""
from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

from . import controller