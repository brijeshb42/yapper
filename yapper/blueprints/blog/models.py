from yapper import db
from yapper.lib.models import BaseModel
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


class Category(BaseModel):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)

    def __repr__(self):
        return '<Category %s>' % self.name


class Post(BaseModel):
    __tablename__ = 'posts'
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(256))
    slug = db.Column(db.String(300))
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
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        for i in range(count):
            author_id = 1
            p = Post(
                content=forgery_py.lorem_ipsum.paragraphs(),
                title=forgery_py.lorem_ipsum.sentence(),
                author_id=author_id
            )
            db.session.add(p)
        db.session.commit()


db.event.listen(Post.body, 'set', Post.on_change_body)
