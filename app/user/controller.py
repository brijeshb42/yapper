from flask import render_template, redirect
from flask.ext.login import login_required
from . import user_blueprint
from .forms import LoginForm

@login_required
@user_blueprint.route('/')
def index():
    return 'user index'

@user_blueprint.route('/<name>')
def user_index(name):
    return  'user ' + name

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return 'OK'
    return render_template('login.html', form=form)
