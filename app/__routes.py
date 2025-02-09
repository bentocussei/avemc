from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

main = Blueprint('main', __name__)

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(8, 150)])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Aqui você implementaria a lógica de login
        pass
    return render_template('login.html', form=form)