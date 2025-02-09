# AVEMC - Assistente Virtual de Educação Moral e Cívica

## 📝 Descrição
O AVEMC é uma plataforma educacional que utiliza inteligência artificial para auxiliar no ensino e aprendizagem de Educação Moral e Cívica. O sistema oferece uma experiência interativa através de um chatbot inteligente, permitindo que os usuários aprendam sobre cidadania, ética e valores morais de forma engajadora.

## 🚀 Funcionalidades

### Principais
- 💬 Chat interativo com IA
- 👤 Sistema de autenticação completo
- 🌙 Modo escuro/claro
- 📊 Histórico de conversas
- ⚙️ Gerenciamento de perfil
- 🔒 Recuperação e alteração de senha

### Características Técnicas
- Interface responsiva
- Armazenamento seguro de senhas
- Sistema de sessão de usuário
- Validações de formulários
- Feedback visual para ações
- Design moderno e intuitivo

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- WTForms

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Bootstrap Icons

### Banco de Dados
- SQLite (desenvolvimento)
- PostgreSQL (produção)

## 📦 Instalação

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/avemc.git
cd avemc
```

2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicialize o banco de dados
```bash
flask db upgrade
```

6. Execute o servidor de desenvolvimento
```bash
flask run
```

## 🔧 Configuração

### Variáveis de Ambiente
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///app.db
```

### Banco de Dados
O sistema utiliza SQLAlchemy como ORM e suporta múltiplos bancos de dados:
- SQLite (desenvolvimento)
- PostgreSQL (produção recomendada)
- MySQL (suportado)

## 👥 Equipe
- Benedito Zacarias - Desenvolvedor Full Stack
- Ana Silva - UX/UI Designer
- Carlos Santos - Backend Developer
- Diana Oliveira - AI Engineer
- Eduardo Costa - Frontend Developer
- Fernanda Lima - Quality Assurance

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuição
1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Contato
- Email: contato@avemc.com
- Website: https://avemc.com
- LinkedIn: [AVEMC](https://linkedin.com/company/avemc)

## 🙏 Agradecimentos
- [Bootstrap](https://getbootstrap.com/)
- [Flask](https://flask.palletsprojects.com/)
- [Python](https://python.org/)
- Todos os contribuidores e apoiadores do projeto

---
Desenvolvido com ❤️ pela equipe AVEMC 