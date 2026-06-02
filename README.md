# SEA - Sistema de Envio de Atividades

Sistema web desenvolvido em Flask para gerenciamento de atividades escolares, permitindo o cadastro de alunos, turmas e atividades em um ambiente simples e organizado.

## 📚 Sobre o Projeto

O SEA (Sistema de Envio de Atividades) foi criado para auxiliar instituições de ensino no gerenciamento de atividades acadêmicas.

A plataforma permite:

- Cadastro de usuários
- Cadastro de alunos
- Gerenciamento de turmas
- Criação de atividades
- Login de usuários
- Painel para estudantes
- Organização das atividades por turma

## 🛠️ Tecnologias Utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite / PostgreSQL (via SQLAlchemy)
- HTML5
- Tailwind CSS
- Jinja2

## 📁 Estrutura do Projeto

```text
SEA/
│
├── backend/
│   ├── __init__.py
│   ├── models.py
│   └── routes_pages.py
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── estudante.html
│   ├── dashboard.html
│   ├── turma.html
│   ├── atividade.html
│   ├── professores.html
│   └── perfilaluno.html
│
├── run.py
├── requirements.txt
└── README.md
```

## 🗄️ Banco de Dados

### Usuário

| Campo | Tipo |
|---------|---------|
| id | Integer |
| name | String |
| username | String |
| curso | String |
| serie | String |
| turma | String |
| matricula | String |
| password | String |

### Turma

| Campo | Tipo |
|---------|---------|
| id | Integer |
| curso | String |
| serie | String |

### Atividade

| Campo | Tipo |
|---------|---------|
| id | Integer |
| nome | String |
| descricao | String |
| data_fim | Date |
| turma_id | Foreign Key |

## ⚙️ Instalação

## 🐘 Configurando o PostgreSQL

### 1. Instale o PostgreSQL

Baixe e instale o PostgreSQL:

 [oai_citation:0‡postgresql.org](https://www.postgresql.org/download/)

Durante a instalação, defina uma senha para o usuário `postgres`.

---

### 2. Criar o Banco de Dados

Abra o terminal do PostgreSQL (psql) e execute:

```sql
CREATE DATABASE sea;
```

Verifique se o banco foi criado:

```sql
\l
```

---

### 3. Configurar a Conexão

Crie um arquivo `.env` na raiz do projeto:

```env
KEY=sua_chave_secreta

DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/sea
```

Exemplo:

```env
DATABASE_URL=postgresql://postgres:123456@localhost:5432/sea
```

---

### 4. Instalar Dependências

Além das dependências do projeto, instale o driver do PostgreSQL:

```bash
pip install psycopg2-binary
```

Ou:

```bash
pip install -r requirements.txt
```

---

### 5. Criar as Tabelas

Com o banco configurado, execute:

```bash
python run.py
```

O SQLAlchemy criará automaticamente as tabelas:

- user
- turma
- atividade

---

### Estrutura das Tabelas

#### user

```sql
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    curso VARCHAR(80) NOT NULL,
    serie VARCHAR(80),
    turma VARCHAR(80),
    matricula VARCHAR(80) UNIQUE,
    password TEXT NOT NULL
);
```

#### turma

```sql
CREATE TABLE turma (
    id SERIAL PRIMARY KEY,
    curso VARCHAR(80) NOT NULL,
    serie VARCHAR(80) NOT NULL
);
```

#### atividade

```sql
CREATE TABLE atividade (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(80) NOT NULL,
    descricao VARCHAR(200) NOT NULL,
    data_fim DATE NOT NULL,
    turma_id INTEGER NOT NULL REFERENCES turma(id)
);
```

### 6. Clone o repositório

```bash
git clone https://github.com/Ualter-Lab/SEA.git
```

### 7. Entre na pasta do projeto

```bash
cd SEA
```

### 8. Crie um ambiente virtual

```bash
python -m venv venv
```

### 9. Ative o ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 10. Instale as dependências

```bash
pip install -r requirements.txt
```

### 11. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
KEY=sua_chave_secreta
DATABASE_URL=sqlite:///sea.db
```

## ▶️ Executando o Projeto

```bash
python run.py
```

O sistema ficará disponível em:

```text
http://localhost:5001
```

## 🚀 Funcionalidades Futuras

- Recuperação de senha
- Upload de arquivos nas atividades
- Dashboard com estatísticas
- Sistema de notas
- Área exclusiva para professores
- Controle de entrega de atividades

## 👨‍💻 Autor

Desenvolvido por Walter Neto.

GitHub:
https://github.com/Ualter-Lab