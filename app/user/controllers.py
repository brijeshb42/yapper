from flask import render_template, redirect, request, url_for
from flask.ext.login import login_required
from . import user_blueprint
from .forms import LoginForm, RegisterForm

@user_blueprint.route('/')
@login_required
def index():
    return 'user index'

@user_blueprint.route('/<name>')
def user_index(name):
    return  'user ' + name

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate():
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('user/login.html', form=form)

@user_blueprint.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate():
        return redirect(url_for('main.index'))
    return render_template('user/signup.html', form=form)