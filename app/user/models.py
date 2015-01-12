from flask import current_app
from app import db
from werkzeug.security import generate_password_hash, \
    check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
#from config import Config
from app import login_manager


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(),\
                            onupdate=db.func.current_timestamp())


class Role(BaseModel):
    __tablename__ = 'roles'
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name

class User(UserMixin,BaseModel):
    __tablename__ = 'users'
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError(u'Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return  check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s>' % self.email

    def is_admin(self):
        return self.email == current_app.config['FLASKY_ADMIN']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
