from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import Tag

def get_tags():
    return Tag.query.all()

def get_tag_name(tag):
    return tag.name

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    tags = QuerySelectMultipleField('Tag(s)',
                                    query_factory=get_tags,
                                    get_label=get_tag_name,
                                    widget = ListWidget(prefix_label = False),
                                    option_widget = CheckboxInput())
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')