document.addEventListener('DOMContentLoaded', function () {
    // Verificar si hay un contenedor de toasts
    var toastContainer = document.getElementById('toast-container');
    
    // Si el contenedor existe y hay toasts para mostrar
    if (toastContainer) {
        // Obtener todos los elementos toast dentro del contenedor
        var toastElements = toastContainer.getElementsByClassName('toast');
        
        // Recorrer cada uno de los toasts y mostrarlos con Bootstrap
        Array.from(toastElements).forEach(function(toastElement) {
            new bootstrap.Toast(toastElement, {
                delay: 1000 // 1.5 segundos para cada toast
            }).show();
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    // Verificar si hay un contenedor de toasts
    var toastContainer = document.getElementById('toast-container');
    
    // Si el contenedor existe y hay toasts para mostrar
    if (toastContainer) {
        var toastElements = toastContainer.getElementsByClassName('toast');
        
        Array.from(toastElements).forEach(function(toastElement) {
            // Mostrar el toast con Bootstrap
            var bsToast = new bootstrap.Toast(toastElement, {
                delay: 1500 // 1.5 segundos para cada toast
            });
            bsToast.show();

            // Agregar un evento de cierre en el botón de cada toast
            var closeButton = toastElement.querySelector('.close');
            if (closeButton) {
                closeButton.addEventListener('click', function () {
                    bsToast.hide(); // Ocultar el toast manualmente al hacer clic
                });
            }
        });
    }
});
