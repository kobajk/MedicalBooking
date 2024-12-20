#%%
# Importar módulos e funções necessários
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from Clinicas import App, database, bcrypt
from Clinicas.forms import Login_Form, Form_Criar_Conta, Form_Foto, Form_Gestao_Consulta, Form_Prontuario, Form_Editar_Conta, Form_Reagendar_Consulta, Form_Realizar_Consulta
from Clinicas.models import Usuario, Foto, Consulta, Prontuario
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

# Função para obter a hora atual em UTC
def now():
    return datetime.utcnow()

# Rota para a página inicial
@App.route('/', methods=['GET', 'POST'])
def homepage():
    form_login = Login_Form()

    # Lidar com a submissão do formulário de login
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        # Verificar se o usuário existe e a senha está correta
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar.data)
            return redirect(url_for('perfil', id_usuario=usuario.id))
        else:
            flash('Email ou senha incorretos', 'danger')

    return render_template('homepage.html', form=form_login)

# Rota para a página de criação de conta
@App.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    form_criar_conta = Form_Criar_Conta()

    # Lidar com a submissão do formulário de criação de conta
    if form_criar_conta.validate_on_submit():
        senha_criptogarfada  = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')

        # Ajustar `crm` e `especialidade` para `None` se o tipo for "Paciente"
        if form_criar_conta.tipo.data == "Médico":
            crm = form_criar_conta.crm.data
            especialidade = form_criar_conta.especialidade.data
        else:
            crm = None
            especialidade = None

        # Criar novo usuário
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

# Rota para a página de perfil
@App.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):

    # Verificar se o usuário atual está acessando seu próprio perfil
    if int(current_user.id) == int(id_usuario):
        form_foto = Form_Foto()

        # Lidar com a submissão do formulário de upload de foto
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
    
    # Verificar se o usuário atual não é um médico
    elif current_user.tipo != "Médico":
        flash("Você não tem permissão para acessar o perfil de outros usuários.", "danger")
        return redirect(url_for('perfil', id_usuario=current_user.id))

    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)

# Rota para fazer logout
@App.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# Rota para editar os detalhes da conta
@App.route('/editar_conta', methods=['GET', 'POST'])
@login_required
def editar_conta():
    form = Form_Editar_Conta(obj=current_user)  # Pré-carregar o formulário com dados do usuário atual

    # Lidar com a submissão do formulário de edição de conta
    if request.method == 'POST':
        if form.validate_on_submit():
            if bcrypt.check_password_hash(current_user.senha, form.senha_atual.data):
                current_user.username = form.username.data
                current_user.email = form.email.data
                current_user.telefone = form.telefone.data
                current_user.tipo = form.tipo.data

                if form.tipo.data == 'Médico':
                    current_user.especialidade = form.especialidade.data
                    current_user.crm = form.crm.data
                else:
                    current_user.especialidade = None
                    current_user.crm = None

                if form.nova_senha.data:
                    current_user.senha = bcrypt.generate_password_hash(form.nova_senha.data).decode('utf-8')

                database.session.commit()
                flash('Conta atualizada com sucesso!', 'success')
                return redirect(url_for('perfil', id_usuario=current_user.id))
            else:
                flash('Senha atual incorreta.', 'danger')

    return render_template('editar_conta.html', form=form)

# Rota para agendar uma consulta
@App.route('/agendar_consulta', methods=['GET', 'POST'])
@login_required
def agendar_consulta():
    form = Form_Gestao_Consulta()
    # Assegurar que os campos Select estão preenchidos com as opções corretas
    form.id_paciente.choices = [(p.id, p.username) for p in Usuario.query.filter_by(tipo='Paciente').all()]
    form.id_profissional.choices = [(m.id, m.username) for m in Usuario.query.filter_by(tipo='Médico').all()]

    # Lidar com a submissão do formulário de agendamento de consulta
    if form.validate_on_submit():
        nova_consulta = Consulta(
            id_paciente=form.id_paciente.data,
            id_profissional=form.id_profissional.data,
            data_hora=form.data_hora.data,
            status="Agendado",
            observacoes=form.observacoes.data
        )
        database.session.add(nova_consulta)
        database.session.commit()
        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('perfil', id_usuario=current_user.id))

    return render_template('agendar_consulta.html', form=form)

# Rota para visualizar prontuários
@App.route('/prontuario/<int:id_usuario>', methods=['GET'])
@login_required
def prontuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    # Verificar se o usuário atual está autorizado a visualizar os prontuários
    if current_user.id != id_usuario and current_user.tipo != 'Médico':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('perfil', id_usuario=current_user.id))

    prontuarios = Prontuario.query.filter_by(id_paciente=id_usuario).all()
    return render_template('prontuario.html', usuario=usuario, prontuarios=prontuarios)

# Rota para visualizar as consultas do usuário atual
@App.route('/minhas_consultas')
@login_required
def minhas_consultas():
    # Verificar se o usuário atual é um paciente
    if current_user.tipo != 'Paciente':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('perfil', id_usuario=current_user.id))
    
    consultas = Consulta.query.filter_by(id_paciente=current_user.id).all()
    return render_template('minhas_consultas.html', consultas=consultas, now=now)

