from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, InputRequired


class AddForm(FlaskForm):
    name = StringField(label='Tên sản phẩm:', validators=[DataRequired()])
    file= FileField("Ảnh sản phẩm", validators=[InputRequired()])
    price = StringField(label='Giá:', validators=[DataRequired()])
    description = StringField(label='Mô tả sản phẩm:', validators=[DataRequired()])
    myChoices = ['Tất cả', 'Đồ điện tử', 'Đồ gia dụng', 'Giải trí', 'Xe cộ']
    category = SelectField(u'Danh mục sản phẩm:', choices = myChoices, validators = [DataRequired()])
    submit = SubmitField(label='Thêm sản phẩm')

class UpdateForm(FlaskForm):
    name = StringField(label='Tên sản phẩm:')
    file= FileField("Ảnh sản phẩm")
    price = StringField(label='Giá:')
    description = StringField(label='Mô tả sản phẩm:')
    myChoices = ['Tất cả', 'Đồ điện tử', 'Đồ gia dụng', 'Giải trí', 'Xe cộ']
    category = SelectField(u'Danh mục sản phẩm:', choices = myChoices)
    submit = SubmitField(label='Cập nhật')

class SearchForm(FlaskForm):
    keyword = StringField(label='Tìm kiếm sản phẩm', validators=[])
    submitSearch = SubmitField(label='🔍')



