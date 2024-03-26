document.addEventListener('DOMContentLoaded', function() {
  // Select all delete buttons
  const deleteButtons = document.querySelectorAll('[data-delete-url]');
  
  // Attach a event listener to each button
  deleteButtons.forEach(button => {
      button.addEventListener('click', function() {
          const deleteUrl = this.getAttribute('data-delete-url');
          setDeleteUrl(deleteUrl);
      });
  });

  // Dark mode
  // Credit: 404GamerNotFound
  const htmlElement = document.documentElement;
  const switchElement = document.getElementById('darkModeSwitch');

  // Set the default theme to dark if no setting is found in local storage
  const currentTheme = localStorage.getItem('bsTheme') || 'dark';
  htmlElement.setAttribute('data-bs-theme', currentTheme);
  switchElement.checked = currentTheme === 'dark';

  switchElement.addEventListener('change', function () {
      if (this.checked) {
          htmlElement.setAttribute('data-bs-theme', 'dark');
          localStorage.setItem('bsTheme', 'dark');
      } else {
          htmlElement.setAttribute('data-bs-theme', 'light');
          localStorage.setItem('bsTheme', 'light');
      }
  });
});

function setDeleteUrl(url) {
  document.getElementById('deleteConfirmBtn').href = url;
}