from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp

from ..models import User


class ChangePassForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('new_password2', message='Passwords must match.')])
    new_password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class EditProfileForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(user_name=username_to_check.data).first()       #phải có .data
        if user:
            raise ValidationError('Username already exists')

    username = StringField('Username:', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    fullname = StringField(label='Full Name:', validators=[Length(min=2, max=40), DataRequired()])
    phone = StringField(label='Phone Number:', validators=[Length(min=8, max=12), DataRequired()])
    bio = StringField(label='About Me:')
    submit = SubmitField(label='Update')

class Go2AddBudgetForm(FlaskForm):
    submit = SubmitField(label='Nạp tài khoản')

class Go2ManageBudgetForm(FlaskForm):
    submit = SubmitField(label='Lịch sử biến động số dư')


class AddBudgetForm(FlaskForm):
    amount = StringField(label='Số đồng Tốt bạn muốn nạp:', validators=[DataRequired()])
    submit = SubmitField(label='Nạp')
