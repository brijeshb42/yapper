from wtforms import Form
import wtforms as f
import wtforms.validators as v
from .models import User


class LoginForm(Form):
    email = f.StringField('Email', validators=[v.DataRequired(),\
            v.Length(1,64), v.Email()])
    password = f.PasswordField('Password', validators=[v.DataRequired()])
    remember_me = f.BooleanField('Remember Me')
    submit = f.SubmitField('Log In')


class RegisterForm(Form):
    email = f.StringField('Email', validators=[v.DataRequired(),\
            v.Length(1,64), v.Email()])
    password = f.PasswordField('Password', validators=[v.DataRequired()])
    cpassword = f.PasswordField('Confirm Password', validators=[v.DataRequired(),\
                    v.EqualTo(password)])
    submit = f.SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise f.ValidationError('Email already registered')
