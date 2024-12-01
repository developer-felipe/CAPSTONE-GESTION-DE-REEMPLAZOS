window.alert = function (message) {
    const alertContainer = document.getElementById('customAlertContainer');
  
    const alertBox = document.createElement('div');
    alertBox.className = 'custom-alert';
    alertBox.innerHTML = `
      <span>${message}</span>
      <button onclick="this.parentElement.remove()">X</button>
    `;
  
    alertContainer.appendChild(alertBox);
  
    setTimeout(() => {
      alertBox.remove();
    }, 5000);
  };

  