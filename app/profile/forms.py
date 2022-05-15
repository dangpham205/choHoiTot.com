from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp

from ..models import User


class ChangePassForm(FlaskForm):
    old_password = PasswordField('Mật khẩu cũ', validators=[DataRequired()])
    new_password = PasswordField('Mật khẩu mới', validators=[
        DataRequired(), EqualTo('new_password2', message='Mật khẩu phải giống nhau.')])
    new_password2 = PasswordField('Nhập lại mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Thay Đổi Mật Khẩu')

class EditProfileForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(user_name=username_to_check.data).first()       #phải có .data
        if user:
            raise ValidationError('Username này đã tồn tại')

    username = StringField('Username:', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               "Usernames chỉ được phép chứa chữ cái, số, '.' or "
               '_')])
    fullname = StringField(label='Họ và tên:', validators=[Length(min=2, max=40), DataRequired()])
    phone = StringField(label='Số điện thoại:', validators=[Length(min=8, max=12), DataRequired()])
    bio = StringField(label='Tiểu sử:')
    submit = SubmitField(label='Cập Nhật')

class Go2AddBudgetForm(FlaskForm):
    submit = SubmitField(label='Nạp tài khoản')

class Go2ManageBudgetForm(FlaskForm):
    submit = SubmitField(label='Lịch sử biến động số dư')


class AddBudgetForm(FlaskForm):
    amount = StringField(label='Số đồng Tốt bạn muốn nạp:', validators=[DataRequired()])
    submit = SubmitField(label='Nạp')
