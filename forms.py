from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp


class SignUpForm(FlaskForm):
    """form for signing up"""

    username = StringField('Username', validators=[Length(min=2,max=30),DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6, max=30), DataRequired(), Regexp('(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$', message="Please use a password that satisfies all of these conditions: The password length must be greater than or equal to 8. The password must contain one or more uppercase characters. The password must contain one or more lowercase characters. The password must contain one or more numeric values. The password must contain one or more special characters.")])

class UserEditForm(FlaskForm):
    """form for editing user"""

    username = StringField('New Username', validators=[Length(min=2,max=30),DataRequired()])
    password = PasswordField('Enter your password to confirm', validators=[Length(min=6, max=30), DataRequired()])
    

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[Length(min=2, max=30),DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6, max=30), DataRequired()])