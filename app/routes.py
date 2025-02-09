from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, ChatMessage
from app import db
from functools import wraps
import random
import string
from itertools import groupby
from datetime import datetime

main = Blueprint('main', __name__)

# Decorador para verificar se o usuário está logado
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             flash('Por favor, faça login para acessar esta página.', 'warning')
#             return redirect(url_for('main.login', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=8, message='A senha deve ter pelo menos 8 caracteres')
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('senha', message='As senhas devem ser iguais')
    ])
    submit = SubmitField('Cadastrar')

class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Recuperar Senha')

class ChangePasswordForm(FlaskForm):
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[
        DataRequired(),
        Length(min=8, message='A senha deve ter pelo menos 8 caracteres')
    ])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(),
        EqualTo('nova_senha', message='As senhas devem ser iguais')
    ])
    submit = SubmitField('Alterar Senha')

class ProfileForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Salvar Alterações')

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.chat'))
        
    login_form = LoginForm()
    registro_form = RegistroForm()
    
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.check_senha(login_form.senha.data):
            login_user(user, remember=login_form.lembrar.data)
            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.chat'))
        flash('Email ou senha inválidos.', 'danger')
        
    return render_template('login.html', 
                         login_form=login_form, 
                         registro_form=registro_form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('main.home'))

@main.route('/cadastro', methods=['POST'])
def cadastro():
    registro_form = RegistroForm()
    
    if registro_form.validate_on_submit():
        if User.query.filter_by(email=registro_form.email.data).first():
            flash('Este email já está registrado.', 'danger')
            return redirect(url_for('main.login'))
            
        user = User(
            nome=registro_form.nome.data,
            email=registro_form.email.data
        )
        user.set_senha(registro_form.senha.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Por favor, faça login.', 'success')
        return redirect(url_for('main.login'))
        
    for field, errors in registro_form.errors.items():
        for error in errors:
            flash(f'Erro no campo {field}: {error}', 'danger')
            
    return redirect(url_for('main.login'))

@main.route('/chat')
@login_required  # Protegendo a rota do chat
def chat():
    return render_template('chat.html')

@main.route('/chat', methods=['POST'])
@login_required  # Protegendo também a rota da API do chat
def process_message():
    data = request.get_json()
    message = data.get('message', '')
    
    # Salvando a mensagem do usuário
    user_message = ChatMessage(
        conteudo=message,
        is_bot=False,
        user_id=current_user.id
    )
    db.session.add(user_message)
    
    # Aqui você implementará a lógica do chatbot
    response = f"Você perguntou sobre: {message}"
    
    # Salvando a resposta do bot
    bot_message = ChatMessage(
        conteudo=response,
        is_bot=True,
        user_id=current_user.id
    )
    db.session.add(bot_message)
    db.session.commit()
    
    return jsonify({'response': response})

def generate_password(length=8):
    """Gera uma senha aleatória segura"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for i in range(length))
    return password

@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.chat'))
        
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            # Gera nova senha
            new_password = generate_password()
            
            # Atualiza a senha no banco de dados
            user.set_senha(new_password)
            db.session.commit()
            
            # Mostra a nova senha para o usuário
            flash(f'Sua nova senha é: {new_password}', 'success')
            flash('Por favor, faça login com sua nova senha e altere-a em seguida.', 'info')
            return redirect(url_for('main.login'))
        else:
            flash('Não existe uma conta com este e-mail.', 'danger')
    
    return render_template('forgot_password.html', form=form)

@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_senha(form.senha_atual.data):
            current_user.set_senha(form.nova_senha.data)
            db.session.commit()
            flash('Sua senha foi alterada com sucesso!', 'success')
            return redirect(url_for('main.chat'))
        else:
            flash('Senha atual incorreta.', 'danger')
    
    return render_template('change_password.html', form=form)

@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = ProfileForm(obj=current_user)  # Preenche o form com dados do usuário atual
    password_form = ChangePasswordForm()  # Adiciona o formulário de alteração de senha
    
    # Buscar mensagens do usuário
    messages = ChatMessage.query.filter_by(user_id=current_user.id)\
        .order_by(ChatMessage.timestamp.desc())\
        .all()
    
    # Agrupar mensagens por data
    chat_history = {}
    for message in messages:
        date = message.timestamp.strftime('%d/%m/%Y')
        if date not in chat_history:
            chat_history[date] = []
        chat_history[date].append(message)
    
    return render_template('settings.html', 
                         form=form,
                         password_form=password_form,
                         chat_history=chat_history)

@main.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    form = ProfileForm()
    
    if form.validate_on_submit():
        # Verificar se o email já existe (exceto para o usuário atual)
        existing_user = User.query.filter(
            User.email == form.email.data,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            flash('Este email já está sendo usado por outro usuário.', 'danger')
        else:
            current_user.nome = form.nome.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Erro no campo {field}: {error}', 'danger')
    
    return redirect(url_for('main.settings'))

@main.route('/about')
def about():
    return render_template('about.html')