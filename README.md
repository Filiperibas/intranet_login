# intranet_login
Um pequeno projeto com o objetivo de autenticar colaboradores numa intranet verificando credenciais contra o cadastro de funcionários pré-existente.

# Intranet de Requisições — Módulo de Login (Flask + SQLite)

## Visão geral
- **Objetivo**: autenticar colaboradores numa intranet verificando credenciais contra o cadastro de funcionários pré-existente.
- **Stack**: Python/Flask, SQLAlchemy, Flask-Login, Flask-Migrate, SQLite.
- **Arquitetura**: MVC simples com *blueprints* `auth` e `main`, ORM para persistência e **um único banco** (arquivo SQLite) em `instance/app.db`.

## Por que SQLite
- Zero fricção: não precisa de servidor de banco. É um arquivo (`app.db`) aberto pela aplicação.
- Instalação mínima: já vem embutido no Python (módulo `sqlite3`). O CLI `sqlite3.exe` é opcional, só para inspeção rápida.
- Perfeito para aula/MVP: poucas escritas concorrentes, fácil de distribuir e versionar (sem o arquivo do banco).
- Portável: roda idêntico no Windows, Linux e Mac.

Em produção ou com alto volume/concorrência, troque por PostgreSQL sem reescrever o app (basta alterar a `DATABASE_URI`).

## Pré-requisitos
- Python 3.10+ instalado
- PowerShell (Windows)
- (Opcional) SQLite CLI para inspeção manual

### Instalar/verificar o SQLite CLI (opcional)
1. Crie `C:\sqlite`
2. Baixe o pacote “sqlite-tools” (zip oficial) e descompacte em `C:\sqlite`
3. Adicione `C:\sqlite` ao PATH do usuário:
   ```powershell
   [System.Environment]::SetEnvironmentVariable('Path', $env:Path + ';C:\sqlite', 'User')
   $env:Path = [System.Environment]::GetEnvironmentVariable('Path','User')
   ```
4. Teste:
   ```powershell
   sqlite3 --version
   ```

## Criando e ativando a venv (Windows/PowerShell)
```powershell
# Criar pasta do projeto
mkdir C:\dev\intranet-login
cd C:\dev\intranet-login

# Permitir scripts da venv (uma vez por usuário)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Criar venv
python -m venv .venv

# Ativar venv
.\.venv\Scripts\Activate.ps1

# Atualizar pip
python -m pip install --upgrade pip
```

### Instalar dependências
```powershell
pip install Flask SQLAlchemy Flask-Login Flask-Migrate python-dotenv email-validator
pip freeze > requirements.txt
```

## Estrutura de pastas e arquivos
```
intranet-login/
├─ .venv/
├─ instance/
│  └─ app.db
├─ app/
│  ├─ __init__.py
│  ├─ models.py
│  ├─ auth/
│  │  ├─ __init__.py
│  │  └─ routes.py
│  ├─ main/
│  │  ├─ __init__.py
│  │  └─ routes.py
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ auth/login.html
│  │  └─ main/index.html
│  └─ static/
│     ├─ css/style.css
│     └─ img/login-illustration.svg
├─ config.py
├─ wsgi.py
├─ .flaskenv
├─ migrations/
├─ seed.py
└─ .gitignore
```

### Principais arquivos
- `config.py`: configurações da aplicação
- `app/__init__.py`: fábrica da aplicação Flask, inicializa db, migrate e login_manager
- `app/models.py`: define Funcionario, Usuario e LogAcesso
- `auth/routes.py`: rotas de login/logout
- `main/routes.py`: rota da home protegida
- `templates/`: páginas base, login e index
- `static/`: CSS e imagens
- `seed.py`: popula banco com 5 funcionários/usuários de teste
- `wsgi.py`: ponto de entrada para rodar

## Banco de Dados
**Funcionario**
- id (PK)
- nome_completo
- cpf (UNIQUE)
- email (UNIQUE)
- endereco, cep, cidade, estado

**Usuario**
- id (PK)
- funcionario_id (FK, UNIQUE)
- username (UNIQUE)
- senha_hash
- ativo
- ultimo_login

**LogAcesso**
- id (PK)
- usuario_id (FK)
- data_hora
- ip
- sucesso
- motivo

## Inicialização do projeto
```powershell
flask db init
flask db migrate -m "tabelas iniciais"
flask db upgrade
python .\seed.py
flask run
```

Login de teste:
- Usuário: ana@empresa.com
- Senha: 123456

## Verificação do SQLite
```powershell
sqlite3 .\instance\app.db
.tables
.schema usuario
SELECT * FROM usuario;
.exit
```

## Fluxo de autenticação
1. Usuário envia username (email) + senha
2. Back-end busca Usuario
3. Confere hash com check_password_hash
4. login_user cria sessão
5. Atualiza ultimo_login
6. LogAcesso registra tentativa

## Estrutura das páginas
- auth/login.html: formulário de login
- base.html: layout principal
- main/index.html: home protegida

## Scripts úteis
```powershell
# Rodar app
.\.venv\Scripts\Activate.ps1
flask run

# Migrações
flask db migrate -m "ajuste"
flask db upgrade

# Repopular
python .\seed.py
```

## Segurança implementada
- Hash seguro de senha (PBKDF2-SHA256 via generate_password_hash)
- Sessão com Flask-Login e @login_required
- Unicidade de CPF, email e username
- Log de acessos (sucesso/falha)
- Cookies de sessão com HttpOnly e Secure (quando em HTTPS)
- CSRF via Flask-WTF (ativável em formulários)
