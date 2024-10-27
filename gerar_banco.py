#%%
# Iniaciatilize database
from Clinicas import database, App
from Clinicas.models import Usuario, Foto

with App.app_context():
    database.create_all()

