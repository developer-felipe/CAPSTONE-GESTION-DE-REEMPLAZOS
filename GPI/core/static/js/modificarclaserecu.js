$('#editModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);  // El botón que abrió el modal
    var editId = button.data('id');  // ID de la recuperación
    var profesor = button.data('profesor'); // Nombre del profesor
    var asignatura = button.data('asignatura'); // Nombre de la asignatura
    var numeroModulos = button.data('numero_modulos'); 
    var fechaClase = button.data('fecha_clase');
    var fechaRecuperacion = button.data('fecha_recuperacion'); 
    var sala = button.data('sala');
    var horaRecuperacion = button.data('hora_recuperacion');  // Hora de recuperación

    // Asignar valores al modal
    $('#edit_id').val(editId);
    $('#edit_numero_modulos').val(numeroModulos);
    $('#edit_fecha_clase').val(convertirFechaFormatoInput(fechaClase));
    $('#edit_fecha_recuperacion').val(convertirFechaFormatoInput(fechaRecuperacion));
    $('#edit_hora_recuperacion').val(horaRecuperacion); // Asignar hora de recuperación

    // Llenar select de profesor
    fetch('/docente_recuperación/')
        .then(response => response.json())
        .then(data => {
            const profesorSelect = $('#edit_profesor');
            profesorSelect.empty();
            profesorSelect.append('<option value="">Selecciona un profesor</option>');

            // Llenar los profesores
            data.profesores.forEach(profesorItem => {
                const option = $('<option></option>');
                option.val(profesorItem.id_profesor);  // Usar id del profesor para asociarlo correctamente
                option.text(`${profesorItem.nombre} ${profesorItem.apellido}`);
                profesorSelect.append(option);
            });

            // Asignar el valor seleccionado del profesor
            profesorSelect.val(profesor); // Aquí asignamos el id del profesor (no el nombre)
        })
        .catch(error => {
            console.error('Error al obtener los datos de los profesores:', error);
        });

    // Llenar select de asignaturas
    fetch(`/docente_asignatura/${profesor}/`)
        .then(response => response.json())
        .then(data => {
            const asignaturaSelect = $('#edit_asignatura');
            asignaturaSelect.empty();
            asignaturaSelect.append('<option value="">Selecciona una asignatura</option>');

            // Llenar las asignaturas
            data.asignaturas.forEach(asignaturaItem => {
                const option = $('<option></option>');
                option.val(asignaturaItem.id_asignatura);  // Usar id de la asignatura para asociarla
                option.text(asignaturaItem.nombre_asignatura);
                asignaturaSelect.append(option);
            });

            // Asignar la asignatura seleccionada
            asignaturaSelect.val(asignatura); // Aquí asignamos el id de la asignatura (no el nombre)
        })
        .catch(error => {
            console.error('Error al obtener las asignaturas:', error);
        });

    // Llenar select de salas de forma dinámica
    fetch('/api/salas')  // Aquí deberías hacer la petición a la API que devuelve las salas
        .then(response => response.json())
        .then(data => {
            const salaSelect = $('#edit_sala');
            salaSelect.empty();
            salaSelect.append('<option value="">Selecciona una sala</option>');

            // Llenar las salas
            data.salas.forEach(salaItem => {
                const option = $('<option></option>');
                option.val(salaItem.id_sala);  // Usamos el id de la sala para asociarla
                option.text(salaItem.codigo);  // Aquí puedes usar el nombre o código de la sala
                salaSelect.append(option);
            });

            // Asignar la sala seleccionada
            salaSelect.val(sala); // Aquí asignamos el id de la sala
        })
        .catch(error => {
            console.error('Error al obtener las salas:', error);
        });
});
