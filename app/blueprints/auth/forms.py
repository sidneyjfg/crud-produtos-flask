from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=4, max=128)])
    submit = SubmitField("Entrar")
