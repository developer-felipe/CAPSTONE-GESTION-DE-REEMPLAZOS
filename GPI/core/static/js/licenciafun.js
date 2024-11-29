document.addEventListener('DOMContentLoaded', function () {
    const botonesAbrirModal = document.querySelectorAll('.btn-primary[data-id]');
    const licenciaModal = new bootstrap.Modal(document.getElementById('licenciaModal')); 

    botonesAbrirModal.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const profesorId = this.getAttribute('data-id'); 
            const idProfesorInput = document.getElementById('idProfesor'); 
            const fechaInicioInput = document.getElementById('fechaInicio');
            const fechaFinInput = document.getElementById('fechaFin');
            const motivoInput = document.getElementById('motivo');
            const observacionesInput = document.getElementById('observaciones');

            console.log("Profesor ID capturado desde el botón:", profesorId); 

            if (!profesorId) {
                alert("Error: No se encontró el ID del profesor en el botón. Revisa la plantilla HTML.");
                return;
            }

            idProfesorInput.value = profesorId; 
            fechaInicioInput.value = ''; 
            fechaFinInput.value = ''; 
            motivoInput.value = ''; 
            observacionesInput.value = ''; 

            console.log("Valor asignado al campo oculto idProfesor:", idProfesorInput.value); 

            licenciaModal.show(); 
        });
    });
});

function guardarLicencia() {
    const form = document.getElementById('licenciaForm'); 
    const profesorId = document.getElementById('idProfesor').value; 

    console.log("Profesor ID antes de enviar el formulario:", profesorId);

    if (!profesorId) {
        alert("Error: El ID del profesor no está definido. Intenta nuevamente.");
        return;
    }

    const fechaInicio = new Date(document.getElementById('fechaInicio').value); 
    const fechaFin = new Date(document.getElementById('fechaFin').value); 
    if (fechaFin < fechaInicio) {
        alert("La fecha de término no puede ser anterior a la de inicio.");
        return;
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
    const formData = new FormData(form); 

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
                alert(data.message); 
                $('#licenciaModal').modal('hide'); 
                form.reset(); 
            } else {
                alert(data.error || "Hubo un error al guardar la licencia.");
            }
        })
        .catch(error => {
            console.error("Error en el proceso:", error);
            alert("Ocurrió un problema al intentar guardar la licencia.");
        });
}
