from flask import current_app, redirect, url_for, render_template, \
    flash, request
from app import db
from flask.ext.login import login_required, current_user
from . import blog_blueprint
from .forms import PostForm
from .models import Post
from ..user.models import Permission
from app.decorators import permission_required


@blog_blueprint.route('/page/<int:page>')
@blog_blueprint.route('/')
def index(page=1):
    pagination = Post.query.order_by(
            Post.created_at.desc()
    ).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template(
        'blog/index.html',
        posts=posts,
        pagination=pagination,
        title='Posts' if page < 2 else 'Posts - Page '+str(page)
    )


@blog_blueprint.route('/<int:pid>', methods=['GET'])
@blog_blueprint.route('/<int:pid>/<string:slug>', methods=['GET'])
def get_post(pid=None, slug=None):
    post = Post.query.get_or_404(pid)
    return render_template(
        'blog/index.html',
        posts=[post],
        pagination=None,
        title=post.title
        )


@blog_blueprint.route('/<int:pid>/edit', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE_POSTS)
def edit_post(pid=None):
    form = PostForm()
    post = Post.query.get_or_404(pid)
    if post.author.id != current_user.id or not current_user.is_admin():
        flash(u'You cannot edit this post.', 'error')
        return redirect(url_for('.get_post', pid=pid))
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.body.data
        db.session.add(post)
        db.session.commit()
        flash(u'Post Updated', 'success')
        return redirect(url_for('.get_post', pid=post.id))
    
    form.title.data = post.title
    form.description.data = post.description
    form.body.data = post.body
    return render_template(
        'blog/add.html',
        form=form,
        title='Edit Post - '+post.title
    )


@blog_blueprint.route('/<int:pid>', methods=['DELETE', 'POST'])
@login_required
def delete(pid):
    post = Post.query.get_or_404(pid)
    if current_user.is_admin() or post.author.id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash(u'Post deleted.', 'success')
        return redirect(url_for('.index'))
    flash(u'You cannot delete this post.', 'error')
    return redirect(url_for('.index'))


@blog_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE_POSTS)
def add():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            description=form.description.data,
            content=form.body.data,
            author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash(u'Post added')
        return redirect(url_for('.index'))
    return render_template('blog/add.html', form=form, title='Create New Post')
