#%%
# Create forms for the application (input)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Clinicas.models import Usuario

class Login_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar de mim', default=False)
    submit = SubmitField('Continuar')

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

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')
        
    def validate_paciente(self, crm):
        if self.tipo.data == 'Paciente':
            # Define crm e especialidade como None se tipo for "Paciente"
            self.crm.data = None
            self.especialidade.data = None
        return True


class Form_Editar_Conta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    # nova_senha = PasswordField('Nova Senha', validators=[Length(min=8, max=20)])
    # confirmar_nova_senha = PasswordField('Confirmar Nova Senha', validators=[EqualTo('nova_senha')])
    tipo = SelectField('Tipo', choices=[('Paciente', 'Paciente'), ('Médico', 'Médico')], validators=[DataRequired()])
    especialidade = StringField('Especialidade', validators=[Length(max=100)])
    crm = StringField('CRM', validators=[Length(max=20)])
    telefone = StringField('Telefone', validators=[Length(max=15)])
    submit = SubmitField('Salvar Alterações')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')

    def validate_paciente(self, crm):
        if self.tipo.data == 'Paciente':
            # Define crm e especialidade como None se tipo for "Paciente"
            self.crm.data = None
            self.especialidade.data = None
        return True


class Form_Foto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    submit = SubmitField('Enviar')




