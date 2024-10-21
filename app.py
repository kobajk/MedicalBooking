from flask import Flask, render_template, request, redirect, url_for, session,jsonify
# Importar outras bibliotecas necessárias e módulos do banco de dados

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Definição da classe Usuario
class Usuario:
    def __init__(self, id, nome, email, senha, tipo_usuario):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha  # Em um ambiente real, as senhas devem ser armazenadas de forma segura (hash)
        self.tipo_usuario = tipo_usuario  # 'Paciente' ou 'Profissional'
    
    # método sobrescrito para retornar um dicionário com os dados do usuário
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario
        }

# Lista de usuários mockados
usuarios_mock = [
    Usuario(1, 'João Silva', 'joao@examplo.com', '12345', 'Paciente'),
    Usuario(2, 'Maria Souza', 'maria@examplo.com', '12345', 'Profissional'),
]

# Função para autenticar o usuário
def autenticar_usuario(email, senha):
    # Itera sobre a lista de usuários mockados
    for usuario in usuarios_mock:
        if usuario.email == email and usuario.senha == senha:
            return usuario  # Credenciais válidas, retorna o objeto usuário
    return None  # Credenciais inválidas

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        # Lógica de autenticação
        usuario = autenticar_usuario(email, senha)
        if usuario:
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['tipo_usuario'] = usuario.tipo_usuario
            if usuario.tipo_usuario == 'Paciente':
                #return redirect(url_for('paciente_dashboard'))
                return render_template('paciente_dashboard.html', usuario_nome=session['usuario_nome'])
            else:
                return redirect(url_for('profissional_dashboard'))
        else:
            return render_template('login.html', mensagem='Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/paciente_dashboard')
def paciente_dashboard(usuario_nome):
    if 'usuario_id' in session and session['tipo_usuario'] == 'Paciente':
        return render_template('paciente_dashboard.html', usuario_nome=session['usuario_nome'])
    else:
        return redirect(url_for('login'))

@app.route('/profissional_dashboard')
def profissional_dashboard():
    if 'usuario_id' in session and session['tipo_usuario'] == 'Profissional':
        return render_template('profissional_dashboard.html', usuario_nome=session['usuario_nome'])
    else:
        return redirect(url_for('login'))

# Rota para agendar consulta
@app.route('/agendar_consulta', methods=['GET', 'POST'])
def agendar_consulta():
    if 'usuario_id' in session and session['tipo_usuario'] == 'Paciente':
        if request.method == 'POST':
            profissional_id = request.form['profissional_id']
            data_hora = request.form['data_hora']
            # Lógica para agendar a consulta no banco de dados
            return redirect(url_for('paciente_dashboard'))
        else:
            # Obter lista de profissionais do banco de dados
            profissionais = obter_profissionais()
            return render_template('agendar_consulta.html', profissionais=profissionais)
    else:
        return redirect(url_for('login'))

# Rota para obter dados de um paciente
@app.route('/paciente/<int:id>', methods=['GET'])
def get_paciente(id):
    paciente = usuarios_mock[id-1]  # Obter paciente do banco de dados
    if paciente:
        return jsonify(paciente.to_dict())
    else:
        return jsonify({'error': 'Paciente não encontrado'}), 404

# Função fictícia para obter profissionais (deve ser implementada)
def obter_profissionais():
    # Retorna uma lista de objetos profissionais
    pass

# Outras rotas e lógica de negócio

if __name__ == '__main__':
    app.run(debug=True)
