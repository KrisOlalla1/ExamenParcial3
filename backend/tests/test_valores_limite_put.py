import pytest
import sys
import os
from flask import json
from datetime import date, timedelta

# Agregar ruta del proyecto
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


# Función auxiliar para crear un paciente válido
def crear_paciente(client):
    resp = client.post('/api/pacientes', json={
        "nombre": "Paciente Test",
        "apellido": "Apellido Test",
        "fecha_nacimiento": "2000-01-01",
        "email": "paciente@example.com"  # ← agregado para pasar la validación
    })
    assert resp.status_code == 201
    return json.loads(resp.data)['id']


# Función auxiliar para crear una cita válida
def crear_cita(client):
    paciente_id = crear_paciente(client)
    resp_med = client.post('/api/medicos', json={
        "nombre": "Medico Test",
        "apellido": "Apellido Medico"
    })
    assert resp_med.status_code == 201
    medico_id = json.loads(resp_med.data)['id']

    resp_cita = client.post('/api/citas', json={
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "fecha": date.today().isoformat(),
        "hora": "10:00:00"
    })
    assert resp_cita.status_code == 201
    return json.loads(resp_cita.data)['id']


# Test de fecha_nacimiento en límites
def test_fecha_nacimiento_valores_limite(client):
    paciente_id = crear_paciente(client)

    # Fecha mínima válida
    resp = client.put(f'/api/pacientes/{paciente_id}', json={"fecha_nacimiento": "1900-01-01"})
    assert resp.status_code == 200

    # Fecha máxima válida (hoy)
    hoy = date.today().isoformat()
    resp = client.put(f'/api/pacientes/{paciente_id}', json={"fecha_nacimiento": hoy})
    assert resp.status_code == 200

    # Fecha inválida: anterior al mínimo
    resp = client.put(f'/api/pacientes/{paciente_id}', json={"fecha_nacimiento": "1899-12-31"})
    assert resp.status_code == 400

    # Fecha inválida: futura
    futura = (date.today() + timedelta(days=1)).isoformat()
    resp = client.put(f'/api/pacientes/{paciente_id}', json={"fecha_nacimiento": futura})
    assert resp.status_code == 400


# Test de hora de cita en límites
def test_hora_cita_valores_limite(client):
    cita_id = crear_cita(client)
    hoy = date.today().isoformat()

    # Hora mínima válida
    resp = client.put(f'/api/citas/{cita_id}', json={"fecha": hoy, "hora": "00:00:00"})
    assert resp.status_code == 200

    # Hora máxima válida
    resp = client.put(f'/api/citas/{cita_id}', json={"fecha": hoy, "hora": "23:59:59"})
    assert resp.status_code == 200

    # Hora inválida: negativa
    resp = client.put(f'/api/citas/{cita_id}', json={"fecha": hoy, "hora": "-01:00:00"})
    assert resp.status_code == 400

    # Hora inválida: fuera de rango
    resp = client.put(f'/api/citas/{cita_id}', json={"fecha": hoy, "hora": "24:00:00"})
    assert resp.status_code == 400
