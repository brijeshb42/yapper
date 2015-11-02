from flask import current_app
from werkzeug.security import generate_password_hash, \
    check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

from yapper import db
from yapper import login_manager
from yapper.lib.models import BaseModel
# from vomitter import LOGGER as L


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


class Role(BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.name and self.name in ["admin", "administrator"]:
            self.permissions = Permission.ADMIN
        else:
            self.permissions = Permission.WRITE_POSTS

    @staticmethod
    def insert_roles():
        # L.i('Inserting default roles.')
        roles = {
            'User': Permission.user(),
            'Admin': Permission.admin()
        }
        for r in roles:
            nm = r.lower()
            role = Role.query.filter_by(name=nm).first()
            if role is None:
                role = Role(name=nm)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
        # L.i('Default roles %s added.', ', '.join(roles.keys()))


class User(UserMixin, BaseModel):
    __tablename__ = 'users'
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    status = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name
        }
        return json_data

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(
                    name="admin"
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

    def get_id(self):
        return self.id

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
    id = -1

    def can(self, permissions):
        return False

    def is_admin(self):
        return False

    def is_administrator(self):
        return self.is_admin()

    def is_confirmed(self):
        return False

    def get_id(self):
        return None


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
