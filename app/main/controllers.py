from . import main_blueprint

@main_blueprint.route('/')
def index():
    return 'main index'