from flask import Blueprint, render_template, url_for, redirect, request, flash, send_file  # type: ignore
from flask_login import current_user, login_user, logout_user, login_required  # type: ignore
from . import db
from .models import user, turma, materia, materias_ref, atividade, dire_aluno
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import os

pages_bp = Blueprint("pages", __name__)

FILES_PATH = os.getenv("FILES_PATH")

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
        materia_array = materia.query.all()

        return render_template(
            "startpage.html",
            turmas=turmas,
            materia_array=materia_array,
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

    array_notas = dire_aluno.query.filter_by(id_aluno=current_user.id).all()

    sum_notas = sum(n.nota for n in array_notas if n.nota is not None)

    len_notas = dire_aluno.query.filter_by(id_aluno=current_user.id).count()

    nota_final = sum_notas / len_notas if len_notas > 0 else 0
    nota_formatada = f"{nota_final:.2f}".replace(".", ",")


    return render_template(
        "startpage.html",
        serie=serie,
        curso=curso,
        name_turma=name_turma,
        nota_final=nota_final,
        nota_formatada=nota_formatada
    )


@pages_bp.route("/cadastro")
def cadastro():
    return render_template("login.html", modo="cadastro")


@pages_bp.route("/aluno/<int:student_id>")
@login_required
def aluno(student_id):
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
    student_url_id = user.query.get_or_404(student_id)

    atividades_pendente = dire_aluno.query.join(
        atividade, dire_aluno.relacao_atividade == atividade.id
    ).join(
        materia, atividade.materia_id == materia.id
    ).filter(
        dire_aluno.id_aluno == student_id,
        dire_aluno.status == "pendente",
        materia.user_id == current_user.id
    ).all()

    atividades_corrigida = dire_aluno.query.join(
        atividade, dire_aluno.relacao_atividade == atividade.id
    ).join(
        materia, atividade.materia_id == materia.id
    ).filter(
        dire_aluno.id_aluno == student_id,
        dire_aluno.status == "corrigida",
        materia.user_id == current_user.id
    ).all()

    atividade_turma = atividade.query.join(
        materia, atividade.materia_id == materia.id
    ).filter(
        atividade.turma_id == student_url_id.turma_id,
        materia.user_id == current_user.id
    ).first()

    return render_template(
        "subpage.html",
        modo="perfilaluno",
        student_id=student_id,
        name=name,
        matricula=matricula,
        serie=serie,
        turma_name=turma_name,
        curso=curso,
        atividades_pendente=atividades_pendente,
        atividades_corrigida=atividades_corrigida,
        atividade_turma=atividade_turma

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

@pages_bp.route("/atividades/<int:materia_id>")
@login_required
def atividades(materia_id):
    if current_user.is_teacher:
        return redirect(url_for("pages.dashboard"))

    turma_id_user = current_user.turma_id

    atividades_array = atividade.query.filter_by(
        turma_id=turma_id_user,
        materia_id=materia_id
    ).all()

    atividade_entregue_array = dire_aluno.query.filter_by(
        id_aluno=current_user.id
    ).all()

    id_atividade_entregue_array = [
        e.relacao_atividade.id
        if hasattr(e.relacao_atividade, "id")
        else int(e.relacao_atividade)
        for e in atividade_entregue_array
    ]

    atividades_pendentes = [
        a for a in atividades_array
        if a.id not in id_atividade_entregue_array
    ]

    return render_template(
        "subpage.html",
        modo="atividades",
        atividades_array=atividades_array,
        id_atividade_entregue_array=id_atividade_entregue_array,
        atividade_entregue_array=atividade_entregue_array,
        atividades_pendentes=atividades_pendentes
    )

@pages_bp.route("/materias")
@login_required
def materias():
    if current_user.is_teacher:
        return redirect(url_for("pages.dashboard"))

    materia_ids = (
        db.session.query(materias_ref.id_materia)
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

    nota_materia = dire_aluno.query.filter_by(id_aluno=current_user.id, relacao_atividade=materia_id).all()

    sum_nota_materia = sum(n.nota for n in nota_materia if n.nota is not None)

    len_nota_materia = dire_aluno.query.filter_by(id_aluno=current_user.id, relacao_atividade=materia_id).count()

    nota_materia = sum_nota_materia / len_nota_materia if len_nota_materia > 0 else 0
    nota_materia = round(nota_materia, 2)
    nota_formatada = f"{nota_materia:.2f}".replace(".", ",")

    return render_template("subpage.html", modo="submateria", nome=nome, materia_id=materia_id, 
    nota_materia=nota_materia, nota_formatada=nota_formatada)


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
        flash("Usuário não encontrado", "erro")
        return redirect(url_for("pages.login"))

    if not check_password_hash(usuario.password, password):
        flash("Senha incorreta", "erro")
        return redirect(url_for("pages.login"))

    login_user(usuario)
    flash("Bem-vindo!", "sucesso")

    return redirect(url_for("pages.dashboard"))


@pages_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "sucesso")
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
        flash("Esse usuário já existe", "erro")
        return redirect(url_for("pages.login"))

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

    flash("Cadastro realizado com sucesso!", "sucesso")
    return redirect(url_for("pages.login"))


@pages_bp.route("/criar-matéria", methods=["POST"])
@login_required
def criar_materia():
    materia_name = request.form["materia"]
    user_id = current_user.id

    materia_obj = materia.query.filter_by(materia_name=materia_name).first()

    if materia_obj:
        flash("Essa matéria já existe!", "erro")
        return redirect(url_for("pages.dashboard"))

    new_materia = materia(materia_name=materia_name, user_id = user_id)

    db.session.add(new_materia)
    db.session.commit()

    flash("Matéria registrada com sucesso!", "sucesso")
    return redirect(url_for("pages.dashboard"))

@pages_bp.route("/excluir_materia/<int:id>", methods=["POST"])
@login_required
def excluir_materia(id):
    materia_obj = materia.query.get(id)
    id_teacher = materia_obj.user_id
    teacher = user.query.get(id_teacher)
    password_hash = teacher.password
    password = request.form["password_teacher"]

    atividade_obj = atividade.query.filter_by(materia_id=id).first()

    if atividade_obj:
        flash("Não é possível remover a matéria, pois existem atividades associadas a ela.", "erro")
        return redirect(url_for("pages.dashboard"))


    if check_password_hash(password_hash, password) and materia_obj:
        db.session.delete(materia_obj)
        db.session.commit()
        flash("Matéria removida com sucesso!", "sucesso")
        return redirect(url_for("pages.dashboard"))
    else:
        flash("Erro ao remover matéria!", "erro")
        return redirect(url_for("pages.dashboard"))


@pages_bp.route("/entrar_matéria", methods=["POST"])
@login_required
def entrar_materia():
    id_materia = request.form["id_materia"]

    user_id = current_user.id

    new_materias_ref = materias_ref(
        id_user=user_id, id_materia=id_materia
    )

    db.session.add(new_materias_ref)
    db.session.commit()

    flash("Matéria entrada com sucesso!", "sucesso")
    return redirect(url_for("pages.materias"))


@pages_bp.route("/logout_materia/<int:materia_id>")
@login_required
def logout_materia(materia_id):
    materia_ref = materias_ref.query.filter_by(id_user=current_user.id, id_materia=materia_id).first()

    if materia_ref:
        db.session.delete(materia_ref)
        db.session.commit()

    flash("Matéria removida com sucesso!", "sucesso")
    return redirect(url_for("pages.materias"))


@pages_bp.route("/p_confirmar/<int:teacher_id>")
@login_required
def confirmar_professor(teacher_id):
    user_teacher = user.query.get(teacher_id)

    if user_teacher:
        user_teacher.is_teacher = True
        db.session.commit()

    flash("Professor confirmado com sucesso!", "sucesso")
    return redirect(url_for("pages.listadeprofessores"))

@pages_bp.route("/p_excluir/<int:teacher_id>")
def excluir_teacher(teacher_id):
    user_teacher = user.query.get(teacher_id)

    if user_teacher:
        db.session.delete(user_teacher)
        db.session.commit()
        flash("Professor excluído com sucesso!", "sucesso")
        return redirect(url_for("pages.listadeprofessores"))
    else:
        return redirect(url_for("pages.listadeprofessores"))

@pages_bp.route("/criar-atividade", methods=["POST"])
@login_required
def criar_atividade():
    name = request.form["titulo"]
    descricao = request.form["descricao"]
    data_fim = request.form["data_entrega"]
    turma = request.form["turma"]
    valor = request.form["valor"]
    materia_id = request.form["materia_id"]

    atividade_ref = atividade(name=name, descricao=descricao, data_fim=data_fim, turma_id=turma, materia_id=materia_id, valor=valor)
    materia_obj = materia.query.get(materia_id)

    if not materia_obj:
        return "Matéria não encontrada", 404
    elif current_user.is_teacher:
        db.session.add(atividade_ref)
        db.session.commit()
        flash("Atividade criada com sucesso!", "sucesso")
        return redirect(url_for("pages.dashboard"))
    else:
        flash("Você não tem permissão para criar atividades.", "erro")
        return redirect(url_for("pages.dashboard"))

@pages_bp.route("/update-files/<int:id_atividade>", methods=["POST"])
@login_required
def update_files(id_atividade):
    atividade_obj = atividade.query.get(id_atividade)
    materia_id = atividade_obj.materia_id
    

    file = request.files.get('arquivo')
    atividade_name = file.filename

    if not file or file.filename == '':
        return "Nenhum arquivo encontrado", 400

    ref_dire_aluno = dire_aluno(id_aluno = current_user.id,
    status = "pendente",
    atividade_nome = atividade_name,
    relacao_atividade = id_atividade,
    nota = 0)

    db.session.add(ref_dire_aluno)
    db.session.flush()

    extensao = os.path.splitext(file.filename)[1]

    ref_dire_aluno.diretorio = os.path.join(f"{FILES_PATH}{ref_dire_aluno.id}{extensao}")

    file.save(ref_dire_aluno.diretorio)

    db.session.commit()  
    flash("Atividade enviada com sucesso!", "sucesso")
    return redirect(url_for("pages.atividades", materia_id=materia_id))

@pages_bp.route("/download-files/<int:id_atividade>/<int:id_student>", methods=["GET"])
@login_required
def download_files(id_atividade, id_student):
    atividade_ref = dire_aluno.query.filter_by(relacao_atividade = id_atividade, id_aluno = id_student).first()

    caminho = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", atividade_ref.diretorio)
)

    return send_file(
        caminho,
        as_attachment=True,
        download_name=atividade_ref.atividade_nome
    )

@pages_bp.route("/corrigir-atividade/<int:id_atividade>/<int:id_student>", methods=["POST"])
@login_required
def corrigir_atividade(id_atividade, id_student):
    atividade_ref = dire_aluno.query.filter_by(relacao_atividade = id_atividade, id_aluno = id_student).first()

    nota = float(request.form.get("nota", "").strip().replace(",", "."))

    atividade_ref.nota = nota
    atividade_ref.status = "corrigida"

    db.session.commit()

    flash("Atividade corrigida com sucesso!", "sucesso")
    return redirect(url_for("pages.aluno", student_id=id_student))

@pages_bp.route("/revisar/atividade/<int:id_atividade>/<int:id_student>", methods=["POST"])
@login_required
def revisar_atividade(id_atividade, id_student):
    atividade_ref = dire_aluno.query.filter_by(relacao_atividade = id_atividade, id_aluno = id_student).first()

    atividade_ref.status = "pendente"

    db.session.commit()

    flash("Atividade revisada com sucesso!", "sucesso")
    return redirect(url_for("pages.aluno", student_id=id_student))