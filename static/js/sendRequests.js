const clasifi = document.getElementById("clasification");
const depende = document.getElementById("dependence");
const form = document.getElementById("form");
const button = document.getElementById("send");

function completeClasifi(data){

    const clasifications = data.data.clasifications;

    clasifications.forEach(clasification => {
        const option = document.createElement("option");
        option.value = clasification.id;
        option.innerHTML = clasification.name
        clasifi.appendChild(option);
    });
}

function completeDependences(data){

    const dependencies = data.data.dependencies;

    
    dependencies.forEach(dependence => {
        const option = document.createElement("option");
        option.value = dependence.id;
        option.innerHTML = dependence.name
        depende.appendChild(option);
    });
}

const queryClasifi = new Provider("routes/getClasifications", null, null, "GET", completeClasifi, false);
queryClasifi.operate()

const queryDependence = new Provider("routes/getDependencies", null, null, "GET", completeDependences, false);
queryDependence.operate()


form.addEventListener("submit", (event) => {

    event.preventDefault();

    const formdata = new FormData(form);
    const query = new FormProvider(formdata, "routes/registerRequest");
});