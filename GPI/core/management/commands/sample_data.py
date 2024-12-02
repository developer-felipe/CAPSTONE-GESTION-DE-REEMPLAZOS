from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Inserta datos de profesores, carrera, sala, asignatura y horario en la base de datos'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO test_profesor (nombre, segundo_nombre, apellido, segundo_apellido) VALUES
                ('LUIS', 'CARLOS', 'VILLAGRAN', 'VERA'),
                ('CONSTANZA', '', 'CHANDIA', 'GARRIDO');
            """)
            cursor.execute("""
                INSERT INTO test_carrera (nombre_carrera) VALUES
                ('INGENIERÍA EN INFORMÁTICA'),
                ('TECNOLOGÍA MEDICA');
            """)
            cursor.execute("""
                INSERT INTO test_sala (numero_sala) VALUES
                ('H610'),
                ('H609'),
                ('H602'),
                ('H601'),
                ('H605'),
                ('H502'),
                ('H608'),
                ('H604'),
                ('H501'),
                ('H606'),
                ('H603');
            """)
            cursor.execute("""
                INSERT INTO test_asignatura (nombre_asignatura) VALUES
                ('INGLES ELEMENTAL II'),
                ('INGLES INTERMEDIO'),
                ('INGLES ELEMENTAL I'),
                ('INGLES BASICO II'),
                ('INGLES INTERMEDIO II');
            """)
            cursor.execute("""
                INSERT INTO test_horario (seccion, jornada, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, activo, profesor_id_profesor, carrera_id_carrera) VALUES
                (19, 'D', 3, 3, 1, 5, 1, 1, 1),
                (19, 'D', 3, 3, 1, 6, 1, 1, 1),
                (4, 'D', 4, 4, 1, 8, 1, 1, 2),
                (4, 'D', 4, 4, 1, 9, 1, 1, 2),
                (7, 'D', 4, 5, 1, 11, 1, 1, 1),
                (7, 'D', 4, 5, 1, 12, 1, 1, 1),
                (7, 'D', 4, 5, 2, 7, 1, 1, 2),
                (7, 'D', 4, 5, 2, 8, 1, 1, 2),
                (7, 'D', 4, 5, 2, 9, 1, 1, 2),
                (29, 'V', 6, 8, 2, 12, 1, 1, 1);
            """)
            cursor.execute("""
                INSERT INTO test_horario (seccion, jornada, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, activo, profesor_id_profesor, carrera_id_carrera) VALUES
                (29, 'V', 6, 8, 2, 13, 1, 1, 1),
                (4, 'D', 4, 9, 3, 3, 1, 1, 2),
                (4, 'D', 4, 9, 3, 4, 1, 1, 2),
                (7, 'D', 4, 10, 3, 6, 1, 1, 1),
                (7, 'D', 4, 10, 3, 7, 1, 1, 1),
                (7, 'D', 4, 10, 3, 8, 1, 1, 1),
                (4, 'D', 7, 5, 3, 9, 1, 1, 2),
                (4, 'D', 7, 5, 3, 10, 1, 1, 2),
                (29, 'D', 6, 8, 4, 12, 1, 1, 1),
                (29, 'D', 6, 8, 4, 13, 1, 1, 1);
            """)
            cursor.execute("""
                INSERT INTO test_horario (seccion, jornada, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, activo, profesor_id_profesor, carrera_id_carrera) VALUES
                (10, 'D', 5, 6, 3, 13, 1, 1, 1),
                (10, 'D', 5, 6, 3, 14, 1, 1, 1),
                (29, 'V', 6, 8, 2, 16, 1, 1, 2),
                (29, 'V', 6, 8, 2, 17, 1, 1, 2),
                (6, 'D', 4, 11, 1, 1, 1, 2, 1),
                (6, 'D', 4, 11, 1, 2, 1, 2, 1),
                (9, 'D', 4, 8, 1, 5, 1, 2, 1),
                (9, 'D', 4, 8, 1, 6, 1, 2, 1),
                (18, 'D', 6, 12, 2, 1, 1, 2, 2),
                (18, 'D', 6, 12, 2, 2, 1, 2, 2);
            """)
            cursor.execute("""
                INSERT INTO test_horario (seccion, jornada, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, activo, profesor_id_profesor, carrera_id_carrera) VALUES
                (9, 'D', 4, 4, 2, 5, 1, 2, 1),
                (9, 'D', 4, 4, 2, 6, 1, 2, 1),
                (2, 'D', 4, 8, 2, 7, 1, 2, 2),
                (2, 'D', 4, 8, 2, 8, 1, 2, 2),
                (10, 'D', 6, 13, 2, 11, 1, 2, 2),
                (10, 'D', 6, 13, 2, 12, 1, 2, 2),
                (6, 'D', 4, 7, 3, 3, 1, 2, 1),
                (6, 'D', 4, 7, 3, 4, 1, 2, 1),
                (6, 'D', 4, 7, 3, 5, 1, 2, 1),
                (6, 'D', 3, 13, 3, 13, 1, 2, 1);
            """)
            cursor.execute("""
                INSERT INTO test_horario (seccion, jornada, asignatura_id_asignatura, sala_id_sala, dia_semana_id_dia, modulo_id_modulo, activo, profesor_id_profesor, carrera_id_carrera) VALUES
                (6, 'D', 3, 13, 3, 14, 1, 2, 1),
                (14, 'V', 4, 8, 3, 17, 1, 2, 1),
                (14, 'V', 4, 8, 3, 18, 1, 2, 1),
                (14, 'V', 4, 8, 3, 19, 1, 2, 1),
                (14, 'V', 4, 11, 4, 17, 1, 2, 1),
                (14, 'V', 4, 11, 4, 18, 1, 2, 1),
                (14, 'V', 4, 11, 4, 19, 1, 2, 1),
                (14, 'V', 4, 11, 5, 16, 1, 2, 1),
                (14, 'V', 4, 11, 5, 15, 1, 2, 1);
            """)
