from datetime import datetime

from flask import current_app
from app import db
from werkzeug.security import generate_password_hash, \
    check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
# from config import Config
from app import login_manager


class Permission:
    WRITE_POSTS = 0x01
    READ_ONLY = 0x02
    ADMIN = 0xff
    ANONYMOUS = 0x00

    @staticmethod
    def user():
        return (Permission.WRITE_POSTS, True)

    @staticmethod
    def admin():
        return (Permission.ADMIN, False)


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow)


class Role(BaseModel):
    __tablename__ = 'roles'
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': Permission.user(),
            'Admin': Permission.admin()
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin, BaseModel):
    __tablename__ = 'users'
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    status = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(
                    permissions=Permission.ADMIN
                ).first()
                self.status = True
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError(u'Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s>' % self.email

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.is_admin()

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def is_confirmed(self):
        return self.status is not None and self.status is True


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False

    def is_administrator(self):
        return is_admin()

    def is_confirmed(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
