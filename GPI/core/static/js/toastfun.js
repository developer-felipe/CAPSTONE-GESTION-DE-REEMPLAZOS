document.addEventListener('DOMContentLoaded', function () {
    var toastContainer = document.getElementById('toast-container');
    
    if (toastContainer) {
        var toastElements = toastContainer.getElementsByClassName('toast');
        
        Array.from(toastElements).forEach(function(toastElement) {
            new bootstrap.Toast(toastElement, {
                delay: 1000 
            }).show();
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    var toastContainer = document.getElementById('toast-container');
    
    if (toastContainer) {
        var toastElements = toastContainer.getElementsByClassName('toast');
        
        Array.from(toastElements).forEach(function(toastElement) {
            var bsToast = new bootstrap.Toast(toastElement, {
                delay: 1500 
            });
            bsToast.show();

            var closeButton = toastElement.querySelector('.close');
            if (closeButton) {
                closeButton.addEventListener('click', function () {
                    bsToast.hide(); 
                });
            }
        });
    }
});
