from django.core.management.base import BaseCommand
from django.db import OperationalError
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea usuarios por defecto en la base de datos'

    def handle(self, *args, **kwargs):
        User = get_user_model()  # Obtiene el modelo de usuario personalizado

        users = [
            {'usuario': 'admin', 'password': 'admin', 'is_staff': True, 'is_superuser': True},
            {'usuario': 'usuario', 'password': 'usuario', 'is_staff': False, 'is_superuser': False},
        ]

        for user_data in users:
            user, created = User.objects.get_or_create(
                usuario=user_data['usuario'],
                defaults={
                    'password': user_data['password'],
                    'is_staff': user_data['is_staff'],
                    'is_superuser': user_data['is_superuser'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Usuario "{user.usuario}" creado exitosamente.'))
            else:
                self.stdout.write(self.style.WARNING(f'El usuario "{user.usuario}" ya existe.'))

        # Asegúrate de que las contraseñas estén correctamente hasheadas
        for user_data in users:
            user = User.objects.get(usuario=user_data['usuario'])
            user.set_password(user_data['password'])
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Contraseña de "{user.usuario}" actualizada correctamente.'))
