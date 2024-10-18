from django.core.management.base import BaseCommand
from django.db import connection, OperationalError

class Command(BaseCommand):
    help = 'Crea usuarios por defecto en la base de datos'

    def handle(self, *args, **kwargs):
        users = [
            (1, 'admin', 'admin', 'admin'),
            (2, 'usuario', 'usuario', 'usuario'),
        ]

        try:
            with connection.cursor() as cursor:
                for user in users:
                    cursor.execute(
                        "INSERT INTO usuario (id_usuario, usuario, password, tipo_usuario) VALUES (%s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE usuario=VALUES(usuario), password=VALUES(password), tipo_usuario=VALUES(tipo_usuario);",
                        user
                    )
            self.stdout.write(self.style.SUCCESS('Usuarios creados exitosamente.'))
        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f'Error al crear usuarios: {e}'))
