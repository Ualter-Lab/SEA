# SEA - Sistema de Envio de Atividades

Sistema web em Flask para gestão acadêmica. Professores criam matérias e atividades por turma. Alunos entram nas matérias, enviam arquivos das atividades e acompanham as notas. Professores baixam as entregas e lançam a nota de cada uma.

## Sumário

- [Funcionalidades](#funcionalidades)
- [Estado atual do projeto](#estado-atual-do-projeto)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Banco de dados](#banco-de-dados)
- [Rotas](#rotas)
- [Instalação](#instalação)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Usando PostgreSQL](#usando-postgresql)
- [Atualizando um banco existente](#atualizando-um-banco-existente)
- [Roadmap](#roadmap)
- [Autor](#autor)

## Funcionalidades

### Autenticação e cadastro

- Login e logout com sessão (Flask-Login).
- Senhas com hash (Werkzeug).
- Cadastro de aluno com curso, série, turma e matrícula.
- Cadastro de professor escolhendo o curso "Professor". Os campos de série, turma e matrícula somem do formulário (`script.js`).
- Turma criada automaticamente no cadastro, caso a combinação curso + série + turma ainda não exista.
- Professor recém-cadastrado fica em espera. Um professor já aprovado confirma ou exclui a solicitação.

### Aluno

- Dashboard com matrícula, curso, série, turma e média geral. A média aparece em verde (6 ou mais) ou vermelho (abaixo de 6).
- Entrar em matérias informando o número da matéria, e sair delas.
- Média por matéria, com atalho para as atividades.
- Lista de atividades pendentes por matéria, com prazo e descrição.
- Envio de arquivo para cada atividade pendente.
- Lista de atividades entregues, com status (`pendente` ou `corrigida`) e pontos (`nota/valor`).

### Professor

- Dashboard com todas as turmas.
- Lista de alunos por turma.
- Perfil do aluno com atividades pendentes e corrigidas.
- Download da entrega de cada atividade.
- Correção das entregas pendentes: o professor informa a nota (0 a 10) e a entrega passa para `corrigida`.
- Criação de matérias.
- Exclusão de matéria com confirmação por senha do professor que a criou.
- Criação de atividades com título, descrição, prazo, valor, turma e matéria.
- Aprovação ou exclusão de solicitações de novos professores.

## Estado atual do projeto

| Recurso | Situação |
|---|---|
| Login, cadastro e logout | Pronto |
| Aprovação de professores | Pronto |
| Turmas, matérias e matrícula do aluno | Pronto |
| Criação de atividades | Pronto |
| Envio de arquivos pelo aluno | Pronto |
| Download das entregas pelo professor | Pronto |
| Correção de entregas com nota | Pronto |
| Exibição de notas e médias | Pronto |
| Notas por bimestre (B1 a B4) | Removido. A nota agora vem das atividades corrigidas |
| Recuperação de senha | Não implementado |
| Migrações de banco | Não implementado |

## Tecnologias

- Python 3
- Flask 3.1
- Flask-SQLAlchemy 3.1 / SQLAlchemy 2.0
- Flask-Login 0.6
- Werkzeug (hash de senhas e `secure_filename`)
- python-dotenv
- SQLite ou PostgreSQL (`psycopg2-binary`)
- Jinja2
- Tailwind CSS via CDN
- JavaScript puro (`backend/static/script.js`)

## Estrutura do projeto

```text
SEA/
├── backend/
│   ├── __init__.py        # Factory da aplicação (create_app), db e LoginManager
│   ├── models.py          # Modelos do banco
│   ├── routes_pages.py    # Blueprint "pages": páginas e ações
│   └── static/
│       └── script.js      # Campos dinâmicos do cadastro
│
├── templates/
│   ├── login.html         # Login e cadastro (modo="login" | "cadastro")
│   ├── startpage.html     # Dashboard (aluno, professor ou aguardando aprovação)
│   └── subpage.html       # Demais telas, escolhidas pela variável "modo"
│
├── src/
│   └── files/             # Arquivos enviados pelos alunos (ignorado pelo Git)
│
├── run.py                 # Ponto de entrada (porta 5234)
├── requirements.txt
├── tailwind.config.js     # Não usado: o Tailwind é carregado via CDN
├── .env                   # Não versionado
└── .gitignore
```

### Modos do `subpage.html`

| `modo` | Tela |
|---|---|
| `perfilaluno` | Perfil do aluno, com download e correção das atividades |
| `turma` | Alunos de uma turma |
| `atividades` | Atividades de uma matéria, envio de arquivo e entregas |
| `listaprofessores` | Solicitações de professores |
| `materias` | Matérias do aluno e formulário para entrar em outra |
| `submateria` | Média do aluno em uma matéria |

## Banco de dados

```mermaid
erDiagram
    TURMA ||--o{ USER : "agrupa"
    TURMA ||--o{ ATIVIDADE : "recebe"
    USER ||--o{ MATERIA : "cria (professor)"
    MATERIA ||--o{ ATIVIDADE : "contém"
    USER ||--o{ MATERIAS_REF : "matricula"
    MATERIA ||--o{ MATERIAS_REF : "referencia"
    USER ||--o{ DIRE_ALUNO : "entrega"
    ATIVIDADE ||--o{ DIRE_ALUNO : "recebe entregas"
```

### user

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | PK |
| name | String(80) | Obrigatório |
| username | String(80) | Único, obrigatório |
| turma_id | Integer | FK para `turma.id`. Nulo para professores |
| matricula | Integer | Único. Nulo para professores |
| password | String | Hash Werkzeug |
| is_teacher | Boolean | `False` por padrão. Vira `True` na aprovação |

### turma

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | PK |
| name | String(1) | Letra da turma (A, B) |
| curso | String(80) | Ex.: Meio Ambiente |
| serie | Integer | 1, 2 ou 3 |

### materia

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | PK. É o número que o aluno usa para entrar na matéria |
| materia_name | String(80) | Obrigatório |
| user_id | Integer | FK para `user.id`. Professor que criou a matéria |

### atividade

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | PK |
| name | String(80) | Título |
| descricao | String(200) | Obrigatório |
| data_fim | Date | Prazo de entrega |
| turma_id | Integer | FK para `turma.id` |
| materia_id | Integer | FK para `materia.id` |
| valor | Float | Pontuação da atividade |

### dire_aluno

Registra cada entrega de atividade.

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | PK. Também é o nome do arquivo salvo |
| id_aluno | Integer | FK para `user.id` |
| relacao_atividade | Integer | FK para `atividade.id` |
| status | String(40) | `pendente` (ao enviar) ou `corrigida` (após a correção) |
| atividade_nome | String(100) | Nome original do arquivo enviado. Usado no download |
| diretorio | String(100) | Caminho do arquivo no disco |
| nota | Float | Nota da entrega. Começa em `0` e muda na correção |

### materias_ref

Matrícula do aluno em uma matéria.

| Campo | Tipo | Observações |
|---|---|---|
| id | Integer | PK |
| id_user | Integer | FK para `user.id` |
| id_materia | Integer | FK para `materia.id` |

Entrar em uma matéria cria uma linha em `materias_ref`. Sair da matéria apaga essa linha.

### Como a média é calculada

- **Média geral (dashboard do aluno):** média simples das notas de todas as entregas do aluno em `dire_aluno`.
- **Média da matéria:** média simples das notas das entregas da matéria.
- Entregas ainda não corrigidas têm nota `0` e entram na conta.

## Rotas

Todas as rotas abaixo ficam no blueprint `pages`.

### Públicas

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Tela de login |
| `/cadastro` | GET | Tela de cadastro |
| `/login` | POST | Autentica o usuário |
| `/register` | POST | Cria usuário (e turma, se necessário) |

### Todos os usuários logados

| Rota | Método | Descrição |
|---|---|---|
| `/dashboard` | GET | Painel do aluno, do professor ou tela de espera |
| `/logout` | GET | Encerra a sessão |
| `/aluno/<student_id>` | GET | Perfil do aluno e suas atividades |

### Aluno

| Rota | Método | Descrição |
|---|---|---|
| `/materias` | GET | Matérias em que está matriculado |
| `/entrar_matéria` | POST | Matricula em uma matéria |
| `/logout_materia/<id>` | GET | Remove a matrícula |
| `/submateria/<materia_id>` | GET | Média da matéria |
| `/atividades/<materia_id>` | GET | Atividades da matéria na turma do aluno |
| `/update-files/<id_atividade>` | POST | Envia o arquivo da atividade |

### Professor

| Rota | Método | Descrição |
|---|---|---|
| `/turma/<classroom_id>` | GET | Alunos da turma |
| `/professores` | GET | Solicitações de novos professores |
| `/p_confirmar/<teacher_id>` | GET | Aprova professor |
| `/p_excluir/<teacher_id>` | GET | Exclui solicitação |
| `/criar-matéria` | POST | Cria matéria |
| `/excluir_materia/<id>` | POST | Exclui matéria (exige a senha do professor que a criou) |
| `/criar-atividade` | POST | Cria atividade para uma turma e matéria |
| `/download-files/<id_atividade>/<id_student>` | GET | Baixa a entrega do aluno |
| `/corrigir-atividade/<id_atividade>/<id_student>` | POST | Lança a nota e marca a entrega como `corrigida` |

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Ualter-Lab/SEA.git
cd SEA
```

### 2. Crie e ative o ambiente virtual

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

### 4. Crie a pasta de uploads

```bash
mkdir -p src/files
```

### 5. Configure o `.env`

Veja [Variáveis de ambiente](#variáveis-de-ambiente).

### 6. Execute

```bash
python run.py
```

As tabelas são criadas automaticamente na primeira execução. O sistema abre em:

```text
http://localhost:5234
```

### 7. Crie o primeiro professor

Todo professor novo precisa da aprovação de outro professor. O primeiro precisa ser promovido manualmente.

1. Cadastre-se em `/cadastro` com o curso "Professor".
2. Rode o script abaixo na raiz do projeto:

```python
from run import app
from backend import db
from backend.models import user

with app.app_context():
    u = user.query.filter_by(username="seu_usuario").first()
    u.is_teacher = True
    db.session.commit()
```

## Variáveis de ambiente

Crie o arquivo `.env` na raiz:

```env
KEY=sua_chave_secreta
DATABASE_URL=sqlite:///sea.db
FILES_PATH=src/files/
```

| Variável | Uso |
|---|---|
| `KEY` | Chave secreta das sessões do Flask |
| `DATABASE_URL` | String de conexão do SQLAlchemy |
| `FILES_PATH` | Pasta dos uploads. Deve terminar com `/` e a pasta precisa existir |

> O nome do arquivo é montado como `FILES_PATH` + id da entrega + extensão. Sem a barra final, o arquivo é salvo no lugar errado.

> Use um caminho relativo à raiz do projeto (`src/files/`). O download resolve o caminho a partir da raiz.

## Usando PostgreSQL

### 1. Instale o PostgreSQL

Baixe em [postgresql.org](https://www.postgresql.org/download/) e defina uma senha para o usuário `postgres`.

### 2. Crie o banco

```sql
CREATE DATABASE sea;
```

### 3. Ajuste o `.env`

```env
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/sea
```

### 4. Rode normalmente

```bash
python run.py
```

## Atualizando um banco existente

O projeto usa `db.create_all()`, sem migrações. Ele cria tabelas novas, mas não altera tabelas já existentes. Se o seu banco é anterior a estas mudanças, recrie o banco (apague o `sea.db` no SQLite) ou aplique as alterações manualmente:

- Nova tabela `materias_ref`, que substitui a antiga `notas` (sem as colunas `b1` a `b4`).
- Nova coluna `dire_aluno.atividade_nome`.
- Colunas `materia.user_id`, `atividade.materia_id` e `atividade.valor`.
- Tabela `dire_aluno`.

## Roadmap

- Corrigir o cálculo da média por matéria.
- Revisar permissões das rotas de professor.
- Migrações com Flask-Migrate.
- Recuperação de senha.
- Estatísticas mais completas no dashboard.

## Autor

Desenvolvido por Walter Neto.

GitHub: [Ualter-Lab](https://github.com/Ualter-Lab)
