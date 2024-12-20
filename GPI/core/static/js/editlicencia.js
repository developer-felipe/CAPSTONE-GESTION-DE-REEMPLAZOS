$(document).ready(function () {
     $('#editarLicenciaModal').on('show.bs.modal', function (event) {
         const button = $(event.relatedTarget); 
         const licenciaId = button.data('id');
         const actionUrl = button.data('url'); 
 
         $('#editarLicenciaForm').attr('action', actionUrl); 
 
         fetch(`/licencias/${licenciaId}/`)
             .then(response => response.json())
             .then(data => {
                 $('#fechaInicio').val(data.fecha_inicio);
                 $('#fecha_termino').val(data.fecha_termino);
                 $('#motivo').val(data.motivo);
                 $('#observaciones').val(data.observaciones);
                 $('#idLicencia').val(data.id_licencia);
             })
             .catch(error => console.error('Error al cargar los datos de la licencia:', error));
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
 });
 