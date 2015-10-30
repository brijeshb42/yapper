from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_required, login_user, logout_user,\
    current_user

from yapper import db
from yapper.decorators import admin_required
from . import user_blueprint as ubp
from .forms import LoginForm, RegisterForm
from .models import User


@ubp.route('/')
@login_required
def index():
    return 'user index'


@ubp.route('/<name>')
def user_index(name):
    return 'user ' + name


@ubp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated() \
            and current_user.is_confirmed():
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data) \
                and user.is_confirmed():
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next', '') or
                            url_for('main.index'))
        flash(u'Invalid combination', 'warning')
    return render_template('user/login.html', form=form)


@ubp.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@ubp.route('/signup', methods=['GET', 'POST'])
@admin_required
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            role_id=form.role.data,
            status=form.confirm.data
        )
        db.session.add(user)
        db.session.commit()
        flash(u'You have been registered', 'success')
        return redirect(url_for('main.index'))
    return render_template('user/signup.html', form=form)
