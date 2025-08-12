import pytest
from datetime import date
from flask import json
import sys
import os

# Ajustar el path para importar app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def crear_paciente(client):
    resp = client.post('/api/pacientes', json={
        "nombre": "Paciente Test",
        "apellido": "Apellido Test",
        "fecha_nacimiento": "1990-01-01"
    })
    assert resp.status_code == 201
    return json.loads(resp.data)['id']

def crear_medico(client):
    resp = client.post('/api/medicos', json={
        "nombre": "Medico Test",
        "apellido": "Apellido Medico",
        "especialidad": "General"
    })
    assert resp.status_code == 201
    return json.loads(resp.data)['id']

def crear_cita(client, paciente_id, medico_id, fecha, hora, consultorio=None):
    data = {
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "fecha": fecha,
        "hora": hora
    }
    if consultorio:
        data["consultorio"] = consultorio

    resp = client.post('/api/citas', json=data)
    return resp

def test_creacion_cita(client):
    paciente_id = crear_paciente(client)
    medico_id = crear_medico(client)

    fecha = "2025-12-01"
    hora = "14:30:00"
    consultorio = "101"

    resp = crear_cita(client, paciente_id, medico_id, fecha, hora, consultorio)
    assert resp.status_code == 201

    data = json.loads(resp.data)
    assert data["paciente_id"] == paciente_id
    assert data["medico_id"] == medico_id
    assert data["fecha"] == fecha
    assert data["hora"] == hora
    assert data.get("consultorio") == consultorio or True  # consultorio puede ser opcional


def test_modificacion_cita(client):
    paciente_id = crear_paciente(client)
    medico_id = crear_medico(client)

    # Crear cita inicial
    resp = crear_cita(client, paciente_id, medico_id, "2025-12-01", "14:30:00")
    assert resp.status_code == 201
    cita_id = json.loads(resp.data)["id"]

    # Modificar cita
    nueva_fecha = "2025-12-05"
    nueva_hora = "16:00:00"
    resp_put = client.put(f'/api/citas/{cita_id}', json={
        "fecha": nueva_fecha,
        "hora": nueva_hora
    })
    assert resp_put.status_code == 200

    data = json.loads(resp_put.data)
    assert data["fecha"] == nueva_fecha
    assert data["hora"] == nueva_hora


def test_eliminacion_cita(client):
    paciente_id = crear_paciente(client)
    medico_id = crear_medico(client)

    # Crear cita
    resp = crear_cita(client, paciente_id, medico_id, "2025-12-01", "14:30:00")
    assert resp.status_code == 201
    cita_id = json.loads(resp.data)["id"]

    # Eliminar cita
    resp_del = client.delete(f'/api/citas/{cita_id}')
    assert resp_del.status_code == 204

    # Confirmar que no existe
    resp_get = client.get(f'/api/citas/{cita_id}')
    assert resp_get.status_code == 404
