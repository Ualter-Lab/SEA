# SEA - Sistema de Envio de Atividades

Sistema web desenvolvido em Flask para gerenciamento acadêmico, permitindo o cadastro de alunos e professores, organização de turmas e matérias, lançamento de notas por bimestre e acompanhamento de atividades.

## 📚 Sobre o Projeto

O SEA (Sistema de Envio de Atividades) foi criado para auxiliar instituições de ensino no gerenciamento de atividades acadêmicas.

A plataforma permite:

- Cadastro e login de usuários (alunos e professores)
- Organização de alunos por turma, curso e série
- Matrícula do aluno em matérias
- Lançamento e acompanhamento de notas por bimestre (B1 a B4)
- Dashboard do aluno com médias calculadas automaticamente
- Painel de atividades

## 🛠️ Tecnologias Utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login (autenticação e sessão)
- Werkzeug Security (hash de senhas)
- SQLite / PostgreSQL (via SQLAlchemy)
- Jinja2
- Tailwind CSS (via CDN)

## 📁 Estrutura do Projeto

```text
SEA/
│
├── backend/
│   ├── __init__.py        # Factory da aplicação (create_app)
│   ├── models.py          # Modelos: user, turma, materia, atividade, notas
│   ├── routes_pages.py    # Rotas de páginas e ações (login, cadastro, notas...)
│   └── static/
│       └── script.js
│
├── templates/
│   ├── login.html         # Login e cadastro (modo="login" | "cadastro")
│   ├── startpage.html     # Dashboard (aluno e professor)
│   └── subpage.html       # Turmas, perfil do aluno, professores, matérias...
│
├── run.py
├── requirements.txt
├── tailwind.config.js
└── README.md
```

## 🗄️ Banco de Dados

### user

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | Chave primária |
| name | String | |
| username | String | Único |
| turma_id | Integer | FK → `turma.id` |
| matricula | Integer | Único |
| password | String | Hash gerado com `werkzeug.security` |
| is_teacher | Boolean | Define se o usuário é professor |

### turma

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | Chave primária |
| name | String(1) | Identificador da turma (ex.: "A") |
| curso | String | |
| serie | Integer | |

### materia

| Campo | Tipo |
|---|---|
| id | Integer |
| materia_name | String |

### atividade

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | Chave primária |
| name | String | |
| descricao | String | |
| data_fim | Date | |
| turma_id | Integer | FK → `turma.id` |

### notas

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | Chave primária |
| id_user | Integer | FK → `user.id` |
| id_materia | Integer | FK → `materia.id` |
| b1, b2, b3, b4 | Float | Notas por bimestre |

## 🌐 Rotas Principais

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Página de login |
| `/cadastro` | GET | Página de cadastro |
| `/login` | POST | Autentica o usuário |
| `/register` | POST | Cria um novo usuário |
| `/logout` | GET | Encerra a sessão |
| `/dashboard` | GET | Painel do aluno (com médias por bimestre) ou do professor |
| `/turmas` | GET | Listagem de turmas (professor) |
| `/aluno` | GET | Perfil do aluno |
| `/professores` | GET | Listagem de professores |
| `/materias` | GET | Matérias em que o aluno está matriculado |
| `/entrar_matéria` | POST | Matricula o aluno em uma matéria |
| `/logout_materia/<id>` | GET | Remove a matrícula do aluno em uma matéria |
| `/criar-matéria` | POST | Cria uma nova matéria |
| `/atividades` | GET | Painel de atividades |

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Ualter-Lab/SEA.git
cd SEA
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
KEY=sua_chave_secreta
DATABASE_URL=sqlite:///sea.db
```

Isso já é suficiente para rodar com SQLite. Para usar PostgreSQL, veja a seção abaixo.

### 5. Execute o projeto

```bash
python run.py
```

O SQLAlchemy criará automaticamente as tabelas (`user`, `turma`, `materia`, `atividade`, `notas`) na primeira execução.

O sistema ficará disponível em:

```text
http://localhost:5234
```

## 🐘 Usando PostgreSQL (opcional)

### 1. Instale o PostgreSQL

Baixe e instale em [postgresql.org](https://www.postgresql.org/download/). Durante a instalação, defina uma senha para o usuário `postgres`.

### 2. Crie o banco de dados

No terminal do PostgreSQL (`psql`):

```sql
CREATE DATABASE sea;
```

### 3. Configure a conexão no `.env`

```env
KEY=sua_chave_secreta
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/sea
```

Exemplo:

```env
DATABASE_URL=postgresql://postgres:123456@localhost:5432/sea
```

### 4. Rode o projeto normalmente

```bash
python run.py
```

O SQLAlchemy cria as tabelas automaticamente ao subir a aplicação.

## 🚀 Funcionalidades Futuras

- Recuperação de senha
- Upload de arquivos nas atividades
- Dashboard com estatísticas mais completas
- Área exclusiva para lançamento de notas pelo professor
- Controle de entrega de atividades

## 👨‍💻 Autor

Desenvolvido por Walter Neto.

GitHub: [Ualter-Lab](https://github.com/Ualter-Lab)
