"""
(c) 2014 by Brijesh Bittu
"""
from flask import current_app, redirect, url_for, render_template, flash, request
from app import db
from flask.ext.login import login_required, current_user
from . import blog_blueprint
from .forms import PostForm
from .models import Post


@blog_blueprint.route('/<int:pid>', methods=['GET'])
def get_post(pid):
    post = Post.query.get_or_404(pid)
    return render_template('blog/index.html', posts=[post], pagination=None)

@blog_blueprint.route('/page/<int:page>')
@blog_blueprint.route('/')
def index(page=1):
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@blog_blueprint.route('/<int:pid>', methods=['DELETE', 'POST'])
@login_required
def delete(pid):
    post = Post.query.get_or_404(pid)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.index'))


@blog_blueprint.route('/add', methods=['GET','POST'])
@login_required
def add():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        flash('Post added')
        return redirect(url_for('.index'))
    return render_template('blog/add.html', form=form)