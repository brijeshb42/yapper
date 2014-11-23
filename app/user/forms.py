from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .models import User


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(),\
            Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegisterForm(Form):
    name = StringField(u'Your Name', validators=[DataRequired()])
    email = StringField(u'Email', validators=[DataRequired(),\
            Length(1,64), Email()])
    password = PasswordField(u'Password', validators=[DataRequired(), EqualTo('cpassword', message=u'Both passwords should be same')])
    cpassword = PasswordField(u'Confirm Password', validators=[DataRequired()])
    submit = SubmitField(u'Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
