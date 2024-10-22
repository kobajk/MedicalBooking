#%%
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# create an instance of the Flask class
App = Flask(__name__)
App.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
App.config["SECRET_KEY"] = '5791628bb0b13ce0c676dfde280ba245'

database = SQLAlchemy(App)
bcrypt = Bcrypt(App)
login_manager = LoginManager(App)
login_manager.login_view = 'homepage'

from Clinicas import routes