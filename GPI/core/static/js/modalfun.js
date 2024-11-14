
document.querySelectorAll('[data-bs-toggle="modal"]').forEach(function(button) {
     button.addEventListener('click', function(event) {
       const modalId = this.getAttribute('data-bs-target');
       const modalElement = document.querySelector(modalId);
       if (modalElement) {
         const modal = new bootstrap.Modal(modalElement);
         modal.show();
       } else {
         console.error(`No se encontró el modal con id: ${modalId}`);
       }
     });
   });
   
   document.addEventListener('hidden.bs.modal', function(event) {
     const openModals = document.querySelectorAll('.modal.show');
     if (openModals.length === 0) {
       const backdrop = document.querySelector('.modal-backdrop');
       if (backdrop) {
         backdrop.remove();
       }
       document.body.classList.remove('modal-open');
     }
   });