CREATE TABLE Terapeutas (
    terapeuta_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    admin BOOLEAN NOT NULL
);

CREATE TABLE Pacientes (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    edad INT,
    num_expediente VARCHAR(255) NOT NULL UNIQUE,
    terapeuta_asignado INT ,
    observaciones TEXT,
    telf_contacto VARCHAR(20),
    FOREIGN KEY (terapeuta_asignado) REFERENCES Terapeutas(terapeuta_id)
);

-- Terapeuta 1 (con permisos de administrador)
INSERT INTO Terapeutas (usuario, contrasena, nombre, apellido, correo, admin)
VALUES ('terapeuta1', 'contrasena123', 'Juan', 'García', 'juan.garcia@example.com', true);

-- Terapeuta 2 (sin permisos de administrador)
INSERT INTO Terapeutas (usuario, contrasena, nombre, apellido, correo, admin)
VALUES ('terapeuta2', 'clave456', 'María', 'López', 'maria.lopez@example.com', false);

-- Paciente 1
INSERT INTO Pacientes (nombre, apellido, edad, num_expediente, terapeuta_asignado, observaciones, telf_contacto)
VALUES ('Ana', 'Martínez', 30, 'EXP001', 1, 'Historial de ansiedad', '661000000');

-- Paciente 2
INSERT INTO Pacientes (nombre, apellido, edad, num_expediente, terapeuta_asignado, observaciones, telf_contacto)
VALUES ('Pedro', 'Ramírez', 45, 'EXP002', 1, 'Trastorno del sueño', '661000000');

-- Paciente 3
INSERT INTO Pacientes (nombre, apellido, edad, num_expediente, terapeuta_asignado, observaciones, telf_contacto)
VALUES ('Laura', 'González', 28, 'EXP003PacientePaciente', 2, 'Depresión posparto', '661000000');

