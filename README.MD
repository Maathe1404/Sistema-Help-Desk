# Sistema Help Desk

Sistema web de gerenciamento de chamados de suporte técnico, desenvolvido com Python e Flask.

## Sobre o projeto

O Sistema Help Desk é uma aplicação web que permite aos usuários abrir e acompanhar chamados de suporte técnico. Os usuários de suporte podem gerenciar os chamados, atualizar seus status e excluí-los.

## Funcionalidades

- Cadastro de usuários.

- Login e autenticação com senhas criptografadas.

- Abertura de chamados com título, descrição e prioridade.

- Painel do solicitante para acompanhar seus chamados.

- Painel de suporte para visualizar todos os chamados.

- Atualização do status dos chamados.

- Exclusão de chamados.

- Controle de acesso por tipo de usuário.

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone git@github.com:Maathe1404/Sistema-Help-Desk.git
```

### 2. Entre na pasta do projeto

```bash
cd Sistema-HelpDesk
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute a aplicação

```bash
python app.py
```

Depois, acesse no navegador:

http://127.0.0.1:5000

## Acesso de demonstração

**Usuário de suporte**

- E-mail: suporte1@helpdesk.com
- Senha: suporte123

**Usuário solicitante**

Crie uma conta pela página de cadastro para testar as funcionalidades de solicitante.

## Banco de dados

O projeto utiliza SQLite. O banco de dados é criado automaticamente na inicialização da aplicação, caso ainda não exista.