from django.core.management.base import BaseCommand
from django.db import connection, OperationalError

class Command(BaseCommand):
    help = 'Crea las tablas en la base de datos si no existen'

    def handle(self, *args, **kwargs):
        sql_script = """
CREATE TABLE asignatura (
    id_asignatura INT AUTO_INCREMENT PRIMARY KEY,
    nombre_asignatura VARCHAR(24) NOT NULL
);

CREATE TABLE dia_semana (
    id_dia INT AUTO_INCREMENT PRIMARY KEY,
    nombre_dia VARCHAR(9) NOT NULL
);

CREATE TABLE modulo (
    id_modulo INT AUTO_INCREMENT PRIMARY KEY,
    hora_modulo VARCHAR(11) NOT NULL
);

CREATE TABLE sala (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    numero_sala VARCHAR(4) NOT NULL
);

CREATE TABLE profesor (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(24) NOT NULL,
    segundo_nombre VARCHAR(24),
    apellido VARCHAR(24) NOT NULL,
    segundo_apellido VARCHAR(24)
);

CREATE TABLE horario (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    seccion INT NOT NULL,
    jornada CHAR(1) NOT NULL,
    asignatura_id_asignatura INT NOT NULL,
    sala_id_sala INT NOT NULL,
    dia_semana_id_dia INT NOT NULL,
    modulo_id_modulo INT NOT NULL,
    activo TINYINT(1) DEFAULT 1;
    profesor_id_profesor INT NOT NULL,
    UNIQUE(seccion, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, profesor_id_profesor),
    FOREIGN KEY (asignatura_id_asignatura) REFERENCES asignatura(id_asignatura),
    FOREIGN KEY (sala_id_sala) REFERENCES sala(id_sala),
    FOREIGN KEY (dia_semana_id_dia) REFERENCES dia_semana(id_dia),
    FOREIGN KEY (modulo_id_modulo) REFERENCES modulo(id_modulo),
    FOREIGN KEY (profesor_id_profesor) REFERENCES profesor(id_profesor)
);

CREATE TABLE licencia (
    id_licencia INT AUTO_INCREMENT PRIMARY KEY,
    motivo VARCHAR(32) NOT NULL,
    observaciones VARCHAR(128),
    fecha_inicio DATE NOT NULL,
    fecha_termino DATE NOT NULL,
    estado VARCHAR(11) NOT NULL,
    profesor_id_profesor INT NOT NULL,
    FOREIGN KEY (profesor_id_profesor) REFERENCES profesor(id_profesor)
);

CREATE TABLE recuperacion (
    id_recuperacion INT AUTO_INCREMENT PRIMARY KEY,
    profesor VARCHAR(100) NOT NULL,
    asignatura VARCHAR(24) NOT NULL,
    numero_modulos INT NOT NULL,
    fecha_clase DATE NOT NULL,
    fecha_recuperacion DATE NOT NULL,
    hora_recuperacion TIME NOT NULL,
    sala VARCHAR(4) NOT NULL
);

CREATE TABLE reemplazos (
    id_reemplazo INT AUTO_INCREMENT PRIMARY KEY,
    semana INT NOT NULL,
    fecha_reemplazo DATE NOT NULL,
    profesor_reemplazo VARCHAR(255) NOT NULL,
    horario_id_horario INT NOT NULL,
    UNIQUE(id_reemplazo, horario_id_horario),
    FOREIGN KEY (horario_id_horario) REFERENCES horario(id_horario)
);

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(16) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login DATETIME,
    is_superuser BOOLEAN DEFAULT FALSE,
    is_staff BOOLEAN DEFAULT FALSE
);

"""

        try:
            with connection.cursor() as cursor:
                for command in sql_script.split(';'):
                    if command.strip():
                        cursor.execute(command)
            self.stdout.write(self.style.SUCCESS('Las tablas se han creado exitosamente.'))
        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f'Error al crear tablas: {e}'))
