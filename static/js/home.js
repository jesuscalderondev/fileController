const files = document.getElementById("files");

function deleted(data){
    const file = data.file;

    file.remove()
}

function renderFiles(data) {

    files.innerHTML = "";

    const filesData = data.data.files;

    filesData.forEach(fileData => {
        const file = document.createElement("div");

        let extension = null;

        switch (fileData.extension) {
            case "xlsx":
                extension = `<i class="bi bi-file-earmark-excel-fill"></i>`
                break;
            case "pdf":
                extension = `<i class="bi bi-file-earmark-pdf-fill"></i>`
                break;
            case "docx":
                extension = `<i class="bi bi-file-earmark-word-fill"></i>`
                break;
            default:
                break;
        }

        file.setAttribute("class", "file row");

        const newConainer = document.createElement("div");

        newConainer.setAttribute("class", "center-vertical col-8")
        file.appendChild(newConainer);

        const name = document.createElement("div");
        name.setAttribute("class", "text-start");
        name.innerHTML = extension + " " + fileData.name;

        newConainer.appendChild(name);

        const actions = document.createElement("div");
        actions.setAttribute("class", "col-4 text-end actions");

        if (fileData.see) {
            const btnSee = document.createElement("button");
            btnSee.setAttribute("class", "btn btn-primary");
            btnSee.innerHTML = `<i class="bi bi-eye-fill"></i>`;

            btnSee.addEventListener("click", () => {
                const myModal = new bootstrap.Modal(document.getElementById('modalPdf'), {
                });

                var options = {

                    fallbackLink: "<p>This is a <a href='https://example.com/'>fallback link</a></p>"

                };
                PDFObject.embed("getDocument/" + fileData.id + "/0", "#render", options);

                myModal.show();
            });

            actions.appendChild(btnSee);
        }

        if (fileData.edit) {
            const btnEdit = document.createElement("a");
            btnEdit.setAttribute("class", "btn btn-dark");
            btnEdit.innerHTML = `<i class="bi bi-pencil-fill"></i>`;
            btnEdit.setAttribute("href", "/routes/edit/"+fileData.id)
            actions.appendChild(btnEdit);
        }

        if (fileData.delete) {
            const btnDelete = document.createElement("button");
            btnDelete.setAttribute("class", "btn btn-danger");
            btnDelete.innerHTML = `<i class="bi bi-trash-fill"></i>`;
            actions.appendChild(btnDelete);

            btnDelete.addEventListener("click", () =>{
                const deleQ = new Provider("routes/deleteFile/"+fileData.id, null, this, "GET", deleted, false, {file}, showAlert=true);
                deleQ.operate();
            })
        }

        if (fileData.download) {
            const btnDown = document.createElement("button");
            btnDown.setAttribute("class", "btn btn-success");
            btnDown.innerHTML = `<i class="bi bi-cloud-download-fill"></i>`;
            actions.appendChild(btnDown);

            btnDown.addEventListener("click", () => {
                window.open(`/routes/getDocument/${fileData.id}/1`)
            });

            const btnShare = document.createElement("button");
            btnShare.setAttribute("class", "btn btn-primary");
            btnShare.innerHTML = `<i class="bi bi-share"></i>`;
            actions.appendChild(btnShare);

            btnShare.addEventListener("click", () => {
                window.open(`/routes/share/${fileData.id}`)
            });   
        }

              


        file.appendChild(actions);
        files.appendChild(file);

    });
}

const queryGetFiles = new Provider("routes/getFiles/1", null, null, "GET", renderFiles, false);
queryGetFiles.operate();

const notifications = document.getElementById("notifications");

function renderNotifications(data) {

    const permisse = data.data.notifications.linked;

    const notifys = data.data.notifications.notifications;

    notifys.forEach(notify => {

        const link = document.createElement("a");
        link.setAttribute("class", "notify text-center");

        if (permisse) {
            link.setAttribute("href", "/routes/view/" + notify.id);
        }
        const content = document.createElement("div");
        content.setAttribute("class", "file center-vertical p-1");
        content.innerHTML = `<span class='bi bi-bell'></span> ` + notify.description;

        link.appendChild(content);
        notifications.appendChild(link);
    });
}

const queryNotify = new Provider("routes/getNotifications", null, null, "GET", renderNotifications, false);
queryNotify.operate()