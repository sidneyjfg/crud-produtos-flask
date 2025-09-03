from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField("Nome do produto", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Descrição")
    quantity = IntegerField("Quantidade", validators=[DataRequired(), NumberRange(min=0, max=1_000_000)])
    price = DecimalField("Preço", places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Salvar")
