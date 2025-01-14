
document.addEventListener('DOMContentLoaded', function () {
    let eliminarForm = document.getElementById('formConfirmarEliminacion');
    let cancelDeleteBtn = document.getElementById('cancelDelete');
    let confirmationMessage = document.getElementById('confirmationMessage');
    
    let idProfesorParaEliminar = null; 

    document.querySelectorAll('#btnEliminar').forEach(function(botonEliminar) {
        botonEliminar.addEventListener('click', function (e) {
            e.preventDefault(); 

            idProfesorParaEliminar = botonEliminar.getAttribute('data-id');
            
            document.getElementById('idProfesorConfirmarEliminacion').value = idProfesorParaEliminar;

            confirmationMessage.style.display = 'block';
        });
    });

    cancelDeleteBtn.addEventListener('click', function () {
        confirmationMessage.style.display = 'none'; 
    });

    eliminarForm.addEventListener('submit', function (e) {
        if (!idProfesorParaEliminar) {
            e.preventDefault(); 
            alert("Debe seleccionar un docente para eliminar.");
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    let alerts = document.querySelectorAll('#alert-container .alert');

    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.display = 'none';
        }, 3000); 
    });
});

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
    const csrftoken = getCookie('csrftoken');

    botonEditar = document.querySelectorAll('#modProfe')
    botonEditar.forEach(function (boton) {
        boton.addEventListener('click', function () {
            id = boton.dataset.mod_prof
            console.log(id)
        })
    })