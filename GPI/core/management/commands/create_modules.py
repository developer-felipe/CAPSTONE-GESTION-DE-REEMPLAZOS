from django.core.management.base import BaseCommand
from django.db import connection, OperationalError

class Command(BaseCommand):
    help = 'Crea los módulos de la semana en la base de datos'
    
    def handle(self, *args, **kwargs):
        modulos = [
            (1, '08:31-09:10'),
            (2, '09:11-09:50'),
            (3, '10:01-10:40'),
            (4, '10:41-11:20'),
            (5, '11:31-12:10'),
            (6, '12:11-12:50'),
            (7, '13:01-13:40'),
            (8, '13:41-14:20'),
            (9, '14:31-15:10'),
            (10, '15:11-15:50'),
            (11, '16:01-16:40'),
            (12, '16:41-17:20'),
            (13, '17:31-18:10'),
            (14, '18:11-18:50'),
            (15, '19:01-19:40'),
            (16, '19:41-20:20'),
            (17, '20:31-21:10'),
            (18, '21:11-21:50'),
            (19, '21:51-22:30'),
        ]

        try:
            with connection.cursor() as cursor:
                for modulo in modulos:
                    cursor.execute(
                        """
                        INSERT INTO MODULO(id_modulo, hora_modulo) 
                        VALUES(%s, %s) 
                        ON DUPLICATE KEY UPDATE 
                        hora_modulo = VALUES(hora_modulo);
                        """,
                        modulo
                    )
            self.stdout.write(self.style.SUCCESS('Módulos creados exitosamente.'))
        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f'Error al crear módulos: {e}'))