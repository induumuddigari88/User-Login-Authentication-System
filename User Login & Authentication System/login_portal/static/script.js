// ======================
// REGISTER
// ======================
async function registerUser(){

    const username =
    document.getElementById("registerUsername").value;

    const email =
    document.getElementById("registerEmail").value;

    const password =
    document.getElementById("registerPassword").value;

    const confirmPassword =
    document.getElementById("confirmPassword").value;

    const error =
    document.getElementById("registerError");

    error.innerText = "";

    if(
        !username ||
        !email ||
        !password ||
        !confirmPassword
    ){
        error.innerText = "All fields are required";
        return;
    }

    if(password !== confirmPassword){
        error.innerText = "Passwords do not match";
        return;
    }

    const response = await fetch('/register', {

        method:'POST',

        headers:{
            'Content-Type':'application/json'
        },

        body:JSON.stringify({
            username,
            email,
            password
        })

    });

    const data = await response.json();

    if(response.ok){

        window.location.href = '/';

    }else{

        error.innerText = data.message;
    }
}

// ======================
// LOGIN
// ======================
async function loginUser(){

    const username =
    document.getElementById("loginUsername").value;

    const password =
    document.getElementById("loginPassword").value;

    const error =
    document.getElementById("loginError");

    error.innerText = "";

    const response = await fetch('/login', {

        method:'POST',

        headers:{
            'Content-Type':'application/json'
        },

        body:JSON.stringify({
            username,
            password
        })

    });

    const data = await response.json();

    if(response.ok){

        window.location.href = '/dashboard.html';

    }else{

        error.innerText = data.message;
    }
}

// ======================
// LOAD DASHBOARD
// ======================
async function loadDashboard() {

    if (
        !window.location.pathname.includes(
            'dashboard.html'
        )
    ) {
        return;
    }

    try {

        const response = await fetch(
            '/dashboard',
            {
                credentials: 'include'
            }
        );

        if (!response.ok) {

            window.location.href =
                '/login.html';

            return;
        }

        const data = await response.json();

        // USERNAME
        document.getElementById(
            'welcomeText'
        ).innerText =
            `Welcome, ${data.user.username}! 🎉`;

        // ROLE
        document.getElementById(
            'role'
        ).innerText =
            data.user.role;

        // EMAIL
        document.getElementById(
            'email'
        ).innerText =
            data.user.email;

        // CREATED DATE
        document.getElementById(
            'createdAt'
        ).innerText =
            data.user.created_at;

    }
    catch (error) {

        console.log(
            'Dashboard Error:',
            error
        );
    }
}
// ======================
// LOGOUT
// ======================
async function logoutUser(){

    await fetch('/logout');

    window.location.href = '/';
}

// LOAD
loadDashboard();