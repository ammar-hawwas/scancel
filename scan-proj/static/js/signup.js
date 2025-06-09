let signupForm = document.querySelector(".my-form");
let username = document.getElementById("username");
let email = document.getElementById("email");
let password = document.getElementById("password");
let confirmPassword = document.getElementById("confirm_password");

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

signupForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append('username', username.value);
    data.append('email', email.value);
    data.append('password', password.value);
    data.append('confirm_password', confirmPassword.value);
    data.append('csrf_token', document.querySelector('input[name="csrf_token"]').value);

    fetch('/signup', {
        method: 'POST',
        body: data
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(response => {
        if (response.status === 200) {
            showToast('Registration successful! Redirecting to login...',"success");
            setTimeout(() => {
                window.location.href = "/login";
            }, 2000);
        } else {
            showToast(response.body.message || 'An error occurred', "error");
        }
    })
    .catch(error => {
        showToast('An error occurred', "error");
    });
});

function onChange() {
    if (confirmPassword.value === password.value) {
        confirmPassword.setCustomValidity('');
    } else {
        confirmPassword.setCustomValidity('Passwords do not match!');
    }
}

password.addEventListener('change', onChange);
confirmPassword.addEventListener('change', onChange);