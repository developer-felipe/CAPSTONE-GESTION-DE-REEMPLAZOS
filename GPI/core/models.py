from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models

class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    nombre_asignatura = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'asignatura'

class DiaSemana(models.Model):
    id_dia = models.AutoField(primary_key=True)
    nombre_dia = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'dia_semana'


class Modulo(models.Model):
    id_modulo = models.AutoField(primary_key=True)
    hora_modulo = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'modulo'


class Sala(models.Model):
    id_sala = models.AutoField(primary_key=True)
    numero_sala = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'sala'

class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=24)
    segundo_nombre = models.CharField(max_length=24, blank=True, null=True)
    apellido = models.CharField(max_length=24)
    segundo_apellido = models.CharField(max_length=24, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profesor'


class Horario(models.Model):
    id_horario = models.AutoField(primary_key=True)
    seccion = models.IntegerField()
    jornada = models.CharField(max_length=1)
    activo = models.BooleanField(default=True)
    asignatura_id_asignatura = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='asignatura_id_asignatura')
    sala_id_sala = models.ForeignKey(Sala, models.DO_NOTHING, db_column='sala_id_sala')
    dia_semana_id_dia = models.ForeignKey(DiaSemana, models.DO_NOTHING, db_column='dia_semana_id_dia')
    modulo_id_modulo = models.ForeignKey(Modulo, models.DO_NOTHING, db_column='modulo_id_modulo')
    profesor_id_profesor = models.ForeignKey(Profesor, models.DO_NOTHING, db_column='profesor_id_profesor')

    class Meta:
        managed = False
        db_table = 'horario'
        unique_together = (('seccion', 'asignatura_id_asignatura', 'sala_id_sala', 'dia_semana_id_dia', 'modulo_id_modulo', 'profesor_id_profesor'))


class Licencia(models.Model):
    id_licencia = models.AutoField(primary_key=True)
    motivo = models.CharField(max_length=32)
    observaciones = models.CharField(max_length=128)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    estado = models.CharField(max_length=11)
    profesor_id_profesor = models.ForeignKey(Profesor, models.DO_NOTHING, db_column='profesor_id_profesor')

    class Meta:
        managed = False
        db_table = 'licencia'


class Recuperacion(models.Model):
    id_recuperacion = models.AutoField(primary_key=True)
    profesor = models.CharField(max_length=100)
    asignatura = models.CharField(max_length=24)
    numero_modulos = models.IntegerField()
    fecha_clase = models.DateField()
    fecha_recuperacion = models.DateField()
    hora_recuperacion = models.TimeField()
    sala = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'recuperacion'



class Reemplazos(models.Model):
    id_reemplazo = models.AutoField(primary_key=True)
    semana = models.IntegerField()
    fecha_reemplazo = models.DateField()
    profesor_reemplazo = models.CharField(max_length=255)
    horario = models.ForeignKey(Horario, models.DO_NOTHING, db_column='horario_id_horario')

    class Meta:
        managed = False
        db_table = 'reemplazos'
        unique_together = (('id_reemplazo', 'horario'),)

class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError('El usuario debe tener un nombre.')
        usuario = self.model(usuario=usuario, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(usuario, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class Usuario(AbstractBaseUser, PermissionsMixin):
    objects = UsuarioManager()

    id_usuario = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'usuario'

    def __str__(self):
        return self.usuario

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)