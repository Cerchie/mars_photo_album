from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length


class SignUpForm(FlaskForm):
    """form for signing up"""

    username = StringField('Username', validators=[Length(max=30),DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])

class UserEditForm(FlaskForm):
    """form for editing user"""

    username = StringField('New Username', validators=[Length(max=30),DataRequired()])
    password = PasswordField('Enter your password to confirm', validators=[Length(min=6), DataRequired()])
    

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[Length(max=30),DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])