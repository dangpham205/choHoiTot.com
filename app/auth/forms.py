from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp
from ..models import User
import re

class LoginForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired()])
    password = PasswordField(label='Mật khẩu:', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField(label='Đăng Nhập')

class RegisterForm(FlaskForm):

    def validate_email(self,email_to_check):
        email = User.query.filter_by(user_email=email_to_check.data).first()
        if email:
            raise ValidationError('Email này đã tồn tại')
            
    def validate_phone(self, field):
        if field.data.isnumeric() == False:
            raise ValidationError('Số điện thoại chỉ được phép chứa số.')

    username = StringField('Username:', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               "Usernames chỉ được phép chứa chữ cái, số, '.' or "
               '_')])
    fullname = StringField(label='Họ và tên:', validators=[Length(min=2, max=40), DataRequired()])      
    email = StringField(label='Email:',  validators=[Email(),  DataRequired()])
    phone = StringField(label='Số điện thoại:', validators=[Length(min=8, max=12), DataRequired()])      
    password1 = PasswordField(label='Mật khẩu:', validators=[Length(min=5),  DataRequired()])
    password2 = PasswordField(label='Nhập lại mật khẩu:',  validators=[EqualTo('password1', message='Mật khẩu phải giống nhau.'), DataRequired()])
    #check password có giống nhau không ở đây
    submit = SubmitField(label='Đăng Kí')


class SendForgotPassForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    submit = SubmitField('Gửi Email')

class ForgotPassForm(FlaskForm):
    new_password = PasswordField('Mật khẩu mới', validators=[
        DataRequired(), EqualTo('new_password2', message='Mật khẩu phải giống nhau.')])
    new_password2 = PasswordField('Nhập lại mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đặt Lại Mật Khẩu')