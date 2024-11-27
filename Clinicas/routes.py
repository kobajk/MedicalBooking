#%%
# Create the routes for the application (links)
from flask import render_template, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from Clinicas import App, database, bcrypt
from Clinicas.forms import Login_Form, Form_Criar_Conta, Form_Foto
from Clinicas.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename

# link to the home page
@App.route('/', methods=['GET', 'POST'])
def homepage():
    form_login = Login_Form()

    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar.data)
            return redirect(url_for('perfil', id_usuario=usuario.id))
        else:
            flash('Email ou senha incorretos', 'danger')

    return render_template('homepage.html', form=form_login)


# link to the create account page
@App.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    form_criar_conta = Form_Criar_Conta()

    if form_criar_conta.validate_on_submit():

        senha_criptogarfada  = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')

        # Ajusta `crm` e `especialidade` para `None` se o tipo for "Paciente"
        if form_criar_conta.tipo.data == "Médico":
            crm = form_criar_conta.crm.data
            especialidade = form_criar_conta.especialidade.data
        else:
            crm = None
            especialidade = None

        usuario = Usuario(username=form_criar_conta.username.data,
                        email=form_criar_conta.email.data,
                        senha=senha_criptogarfada,
                        tipo=form_criar_conta.tipo.data,
                        especialidade=especialidade,
                        crm=crm,
                        telefone=form_criar_conta.telefone.data
                       )
        
        database.session.add(usuario)
        database.session.commit()

        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('criar_conta.html', form=form_criar_conta)


# link to the perfil page
@App.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):

    if int(current_user.id) == int(id_usuario):
        form_foto = Form_Foto()

        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            
            nome_seguro = secure_filename(arquivo.filename)
            caminho_proj = os.path.abspath(os.path.dirname(__file__))
            caminho = os.path.join(caminho_proj, App.config['UPLOAD FOLDER'], nome_seguro)
            arquivo.save(caminho)

            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template('perfil.html', usuario=current_user, form=form_foto)
    
    elif current_user.tipo != "Médico":
        flash("Você não tem permissão para acessar o perfil de outros usuários.", "danger")
        return redirect(url_for('perfil', id_usuario=current_user.id))

    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)


@App.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))
