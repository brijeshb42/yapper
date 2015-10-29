"""Manger script."""
import os
from yapper import create_app, db
from yapper.user.models import Role, User
from yapper.blog.models import Tag, Category, Post
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(
        app=app, db=db,
        User=User, Role=Role, Post=Post,
        Tag=Tag, Category=Category
    )


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    os.environ["FLASK_CONFIG"] = "test"
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    del os.environ["FLASK_CONFIG"]


@manager.command
def init():
    """Enter initial data"""
    # db.create_all()
    Role.insert_roles()
    c = Category(name='default')
    db.session.add(c)
    db.session.commit()
    u = User.query.filter_by(email=app.config['FLASKY_ADMIN']).first()
    if u is None:
        u = User(
            email=app.config['FLASKY_ADMIN'],
            password='testpass',
            name='Admin'
        )
        db.session.add(u)
        db.session.commit()
    print('DB initialized')


if __name__ == '__main__':
    manager.run()
