# CRUD de Produtos (Flask + SQLAlchemy + MySQL + Tailwind)

Este é um sistema simples de CRUD de produtos para teste técnico, com autenticação de usuário, interface web usando **TailwindCSS**, back-end em **Flask** e banco de dados **MySQL** e ORM SQLAlchemy.  
Permite **login**, **cadastro/listagem/edição/exclusão** de produtos.

---

## 📚 Sumário

- [🚀 Tecnologias](#-tecnologias)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [⚙️ Pré-requisitos](#️-pré-requisitos)
- [🔧 Instalação](#-instalação)
- [🗄️ Inicializando o Banco de Dados](#️-inicializando-o-banco-de-dados)
  - [Criar tabelas](#criar-tabelas)
  - [Criar usuário admin](#criar-usuário-admin)
- [▶️ Rodando o Projeto](#️-rodando-o-projeto)
- [👤 Login](#-login)
- [✨ Funcionalidades](#-funcionalidades)
- [🔒 Segurança](#-segurança)
- [📦 Organização do Projeto](#-organização-do-projeto)
- [🐳 Executar com Docker](#-executar-com-docker) <!-- remova se não for usar Docker -->
- [📝 Licença](#-licença) <!-- remova se não tiver -->

---
## 🚀 Tecnologias
- Python 3.10+
- Flask
- SQLAlchemy (ORM)
- Flask-Login (autenticação)
- Flask-WTF (CSRF + formulários)
- MySQL
- TailwindCSS (via CDN)

---

## 📂 Estrutura do Projeto

```
crud-produtos/
│
├── app/                         # pacote Python
│   ├── __init__.py              # cria a app e registra blueprints
│   ├── db.py                    # engine + Session (SQLAlchemy Core/ORM)
│   ├── helpers.py               # csrf, login_manager, etc.
│   ├── utils.py                 # helpers gerais (se usar)
│   ├── models/
│   │   ├── __init__.py          # Base, imports de modelos
│   │   ├── product.py
│   │   └── user.py
│   └── blueprints/
│       ├── auth/
│       │   ├── __init__.py      # bp = Blueprint("auth", __name__)
│       │   ├── forms.py
│       │   └── routes.py        # / (login), /logout
│       └── products/
│           ├── __init__.py      # bp = Blueprint("products", __name__, url_prefix="/products")
│           ├── forms.py
│           └── routes.py        # lista/cria/edita/exclui
│
├── templates/                   # Jinja2 globais
│   ├── _shared/
│   │   └── base.html
│   ├── auth/
│   │   └── login.html
│   └── products/
│       ├── lista_produtos.html
│       ├── formulario_produto.html
│       └── confirma_delete.html
│
├── static/                      # arquivos estáticos globais
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── ui.js
│
├── cli.py                       # comandos: init-db / create-user
├── run.py                       # roda o servidor (flask app)
├── config.py                    # classe Config (SECRET_KEY, DATABASE_URL, etc.)
├── requirements.txt
├── .env.example
├── .env
├── .gitignore
└── README.md
```

---

## ⚙️ Pré-requisitos

1. **Python 3.10+**
2. **MySQL** instalado e rodando
3. Criar banco e usuário no MySQL:

```sql
CREATE DATABASE crud_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'crud_user'@'localhost' IDENTIFIED BY 'crud_password';
GRANT ALL PRIVILEGES ON crud_db.* TO 'crud_user'@'localhost';
FLUSH PRIVILEGES;
```

4. Criar arquivo `.env` na raiz com:

```ini
# GERE uma chave segura, por exemplo com: python -c "import secrets; print(secrets.token_hex(32))"
# chave secreta para sessão/CSRF (gere uma diferente em produção)
SECRET_KEY=92407b4026d0bcd61e718e938db7381a4daab4cd05c2faf73bc860d21e5066ff

# conexão MySQL
DATABASE_URL=mysql+pymysql://crud_user:crud_password@localhost/crud_db

# modo debug
FLASK_DEBUG=True #ou False
```

---

## 🔧 Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/sidneyjfg/crud-produtos-flask.git
cd crud-produtos
pip install -r requirements.txt
```

---

## 🗄️ Inicializando o Banco de Dados

### Criar tabelas:
```bash
python cli.py init-db
```

### Criar usuário admin:
```bash
python cli.py create-user --username admin --password 123456
```

---

## ▶️ Rodando o Projeto

```bash
python run.py
```

Abra em [http://localhost:5000](http://localhost:5000)

---

## 👤 Login

- Usuário criado no passo anterior (`create-user`).
- Exemplo:  
  **Usuário:** `admin`  
  **Senha:** `123456`

---

## ✨ Funcionalidades

- Autenticação com login/logout
- Lista de produtos com ações:
  - Adicionar produto
  - Editar produto
  - Excluir produto
- Campos do produto:
  - ID (auto)
  - Nome
  - Descrição
  - Quantidade
  - Preço

---

## 🔒 Segurança

1. **Login obrigatório (`@login_required`)**  
   Toda rota protegida só pode ser acessada se o usuário estiver autenticado.  
   Se alguém tentar acessar `/products/` ou enviar um POST para `/products/create` sem login, é redirecionado para a tela de login.

2. **Proteção contra CSRF (`Flask-WTF`)**  
   Cada formulário contém um **token único** que deve ser enviado junto com a requisição.  
   Isso impede que um site externo envie requisições falsas em nome do usuário logado.

3. **Senhas com hash seguro**  
   Nunca são salvas em texto plano, sempre com hash (`werkzeug.security`).

---

## 📦 Organização do Projeto

A estrutura foi organizada em **blueprints** e **pastas modulares**:
- `blueprints/auth` → cuida apenas do login/logout.  
- `blueprints/products` → cuida apenas do CRUD de produtos.  
- `models/` → contém apenas as definições das tabelas (User, Product).  
- `templates/` e `static/` → ficam separados, facilitando manutenção do front-end.  

👉 Essa divisão torna o projeto **mais claro, fácil de escalar e manter**, porque cada parte tem sua responsabilidade bem definida.

---

## Projeto criado para fins de desafio