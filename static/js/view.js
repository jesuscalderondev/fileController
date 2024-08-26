const form = document.getElementById("form");
const btnSub = document.getElementById("button");
const containerA = document.getElementById("containerA");
const archive = document.getElementById("archive");

function showInfo(data){
    const info = data.data.request;

    document.getElementById("description").innerHTML = info.description;
    document.getElementById("permission").innerHTML = info.permission;
    document.getElementById("name").innerHTML = info.name;
    document.getElementById("emails").innerHTML = info.emails;

    console.log(info);

    const downBtn = document.createElement("a");
    downBtn.setAttribute("class", "btn btn-primary");
    downBtn.setAttribute("href", production+"routes/getDocumentUrl/"+info.route);
    downBtn.innerHTML = `Archivo enviado en la solicitud <i class="bi bi-cloud-download-fill"></i>`
    containerA.appendChild(downBtn);

    
    if(info.nameOld != "No"){
        const downBtnOld = document.createElement("a");
        downBtnOld.setAttribute("class", "btn btn-success m-3");
        downBtnOld.setAttribute("href", production+"routes/getDocumentUrl/"+info.routeOld);
        downBtnOld.innerHTML = `Archivo actual <i class="bi bi-cloud-download-fill"></i>`
        containerA.appendChild(downBtnOld);
    }

}

const queryRequest = new Provider("routes/getDetailsRequest/"+ idRequest, null, null, "GET", showInfo, false);
queryRequest.operate()

function redirect(data){
    window.location.href = "routes/home";
}

form.addEventListener("submit", (event) => {

    event.preventDefault();

    const accept = document.getElementById("accept").checked;
    const details = document.getElementById("details");

    if(accept == false){
        details.required = true;
    }
    else{
        details.required = false;
    }
    
    const idRe = document.createElement("input");
    idRe.hidden = true;
    idRe.value = idRequest;
    idRe.name = "requestId";
    form.appendChild(idRe);
    const formdata = new FormData(form);

    const query = new FormProvider(formdata, "routes/responseRequest", "POST", null, btnSub);

});