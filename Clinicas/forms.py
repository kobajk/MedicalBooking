#%%
# Create forms for the application (input)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from Clinicas.models import Usuario
from flask_login import current_user

class Form_Validar(FlaskForm):
    def validate_email(self, email):
        if email.data != current_user.email:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Este email já está em uso. Por favor, escolha outro.')
            
class Login_Form(Form_Validar):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar de mim', default=False)
    submit = SubmitField('Continuar')
            
class Form_Criar_Conta(Form_Validar):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=20),
                                               Regexp("(?=.*[a-z])", message = "Precisa ser incluido na senha pelo menos uma letra minuscula."),
                                               Regexp("(?=.*[A-Z])", message = "Precisa ser incluido na senha pelo menos uma letra maiúscula."),
                                               Regexp("(?=.*[0-9])", message = "Precisa ser incluido na senha pelo menos um número."),
                                               Regexp("(?=.*[!@#$%^&*])", message = "Precisa ser incluido na senha pelo menos um caractere especial."),
                                               ]) 
    confirmar_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    consentimento = BooleanField('Eu concordo com a <a href="/termos">política de privacidade</a> e os termos de uso', validators=[DataRequired()])
    submit = SubmitField('Criar conta')

class Form_Excluir_Conta(FlaskForm):
    subit = SubmitField("Excluir Conta")

class Form_Atualizar_Perfil(Form_Validar):
    usuarname = StringField("Nome de usuário", validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Atualizar")

class Form_Foto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    submit = SubmitField('Enviar')








