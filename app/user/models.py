from app import db
from werkzeug.security import generate_password_hash, \
    check_password_hash
from flask.ext.login import UserMixin
#from config import Config
from .. import login_manager

ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(),\
                            onupdate=db.func.current_timestamp())


class Role(BaseModel):
    __tablename__ = 'roles'
    name = db.Column(db.String(64), unique=True ,default=ROLE_USER)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        if self.id is None:
            return '<Role %s>' % self.name
        else:
            return '<Role %d - %s>' % self.id, self.name


class User(UserMixin,BaseModel):
    __tablename__ = 'users'
    #username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return  check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))