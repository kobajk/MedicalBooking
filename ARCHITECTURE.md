# Arquitetura do Projeto MedicalBooking

## Visão Geral
O projeto MedicalBooking é projetado para gerenciar consultas médicas, registros de pacientes e horários de médicos. A arquitetura é dividida em vários componentes-chave para garantir modularidade, escalabilidade e manutenção.

## Componentes

### 1. Frontend
- **Tecnologia**: HTML, CSS
- **Descrição**: A interface do usuário para pacientes e médicos interagirem com o sistema.
- **Principais Funcionalidades**:
    - Agendamento de consultas
    - Painéis de controle para pacientes e médicos

### 2. Backend
- **Tecnologia**: Flask (Python)
- **Descrição**: Framework web utilizado para construir a aplicação backend.
- **Principais Funcionalidades**:
    - API para comunicação com o frontend
    - Autenticação e autorização
    - Validação e processamento de dados

### 3. Banco de Dados
- **Tecnologia**: SQLite
- **Descrição**: O banco de dados relacional para armazenar todos os dados da aplicação.
- **Principais Funcionalidades**:
    - Registros de pacientes
    - Agendamentos de consultas
    - Informações dos médicos

### 4. Serviço de Autenticação
- **Tecnologia**: Flask com Flask-Login
- **Descrição**: Gerencia a autenticação e autorização dos usuários.
- **Principais Funcionalidades**:
    - Registro e login de usuários
    - Controle de acesso baseado em funções

## Interação entre Componentes

### Fluxo de Interação

1. **Frontend e Backend**:
    - O frontend envia requisições HTTP para o backend utilizando formulários HTML.
    - O backend, implementado com Flask, recebe essas requisições e as processa.
    - O backend valida os dados recebidos e, se necessário, interage com o banco de dados.
    - Após o processamento, o backend retorna uma resposta ao frontend, que pode ser uma página HTML renderizada ou uma mensagem de erro.

2. **Backend e Banco de Dados**:
    - O backend utiliza SQLAlchemy para interagir com o banco de dados SQLite.
    - Operações como criação, leitura, atualização e exclusão (CRUD) são realizadas através de modelos definidos em [Clinicas/models.py](Clinicas/models.py).
    - Por exemplo, ao registrar um novo usuário, o backend cria uma nova instância do modelo `Usuario` e a salva no banco de dados.

3. **Serviço de Autenticação**:
    - O serviço de autenticação utiliza Flask-Login para gerenciar sessões de usuário.
    - Quando um usuário faz login, suas credenciais são verificadas e, se corretas, uma sessão é iniciada.
    - Flask-Login utiliza cookies para manter a sessão do usuário ativa.
    - O backend verifica a sessão do usuário em cada requisição para garantir que apenas usuários autenticados possam acessar determinadas rotas.

### Exemplo de Fluxo de Usuário

1. **Login**:
    - O usuário acessa a página de login e envia suas credenciais.
    - O backend recebe as credenciais, verifica-as no banco de dados e, se corretas, inicia uma sessão.
    - O usuário é redirecionado para sua página de perfil.

2. **Agendamento de Consulta**:
    - O usuário autenticado acessa a página de agendamento de consultas.
    - O frontend envia os dados do agendamento para o backend.
    - O backend valida os dados e cria um novo registro de consulta no banco de dados.
    - O usuário recebe uma confirmação do agendamento.

## Estrutura de Diretórios

```
MedicalBooking/
├── Clinicas/
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── forms.cpython-311.pyc
│   │   ├── models.cpython-311.pyc
│   │   ├── routes.cpython-311.pyc
│   ├── static
│   │   ├── fotos_post
│   │   │   ├── default.png
│   │   │   ├── teste1.png
│   │   │   ├── teste2.png
│   │   ├── styles
│   │   │   ├── styles.css
│   ├── Templates
│   │   ├── agendar_consulta.html
│   │   ├── base.html
│   │   ├── consultas_agendadas.html
│   │   ├── criar_conta.html
│   │   ├── editar_conta.html
│   │   ├── homepage.html
│   │   ├── minhas_consultas.html
│   │   ├── perfil.html
│   │   ├── prontuario.html
│   │   ├── reagendar_consulta.html
│   │   ├── realizar_consulta.html
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
├── instance
│   ├── usuarios.db
├── .gitignore
├── ARCHITECTURE.md
├── gerar_banco.py
├── main.py
└── README.md
```

## Implantação
- **Plataforma**: Ambiente local
- **Descrição**: A aplicação é executada em um ambiente local para desenvolvimento e testes.
- **Principais Funcionalidades**:
    - Scripts automatizados de criação de banco de dados e execução da aplicação

## Detalhes de Segurança

- **Dados_pessoais**: O ambiente possui um sistema de encriptação de senhas que fortalece a segurança dos usuarios com o sistema, além disso, 
possui um banco de dados privado o que ajuda a não a vazar informações sensiveis. Ao fazer o cadastro o usuario concorda com os termos de uso do sistema.