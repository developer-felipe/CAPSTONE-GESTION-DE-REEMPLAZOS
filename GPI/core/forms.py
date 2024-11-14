from django import forms
from .models import Profesor, Asignatura, Horario, Sala, DiaSemana, Modulo



class ClaseForm(forms.Form):
    semana = forms.ChoiceField(choices=[(i, f'Semana {i}') for i in range(1, 19)], required=True)
    docente = forms.ModelChoiceField(queryset=Profesor.objects.all(), required=True, to_field_name='nombre')
    asignatura = forms.ModelChoiceField(queryset=Asignatura.objects.all(), required=True)
    seccion = forms.IntegerField(required=True)
    jornada = forms.ChoiceField(choices=[('Mañana', 'Mañana'), ('Tarde', 'Tarde')], required=True)
    hora_inicio = forms.ChoiceField(choices=[('08:00', '08:00'), ('10:00', '10:00')], required=True)
    hora_termino = forms.ChoiceField(choices=[('10:00', '10:00'), ('12:00', '12:00')], required=True)
    numero_modulos = forms.IntegerField(min_value=1, max_value=5, required=True)
    sala = forms.ModelChoiceField(queryset=Sala.objects.all(), required=True)
    fecha_clase = forms.DateField(widget=forms.SelectDateWidget(), required=True)
    docente_remplazo = forms.ModelChoiceField(queryset=Profesor.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        profesor_id = kwargs.get('initial', {}).get('profesor_id')
        super().__init__(*args, **kwargs)
        if profesor_id:
            horarios = Horario.objects.filter(profesor_id_profesor=profesor_id)
            if horarios.exists():
                horario = horarios.first()  # Tomamos el primer horario para este docente, podrías modificar esto si el docente tiene más horarios

                # Asignar valores predeterminados a los campos
                self.fields['asignatura'].initial = horario.asignatura_id_asignatura
                self.fields['seccion'].initial = horario.seccion
                self.fields['jornada'].initial = horario.jornada
                self.fields['hora_inicio'].initial = horario.modulo_id_modulo.hora_modulo
                self.fields['hora_termino'].initial = horario.modulo_id_modulo.hora_modulo
                self.fields['numero_modulos'].initial = len(horarios)  # Esto asume que el número de módulos se calcula con los horarios del docente
                self.fields['sala'].initial = horario.sala_id_sala

            # Filtrar docentes de reemplazo para que no tengan clases en el mismo día y módulo
            docente_remplazo_queryset = Profesor.objects.exclude(
                id_profesor__in=Horario.objects.filter(
                    dia_semana_id_dia=horario.dia_semana_id_dia,
                    modulo_id_modulo=horario.modulo_id_modulo
                ).values_list('profesor_id_profesor', flat=True)
            )

            self.fields['docente_remplazo'].queryset = docente_remplazo_queryset

