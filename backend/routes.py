from flask import Blueprint, request, jsonify
from datetime import datetime, date, time
from app import db
from models import Paciente, Medico, Cita

bp = Blueprint("api", __name__)

# Helpers para parsear fechas y horas
def parse_date(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

def parse_time(hora_str):
    try:
        return datetime.strptime(hora_str, "%H:%M:%S").time()
    except (ValueError, TypeError):
        return None


# -------------------- PACIENTES --------------------
@bp.route("/pacientes", methods=["POST"])
def create_paciente():
    data = request.get_json()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    fecha_nacimiento_str = data.get("fecha_nacimiento")

    if not nombre or not apellido or not fecha_nacimiento_str:
        return jsonify({"error": "Nombre, apellido y fecha_nacimiento son requeridos"}), 400

    fecha_nacimiento = parse_date(fecha_nacimiento_str)
    if not fecha_nacimiento:
        return jsonify({"error": "Formato de fecha inválido. Debe ser YYYY-MM-DD"}), 400

    if fecha_nacimiento < date(1900, 1, 1) or fecha_nacimiento > date.today():
        return jsonify({"error": "Fecha de nacimiento fuera de rango"}), 400

    paciente = Paciente(nombre=nombre, apellido=apellido, fecha_nacimiento=fecha_nacimiento)
    db.session.add(paciente)
    db.session.commit()

    return jsonify({
        "id": paciente.id,
        "nombre": paciente.nombre,
        "apellido": paciente.apellido,
        "fecha_nacimiento": paciente.fecha_nacimiento.isoformat()
    }), 201


@bp.route("/pacientes/<int:id>", methods=["PUT"])
def update_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    data = request.get_json()

    if "nombre" in data:
        paciente.nombre = data["nombre"]

    if "apellido" in data:
        paciente.apellido = data["apellido"]

    if "fecha_nacimiento" in data:
        fecha_nacimiento = parse_date(data["fecha_nacimiento"])
        if not fecha_nacimiento:
            return jsonify({"error": "Formato de fecha inválido"}), 400
        if fecha_nacimiento < date(1900, 1, 1) or fecha_nacimiento > date.today():
            return jsonify({"error": "Fecha de nacimiento fuera de rango"}), 400
        paciente.fecha_nacimiento = fecha_nacimiento

    db.session.commit()

    return jsonify({
        "id": paciente.id,
        "nombre": paciente.nombre,
        "apellido": paciente.apellido,
        "fecha_nacimiento": paciente.fecha_nacimiento.isoformat()
    }), 200


# -------------------- MEDICOS --------------------
@bp.route("/medicos", methods=["POST"])
def create_medico():
    data = request.get_json()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    especialidad = data.get("especialidad", "General")  # Valor por defecto

    if not nombre or not apellido:
        return jsonify({"error": "Nombre y apellido son requeridos"}), 400

    medico = Medico(nombre=nombre, apellido=apellido, especialidad=especialidad)
    db.session.add(medico)
    db.session.commit()

    return jsonify({
        "id": medico.id,
        "nombre": medico.nombre,
        "apellido": medico.apellido,
        "especialidad": medico.especialidad
    }), 201


# -------------------- CITAS --------------------
@bp.route("/citas", methods=["POST"])
def create_cita():
    data = request.get_json()
    paciente_id = data.get("paciente_id")
    medico_id = data.get("medico_id")
    fecha_str = data.get("fecha")
    hora_str = data.get("hora")
    consultorio = data.get("consultorio", None)

    if not paciente_id or not medico_id or not fecha_str or not hora_str:
        return jsonify({"error": "paciente_id, medico_id, fecha y hora son requeridos"}), 400

    paciente = Paciente.query.get(paciente_id)
    if not paciente:
        return jsonify("Paciente no existe"), 400

    medico = Medico.query.get(medico_id)
    if not medico:
        return jsonify("Medico no existe"), 400

    fecha = parse_date(fecha_str)
    hora = parse_time(hora_str)
    if not fecha:
        return jsonify({"error": "Formato de fecha inválido"}), 400
    if not hora:
        return jsonify({"error": "Formato de hora inválido"}), 400

    if hora < time(0, 0, 0) or hora > time(23, 59, 59):
        return jsonify({"error": "Hora fuera de rango"}), 400

    cita = Cita(paciente_id=paciente_id, medico_id=medico_id, fecha=fecha, hora=hora, consultorio=consultorio)
    db.session.add(cita)
    db.session.commit()

    return jsonify({
        "id": cita.id,
        "paciente_id": cita.paciente_id,
        "medico_id": cita.medico_id,
        "fecha": cita.fecha.isoformat(),
        "hora": cita.hora.strftime("%H:%M:%S"),
        "consultorio": cita.consultorio
    }), 201


@bp.route("/citas/<int:id>", methods=["PUT"])
def update_cita(id):
    cita = Cita.query.get_or_404(id)
    data = request.get_json()

    if "fecha" in data:
        fecha = parse_date(data["fecha"])
        if not fecha:
            return jsonify({"error": "Formato de fecha inválido"}), 400
        cita.fecha = fecha

    if "hora" in data:
        hora = parse_time(data["hora"])
        if not hora:
            return jsonify({"error": "Formato de hora inválido"}), 400
        if hora < time(0, 0, 0) or hora > time(23, 59, 59):
            return jsonify({"error": "Hora fuera de rango"}), 400
        cita.hora = hora

    db.session.commit()

    return jsonify({
        "id": cita.id,
        "paciente_id": cita.paciente_id,
        "medico_id": cita.medico_id,
        "fecha": cita.fecha.isoformat(),
        "hora": cita.hora.strftime("%H:%M:%S")
    }), 200


@bp.route("/citas/<int:id>", methods=["GET"])
def get_cita(id):
    cita = Cita.query.get_or_404(id)
    return jsonify({
        "id": cita.id,
        "paciente_id": cita.paciente_id,
        "medico_id": cita.medico_id,
        "fecha": cita.fecha.isoformat(),
        "hora": cita.hora.strftime("%H:%M:%S"),
        "consultorio": cita.consultorio
    })
@bp.route("/citas/<int:id>", methods=["DELETE"])
def delete_cita(id):
    cita = Cita.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    return '', 204
