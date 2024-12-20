#%%
# Criar a estrutura do banco de dados
from Clinicas import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# Função para carregar o usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Modelo para a tabela de Usuários
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha = database.Column(database.String(80), nullable=False)
    tipo = database.Column(database.String(50), nullable=False)  # Tipo do usuário
    especialidade = database.Column(database.String(100), nullable=True)  # Especialidade do usuário
    crm = database.Column(database.String(20), nullable=True)  # CRM do usuário, caso seja um médico
    telefone = database.Column(database.String(15), nullable=True)  # Telefone de contato
    fotos = database.relationship('Foto', backref='usuario', lazy=True)  # Relacionamento com a tabela de Fotos

    # Construtor opcional
    # def __init__(self, username, email, senha, tipo, especialidade=None, crm=None, telefone=None):
    #     self.username = username
    #     self.email = email
    #     self.senha = senha
    #     self.tipo = tipo
    #     self.especialidade = especialidade
    #     self.crm = crm
    #     self.telefone = telefone

# Modelo para a tabela de Fotos
class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default='default.png')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)  # Chave estrangeira da tabela Usuario
    
    # Construtor opcional
    # def __init__(self, imagem='default.png', id_usuario=None):
    #     self.imagem = imagem
    #     self.data_criacao = datetime.utcnow()
    #     self.id_usuario = id_usuario

# Modelo para a tabela de Consultas
class Consulta(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_paciente = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_profissional = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    data_hora = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    status = database.Column(database.String(20), nullable=True)
    observacoes = database.Column(database.Text)

    # Relacionamentos com a tabela de Usuários
    paciente = database.relationship('Usuario', foreign_keys=[id_paciente], backref='consultas_paciente')
    profissional = database.relationship('Usuario', foreign_keys=[id_profissional], backref='consultas_profissional')

# Modelo para a tabela de Prontuários
class Prontuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_paciente = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_profissional = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    anamnese = database.Column(database.Text, nullable=False)
    exame_fisico = database.Column(database.Text, nullable=False)
    diagnostico = database.Column(database.Text, nullable=False)
    prescricoes = database.Column(database.Text, nullable=False)
    anotacoes_medicas = database.Column(database.Text, nullable=True)
    data = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

    # Relacionamentos com a tabela de Usuários
    paciente = database.relationship('Usuario', foreign_keys=[id_paciente], backref='prontuarios_paciente')
    profissional = database.relationship('Usuario', foreign_keys=[id_profissional], backref='prontuarios_profissional')