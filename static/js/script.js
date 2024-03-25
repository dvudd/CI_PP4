document.addEventListener('DOMContentLoaded', function() {
  // Select att delete buttons
  const deleteButtons = document.querySelectorAll('[data-delete-url]');
  
  // Attach a event listener to each button
  deleteButtons.forEach(button => {
      button.addEventListener('click', function() {
          const deleteUrl = this.getAttribute('data-delete-url');
          setDeleteUrl(deleteUrl);
      });
  });
});

function setDeleteUrl(url) {
  document.getElementById('deleteConfirmBtn').href = url;
}