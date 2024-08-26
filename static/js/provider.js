const production = window.location.origin + "/";
var color = "#005ff1";

class Provider {
    host = production;
    button = null;
    parameters = null;
    func = null;
    headers = {
        'Content-Type': 'application/json'
    };

    config = {
    };

    graphic = null;

    constructor(route, body, button, method, func, auth = false, parameters = {}, multiplatform = false, showAlert = false) {
        this.route = route;

        if (body != null) {
            body = (body instanceof FormData) ? body : JSON.stringify(body);
            this.config["body"] = body;
        }

        this.button = button;
        this.config.method = method;
        this.parameters = parameters;
        this.func = func;

        if (auth && sessionStorage.getItem("token") != null) {
            this.headers["Authorization"] = "Bearer " + sessionStorage.getItem("token");
        }
        if (multiplatform) {
            this.headers["Content-Type"] = "multipart/form-data";
        }
        this.config.headers = this.headers;

    }

    operate() {
        fetch(this.host + this.route, this.config)

            .then(response => response.json())

            .then(data => {

                if ("error" in data) {
                    const colorIcon = "#e81400";
                    const toast = new Toast(colorIcon, data.message);
                    toast.show();

                } else {

                    if (this.parameters != undefined) {
                        this.parameters["data"] = data;
                    }
                    
                    if("message" in data){
                        const toast = new Toast(color, data["message"]);
                        toast.show()
                    }

                    if (this.func != null) {
                        this.graphic = this.func(this.parameters);
                    }


                }

            })

            .catch(error => {
                console.error(error);

                const colorIcon = "#e81400";
                const toast = new Toast(colorIcon, "No se puedo conectar con el servidor");
                toast.show();
            })

            .finally(() => {

                if (this.button != null) {
                    this.button.disabled = false;
                }

            });
    }

    getData() {
        return this.data;
    }
}

class FormProvider {

    checked = false;

    constructor(formData, route, method = "POST", func = null, button = null) {

        const myHeaders = new Headers();
        myHeaders.append("Authorization", "Bearer " + sessionStorage.getItem("token"));

        const requestOptions = {
            method: method,
            headers: myHeaders,
            body: formData
        };

        fetch(production + route, requestOptions)
            .then((response) => response.json())
            .then(data => {
                if ("error" in data) {
                    color = "#e81400";
                } else {
                    form.reset();
                }

                if (func != null) {
                    func(data);
                }
                else {
                    const toast = new Toast(color, data["message"]);
                    toast.show();
                    this.checked = true;
                }

            })
            .catch(error => {
                const colorIcon = "#e81400";
                const message = "No se pudo conectar al servidor, no se enviaron los datos";
                const toast = new Toast(colorIcon, message);
                toast.show()
            })

    }
}