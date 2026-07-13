from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from . import db
from .models import user
from werkzeug.security import generate_password_hash, check_password_hash


pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def login():
    return render_template('login.html')

@pages_bp.route('/dashboard')
def dashboard():
    return render_template('startpage.html')

@pages_bp.route('/register')
def register():
    return render_template('register.html')


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

@pages_bp.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form['name']
    username = request.form['username']
    curso = request.form['curso']
    serie = request.form.get('serie')
    turma_valor = request.form.get('turma')
    matricula = request.form.get('matricula')
    password = request.form['password']

    usuario_existente = user.query.filter_by(username=username).first()

    if usuario_existente:
        return render_template('register.html', error="Esse usuário já existe")

    if not serie or serie.strip() == '':
        serie = None

    if not turma_valor or turma_valor.strip() == '':
        turma_valor = None

    if not matricula or matricula.strip() == '':
        matricula = None

    password_hashed = generate_password_hash(password)

    new_user = user(
        name=nome,
        username=username,
        curso=curso,
        serie=serie,
        turma=turma_valor,
        matricula=matricula,
        password=password_hashed
    )

    db.session.add(new_user)
    db.session.commit()

    flash("Cadastro realizado com sucesso!", "success")
    return redirect(url_for('pages.login'))