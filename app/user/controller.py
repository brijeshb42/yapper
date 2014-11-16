from . import user_blueprint

@user_blueprint.route('/')
def index():
    return 'user index'

@user_blueprint.route('/<name>')
def user_index(name):
    return  'user ' + name