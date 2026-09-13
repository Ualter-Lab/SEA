from flask import Blueprint, render_template, url_for, redirect, request, flash  # type: ignore
from flask_login import current_user, login_user, logout_user, login_required  # type: ignore
from . import db
from .models import user, turma, materia, notas
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore

pages_bp = Blueprint("pages", __name__)

# Funções


# Rotas dos templates


@pages_bp.route("/")
def login():
    return render_template("login.html", modo="login")


@pages_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_teacher:
        turmas = turma.query.all()

        return render_template(
            "startpage.html",
            turmas=turmas,
            serie=None,
            curso=None,
            name_turma=None,
            media_b1=None,
            media_b2=None,
            media_b3=None,
            media_b4=None,
        )

    turma_user = turma.query.get(current_user.turma_id)
    if turma_user is not None:
        serie = turma_user.serie
        curso = turma_user.curso
        name_turma = turma_user.name
    else:
        serie = curso = name_turma = None

    array_notas = notas.query.filter_by(id_user=current_user.id).all()

    def media(valores):
        array_bi = [v for v in valores if v is not None]
        return sum(array_bi) / len(array_bi) if array_bi else 0

    mb1 = media([n.b1 for n in array_notas])
    mb2 = media([n.b2 for n in array_notas])
    mb3 = media([n.b3 for n in array_notas])
    mb4 = media([n.b4 for n in array_notas])

    return render_template(
        "startpage.html",
        serie=serie,
        curso=curso,
        name_turma=name_turma,
        media_b1=mb1,
        media_b2=mb2,
        media_b3=mb3,
        media_b4=mb4,
    )


@pages_bp.route("/cadastro")
def cadastro():
    return render_template("login.html", modo="cadastro")


@pages_bp.route("/aluno/<int:student_id>")
@login_required
def aluno(student_id):
    if current_user.is_teacher:
        return redirect(url_for("pages.dashboard"))

    # Procura do estudante
    student_url_id = user.query.get(student_id)

    # Procura dos dados do aluno
    name = student_url_id.name
    matricula = student_url_id.matricula

    classroom_student = turma.query.get(student_url_id.turma_id)
    serie = classroom_student.serie
    turma_name = classroom_student.name
    curso = classroom_student.curso

    # Atividades

    # Desempenho por Bimestre
    array_notas = notas.query.filter_by(id_user=student_id).all()

    def media(valores):
        array_bi = [v for v in valores if v is not None]
        return sum(array_bi) / len(array_bi) if array_bi else 0

    mb1 = media([n.b1 for n in array_notas])
    mb2 = media([n.b2 for n in array_notas])
    mb3 = media([n.b3 for n in array_notas])
    mb4 = media([n.b4 for n in array_notas])

    return render_template(
        "subpage.html",
        modo="perfilaluno",
        name=name,
        matricula=matricula,
        serie=serie,
        turma_name=turma_name,
        curso=curso,
        mb1=mb1,
        mb2=mb2,
        mb3=mb3,
        mb4=mb4,
    )


@pages_bp.route("/professores")
@login_required
def listadeprofessores():
    if not current_user.is_teacher:
        return redirect(url_for("pages.dashboard"))

    professores_array = user.query.filter_by(
        turma_id=None, matricula=None, is_teacher=False
    ).all()

    return render_template(
        "subpage.html", modo="listaprofessores", professores_array=professores_array
    )


@pages_bp.route("/atividades")
@login_required
def atividades():
    if current_user.is_teacher:
        return redirect(url_for("pages.dashboard"))

    render_template("atividade.html", modo="atividades"),
    url_for("pages.dashboard")


@pages_bp.route("/materias")
@login_required
def materias():
    if current_user.is_teacher:
        return redirect(url_for("pages.dashboard"))

    materia_ids = (
        db.session.query(notas.id_materia)
        .filter_by(id_user=current_user.id)
        .distinct()
        .all()
    )
    materia_ids = [m[0] for m in materia_ids]
    materias = materia.query.filter(materia.id.in_(materia_ids)).all()

    return render_template("subpage.html", modo="materias", materias=materias)


