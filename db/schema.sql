-- schema.sql
CREATE DATABASE IF NOT EXISTS medical_appointments;
USE medical_appointments;

-- Pacientes
CREATE TABLE IF NOT EXISTS pacientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  fecha_nacimiento DATE NOT NULL,
  email VARCHAR(150) UNIQUE
);

-- Medicos
CREATE TABLE IF NOT EXISTS medicos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  especialidad VARCHAR(100) NOT NULL
);

-- Consultorios
CREATE TABLE IF NOT EXISTS consultorios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  numero VARCHAR(20) NOT NULL,
  piso INT NOT NULL
);

-- Citas
CREATE TABLE IF NOT EXISTS citas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  paciente_id INT NOT NULL,
  medico_id INT NOT NULL,
  fecha DATE NOT NULL,
  hora TIME NOT NULL,
  consultorio VARCHAR(50),
  FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
  FOREIGN KEY (medico_id) REFERENCES medicos(id) ON DELETE CASCADE
);
