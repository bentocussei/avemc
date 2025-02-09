from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Inicialização das extensões
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avemc.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicialização das extensões com o app
    Bootstrap5(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    # Registro dos blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Criação das tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app

# Função para carregar o usuário pelo ID (necessária para o Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
