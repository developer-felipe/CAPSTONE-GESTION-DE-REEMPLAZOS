from django.core.management.base import BaseCommand
from django.db import connection, OperationalError

class Command(BaseCommand):
    help = 'Crea las tablas en la base de datos si no existen'

    def handle(self, *args, **kwargs):
        sql_script = """
CREATE TABLE asignatura (
    id_asignatura       INT NOT NULL,
    nombre_asignatura   VARCHAR(24) NOT NULL,
    PRIMARY KEY (id_asignatura)
);

CREATE TABLE dia_semana (
    id_dia       INT NOT NULL,
    nombre_dia   VARCHAR(9) NOT NULL,
    PRIMARY KEY (id_dia)
);

CREATE TABLE horario (
    id_horario                 INT NOT NULL,
    seccion                    INT NOT NULL,
    jornada                    CHAR(1) NOT NULL,
    asignatura_id_asignatura   INT NOT NULL,
    sala_id_sala               INT NOT NULL,
    dia_semana_id_dia          INT NOT NULL,
    modulo_id_modulo           INT NOT NULL,
    profesor_id_profesor       INT NOT NULL,
    semestre_id_semestre       INT NOT NULL,
    PRIMARY KEY (id_horario, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, profesor_id_profesor, semestre_id_semestre),
    FOREIGN KEY (asignatura_id_asignatura) REFERENCES asignatura (id_asignatura),
    FOREIGN KEY (dia_semana_id_dia) REFERENCES dia_semana (id_dia),
    FOREIGN KEY (modulo_id_modulo) REFERENCES modulo (id_modulo),
    FOREIGN KEY (profesor_id_profesor) REFERENCES profesor (id_profesor),
    FOREIGN KEY (sala_id_sala) REFERENCES sala (id_sala),
    FOREIGN KEY (semestre_id_semestre) REFERENCES semestre (id_semestre)
);

CREATE TABLE licencia (
    id_licencia            INT NOT NULL,
    motivo                 VARCHAR(32) NOT NULL,
    observaciones          VARCHAR(128) NOT NULL,
    fecha_inicio           DATE NOT NULL,
    fecha_termino          DATE NOT NULL,
    profesor_id_profesor   INT NOT NULL,
    PRIMARY KEY (id_licencia),
    FOREIGN KEY (profesor_id_profesor) REFERENCES profesor (id_profesor)
);

CREATE TABLE modulo (
    id_modulo     INT NOT NULL,
    hora_modulo   VARCHAR(11) NOT NULL,
    PRIMARY KEY (id_modulo)
);

CREATE TABLE profesor (
    id_profesor        INT NOT NULL,
    nombre             VARCHAR(16) NOT NULL,
    segundo_nombre     VARCHAR(16),
    apellido           VARCHAR(16) NOT NULL,
    segundo_apellido   VARCHAR(16),
    PRIMARY KEY (id_profesor)
);

CREATE TABLE recuperacion (
    id_recuperacion                    INT NOT NULL,
    numero_modulos                     INT NOT NULL,
    fecha_clase                        DATE NOT NULL,
    fecha_recuperacion                 DATE NOT NULL,
    hora_recuperacion                  TIME NOT NULL,
    sala                               VARCHAR(4) NOT NULL,
    horario_id_horario                 INT NOT NULL,
    horario_asignatura_id_asignatura   INT NOT NULL,
    horario_sala_id_sala               INT NOT NULL,
    horario_dia_semana_id_dia          INT NOT NULL,
    horario_modulo_id_modulo           INT NOT NULL,
    horario_profesor_id_profesor       INT NOT NULL,
    horario_semestre_id_semestre       INT NOT NULL,
    PRIMARY KEY (id_recuperacion, horario_id_horario, horario_asignatura_id_asignatura, horario_sala_id_sala, horario_dia_semana_id_dia, horario_modulo_id_modulo, horario_profesor_id_profesor, horario_semestre_id_semestre),
    FOREIGN KEY (horario_id_horario, horario_asignatura_id_asignatura, horario_sala_id_sala, horario_dia_semana_id_dia, horario_modulo_id_modulo, horario_profesor_id_profesor, horario_semestre_id_semestre) REFERENCES horario (id_horario, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, profesor_id_profesor, semestre_id_semestre)
);

CREATE TABLE reemplazos (
    id_reemplazo                       INT NOT NULL,
    semana                             INT NOT NULL,
    fecha_reemplazo                    DATE NOT NULL,
    numero_modulos                     INT NOT NULL,
    profesor_reemplazo                 VARCHAR(255) NOT NULL,
    horario_id_horario                 INT NOT NULL,
    horario_asignatura_id_asignatura   INT NOT NULL,
    horario_sala_id_sala               INT NOT NULL,
    horario_dia_semana_id_dia          INT NOT NULL,
    horario_modulo_id_modulo           INT NOT NULL,
    horario_profesor_id_profesor       INT NOT NULL,
    horario_semestre_id_semestre       INT NOT NULL,
    PRIMARY KEY (id_reemplazo, horario_id_horario, horario_asignatura_id_asignatura, horario_sala_id_sala, horario_dia_semana_id_dia, horario_modulo_id_modulo, horario_profesor_id_profesor, horario_semestre_id_semestre),
    FOREIGN KEY (horario_id_horario, horario_asignatura_id_asignatura, horario_sala_id_sala, horario_dia_semana_id_dia, horario_modulo_id_modulo, horario_profesor_id_profesor, horario_semestre_id_semestre) REFERENCES horario (id_horario, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, profesor_id_profesor, semestre_id_semestre)
);

CREATE TABLE sala (
    id_sala       INT NOT NULL,
    numero_sala   VARCHAR(4) NOT NULL,
    PRIMARY KEY (id_sala)
);

CREATE TABLE semestre (
    id_semestre   INT NOT NULL,
    year          INT NOT NULL,
    semestre      INT NOT NULL,
    PRIMARY KEY (id_semestre)
);

CREATE TABLE usuario (
    id_usuario     INT NOT NULL,
    usuario        VARCHAR(16) NOT NULL,
    password       VARCHAR(16) NOT NULL,
    tipo_usuario   VARCHAR(8) NOT NULL,
    PRIMARY KEY (id_usuario)
);

        """
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_script)
            self.stdout.write(self.style.SUCCESS('Las tablas se han creado exitosamente.'))
        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f'Error al crear tablas: {e}'))
