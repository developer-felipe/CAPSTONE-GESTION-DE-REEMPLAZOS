document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todos los botones para abrir el modal de agregar licencia
    const botonesAbrirModal = document.querySelectorAll('.btn-primary[data-id]');
    const licenciaModal = new bootstrap.Modal(document.getElementById('licenciaModal')); // Inicializa el modal de bootstrap

    // Para cada botón con la clase 'btn-primary' y un 'data-id'
    botonesAbrirModal.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const profesorId = this.getAttribute('data-id'); // Captura el ID del profesor desde el atributo 'data-id' del botón
            const idProfesorInput = document.getElementById('idProfesor'); // Obtén el campo oculto para el ID del profesor
            const fechaInicioInput = document.getElementById('fechaInicio');
            const fechaFinInput = document.getElementById('fechaFin');
            const motivoInput = document.getElementById('motivo');
            const observacionesInput = document.getElementById('observaciones');

            console.log("Profesor ID capturado desde el botón:", profesorId); // Depuración

            if (!profesorId) {
                alert("Error: No se encontró el ID del profesor en el botón. Revisa la plantilla HTML.");
                return;
            }

            // Limpia cualquier valor previo en el campo oculto y en los otros campos del formulario
            idProfesorInput.value = profesorId; // Asigna el nuevo ID del profesor al campo oculto
            fechaInicioInput.value = ''; // Limpia el campo de fecha de inicio
            fechaFinInput.value = ''; // Limpia el campo de fecha de fin
            motivoInput.value = ''; // Limpia el campo de motivo
            observacionesInput.value = ''; // Limpia el campo de observaciones

            console.log("Valor asignado al campo oculto idProfesor:", idProfesorInput.value); // Depuración

            licenciaModal.show(); // Muestra el modal
        });
    });
});

// Función para guardar la licencia
function guardarLicencia() {
    const form = document.getElementById('licenciaForm'); // Obtén el formulario de licencia
    const profesorId = document.getElementById('idProfesor').value; // Obtén el valor del ID del profesor del campo oculto

    console.log("Profesor ID antes de enviar el formulario:", profesorId); // Depuración

    if (!profesorId) {
        alert("Error: El ID del profesor no está definido. Intenta nuevamente.");
        return;
    }

    const fechaInicio = new Date(document.getElementById('fechaInicio').value); // Obtén la fecha de inicio
    const fechaFin = new Date(document.getElementById('fechaFin').value); // Obtén la fecha de fin

    // Validación de las fechas
    if (fechaFin < fechaInicio) {
        alert("La fecha de término no puede ser anterior a la de inicio.");
        return;
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Obtén el token CSRF para seguridad
    const formData = new FormData(form); // Crea un objeto FormData con los datos del formulario

    // Realiza la solicitud AJAX para enviar los datos al servidor
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert(data.message); // Muestra mensaje de éxito
                $('#licenciaModal').modal('hide'); // Cierra el modal
                form.reset(); // Resetea el formulario
            } else {
                alert(data.error || "Hubo un error al guardar la licencia.");
            }
        })
        .catch(error => {
            console.error("Error en el proceso:", error);
            alert("Ocurrió un problema al intentar guardar la licencia.");
        });
}
