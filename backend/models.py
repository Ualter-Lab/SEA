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
    name = db.Column(db.Integer, nullable=False)
    curso = db.Column(db.String(80), nullable=False)
    serie = db.Column(db.String(80), nullable=False)

class materia(db.Model):
    __tablename__ = 'materia'
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(80), nullable=False)

class atividade(db.Model):
    __tablename__ = 'atividade'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)

class notas(db.Model):
    __tablename__ = 'notas'
    id = db.Column(db.Interger, primary_key=True)
    id_aluno = db.Column(db.Interger, db.ForeingKey("user.id"), nullable=False )
    id_materia = db.Column(db.Interger, db.ForeingKey("materia.id"), nullable=False)
    b1 = db.Column(db.Float)
    b2 = db.Column(db.Float)
    b3 = db.Column(db.Float)
    b4 = db.Column(db.Float)