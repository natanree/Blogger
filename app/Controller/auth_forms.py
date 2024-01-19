from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import  DataRequired, Length, EqualTo, Email, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from app.Model.models import User, Tag

def get_tags():
    return Tag.query.all()

def get_tag_name(tag):
    return tag.name

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email',validators=[DataRequired(),Email()])
    first_name = StringField('First Name',validators=[DataRequired(),Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(max=64)])
    tags = QuerySelectMultipleField('Tag(s)',
                                    query_factory=get_tags,
                                    get_label=get_tag_name,
                                    widget = ListWidget(prefix_label = False),
                                    option_widget = CheckboxInput())
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already being used! Please choose another username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is already being used! Please choose another email.')
        
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    new_password = PasswordField('New Password')
    new_password2 = PasswordField('Repeat New Password', validators=[EqualTo('new_password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    tags = QuerySelectMultipleField('Tag(s)',
                                    query_factory=get_tags,
                                    get_label=get_tag_name,
                                    widget = ListWidget(prefix_label = False),
                                    option_widget = CheckboxInput())
    submit = SubmitField('Save Changes')