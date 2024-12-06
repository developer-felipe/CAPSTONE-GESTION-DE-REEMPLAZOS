$(document).ready(function () {
    $('#editModal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget);  
        const id = button.data('id');
        const profesorNombreCompleto = button.data('profesor'); 
        const asignaturaNombre = button.data('asignatura'); 
        const salaNombre = button.data('sala'); 
        const numeroModulos = button.data('numero_modulos');
        const fechaClase = button.data('fecha_clase');
        const fechaRecuperacion = button.data('fecha_recuperacion');
        const horaRecuperacion = button.data('hora_recuperacion');
        const horarioId = button.data('horario_id');  // Suponiendo que el ID del horario se pasa también

        // Rellenamos los campos del formulario con los datos actuales
        $('#edit_id').val(id);
        $('#edit_numero_modulos').val(numeroModulos);
        $('#edit_fecha_clase').val(fechaClase);
        $('#edit_fecha_recuperacion').val(fechaRecuperacion);
        $('#edit_hora_recuperacion').val(horaRecuperacion);

        // Cargar profesores, asignaturas y salas de forma dinámica
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
                profesorSelect.val(profesorSelect.find('option:selected').val()).change();
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
                asignaturaSelect.val(asignaturaSelect.find('option:selected').val()).change();
            });

            fetch('/salas/')
            .then(response => response.json())
            .then(data => {
                const salaSelect = $('#edit_sala');  // Asegúrate de que el id sea correcto
                salaSelect.empty();  // Limpiamos las opciones anteriores
                data.forEach(sala => {
                    salaSelect.append(
                        `<option value="${sala.numero_sala}" ${sala.numero_sala === salaNombre ? 'selected' : ''}>
                            ${sala.numero_sala}
                        </option>`
                    );
                });
                salaSelect.val(salaSelect.find('option:selected').val()).change();  // Asegúrate de que el valor sea correcto
            })
            .catch(error => console.error('Error al obtener salas:', error));

        // Manejo del formulario al enviar
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
                horario_id: horarioId  // Incluimos el ID del horario
            };

            fetch(`/actualizar-recuperacion/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // Asegúrate de que la CSRF Token esté disponible
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Recuperación actualizada correctamente');
                    $('#editModal').modal('hide');
                    location.reload(); 
                    // Actualiza la tabla o la vista para reflejar los cambios
                } else {
                    alert('Error al actualizar la recuperación: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
            
        });
    });
});
