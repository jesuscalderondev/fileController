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

    function login(...parameters) {
        const data = parameters[0].data;
        if (data != null && data.hasOwnProperty("token")) {
            sessionStorage.setItem("token", data.token);
            window.location.href = "routes/home";
        }
        else {
            const toast = new Toast("08f", data.message);
            toast.show();
        }
    }

    const query = new Provider(route, body, loginBtn, "POST", login, false);
    query.operate();

});
