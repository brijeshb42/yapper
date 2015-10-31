from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(Form):
    title = StringField(
        u'Post Title',
        validators=[
            DataRequired(message=u'Empty title'),
            Length(max=256, message=u'Maximum 256 characters allowed')
        ]
    )
    description = TextAreaField(
        u'Description',
        validators=[
            DataRequired(message=u'Provide a description/summary.'),
            Length(max=300, message=u'Maximum 300 characters allowed')
        ]
    )
    body = TextAreaField(
        u'Content',
        validators=[DataRequired(message=u'Empty Post')]
    )
    submit = SubmitField(u'Add Post')


class TagForm(Form):

    """Form for tag/category creation."""

    name = StringField(
        u'Tag/Category Name',
        validators=[
            DataRequired(message=u'Empty name'),
            Length(max=100, message=u'Maximum 100 characters')
        ]
    )
