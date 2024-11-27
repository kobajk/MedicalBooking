# MedicalBooking

## Visão Geral
MedicalBooking é uma aplicação web para gerenciar consultas médicas, registros de pacientes e horários de médicos. A aplicação permite que pacientes e médicos interajam de forma eficiente, facilitando o agendamento e a gestão de consultas.

## Funcionalidades
- Cadastro de usuários (pacientes e médicos)
- Login de usuários
- Upload de fotos de exames do paciente
- Agendamento de consultas
- Visualização de prontuários
- Visualização de consultas marcadas

## Tecnologias Utilizadas
- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF
- **Segurança**: Flask-Bcrypt
- **Frontend**: HTML, CSS


## Instalação

### Pré-requisitos
- Python 3.11
- Virtualenv

### Passo a Passo

1. **Clonar o repositório**
    ```bash
    git clone https://github.com/kobajk/MedicalBooking.git
    cd MedicalBooking
    ```

2. **Criar e ativar um ambiente virtual**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # No Windows
    source venv/bin/activate  # No macOS/Linux
    ```

3. **Instalar as dependências**
    ```bash
    pip install -r requirements.txt
    ```

4. **Criar o banco de dados**
    ```bash
    python gerar_banco.py
    ```

5. **Executar a aplicação**
    ```bash
    python main.py
    ```

## Uso
- Acesse a aplicação em `http://127.0.0.1:5000`
- Registre-se como paciente ou médico
- Faça login para acessar as funcionalidades

## Documentação
Para mais detalhes sobre a arquitetura do projeto, consulte o arquivo [`ARCHITECTURE.md`](ARCHITECTURE.md).