from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from . import db

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(80), nullable=False)
    curso = db.Column(db.String(80), nullable=False)
    serie = db.Column(db.String(80), nullable=False)
    matricula = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curso = db.Column(db.String(80), nullable=False)
    serie = db.Column(db.String(80), nullable=False)

class atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)