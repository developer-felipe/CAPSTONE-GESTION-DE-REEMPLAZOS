// NOSIRVE LYA SE PUEDE ELIMINAR EL .JS  Función para obtener el valor de un cookie (CSRF Token)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Función para convertir la fecha en formato yyyy-mm-dd a dd-mm-yyyy
function convertirFechaFormatoInput(fecha) {
    const partes = fecha.split('-');  // Dividir la fecha en partes [yyyy, mm, dd]
    return `${partes[2]}-${partes[1]}-${partes[0]}`;  // Devolver en formato dd-mm-yyyy
}

// Función para actualizar la recuperación en el backend usando fetch
function actualizarRecuperacion(idRecuperacion, data) {
    fetch(`/ruta/actualizar-recuperacion/${idRecuperacion}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Asegúrate de tener el token CSRF
        },
        body: JSON.stringify(data)  // Convertir los datos a formato JSON
    })
    .then(response => response.json())  // Procesar la respuesta como JSON
    .then(data => {
        if (data.success) {
            alert('Recuperación actualizada correctamente.');
        } else {
            alert('Error al actualizar la recuperación: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al procesar la solicitud.');
    });
}

// Función para recolectar los datos del modal y llamar a la función de actualización
function actualizarRecuperacionDesdeModal() {
    const idRecuperacion = document.getElementById('edit_id').value;
    const profesorId = document.getElementById('edit_profesor').value;
    const asignaturaId = document.getElementById('edit_asignatura').value;
    const salaId = document.getElementById('edit_sala').value;
    const numeroModulos = document.getElementById('edit_numero_modulos').value;
    const fechaClase = document.getElementById('edit_fecha_clase').value;
    const fechaRecuperacion = document.getElementById('edit_fecha_recuperacion').value;
    const horaRecuperacion = document.getElementById('edit_hora_recuperacion').value;

    const data = {
        profesor_id: profesorId,
        asignatura_id: asignaturaId,
        sala_id: salaId,
        numero_modulos: numeroModulos,
        fecha_clase: fechaClase,
        fecha_recuperacion: fechaRecuperacion,
        hora_recuperacion: horaRecuperacion
    };

    // Llamar a la función para actualizar la recuperación
    actualizarRecuperacion(idRecuperacion, data);
}

// Esta función debe ser llamada cuando se abre el modal para editar la recuperación
function abrirModalEditar(idRecuperacion) {
    // Obtener los datos actuales de la recuperación
    fetch(`/ruta/obtener-recuperacion/${idRecuperacion}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Rellenar el formulario con los datos de la recuperación
                const recuperacion = data.recuperacion;
                document.getElementById('edit_id').value = recuperacion.id;
                document.getElementById('edit_profesor').value = recuperacion.profesor_id;
                document.getElementById('edit_asignatura').value = recuperacion.asignatura_id;
                document.getElementById('edit_sala').value = recuperacion.sala_id;
                document.getElementById('edit_numero_modulos').value = recuperacion.numero_modulos;
                document.getElementById('edit_fecha_clase').value = convertirFechaFormatoInput(recuperacion.fecha_clase);
                document.getElementById('edit_fecha_recuperacion').value = convertirFechaFormatoInput(recuperacion.fecha_recuperacion);
                document.getElementById('edit_hora_recuperacion').value = recuperacion.hora_recuperacion;

                // Abrir el modal
                $('#modalEditar').modal('show');
            } else {
                alert('No se pudo cargar la recuperación para editar.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un error al obtener los datos de la recuperación.');
        });
}

// Esta función debe ser llamada cuando se haga clic en el botón "Actualizar"
function actualizarRecuperacion(idRecuperacion, data) {
    fetch(`/ruta/actualizar-recuperacion/${idRecuperacion}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Asegúrate de tener el token CSRF
        },
        body: JSON.stringify(data)  // Convertir los datos a formato JSON
    })
    .then(response => response.json())  // Procesar la respuesta como JSON
    .then(data => {
        if (data.success) {
            alert('Recuperación actualizada correctamente.');
            // Cerrar el modal después de la actualización
            $('#modalEditar').modal('hide');
            // Recargar o actualizar la tabla de recuperaciones si es necesario
            // location.reload(); // o actualizar los datos en la tabla manualmente
        } else {
            alert('Error al actualizar la recuperación: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al procesar la solicitud.');
    });
}
