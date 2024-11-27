#%%
# Criar formulários para a aplicação (input)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField, DateTimeLocalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Clinicas.models import Usuario
from flask_login import current_user

# Formulário de Login
class Login_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar de mim', default=False)
    submit = SubmitField('Continuar')

# Formulário de Criação de Conta
class Form_Criar_Conta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=20)])
    confirmar_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    tipo = SelectField('Tipo', choices=[('Paciente', 'Paciente'), ('Médico', 'Médico')], validators=[DataRequired()])
    especialidade = StringField('Especialidade', validators=[Length(max=100)])
    crm = StringField('CRM', validators=[Length(max=20)])
    telefone = StringField('Telefone', validators=[Length(max=15)])
    submit = SubmitField('Criar conta')

    # Validação para verificar se o email já está em uso
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')
        
    # Validação para definir crm e especialidade como None se o tipo for "Paciente"
    def validate_paciente(self, crm):
        if self.tipo.data == 'Paciente':
            self.crm.data = None
            self.especialidade.data = None
        return True

# Formulário de Edição de Conta
class Form_Editar_Conta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[Length(min=8, max=20)])
    confirmar_nova_senha = PasswordField('Confirmar Nova Senha', validators=[EqualTo('nova_senha')])
    tipo = SelectField('Tipo', choices=[('Paciente', 'Paciente'), ('Médico', 'Médico')], validators=[DataRequired()])
    especialidade = StringField('Especialidade', validators=[Length(max=100)])
    crm = StringField('CRM', validators=[Length(max=20)])
    telefone = StringField('Telefone', validators=[Length(max=15)])
    submit = SubmitField('Salvar Alterações')

    # Validação para verificar se o email já está em uso por outro usuário
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario and usuario.id != current_user.id:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')

# Formulário de Upload de Foto
class Form_Foto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Formulário de Gestão de Consulta
class Form_Gestao_Consulta(FlaskForm):
    id_paciente = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    id_profissional = SelectField('Profissional', coerce=int, validators=[DataRequired()])
    data_hora = DateTimeLocalField('Data e Hora', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    observacoes = TextAreaField('Observações')
    submit = SubmitField('Agendar Consulta')

# Formulário de Reagendamento de Consulta
class Form_Reagendar_Consulta(FlaskForm):
    data_hora = DateTimeLocalField('Nova Data e Hora', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Reagendar Consulta')

# Formulário de Prontuário
class Form_Prontuario(FlaskForm):
    id_paciente = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    id_profissional = SelectField('Profissional', coerce=int, validators=[DataRequired()])
    anotacoes_medicas = TextAreaField('Anotações Médicas')
    prescricoes = TextAreaField('Prescrições')
    submit = SubmitField('Salvar Prontuário')

# Formulário de Realização de Consulta
class Form_Realizar_Consulta(FlaskForm):
    anamnese = TextAreaField('Anamnese', validators=[DataRequired()])
    exame_fisico = TextAreaField('Exame Físico', validators=[DataRequired()])
    diagnostico = TextAreaField('Diagnóstico', validators=[DataRequired()])
    prescricao = TextAreaField('Prescrição', validators=[DataRequired()])
    anotacoes_medicas = TextAreaField('Anotações Médicas')
    submit = SubmitField('Concluir Consulta')