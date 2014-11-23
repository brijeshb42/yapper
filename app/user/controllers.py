from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user
from . import user_blueprint
from .forms import LoginForm, RegisterForm
from app import db
from .models import User

@user_blueprint.route('/')
@login_required
def index():
    return 'user index'

@user_blueprint.route('/<name>')
def user_index(name):
    return  'user ' + name

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next', '') or url_for('main.index'))
        flash(u'Invalid combination')
    return render_template('user/login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'You have been logged out.')
    return redirect(url_for('main.index'))


@user_blueprint.route('/signup', methods=['GET','POST'])
@login_required
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You have been registered')
        return redirect(url_for('main.index'))
    return render_template('user/signup.html', form=form)