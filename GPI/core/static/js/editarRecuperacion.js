function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    $('#editModal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget);  
        const id = button.data('id');
        const profesorNombreCompleto = button.data('profesor');
        const asignaturaNombre = button.data('asignatura');
        const numeroModulos = button.data('numero_modulos');
        const fechaClase = button.data('fecha_clase');
        const fechaRecuperacion = button.data('fecha_recuperacion');
        const horaRecuperacion = button.data('hora_recuperacion');
        const salaNombre = button.data('sala');
        const horarioId = button.data('horario');  

        $('#edit_id').val(id);
        $('#horario_id_horario').val(horarioId);  
        $('#edit_numero_modulos').val(numeroModulos);
        $('#edit_fecha_clase').val(fechaClase);
        $('#edit_fecha_recuperacion').val(fechaRecuperacion);
        $('#edit_hora_recuperacion').val(horaRecuperacion);
        $('#edit_sala').val(salaNombre);

        fetch('/docente_recuperación/')
            .then(response => response.json())
            .then(data => {
                const profesorSelect = $('#edit_profesor');
                profesorSelect.empty();  
                data.profesores.forEach(profesor => {
                    const nombreCompleto = `${profesor.nombre} ${profesor.segundo_nombre || ''} ${profesor.apellido} ${profesor.segundo_apellido || ''}`.trim();
                    profesorSelect.append(
                        `<option value="${profesor.id_profesor}" ${nombreCompleto === profesorNombreCompleto ? 'selected' : ''}>
                            ${nombreCompleto}
                        </option>`
                    );
                });
            });

        fetch('/todas_asignaturas/')
            .then(response => response.json())
            .then(data => {
                const asignaturaSelect = $('#edit_asignatura');
                asignaturaSelect.empty();
                data.todas_asignaturas.forEach(asignatura => {
                    asignaturaSelect.append(
                        `<option value="${asignatura.id_asignatura}" ${asignatura.nombre_asignatura === asignaturaNombre ? 'selected' : ''}>
                            ${asignatura.nombre_asignatura}
                        </option>`
                    );
                });
            });

        fetch('/salas/')
            .then(response => response.json())
            .then(data => {
                const salaSelect = $('#edit_sala');
                salaSelect.empty();
                data.forEach(sala => {
                    salaSelect.append(
                        `<option value="${sala.numero_sala}" ${sala.numero_sala === salaNombre ? 'selected' : ''}>
                            ${sala.numero_sala}
                        </option>`
                    );
                });
            });

        $('#edit-recuperacion-form').on('submit', function (e) {
            e.preventDefault();

            const formData = {
                profesor: $('#edit_profesor').val(),
                asignatura: $('#edit_asignatura').val(),
                numero_modulos: $('#edit_numero_modulos').val(),
                fecha_clase: $('#edit_fecha_clase').val(),
                fecha_recuperacion: $('#edit_fecha_recuperacion').val(),
                hora_recuperacion: $('#edit_hora_recuperacion').val(),
                sala: $('#edit_sala').val(),
                horario_id: $('#horario_id_horario').val()  
            };

            fetch(`/actualizar-recuperacion/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Recuperación actualizada correctamente');
                    $('#editModal').modal('hide');
                    location.reload();  
                } else {
                    alert('Error al actualizar la recuperación: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
