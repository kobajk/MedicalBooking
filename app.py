from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Classe Usuario
class Usuario:
    def __init__(self, id, nome, email, senha, tipo):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo

# Lista de usuários mockados
usuarios_mock = [
    Usuario(1, 'João Silva', 'joao@examplo.com', '12345', 'Paciente'),
    Usuario(2, 'Maria Souza', 'maria@examplo.com', '12345', 'Profissional'),
]

# Função para autenticar o usuário
def autenticar_usuario(email, senha):
    for usuario in usuarios_mock:
        if usuario.email == email and usuario.senha == senha:
            return usuario
    return None

# Função para verificar se o email existe
def verificar_email(email):
    for usuario in usuarios_mock:
        if usuario.email == email:
            return True
    return False

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/check-email', methods=['POST'])
def check_email():
    email = request.form['email']
    if verificar_email(email):
        return render_template('login.html', step=2, email=email)
    else:
        return render_template('login.html', step=3)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    usuario = autenticar_usuario(email, senha)
    if usuario:
        return redirect(url_for('welcome', nome=usuario.nome))
    else:
        return 'Credenciais inválidas, tente novamente.'

@app.route('/welcome')
def welcome():
    nome = request.args.get('nome')
    return f'Bem-vindo, {nome}!'

if __name__ == '__main__':
    app.run(debug=True)