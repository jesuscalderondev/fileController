const host = window.location.host + "/";
const loginBtn = document.getElementById("loginBtn");

loginBtn.addEventListener("click", () => {
    loginBtn.disabled = true;


    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const route = "routes/login";

    const body = {
        email: email,
        password: password
    }

    function login(data) {
        console.log(data);
        
        const response = data.data;
        if (response != null && response.hasOwnProperty("token")) {
            sessionStorage.setItem("token", response.token);
            window.location.href = "routes/home";
        }
        else {
            const toast = new Toast("08f", response.message);
            toast.show();
        }
    }

    const query = new Provider(route, body, loginBtn, "POST", login, false);
    query.operate();

});