@pages_bp.route("/submateria/<int:materia_id>")
@login_required
def submateria(materia_id):
    if current_user.is_teacher:
        return redirect(url_for("pages.dashboard"))

    m = materia.query.get(materia_id)
    nome = m.materia_name

    notas_materia = notas.query.filter_by(id_materia=materia_id, id_user=current_user.id).first()

    b1 = notas_materia.b1 if notas_materia and notas_materia.b1 is not None else 0.0
    b2 = notas_materia.b2 if notas_materia and notas_materia.b2 is not None else 0.0
    b3 = notas_materia.b3 if notas_materia and notas_materia.b3 is not None else 0.0
    b4 = notas_materia.b4 if notas_materia and notas_materia.b4 is not None else 0.0

    return render_template("subpage.html", modo="submateria", nome=nome, materia_id = materia_id, b1=b1, b2=b2, b3=b3, b4=b4)


@pages_bp.route("/turma/<int:classroom_id>")
@login_required
def turma_list(classroom_id):
    if not current_user.is_teacher:
        return redirect(url_for("pages.dashboard"))

    users_classroom = user.query.filter_by(turma_id=classroom_id).all()
    turma_info = turma.query.get(classroom_id)

    return render_template(
        "subpage.html",
        modo="turma",
        users_classroom=users_classroom,
        turma_info=turma_info,
    )


# Rotas post / Rotas de ações


@pages_bp.route("/login", methods=["POST"])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for("pages.dashboard"))

    username = request.form["username"]
    password = request.form["password"]

    usuario = user.query.filter_by(username=username).first()

    if not usuario:
        flash("Usuário não encontrado", "error")
        return redirect(url_for("pages.login"))

    if not check_password_hash(usuario.password, password):
        flash("Senha incorreta", "error")
        return redirect(url_for("pages.login"))

    login_user(usuario)
    flash("Bem-vindo!", "success")

    return redirect(url_for("pages.dashboard"))


@pages_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("pages.login"))


@pages_bp.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    username = request.form["username"]
    curso = request.form["curso"]
    serie = request.form.get("serie")
    turma_valor = request.form.get("turma")
    matricula = request.form.get("matricula")
    password = request.form["password"]

    usuario_existente = user.query.filter_by(username=username).first()

    if usuario_existente:
        return url_for("pages.login", error="Esse usuário já existe")

    if not serie or serie.strip() == "":
        serie = None

    if not turma_valor or turma_valor.strip() == "":
        turma_valor = None

    if not matricula or matricula.strip() == "":
        matricula = None

    password_hashed = generate_password_hash(password)

    turma_ref = None
    if serie and turma_valor:
        turma_ref = turma.query.filter_by(
            curso=curso, serie=serie, name=turma_valor
        ).first()
        if not turma_ref:
            turma_ref = turma(curso=curso, serie=serie, name=turma_valor)
            db.session.add(turma_ref)
            db.session.flush()

    new_user = user(
        name=name,
        username=username,
        turma_id=turma_ref.id if turma_ref else None,
        matricula=matricula,
        password=password_hashed,
    )

    db.session.add(new_user)
    db.session.commit()

    flash("Cadastro realizado com sucesso!", "success")
    return redirect(url_for("pages.login"))


@pages_bp.route("/criar-matéria", methods=["POST"])
@login_required
def criar_materia():
    materia_name = request.form["materia"]

    new_materia = materia(materia_name=materia_name)

    db.session.add(new_materia)
    db.session.commit()

    flash("Matéria registrada com sucesso!", "sucesso")
    return redirect(url_for("pages.dashboard"))


@pages_bp.route("/entrar_matéria", methods=["POST"])
@login_required
def entrar_materia():
    id_materia = request.form["id_materia"]

    user_id = current_user.id

    new_nota = notas(
        id_user=user_id, id_materia=id_materia, b1=None, b2=None, b3=None, b4=None
    )

    db.session.add(new_nota)
    db.session.commit()

    flash("Matéria entrada com sucesso!", "sucesso")
    return redirect(url_for("pages.materias"))


@pages_bp.route("/logout_materia/<int:materia_id>")
@login_required
def logout_materia(materia_id):
    nota = notas.query.filter_by(id_user=current_user.id, id_materia=materia_id).first()

    if nota:
        db.session.delete(nota)
        db.session.commit()

    return redirect(url_for("pages.materias"))


@pages_bp.route("/p_confirmar/<int:teacher_id>")
@login_required
def confirmar_professor(teacher_id):
    user_teacher = user.query.get(teacher_id)

    if user_teacher:
        user_teacher.is_teacher = True
        db.session.commit()

    return redirect(url_for("pages.listadeprofessores"))
