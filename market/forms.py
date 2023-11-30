from market.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, Length, DataRequired, Email, ValidationError


# registration form class inheriting from FlaskForm
class RegisterForm(FlaskForm):
    # automatically invoked by FlaskForm
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                'Username already exists! Please try a different username')

    # automatically invoked by FlaskForm
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError(
                'Email already exists! Please try a different email')

    username = StringField(label="User Name:", validators=[
                           DataRequired(), Length(min=6, max=30)])

    email = StringField(label="Email:", validators=[DataRequired(
        message='Email is required to create a user account'), Email()])

    password = PasswordField(label="Password:", validators=[
                             DataRequired(message='Password is required to create a user account'), Length(min=6)])

    password_confirm = PasswordField(label="Confirm Password:", validators=[
                                     DataRequired(message='Confirm Password is required to create a user account'), EqualTo('password', message='Both Passwords do not match')])

    submit = SubmitField(label="Create Account")


# login form class inheriting from FlaskForm
class LoginForm(FlaskForm):
    username = StringField(label="User Name:", validators=[DataRequired()])

    password = PasswordField(label="Password:", validators=[DataRequired(
        message='Password is required to login to user account')])

    submit = SubmitField(label="Log In")


# Purchase Item form class inheriting from FlaskForm
class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase Item!")


# Sell Item form class inheriting from FlaskForm
class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell Item!")
