from flask import Blueprint

from ..user.models import Permission

BP_NM = 'main'

main_blueprint = Blueprint(BP_NM, __name__, template_folder='views')

from . import controllers
from . import errors


@main_blueprint.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
