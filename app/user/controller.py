from flask import Blueprint

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/')
def index():
    return 'user index'

@user.route('/<name>')
def user_index(name):
    return  'user ' + name