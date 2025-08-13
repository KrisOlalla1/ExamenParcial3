# tests/test_integracion.py
import sys
import os

# Agregar la carpeta "backend" al path para importar app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from app import create_app, db
from flask import json
import pytest

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()

def test_integracion_pacientes_medicos_citas(client):
    # Crear paciente
    resp_paciente = client.post("/api/pacientes", json={
        "nombre": "Juan",
        "apellido": "Perez",
        "fecha_nacimiento": "1990-05-01",
        "email": "juan@example.com"
    })
    assert resp_paciente.status_code == 201
    paciente_id = resp_paciente.get_json()["id"]

    # Crear médico
    resp_medico = client.post("/api/medicos", json={
        "nombre": "Ana",
        "apellido": "Lopez",
        "especialidad": "Cardiología"
    })
    assert resp_medico.status_code == 201
    medico_id = resp_medico.get_json()["id"]

    # Crear cita
    resp_cita = client.post("/api/citas", json={
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "fecha": "2025-08-15",
        "hora": "10:30:00",
        "consultorio": "101"
    })
    assert resp_cita.status_code == 201
    cita_id = resp_cita.get_json()["id"]

    # Obtener cita y validar datos
    resp_get_cita = client.get(f"/api/citas/{cita_id}")
    assert resp_get_cita.status_code == 200
    cita = resp_get_cita.get_json()
    assert cita["paciente_id"] == paciente_id
    assert cita["medico_id"] == medico_id
    assert cita["fecha"] == "2025-08-15"
    assert cita["hora"] == "10:30:00"

def test_cita_con_paciente_inexistente(client):
    # Crear médico válido
    resp_medico = client.post("/api/medicos", json={
        "nombre": "Carlos",
        "apellido": "Ruiz",
        "especialidad": "Neurología"
    })
    medico_id = resp_medico.get_json()["id"]

    # Intentar crear cita con paciente inexistente
    resp_cita = client.post("/api/citas", json={
        "paciente_id": 9999,
        "medico_id": medico_id,
        "fecha": "2025-08-20",
        "hora": "11:00:00",
        "consultorio": "102"
    })
    assert resp_cita.status_code == 400
    assert "Paciente no existe" in resp_cita.get_data(as_text=True)

def test_cita_con_medico_inexistente(client):
    # Crear paciente válido
    resp_paciente = client.post("/api/pacientes", json={
        "nombre": "Laura",
        "apellido": "Martinez",
        "fecha_nacimiento": "1987-09-09",
        "email": "laura@example.com"
    })
    paciente_id = resp_paciente.get_json()["id"]

    # Intentar crear cita con médico inexistente
    resp_cita = client.post("/api/citas", json={
        "paciente_id": paciente_id,
        "medico_id": 9999,
        "fecha": "2025-08-22",
        "hora": "09:00:00",
        "consultorio": "103"
    })
    assert resp_cita.status_code == 400
    assert "Medico no existe" in resp_cita.get_data(as_text=True)
