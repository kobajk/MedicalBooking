#%%
from Clinicas import App
from flask_talisman import Talisman
import os

App.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "sua_chave_secreta")
App.config["SESSION_COOKIE_SECURE"] = True
App.config["REMEMBER_COOKIE_SECURE"] = True
App.config["SESSION_COOKIE_HTTPONLY"] = True
App.config["REMEMBER_COOKIE_HTTPONLY"] = True

talisman = Talisman(App, content_security_policy = None)

if __name__ == '__main__':
    App.run(debug=True)

