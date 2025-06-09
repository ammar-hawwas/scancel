let loginForm = document.querySelector(".my-form");


loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    let email = document.getElementById("email");
    let password = document.getElementById("password");

    const data = new FormData();
    data.append('email', email.value);
    data.append('password', password.value);
    data.append('csrf_token', document.querySelector('input[name="csrf_token"]').value);

    fetch('/login', {
        method: 'POST',
        body: data
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(response => {
        if (response.status === 200) {
            showToast('Login successful! Redirecting...', "success");
            setTimeout(() => {
                window.location.href = "/profile"; // Redirect to profile or dashboard
            }, 2000);
        } else {
            showToast(response.body.message || 'Invalid email or password', "error");
        }
    })
    .catch(error => {
        showToast('An error occurred', "error");
    });
});

function showToast(message, type="error") {
    const toast = document.getElementById('toast-alert');
    if (type == "success") {
        toast.style.backgroundColor = "#4CAF50";
    }
    else {
        toast.style.backgroundColor = "#ff4444";
    }
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}