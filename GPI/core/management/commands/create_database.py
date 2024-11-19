from django.core.management.base import BaseCommand
from django.db import connection
from decouple import config

class Command(BaseCommand):
    help = 'Crea la base de datos si no existe'

    def handle(self, *args, **kwargs):
        db_name = config('DATABASE_NAME')
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")

        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES;")
            databases = [row[0] for row in cursor.fetchall()]

        if db_name in databases:
            self.stdout.write(self.style.SUCCESS(f'La base de datos  ya existía o fue creada correctamente.'))
        else:
            self.stdout.write(self.style.ERROR(f'Error: La base de datos  no fue creada.'))
