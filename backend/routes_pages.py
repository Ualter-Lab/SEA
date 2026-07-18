from flask import Blueprint, render_template, url_for, redirect, request, flash # type: ignore
from flask_login import current_user, login_user, logout_user, login_required # type: ignore
from . import db
from .models import user, turma
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
    return render_template('startpage.html')

@pages_bp.route('/cadastro')
def cadastro():
    return render_template('login.html', modo="cadastro")

@pages_bp.route('/turmas')
@login_required
def turma():
    check_teacher(render_template('turma.html'), url_for('/dashboard'), True)

@pages_bp.route('/aluno')
@login_required
def aluno():
    check_teacher(render_template('aluno.html'), url_for('/dashboard'), True)

@pages_bp.route('/atividades')
@login_required
def atividades():
    check_teacher(render_template('atividade.html'), url_for('/dashboard'), True)

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
    nome = request.form['name']
    username = request.form['username']
    curso = request.form['curso']
    serie = request.form.get('serie')
    turma_valor = request.form.get('turma')
    matricula = request.form.get('matricula')
    password = request.form['password']

    usuario_existente = user.query.filter_by(username=username).first()

    if usuario_existente:
        return render_template('pages.login', error="Esse usuário já existe")

    if not serie or serie.strip() == '':
        serie = None

    if not turma_valor or turma_valor.strip() == '':
        turma_valor = None

    if not matricula or matricula.strip() == '':
        matricula = None

    password_hashed = generate_password_hash(password)

    turma_ref = None
    if serie and turma_valor:
        turma_ref = turma.query.filter_by(curso=curso, serie=serie, nome=turma_valor).first()
        if not turma_ref:
            turma_ref = turma(curso=curso, serie=serie, nome=turma_valor)
            db.session.add(turma_ref)
            db.session.flush()

    new_user = user(
        name=nome,
        username=username,
        curso=curso,
        turma_id=turma_ref.id if turma_ref else None,
        matricula=matricula,
        password=password_hashed
    )

    db.session.add(new_user)
    db.session.commit()

    flash("Cadastro realizado com sucesso!", "success")
    return redirect(url_for('pages.login'))