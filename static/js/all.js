const resquest = document.getElementById("requests");
const chat = document.getElementById("chat");
const creators = document.getElementById("creators");
const log = document.getElementById("log");

function replitPermissions(data){
    const permissions = data.data.permissions;

    console.log(permissions);
    
    if(permissions.admin){
        resquest.innerHTML = `<a class="nav-link" href="/routes/requests">Solicitudes</i></a>`;
    }

    if(permissions.chatIA){
        chat.innerHTML = `<a class="nav-link" href="/routes/chatBot">ChatBot</i></a>`;
    }

    if(permissions.create){
        try {
            log.innerHTML += `<a class="nav-link" href="/routes/log">Historial</i></a>`
            creators.innerHTML += `<a href="/routes/formFile" class="btn btn-success col-auto me-md-3">
                    <i class="bi bi-cloud-upload-fill"></i>
                </a>`
        } catch (error) {
            
        }
        
    }
}

const queryPermissions = new Provider("routes/getPermissions", null, null, "GET", replitPermissions, false)
queryPermissions.operate()