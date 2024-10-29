from django.core.management.base import BaseCommand
from django.db import connection, OperationalError

class Command(BaseCommand):
    help = 'Crea las tablas en la base de datos si no existen'

    def handle(self, *args, **kwargs):
        sql_script = """
CREATE TABLE IF NOT EXISTS asignatura (
    id_asignatura       INT AUTO_INCREMENT PRIMARY KEY,
    nombre_asignatura   VARCHAR(24) NOT NULL
);

CREATE TABLE IF NOT EXISTS dia_semana (
    id_dia       INT AUTO_INCREMENT PRIMARY KEY,
    nombre_dia   VARCHAR(9) NOT NULL
);

CREATE TABLE IF NOT EXISTS modulo (
    id_modulo     INT AUTO_INCREMENT PRIMARY KEY,
    hora_modulo   VARCHAR(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS profesor (
    id_profesor        INT AUTO_INCREMENT PRIMARY KEY,
    nombre             VARCHAR(16) NOT NULL,
    segundo_nombre     VARCHAR(16),
    apellido           VARCHAR(16) NOT NULL,
    segundo_apellido   VARCHAR(16)
);

CREATE TABLE IF NOT EXISTS sala (
    id_sala       INT AUTO_INCREMENT PRIMARY KEY,
    numero_sala   VARCHAR(4) NOT NULL
);

CREATE TABLE IF NOT EXISTS semestre (
    id_semestre   INT AUTO_INCREMENT PRIMARY KEY,
    year          INT NOT NULL,
    semestre      INT NOT NULL
);

CREATE TABLE IF NOT EXISTS horario (
    id_horario                 INT AUTO_INCREMENT PRIMARY KEY,
    seccion                    INT NOT NULL,
    jornada                    CHAR(1) NOT NULL,
    asignatura_id_asignatura   INT NOT NULL,
    sala_id_sala               INT NOT NULL,
    dia_semana_id_dia          INT NOT NULL,
    modulo_id_modulo           INT NOT NULL,
    profesor_id_profesor       INT NOT NULL,
    semestre_id_semestre       INT NOT NULL,
    UNIQUE (seccion, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, profesor_id_profesor, semestre_id_semestre),
    FOREIGN KEY (asignatura_id_asignatura) REFERENCES asignatura (id_asignatura),
    FOREIGN KEY (dia_semana_id_dia) REFERENCES dia_semana (id_dia),
    FOREIGN KEY (modulo_id_modulo) REFERENCES modulo (id_modulo),
    FOREIGN KEY (profesor_id_profesor) REFERENCES profesor (id_profesor),
    FOREIGN KEY (sala_id_sala) REFERENCES sala (id_sala),
    FOREIGN KEY (semestre_id_semestre) REFERENCES semestre (id_semestre)
);

CREATE TABLE IF NOT EXISTS licencia (
    id_licencia            INT AUTO_INCREMENT PRIMARY KEY,
    motivo                 VARCHAR(32) NOT NULL,
    observaciones          VARCHAR(128) NOT NULL,
    fecha_inicio           DATE NOT NULL,
    fecha_termino          DATE NOT NULL,
    profesor_id_profesor   INT NOT NULL,
    FOREIGN KEY (profesor_id_profesor) REFERENCES profesor (id_profesor)
);

CREATE TABLE IF NOT EXISTS recuperacion (
    id_recuperacion                    INT AUTO_INCREMENT PRIMARY KEY,
    numero_modulos                     INT NOT NULL,
    fecha_clase                        DATE NOT NULL,
    fecha_recuperacion                 DATE NOT NULL,
    hora_recuperacion                  TIME NOT NULL,
    sala                               VARCHAR(4) NOT NULL,
    horario_id_horario                 INT NOT NULL,
    FOREIGN KEY (horario_id_horario) REFERENCES horario (id_horario)
);

CREATE TABLE IF NOT EXISTS reemplazos (
    id_reemplazo                       INT AUTO_INCREMENT PRIMARY KEY,
    semana                             INT NOT NULL,
    fecha_reemplazo                    DATE NOT NULL,
    numero_modulos                     INT NOT NULL,
    profesor_reemplazo                 VARCHAR(255) NOT NULL,
    horario_id_horario                 INT NOT NULL,
    FOREIGN KEY (horario_id_horario) REFERENCES horario (id_horario)
);

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario     INT AUTO_INCREMENT PRIMARY KEY,
    usuario        VARCHAR(16) NOT NULL UNIQUE,
    password       VARCHAR(128) NOT NULL,
    is_active      BOOLEAN NOT NULL DEFAULT TRUE,
    last_login     DATETIME,
    is_superuser   BOOLEAN NOT NULL DEFAULT FALSE,
    is_staff       BOOLEAN NOT NULL DEFAULT FALSE
);
"""

        try:
            with connection.cursor() as cursor:
                for command in sql_script.split(';'):
                    if command.strip():  # Ejecutar solo comandos no vacíos
                        cursor.execute(command)
            self.stdout.write(self.style.SUCCESS('Las tablas se han creado exitosamente.'))
        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f'Error al crear tablas: {e}'))
