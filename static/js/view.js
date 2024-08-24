const form = document.getElementById("form");
const btnSub = document.getElementById("button");

function showInfo(data){
    const info = data.data.request;

    document.getElementById("description").innerHTML = info.description;
    document.getElementById("permission").innerHTML = info.permission;
    document.getElementById("name").innerHTML = info.name;
    document.getElementById("emails").innerHTML = info.emails;
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

    const formdata = {
        "action" : (accept)? "accept" : "decline",
        "requestId" : idRequest,
    };

    if(!accept){
        details.required = true;
        formdata["details"] = details.value;
    }
    

    const query = new Provider("routes/responseRequest", formdata, btnSub, "POST", null, false, showAlert=true);
    query.operate();

    form.reset()


});