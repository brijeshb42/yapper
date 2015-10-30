"""Blog post controller."""
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from flask import (
    current_app,
    redirect,
    url_for,
    render_template,
    flash,
    request,
    abort,
    jsonify,
    Blueprint
)
from flask.ext.login import login_required, current_user

from ..user.decorators import permission_required
from .forms import PostForm
from .models import Post, Tag
from ..user.models import Permission


BP_NM = 'blog'

blog = Blueprint(BP_NM, __name__)


@blog.route('/page/<int:page>')
@blog.route('/')
def index(page=1):
    """Show list of latest blog posts."""
    pagination = Post.query.order_by(
        Post.created_at.desc()
    ).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    status = 200
    if len(posts) < 1:
        status = 404
    return render_template(
        'blog/index.html',
        posts=posts,
        pagination=pagination,
        title='Posts' if page < 2 else 'Posts - Page '+str(page)
    ), status


@blog.route('/<int:pid>', methods=['GET'])
@blog.route('/<int:pid>/<string:slug>', methods=['GET'])
def get_post(pid=None, slug=None):
    """Display a blog post with given id."""
    post = Post.query.get_or_404(pid)
    return render_template(
        'blog/index.html',
        posts=[post],
        pagination=None,
        title=post.title
    )


@blog.route('/new', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE_POSTS)
def add():
    """Create a new blog post."""
    form = PostForm()
    status = 200
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            description=form.description.data,
            content=form.body.data,
            author=current_user._get_current_object()
        )
        post.save()
        flash(u'Post added')
        return redirect(url_for('.index'))
    else:
        status = 406
    return render_template(
        'blog/add.html',
        form=form,
        title='Create New Post'), status


@blog.route('/<int:pid>/edit', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE_POSTS)
def edit_post(pid=None):
    """Edit a blog post with given id."""
    post = Post.query.get_or_404(pid)
    if not (current_user.is_admin() or current_user.id == post.author.id):
        abort(403)
    form = PostForm()
    status = 200
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.body.data
        post.save()
        flash(u'Post Updated', 'success')
        return redirect(url_for('.get_post', pid=post.id))
    else:
        status = 406
    form.title.data = post.title
    form.description.data = post.description
    form.body.data = post.body
    return render_template(
        'blog/add.html',
        form=form,
        title='Edit Post - '+post.title
    ), status


@blog.route('/<int:pid>', methods=['DELETE', 'POST'])
@login_required
def delete(pid):
    """Delete a blog post with given id."""
    post = Post.query.get_or_404(pid)
    if current_user.is_admin() or post.author.id == current_user.id:
        post.delete()
        flash('Post deleted.', 'success')
        return redirect(url_for('.index'))
    else:
        abort(403)


@blog.route('/tag/', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def add_tag():
    """Tag addition and deletion."""
    if request.method == 'GET':
        tag_name = request.args.get('name', '')
        if tag_name == '':
            return jsonify({
                'type': 'error',
                'message': 'Invalid paramater.'
            }), 400
        tags = Tag.query.filter_by(name=tag_name.lower()).all()
        return jsonify({
            'type': 'success',
            'message': tags
        })
    if request.method == 'POST':
        taglist = request.form.get('name', '')
        if taglist == '':
            return jsonify({
                'type': 'error',
                'message': 'Invalid paramater.'
            }), 400
        taglist = taglist.lower().split(',')
        tags = []
        for tag in taglist:
            try:
                Tag.query.filter_by(name=tag).one()
            except NoResultFound:
                tags.append(Tag(name=tag))
            except MultipleResultsFound:
                pass
        if len(tags) > 0:
            Tag.save_all(tags)
        return jsonify({
            'type': 'success',
            'message': tags
        })
