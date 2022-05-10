from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp
from ..models import User
import re

class LoginForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    # recaptcha = RecaptchaField()
    remember_me = BooleanField('Remember me')
    submit = SubmitField(label='Log In')

class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(user_name=username_to_check.data).first()       #phải có .data
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self,email_to_check):
        email = User.query.filter_by(user_email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists')

    username = StringField('Username:', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    fullname = StringField(label='Full Name:', validators=[Length(min=2, max=40), DataRequired()])      
    email = StringField(label='Email:',  validators=[Email(),  DataRequired()])
    phone = StringField(label='Phone Number:', validators=[Length(min=8, max=12), DataRequired()])      
    password1 = PasswordField(label='Password:', validators=[Length(min=5),  DataRequired()])
    password2 = PasswordField(label='Confirm Password:',  validators=[EqualTo('password1'), DataRequired()])
    #check password có giống nhau không ở đây
    submit = SubmitField(label='Register')

    def validate_phone(self, field):
        if field.data.isnumeric() == False:
            raise ValidationError('Phone number can only contains number.')

class SendForgotPassForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    submit = SubmitField('Send Email')

class ForgotPassForm(FlaskForm):
    new_password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('new_password2', message='Passwords must match.')])
    new_password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')