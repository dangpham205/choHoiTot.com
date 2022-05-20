from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, EqualTo, InputRequired
from wtforms.validators import EqualTo, DataRequired



class ChangePassForm(FlaskForm):
    old_password = PasswordField('Mật khẩu cũ', validators=[DataRequired()])
    new_password = PasswordField('Mật khẩu mới', validators=[
        DataRequired(), EqualTo('new_password2', message='Mật khẩu phải giống nhau.')])
    new_password2 = PasswordField('Nhập lại mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Thay Đổi Mật Khẩu')

class EditProfileForm(FlaskForm):
    username = StringField('Username:')
    fullname = StringField(label='Họ và tên:')
    phone = StringField(label='Số điện thoại:')
    bio = StringField(label='Tiểu sử:')
    submit = SubmitField(label='Cập Nhật')

class Go2AddBudgetForm(FlaskForm):
    submit = SubmitField(label='Nạp tài khoản')

class Go2ManageBudgetForm(FlaskForm):
    submit = SubmitField(label='Lịch sử biến động số dư')


class AddBudgetForm(FlaskForm):
    amount = StringField(label='Số tiền bạn muốn nạp:', validators=[DataRequired()])
    submit = SubmitField(label='Nạp')

class ConfirmAddBudgetForm(FlaskForm):
    otp = StringField(label='Mã OTP của bạn:', validators=[DataRequired()])
    submit = SubmitField(label='Xác nhận')

class UploadFileForm(FlaskForm):                #dùng trong change avatar
    file= FileField("File", validators=[InputRequired()])
    submit=SubmitField("Cập Nhật")