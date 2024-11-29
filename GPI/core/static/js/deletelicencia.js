document.addEventListener('DOMContentLoaded', function () {
     document.body.addEventListener('click', function (event) {
         if (event.target.classList.contains('btn-danger')) {
             const licenciaId = event.target.getAttribute('data-id');
             console.log('ID Licencia:', licenciaId);
 
             const url = `/licencias/eliminar/${licenciaId}/`; 
             console.log('URL de eliminación:', url);
 
             fetch(url, {
                 method: 'DELETE',
                 headers: {
                     'Content-Type': 'application/json',
                     'X-CSRFToken': getCookie('csrftoken')
                 }
             })
             .then(response => {
                 console.log('Código de estado:', response.status);
                 return response.json();
             })
             .then(data => {
                 console.log('Respuesta JSON:', data);
                 if (data.success) {
                     alert(data.message);
 
                     const row = event.target.closest('tr');
                     row.remove();  
                 } else {
                     alert('Error al eliminar la licencia: ' + data.message);
                 }
             })
             .catch(error => {
                 console.error('Error al eliminar la licencia:', error);
                 alert('Error al eliminar la licencia');
             });
         }
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
     console.log('CSRF Token:', cookieValue); 
     return cookieValue;
 }
 