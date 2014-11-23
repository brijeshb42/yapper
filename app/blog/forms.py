"""
(c) 2014 by Brijesh Bittu
"""
from flask.ext.wtf import Form
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(Form):
    title = StringField('Post Title', validators=[DataRequired(message=u'Empty title'), Length(max=256, message=u'Maximum 256 characters allowed')])
    body = TextAreaField('Content', validators=[DataRequired(message=u'Empty Post')])
    submit = SubmitField('Add Post')
