// First set of input fields
var userLabel = document.getElementById("userLabel");
var username = document.getElementById("userName");
var passLabel = document.getElementById("passLabel");
var password = document.getElementById("password");

username.addEventListener("focus", () => {
    userLabel.classList.add("active");
});

password.addEventListener("focus", () => {
    passLabel.classList.add("active");
});

// Blur event to remove active class if input is empty
username.addEventListener("blur", () => {
    if (username.value === "") {
        userLabel.classList.remove("active");
    }
});

password.addEventListener("blur", () => {
    if (password.value === "") {
        passLabel.classList.remove("active");
    }
});

// Second set of input fields
var newUserLabel = document.getElementById("newUserLabel");
var newUsername = document.getElementById("newUser");
var newPassLabel = document.getElementById("newPassLabel");
var newPassword = document.getElementById("newPass");
var confirmPassLabel = document.getElementById("confirmPassLabel");
var confirmPass = document.getElementById("confirmPass");

newUsername.addEventListener("focus", () => {
    newUserLabel.classList.add("active");
});

newPassword.addEventListener("focus", () => {
    newPassLabel.classList.add("active");
});

confirmPass.addEventListener("focus", () => {
    confirmPassLabel.classList.add("active");
});

// Blur event to remove active class if input is empty
newUsername.addEventListener("blur", () => {
    if (newUsername.value === "") {
        newUserLabel.classList.remove("active");
    }
});

newPassword.addEventListener("blur", () => {
    if (newPassword.value === "") {
        newPassLabel.classList.remove("active");
    }
});

confirmPass.addEventListener("blur", () => {
    if (confirmPass.value === "") {
        confirmPassLabel.classList.remove("active");
    }
});

const signUpForm = document.getElementById('signup-form');
const signInForm = document.getElementById('signin-form');
const formContainer = document.querySelector('.form-container');
const signUp = document.getElementById("signUp");
signUp.addEventListener("click", () => {
    formContainer.classList.add('active');
    userLabel.classList.remove("active");
    passLabel.classList.remove("active");
    username.value = "";
    password.value = "";
    setTimeout(() => {
        signInForm.style.display = "none";
        signUpForm.style.display = "flex";
    }, 300);
});

const signIn = document.getElementById("signIn");
signIn.addEventListener("click", () => {
    newUserLabel.classList.remove("active");
    newPassLabel.classList.remove("active");
    newUsername.value = "";
    newPassword.value = "";
    setTimeout(() => {
        formContainer.classList.remove('active');
        signInForm.style.display = "flex";
        signUpForm.style.display = "none";
    }, 300);
});

// Sign up form submission
const signUpBtn = document.getElementById("signUpBtn");

// Sign up form submission
signUpBtn.addEventListener("click", async(event) => {
    event.preventDefault(); // Prevent default form submission

    const newUsername = document.getElementById("newUser").value;
    const newPassword = document.getElementById("newPass").value;
    const confirmPass = document.getElementById("confirmPass").value;

    if (newPassword.length < 8) {
        alert("Password should be at least 8 characters long!")
        return
    }
    // Check if passwords match
    if (newPassword !== confirmPass) {
        alert("Passwords do not match!");
        return;
    }

    const userData = {
        username: newUsername,
        password: newPassword
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/api/sign-up', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message); // Success message
            // Redirect to sign-in page after successful signup
            window.location.href = "http://127.0.0.1:5000"
        } else {
            alert(data.message); // Error message
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while signing up.');
    }
});


// Sign in form submission
const signInBtn = document.getElementById("signInBtn");

signInBtn.addEventListener("click", async(event) => {
    event.preventDefault();

    const username = document.getElementById("userName").value;
    const password = document.getElementById("password").value;
    const userData = {
        username: username,
        password: password
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();
        if (response.ok) {
            // alert(data.message);
            // Proceed with logged-in user actions
            localStorage.setItem('username', username)
            window.location.href = "/micro-chat-bot";
        } else {
            alert(data.message); // Error message
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while logging in.');
    }
});