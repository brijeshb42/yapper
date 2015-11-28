import slugify
from flask import url_for

from vomitter import LOGGER as L
from yapper import db
from yapper.lib.models import BaseModel
from yapper.lib.cache import cache
from yapper.lib.decorators import profile
from yapper.utilities.md import create_post_from_md

TYPE_POST = 1
TYPE_PAGE = 2


tags_posts = db.Table(
    'tags_posts',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)

categories_posts = db.Table(
    'categories_posts',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)


class Tag(BaseModel):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)

    def __repr__(self):
        return '<Tag %s>' % self.name

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'created_at': str(self.created_at)}
        return json_data


class Category(BaseModel):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)

    def __repr__(self):
        return '<Category %s>' % self.name

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'created_at': str(self.created_at)}
        return json_data


class Post(BaseModel):
    __tablename__ = 'posts'
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(256))
    slug = db.Column(db.String(500), unique=True)
    description = db.Column(db.Text, default='')
    body = db.Column(db.Text, default='')
    status = db.Column(db.Boolean, default=True)
    body_html = db.Column(db.Text, default='')
    tags = db.relationship(
        'Tag', secondary=tags_posts,
        backref=db.backref('posts', lazy='dynamic')
    )
    categories = db.relationship(
        'Category', secondary=categories_posts,
        backref=db.backref('posts', lazy='dynamic')
    )

    def to_json(self):
        json_data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'created_at': str(self.created_at),
            'modified_at': str(self.modified_at),
            'author': self.author.to_json(),
            'permalink': url_for('blog.get_post_by_slug',
                                 slug=self.slug, _external=True)
        }
        return json_data

    @classmethod
    @profile
    def get_by_slug(cls, slug):
        L.d('Getting from Cache.')
        obj = cache.get(cls.key(slug))
        if obj:
            L.d('Cache hit for - %s' % cls.key(slug))
            return obj
        L.d('Cache miss for - %s' % cls.key(slug))
        obj = cls.query.filter_by(slug=slug).first()
        if obj:
            L.d('Saving in cache - %s' % cls.key(slug))
            cache.set(cls.key(slug), obj)
        else:
            L.d('The object was None')
        return obj

    @property
    def content(self):
        return self.body

    @content.setter
    def content(self, body):
        self.body = body
        self.body_html = create_post_from_md(body)

    @property
    def html(self):
        return self.body_html

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        target.body_html = create_post_from_md(value)

    @staticmethod
    def generate_fake(count=10):
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            author_id = 1
            title = forgery_py.lorem_ipsum.sentence()
            p = Post(
                content=forgery_py.lorem_ipsum.paragraphs(),
                title=title,
                slug=slugify.slugify(title),
                description=forgery_py.lorem_ipsum.sentence(),
                author_id=author_id
            )
            db.session.add(p)
        db.session.commit()


db.event.listen(Post.body, 'set', Post.on_change_body)
