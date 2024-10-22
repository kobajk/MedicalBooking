#%%
# Create the routes for the application (links)
from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user
from Clinicas import App, database, bcrypt
from Clinicas.forms import Login_Form, Form_Criar_Conta
from Clinicas.models import Usuario, Foto

# link to the home page
@App.route('/', methods=['GET', 'POST'])
def homepage():
    form_login = Login_Form()

    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for('perfil', usuario=usuario.username))

    return render_template('homepage.html', form=form_login)


# link to the create account page
@App.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    form_criar_conta = Form_Criar_Conta()

    if form_criar_conta.validate_on_submit():

        senha_criptogarfada  = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')

        usuario = Usuario(username=form_criar_conta.username.data,
                       email=form_criar_conta.email.data,
                       senha=senha_criptogarfada
                       )
        
        database.session.add(usuario)
        database.session.commit()

        login_user(usuario, remember=True)
        return redirect(url_for('perfil', usuario=usuario.username))

    return render_template('criar_conta.html', form=form_criar_conta)




# link to the perfil page
@App.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)



