
document.addEventListener('DOMContentLoaded', function() {
    const logoutLink = document.getElementById('logout-link');
    const customPopup = document.getElementById('custom-popup');
    const popupOverlay = document.getElementById('popup-overlay');
    const confirmButton = document.getElementById('popup-confirm');
    const cancelButton = document.getElementById('popup-cancel');
  
    logoutLink.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent the default logout action
      popupOverlay.style.display = 'block';
      customPopup.style.display = 'block';
    });
  
    confirmButton.addEventListener('click', function() {
      window.location.href = logoutLink.href; // Redirect to the logout URL
    });
  
    cancelButton.addEventListener('click', function() {
      customPopup.style.display = 'none';
      popupOverlay.style.display = 'none';
    });
  
    popupOverlay.addEventListener('click', function() {
      customPopup.style.display = 'none';
      popupOverlay.style.display = 'none';
    });
  });
  