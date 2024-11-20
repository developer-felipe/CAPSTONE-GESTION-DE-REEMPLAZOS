$(document).ready(function () {
    $('#editModal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); 
        const id = button.data('id');
        const profesorId = button.data('profesor');
        const asignaturaId = button.data('asignatura');
        const numeroModulos = button.data('numero_modulos');
        const fechaClase = button.data('fecha_clase');
        const fechaRecuperacion = button.data('fecha_recuperacion');
        const horaRecuperacion = button.data('hora_recuperacion');
        const salaId = button.data('sala');

        $('#edit_id').val(id);
        $('#edit_profesor').val(profesorId);
        $('#edit_asignatura').val(asignaturaId);
        $('#edit_numero_modulos').val(numeroModulos);
        $('#edit_fecha_clase').val(fechaClase);
        $('#edit_fecha_recuperacion').val(fechaRecuperacion);
        $('#edit_hora_recuperacion').val(horaRecuperacion);

        fetch('/docente_recuperación/')
            .then(response => response.json())
            .then(data => {
                const profesorSelect = $('#edit_profesor');
                profesorSelect.empty();
                data.profesores.forEach(profesor => {
                    profesorSelect.append(
                        `<option value="${profesor.id_profesor}" ${profesor.id_profesor == profesorId ? 'selected' : ''}>
                            ${profesor.nombre} ${profesor.apellido} ${profesor.segundo_nombre} ${profesor.segundo_apellido}
                        </option>`
                    );
                });
                profesorSelect.trigger('change'); // Activar cambio en el select si es necesario
            })
            .catch(error => console.error('Error al cargar los profesores:', error));

        fetch('/asignaturas/')
            .then(response => response.json())
            .then(data => {
                const asignaturaSelect = $('#edit_asignatura');
                asignaturaSelect.empty();
                if (data && data.todas_asignaturas) {
                    data.todas_asignaturas.forEach(asignatura => {
                        asignaturaSelect.append(
                            `<option value="${asignatura.id_asignatura}" ${asignatura.id_asignatura == asignaturaId ? 'selected' : ''}>
                                ${asignatura.nombre_asignatura}
                            </option>`
                        );
                    });
                } else {
                    console.error('No se encontraron asignaturas');
                }
            })
            .catch(error => console.error('Error al cargar las asignaturas:', error));

        fetch('/salas/')
            .then(response => response.json())
            .then(data => {
                const salaSelect = $('#edit_sala');
                salaSelect.empty();  
                if (data && Array.isArray(data)) { 
                    data.forEach(sala => {
                        salaSelect.append(
                            `<option value="${sala.id_sala}" ${sala.id_sala == salaId ? 'selected' : ''}>
                                ${sala.numero_sala}
                            </option>`
                        );
                    });
                } else {
                    console.error('No se encontraron salas');
                }
            })
            .catch(error => console.error('Error al cargar las salas:', error));
    });

    $('#edit_profesor').on('change', function () {
        const profesorId = $(this).val();
        fetch(`/asignaturas/`)  
            .then(response => response.json())
            .then(asignaturas => {
                const asignaturaSelect = $('#edit_asignatura');
                asignaturaSelect.empty();
                asignaturas.forEach(asignatura => {
                    asignaturaSelect.append(
                        `<option value="${asignatura.id_asignatura}">${asignatura.nombre_asignatura}</option>`
                    );
                });
            })
            .catch(error => console.error('Error al cargar las asignaturas:', error));
    });
});
