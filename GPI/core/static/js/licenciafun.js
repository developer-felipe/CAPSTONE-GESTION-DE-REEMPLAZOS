document.addEventListener('DOMContentLoaded', function () {
     const fechaInicioInput = document.getElementById('fechaInicio');
     const fechaFinInput = document.getElementById('fechaFin');
 
     function validarFechas() {
         const fechaInicio = new Date(fechaInicioInput.value);
         const fechaFin = new Date(fechaFinInput.value);
 
         if (fechaFin < fechaInicio) {
             fechaFinInput.setCustomValidity("La fecha de término no puede ser anterior a la de inicio.");

             fechaFinInput.reportValidity();
         } else {
             fechaFinInput.setCustomValidity("");  
         }
     }
 
     fechaInicioInput.addEventListener('input', validarFechas);
     fechaFinInput.addEventListener('input', validarFechas);
 });
 

 document.addEventListener('DOMContentLoaded', function () {
    const botonesAbrirModal = document.querySelectorAll('.btn-primary[data-id]');
    
    const licenciaModal = new bootstrap.Modal(document.getElementById('licenciaModal'));

    botonesAbrirModal.forEach(function(btn) {
        btn.addEventListener('click', function (event) {
            const profesorId = event.target.getAttribute('data-id');
            
            document.getElementById('idProfesor').value = profesorId;
            
            licenciaModal.show();
        });
    });
});


function guardarLicencia() {
    const form = document.getElementById('licenciaForm');
    
    const fechaInicio = new Date(document.getElementById('fechaInicio').value);
    const fechaFin = new Date(document.getElementById('fechaFin').value);
    
    // Validación de fechas
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
            // Mostrar un mensaje de éxito
            toastr.success(data.message); // Usar toastr o el método de notificación que prefieras

            // Cerrar el modal
            $('#licenciaModal').modal('hide'); 

            // Limpiar los campos del formulario
            document.getElementById('fechaInicio').value = '';
            document.getElementById('fechaFin').value = '';
            document.getElementById('motivo').value = '';
            document.getElementById('observaciones').value = '';
        } else {
            // Mostrar mensaje de error
            toastr.error(data.error || "Hubo un error al guardar la licencia.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        toastr.error("Ocurrió un problema al intentar guardar la licencia.");
    });
}