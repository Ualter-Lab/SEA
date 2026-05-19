from flask import Flask, Blueprint, render_template, url_for, redirect, request, session
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from . import db
from .models import user, turma, atividade
from werkzeug.security import generate_password_hash, check_password_hash


pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def login():
    return render_template('login.html')

@pages_bp.route('/register')
def register():
    return render_template('register.html')

@pages_bp.route('/estudante')
@login_required
def index():
    return render_template('estudante.html')

@pages_bp.route('/professor')
@login_required
def professor():
    return render_template('professor.html')

@pages_bp.route('/cadastro', methods=['POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['name']
        username = request.form['username']
        curso = request.form['curso']
        serie = request.form['serie']
        turma = request.form['turma']
        matricula = request.form['matricula']
        password = request.form['password']


        if not serie or serie.strip() == '':
          turma = None

        if not turma or turma.strip() == '':
          turma = None

        if not matricula or matricula.strip() == '':
          matricula = None



        password_hashed = generate_password_hash(password)

        new_user = user(name=nome, username=username, curso=curso, serie=serie, turma=turma, matricula=matricula, password=password_hashed)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('pages.login'))