# Rota para visualizar consultas agendadas para médicos
@App.route('/consultas_agendadas')
@login_required
def consultas_agendadas():
    # Verificar se o usuário atual é um médico
    if current_user.tipo != 'Médico':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('perfil', id_usuario=current_user.id))
    
    # Obter a data atual e a data final (7 dias a partir de hoje)
    data_inicio = datetime.now().date()
    data_fim = data_inicio + timedelta(days=7)
    
    # Buscar consultas não canceladas para os próximos 7 dias
    consultas = Consulta.query.filter(
        Consulta.id_profissional == current_user.id,
        Consulta.status != 'Cancelada',
        Consulta.data_hora >= data_inicio,
        Consulta.data_hora < data_fim
    ).order_by(Consulta.data_hora).all()
    
    # Organizar consultas por dia e hora
    agenda = {}
    for consulta in consultas:
        dia = consulta.data_hora.date()
        if dia not in agenda:
            agenda[dia] = []
        agenda[dia].append(consulta)
    
    return render_template('consultas_agendadas.html', agenda=agenda, data_inicio=data_inicio, data_fim=data_fim)

# Rota para excluir a conta do usuário atual
@App.route('/excluir_conta', methods=['POST'])
@login_required
def excluir_conta():
    try:
        user = Usuario.query.get(current_user.id)
        if user:
            # Remover todas as relações do usuário
            user.fotos = []
            user.consultas_paciente = []
            user.consultas_profissional = []
            user.prontuarios_paciente = []
            user.prontuarios_profissional = []
            
            # Commit para salvar as alterações nas relações
            database.session.commit()
            
            # Agora podemos excluir o usuário
            database.session.delete(user)
            database.session.commit()
            
            logout_user()
            flash('Sua conta foi excluída com sucesso.', 'success')
        else:
            flash('Usuário não encontrado.', 'error')
    except Exception as e:
        database.session.rollback()
        flash(f'Ocorreu um erro ao excluir a conta: {str(e)}', 'error')
    
    return redirect(url_for('homepage'))

# Rota para reagendar uma consulta
@App.route('/reagendar_consulta/<int:id_consulta>', methods=['GET', 'POST'])
@login_required
def reagendar_consulta(id_consulta):
    consulta = Consulta.query.get_or_404(id_consulta)
    # Verificar se o usuário atual está autorizado a reagendar a consulta
    if consulta.id_paciente != current_user.id:
        flash('Você não tem permissão para reagendar esta consulta.', 'danger')
        return redirect(url_for('minhas_consultas'))

    form = Form_Reagendar_Consulta()

    # Lidar com a submissão do formulário de reagendamento de consulta
    if form.validate_on_submit():
        consulta.data_hora = form.data_hora.data
        consulta.status = 'Reagendado'
        database.session.commit()
        flash('Consulta reagendada com sucesso!', 'success')
        return redirect(url_for('minhas_consultas'))

    return render_template('reagendar_consulta.html', form=form, consulta=consulta)

# Rota para atualizar uma consulta (cancelar ou atualizar prescrição)
@App.route('/atualizar_consulta/<int:id_consulta>', methods=['POST'])
@login_required
def atualizar_consulta(id_consulta):
    consulta = Consulta.query.get_or_404(id_consulta)
    action = request.form.get('action')

    # Lidar com o cancelamento da consulta
    if action == 'cancelar':
        consulta.status = 'Cancelada'
        flash('Consulta cancelada com sucesso.', 'success')
    # Lidar com a atualização da prescrição se o usuário atual for um médico
    elif action == 'atualizar' and current_user.tipo == 'Médico':
        consulta.prescricao = request.form.get('prescricao')
        flash('Prescrição atualizada com sucesso.', 'success')

    database.session.commit()
    
    if current_user.tipo == 'Médico':
        return redirect(url_for('consultas_agendadas'))
    else:
        return redirect(url_for('minhas_consultas'))

# Rota para realizar uma consulta
@App.route('/realizar_consulta/<int:id_consulta>', methods=['GET', 'POST'])
@login_required
def realizar_consulta(id_consulta):
    # Verificar se o usuário atual é um médico
    if current_user.tipo != 'Médico':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('perfil', id_usuario=current_user.id))

    consulta = Consulta.query.get_or_404(id_consulta)
    # Verificar se o usuário atual está autorizado a realizar a consulta
    if consulta.id_profissional != current_user.id:
        flash('Você não tem permissão para realizar esta consulta.', 'danger')
        return redirect(url_for('consultas_agendadas'))

    form = Form_Realizar_Consulta()

    # Lidar com a submissão do formulário de realização de consulta
    if form.validate_on_submit():
        prontuario = Prontuario(
            id_paciente=consulta.id_paciente,
            id_profissional=current_user.id,
            anamnese=form.anamnese.data,
            exame_fisico=form.exame_fisico.data,
            diagnostico=form.diagnostico.data,
            prescricoes=form.prescricao.data,
            anotacoes_medicas=form.anotacoes_medicas.data,
            data=datetime.utcnow()
        )
        consulta.status = 'Concluído'
        database.session.add(prontuario)
        database.session.commit()
        flash('Consulta concluída com sucesso!', 'success')
        return redirect(url_for('consultas_agendadas'))

    return render_template('realizar_consulta.html', form=form, consulta=consulta)