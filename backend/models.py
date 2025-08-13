# backend/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import date, time

db = SQLAlchemy()

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(150), unique=True)

class Medico(db.Model):
    __tablename__ = 'medicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)

class Consultorio(db.Model):
    __tablename__ = 'consultorios'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False)
    piso = db.Column(db.Integer, nullable=False)

class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    consultorio = db.Column(db.String(50))

    paciente = db.relationship('Paciente', backref=db.backref('citas', cascade="all,delete"))
    medico = db.relationship('Medico', backref=db.backref('citas', cascade="all,delete"))
