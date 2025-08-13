# backend/sample_data.py
from app import create_app
from models import db, Paciente, Medico, Consultorio
from datetime import date

app = create_app()
with app.app_context():
    db.create_all()
    # Insert sample pacientes
    p1 = Paciente(nombre='Juan', apellido='Perez', fecha_nacimiento=date(1990,1,1), email='juan@example.com')
    p2 = Paciente(nombre='Ana', apellido='Lopez', fecha_nacimiento=date(1985,5,12), email='ana@example.com')
    db.session.add_all([p1,p2])
    # medicos
    m1 = Medico(nombre='Luis', apellido='Gomez', especialidad='Cardiologia')
    m2 = Medico(nombre='Marta', apellido='Diaz', especialidad='Pediatria')
    db.session.add_all([m1,m2])
    # consultorios
    c1 = Consultorio(numero='C-101', piso=1)
    c2 = Consultorio(numero='C-202', piso=2)
    db.session.add_all([c1,c2])
    db.session.commit()
    print("Datos insertados")
