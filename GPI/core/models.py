from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=16)
    tipo_usuario = models.CharField(max_length=8)
    
    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.usuario