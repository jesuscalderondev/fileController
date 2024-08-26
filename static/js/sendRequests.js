const clasifi = document.getElementById("clasification");
const depende = document.getElementById("dependence");

const clasifiNew = document.getElementById("newClasification");
const dependeNew = document.getElementById("newDependence");

const form = document.getElementById("form");
const button = document.getElementById("send");

const edit2 = document.getElementById("edit2");

const noView = document.getElementById("noView");

document.getElementsByName("action").forEach(element => {
    element.addEventListener("change", () => {

        console.log(edit2.checked);
        
        if(edit2.checked){
            noView.hidden = false;
        }
        else{
            noView.hidden = true;
        }
    })
});


function completeClasifi(data){

    const clasifications = data.data.clasifications;

    clasifications.forEach(clasification => {
        const option = document.createElement("option");
        option.value = clasification.id;
        option.innerHTML = clasification.name
        clasifi.appendChild(option);


        const optionNew = document.createElement("option");
        optionNew.value = clasification.id;
        optionNew.innerHTML = clasification.name
        clasifiNew.appendChild(optionNew);
    });
}

function completeDependences(data){

    const dependencies = data.data.dependencies;

    
    dependencies.forEach(dependence => {
        const option = document.createElement("option");
        option.value = dependence.id;
        option.innerHTML = dependence.name
        depende.appendChild(option);

        const optionNew = document.createElement("option");
        optionNew.value = dependence.id;
        optionNew.innerHTML = dependence.name
        dependeNew.appendChild(optionNew);
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