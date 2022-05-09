from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PurchaseForm(FlaskForm):
    submitPurchase = SubmitField(label='Purchase')

class AddForm(FlaskForm):
    fullname = StringField(label='Student Name:', validators=[DataRequired()])
    studentID = StringField(label='Student ID:', validators=[DataRequired()])
    price = StringField(label='Price:', validators=[DataRequired()])
    submitAdd = SubmitField(label='Add')


class SearchForm(FlaskForm):
    keyword = StringField(label='Student ID:', validators=[])
    submitSearch = SubmitField(label='Search')
