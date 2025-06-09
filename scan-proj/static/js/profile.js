

function home() { window.open("/"   , )   }
function scrollWin() { window.open("/profile"   , "_self")  }
function fun() { window.open("/scan"   , "_self")  }

function logout() { window.open("/logout" , "_self") } 

function showToast(message,type="error") {
  const toast = document.getElementById('toast-alert');

  // Update the toast message
  toast.textContent = message;
  
  if (type == "success") {
    toast.style.backgroundColor = "#4CAF50";
  }
  else {
    toast.style.backgroundColor = "#ff4444";
  }
  // Show the toast
  toast.classList.add('show');

  // Hide the toast after 2 seconds
  setTimeout(() => {
      toast.classList.remove('show');
  }, 2000);
}

// Delete the specific row when the circular delete button is clicked
document.querySelectorAll('.delete-btn').forEach((button) => {
    button.addEventListener('click', (event) => {
      const row = event.target.closest('.row');
      row.remove();
    });
  });
  // Warning message before "Clear All" operation
document.getElementById('clear-all').addEventListener('click', (e) => {
  const container = document.getElementById('options-container');
  const rows = container.querySelectorAll('.row'); // Assuming each row has the class 'row'

  // Check if rows exist
  if (rows.length === 0) {
    showToast("No rows to clear", "info"); // Show a message if no rows exist
    return; // Exit the function early
  }
  const confirmClear = confirm("Are you sure you want to clear all the rows?");
  if (confirmClear) {
    fetch('/clearall', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(response => {
      if (response.ok) {
        // Clear all rows if confirmed
        const container = document.getElementById('options-container');
        container.innerHTML = 'No scans found';
        showToast("data cleared successfully","success");
      }
    })
    .catch(error => {
      showToast("Error clearing data", "error");
    });
  }
});

// Delete selected rows when "Clear Selected" is clicked
document.getElementById('clear-selected').addEventListener('click', (e) => {
  const checkboxes = document.querySelectorAll('.option-checkbox:checked');
  const ids = Array.from(checkboxes).map(checkbox => checkbox.value); // Extract IDs from checked checkboxes
  
  if (ids.length === 0) {
    showToast("No rows selected for deletion", "error"); // Show a message if no rows are selected
    return; // Exit the function early
  }
  
  // Send a POST request to the Flask endpoint
  fetch('/clear', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ ids: ids }), // Send the list of IDs as JSON
  })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        // Remove the rows from the DOM if the server deletion was successful
        checkboxes.forEach(checkbox => {
          const row = checkbox.closest('.row');
          row.remove();
        });
        const container = document.getElementById('options-container');
        const rows = container.querySelectorAll('.row');
        const tableHeader = container.querySelector('thead'); // Assuming the table header is in a thead element

        if (rows.length === 0) {
          if (tableHeader) {
            tableHeader.remove(); // Remove the table header if no rows are left
          }
          container.innerHTML = '<div>No scans found</div>'; // Display "No scans found" message
        }

        showToast(data.message, "success"); // Show success message
      } else if (data.error) {
        showToast(data.error, "error"); // Show error message
      }
    })
    .catch(error => {
      showToast("An error occurred while deleting reports", "error"); // Show error message
      throw error;
    });

});