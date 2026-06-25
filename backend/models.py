from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db

class user(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    curso = db.Column(db.String(80), nullable=False)
    serie = db.Column(db.String(80))
    turma = db.Column(db.String(80))
    matricula = db.Column(db.String(80), unique=True)
    password = db.Column(db.String, nullable=False)

class turma(db.Model):
    __tablename__ = 'turma'
    id = db.Column(db.Integer, primary_key=True)
    curso = db.Column(db.String(80), nullable=False)
    serie = db.Column(db.String(80), nullable=False)

class atividade(db.Model):
    __tablename__ = 'atividade'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)