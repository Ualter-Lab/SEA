from flask import Flask, redirect, url_for # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import UserMixin # type: ignore
from . import db

class user(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"))
    matricula = db.Column(db.Integer, unique=True)
    password = db.Column(db.String, nullable=False) 
    is_teacher = db.Column(db.Boolean, default=False, nullable=False)

class turma(db.Model):
    __tablename__ = 'turma'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1), nullable=False)
    curso = db.Column(db.String(80), nullable=False)
    serie = db.Column(db.Integer, nullable=False)

class materia(db.Model):
    __tablename__ = 'materia'
    id = db.Column(db.Integer, primary_key=True)
    materia_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("user", backref="materias")

class atividade(db.Model):
    __tablename__ = 'atividade'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)
    valor = db.Column(db.Float)

class dire_aluno(db.Model):
    __tablename__ = 'dire_aluno'
    id = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(40))
    atividade_nome = db.Column(db.String(100), nullable=True)
    diretorio = db.Column(db.String(100), nullable=True)
    relacao_atividade = db.Column(db.Integer, db.ForeignKey('atividade.id'), nullable=False)
    nota = db.Column(db.Float)
    atividade_ref = db.relationship("atividade")


class materias_ref(db.Model):
    __tablename__ = 'materias_ref'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False )
    id_materia = db.Column(db.Integer, db.ForeignKey("materia.id"), nullable=False)