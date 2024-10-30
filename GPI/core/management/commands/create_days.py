from django.core.management.base import BaseCommand
from django.db import connection, OperationalError

class Command(BaseCommand):
    help = 'Crea los días de la semana en la base de datos'
    
    def handle(self, *args, **kwargs):
        dias = [
            (1, 'Lunes'),
            (2, 'Martes'),
            (3, 'Miércoles'),
            (4, 'Jueves'),
            (5, 'Viernes'),
            (6, 'Sábado'),
        ]

        try:
            with connection.cursor() as cursor:
                for dia in dias:
                    cursor.execute(
                        """
                        INSERT INTO DIA_SEMANA(id_dia, nombre_dia) 
                        VALUES(%s, %s) 
                        ON DUPLICATE KEY UPDATE 
                        nombre_dia = VALUES(nombre_dia);
                        """,
                        dia
                    )
            self.stdout.write(self.style.SUCCESS('Días creados exitosamente.'))
        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f'Error al crear días de la semana: {e}'))