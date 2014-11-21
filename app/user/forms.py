from wtforms import Form
import wtforms as f
import wtforms.validators as v


class LoginForm(Form):
    email = f.StringField('Email', validators=[v.DataRequired(),\
            v.Length(1,64), v.Email()])
    password = f.PasswordField('Password', validators=[v.DataRequired()])
    remember_me = f.BooleanField('Remember Me')
    submit = f.SubmitField('Log In')

