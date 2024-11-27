#%%
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Criar uma instância da classe Flask
App = Flask(__name__)
# Configurar a URI do banco de dados SQLite
App.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
# Configurar a chave secreta para a aplicação
App.config["SECRET_KEY"] = '5791628bb0b13ce0c676dfde280ba245'
# Configurar a pasta de upload para fotos
App.config["UPLOAD FOLDER"] = 'static/fotos_post'

# Criar uma instância do SQLAlchemy para gerenciar o banco de dados
database = SQLAlchemy(App)
# Criar uma instância do Bcrypt para hashing de senhas
bcrypt = Bcrypt(App)
# Criar uma instância do LoginManager para gerenciar sessões de login
login_manager = LoginManager(App)
# Definir a rota de login padrão
login_manager.login_view = 'homepage'

# Importar as rotas da aplicação
from Clinicas import routes