#%%
# Create forms for the application (input)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Clinicas.models import Usuario

class Login_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    # lembrar = BooleanField('Lembrar de mim', default=False)
    submit = SubmitField('Login')

class Form_Criar_Conta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=20)])
    confirmar_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')

class Form_Foto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    submit = SubmitField('Enviar')








