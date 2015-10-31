from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .models import User, Role


class LoginForm(Form):
    email = StringField(u'Email', validators=[DataRequired(),
                        Length(1, 64), Email()])
    password = PasswordField(u'Password', validators=[DataRequired()])
    remember_me = BooleanField(u'Remember Me')
    submit = SubmitField(u'Log In')


class RegisterForm(Form):
    name = StringField(u'Your Name', validators=[DataRequired()])
    email = StringField(u'Email', validators=[DataRequired(),
                        Length(1, 64), Email()])

    password = PasswordField(u'Password', validators=[DataRequired(),
                             EqualTo('cpassword',
                             message=u'Both passwords should be same')])
    cpassword = PasswordField(u'Confirm Password', validators=[DataRequired()])
    role = SelectField(u'Role', coerce=int)
    confirm = BooleanField(u'Register With Confirmation?')
    submit = SubmitField(u'Sign Up')

    def __init__(self, **kwargs):
        super(RegisterForm, self).__init__(**kwargs)
        self.role.choices = [(r.id, r.name)
                             for r in Role.query.with_entities(
                             Role.id, Role.name).all()]

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
