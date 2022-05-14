from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class PurchaseForm(FlaskForm):
    submitPurchase = SubmitField(label='Purchase')

class AddForm(FlaskForm):
    name = StringField(label='Tên sản phẩm:', validators=[DataRequired()])
    price = StringField(label='Giá:', validators=[DataRequired()])
    description = StringField(label='Mô tả sản phẩm:', validators=[DataRequired()])
    myChoices = ['Tất cả', 'Đồ điện tử', 'Đồ gia dụng', 'Giải trí', 'Xe cộ']
    category = SelectField(u'Danh mục sản phẩm:', choices = myChoices, validators = [DataRequired()])
    submit = SubmitField(label='Add')


class SearchForm(FlaskForm):
    keyword = StringField(label='Student ID:', validators=[])
    submitSearch = SubmitField(label='Search')

class Go2ProductDetailForm(FlaskForm):
    submit = SubmitField(label='Detail')

