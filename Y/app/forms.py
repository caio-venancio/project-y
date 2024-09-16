from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea

# Create User Base Form Class
class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    profile_pic = FileField("Profile Picture")
    submit = SubmitField("Submit")

# Create Register Form Class
class RegisterForm(UserForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email Address", validators=[Email(), DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])

# Create Login Form Class
class LoginForm(UserForm):
    password = PasswordField("Password", validators=[DataRequired()])

# Create Posts Form Class
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author")
    submit = SubmitField("Submit")

# Create Search Form Class
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")