const body = document.querySelector("body");

class Toast {

    toast = null;
    content = null;

    constructor(colorIcon, message) {
        const toastContent = document.createElement("div");
        this.content = toastContent;
        toastContent.setAttribute("class", "toast fixed-bottom m-3");
        toastContent.role = "alert";
        toastContent.ariaLive = "assertive";
        toastContent.ariaAtomic = true;

        const headerT = document.createElement("div");
        headerT.setAttribute("class", "toast-header");
        headerT.innerHTML = "<strong class='me-auto' id='titleNotification'><span class='bi bi-bell' id='iconNotification' style = ' margin-right: 10px; color : " + colorIcon + " ; '" + "></span>  Notificación</strong><button type='button' class='btn-close' data-bs-dismiss='toast' aria-label='Close'></button>";
        const bodyT = document.createElement("div");
        bodyT.setAttribute("class", "toast-body");
        bodyT.innerHTML = message;

        toastContent.appendChild(headerT);
        toastContent.appendChild(bodyT);

        body.appendChild(toastContent);

        const icon = document.getElementById("iconNotification");

        this.toast = new bootstrap.Toast(toastContent);

    }

    show() {
        this.toast.show();
        setTimeout(() => {
            this.content.remove();
        }, 3000);
    }
}