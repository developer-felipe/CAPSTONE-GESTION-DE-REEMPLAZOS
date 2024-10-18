from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Crea la base de datos si no existe'

    def handle(self, *args, **kwargs):
        db_name = connection.settings_dict['NAME']
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        self.stdout.write(self.style.SUCCESS(f'Database {db_name} created if it did not exist.'))
