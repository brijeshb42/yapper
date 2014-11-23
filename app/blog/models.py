"""
(c) 2014 by Brijesh Bittu
"""
from app import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(),\
                            onupdate=db.func.current_timestamp())


class Post(BaseModel):
    __tablename__ = 'posts'
    title = db.Column(db.String(256))
    #slug = db.Column(db.String(300))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def content(self):
        return self.body

    @content.setter
    def content(self, body):
        self.body = body
        from markdown import markdown
        import bleach
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'li', 'i', 'ol', 'pre', 'strong', 'ul', 'h1',
                        'h2', 'h3', 'p']
        self.body_html = bleach.linkify(bleach.clean(
            markdown(body, output_format='html5'),
            tags=allowed_tags, strip=True
        ))

    @property
    def html(self):
        return self.body_html

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        from markdown import markdown
        import bleach
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'li', 'i', 'ol', 'pre', 'strong', 'ul', 'h1',
                        'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        for i in range(count):
            author_id = 1
            p = Post(content=forgery_py.lorem_ipsum.sentences(randint(1,3)),
                     title=forgery_py.lorem_ipsum.sentence(),
                     author_id=author_id)
            db.session.add(p)
        db.session.commit()

    def __repr__(self):
        return '<Post %s>' % self.body

db.event.listen(Post.body, 'set', Post.on_change_body)