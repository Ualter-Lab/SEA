from flask import Blueprint, render_template, url_for, redirect, request, flash # type: ignore
from flask_login import current_user, login_user, logout_user, login_required # type: ignore
from . import db
from .models import user, turma, materia, notas
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore


pages_bp = Blueprint('pages', __name__)

#Funções

def check_teacher(rota1, rota2, TrueOrFalse):
    if current_user.is_teacher == TrueOrFalse:
        return rota1
    else:
        return rota2

#Rotas dos templates

@pages_bp.route('/')
def login():
    return render_template('login.html', modo="login")

@pages_bp.route('/dashboard')
@login_required
def dashboard():

    if not current_user.is_teacher:
      turma_user_id = current_user.turma_id
      turma_user = turma.query.get_or_404(turma_user_id)
      
      serie = turma_user.serie
      curso = turma_user.curso
      name_turma = turma_user.name
    else:
        serie = None
        curso = None
        name_turma = None

    return render_template('startpage.html',
                           serie = serie,
                           curso = curso,
                           name_turma = name_turma
                           )

@pages_bp.route('/cadastro')
def cadastro():
    return render_template('login.html', modo="cadastro")

@pages_bp.route('/turmas')
@login_required
def turma_page():
    return check_teacher(render_template('subpage.html', modo="turma"), url_for('pages.dashboard'), True)

@pages_bp.route('/aluno')
@login_required
def aluno():
    return check_teacher(render_template('subpage.html', modo="perfilaluno"), url_for('/dashboard'), True)

@pages_bp.route('/professores')
@login_required
def perfilprofessores():
    return check_teacher(render_template('subpage.html', modo="listaprofessores"), url_for('/dashboard'), True)

@pages_bp.route('/atividades')
@login_required
def atividades():
    return check_teacher(render_template('atividade.html', modo="atividades"), url_for('/dashboard'), False)

@pages_bp.route('/materias')
@login_required
def materias():
    materia_ids = db.session.query(notas.id_materia). filter_by(id_user = current_user.id).distinct().all()
    materia_ids = [m[0] for m in materia_ids]
    materias = materia.query.filter(materia.id.in_(materia_ids)).all()

    return check_teacher(render_template('subpage.html', modo="materias", materias=materias), url_for('pages.dashboard'), False)

@pages_bp.route('/submateria')
@login_required
def submateria():
    return check_teacher(render_template('subpage.html', modo="submateria"), url_for('pages.dashboard'), False)

#Rotas post / Rotas de ações

@pages_bp.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('pages.dashboard'))

    username = request.form['username']
    password = request.form['password']

    usuario = user.query.filter_by(username=username).first()

    if not usuario:
        flash("Usuário não encontrado", "error")
        return redirect(url_for('pages.login'))

    if not check_password_hash(usuario.password, password):
        flash("Senha incorreta", "error")
        return redirect(url_for("pages.login"))

    login_user(usuario)
    flash("Bem-vindo!", "success")

    return redirect(url_for('pages.dashboard'))

@pages_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for('pages.login'))

@pages_bp.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    username = request.form['username']
    curso = request.form['curso']
    serie = request.form.get('serie')
    turma_valor = request.form.get('turma')
    matricula = request.form.get('matricula')
    password = request.form['password']

    usuario_existente = user.query.filter_by(username=username).first()

    if usuario_existente:
        return url_for('pages.login', error="Esse usuário já existe")

    if not serie or serie.strip() == '':
        serie = None

    if not turma_valor or turma_valor.strip() == '':
        turma_valor = None

    if not matricula or matricula.strip() == '':
        matricula = None

    password_hashed = generate_password_hash(password)

    turma_ref = None
    if serie and turma_valor:
        turma_ref = turma.query.filter_by(curso=curso, serie=serie, name=turma_valor).first()
        if not turma_ref:
            turma_ref = turma(curso=curso, serie=serie, name=turma_valor)
            db.session.add(turma_ref)
            db.session.flush()

    new_user = user(
        name=name,
        username=username,
        turma_id=turma_ref.id if turma_ref else None,
        matricula=matricula,
        password=password_hashed
    )

    db.session.add(new_user)
    db.session.commit()

    flash("Cadastro realizado com sucesso!", "success")
    return redirect(url_for('pages.login'))

@pages_bp.route('/criar-matéria', methods=['POST'])
@login_required
def criar_materia():
    materia_name = request.form['materia']

    new_materia = materia(
        materia_name = materia_name
    )

    db.session.add(new_materia)
    db.session.commit()

    flash("Matéria registrada com sucesso!", "sucesso")
    return redirect(url_for('pages.dashboard'))

@pages_bp.route('/entrar_matéria', methods=['POST'])
@login_required
def entrar_materia():
    id_materia = request.form['id_materia']

    user_id= current_user.id

    new_nota = notas(
        id_user = user_id,
        id_materia = id_materia,
        b1 = None,
        b2 = None,
        b3 = None,
        b4 = None
    )

    db.session.add(new_nota)
    db.session.commit()

    flash("Matéria entrada com sucesso!", "sucesso")
    return redirect(url_for('pages.materias'))

@pages_bp.route('/logout_materia/<int:id>')
@login_required
def logout_materia(id):
    nota = notas.query.filter_by(id_user = current_user.id, id_materia = id).first()

    if nota:
        db.session.delete(nota)
        db.session.commit()
    
    return redirect(url_for('pages.materias'))