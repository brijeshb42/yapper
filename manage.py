"""Manger script."""
import os
from yapper import create_app, db
from yapper.blueprints.user.models import Role, User
from yapper.blueprints.blog.models import Tag, Category, Post
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
    os.unlink('data-test.db')


@manager.command
def init():
    """Enter initial data"""
    # db.create_all()
    Role.insert_roles()
    c = Category(name='default')
    db.session.add(c)
    db.session.commit()
    u = User.query.filter_by(email=app.config['FLASKY_ADMIN']).first()
    if not u:
        u = User(
            email=app.config['FLASKY_ADMIN'],
            password='testpass',
            name='Admin'
        )
        u.save()
    if app.debug:
        Post.generate_fake()


if __name__ == '__main__':
    manager.run()
