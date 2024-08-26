const files = document.getElementById("files");

function deletedMe(data){
    const file = data.file
    console.log(data);
    
    file.remove()
}

function renderFiles(data) {

    files.innerHTML = "";
    console.log(data);
    

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

        newConainer.setAttribute("class", "center-vertical col-10")
        file.appendChild(newConainer);

        const name = document.createElement("div");
        name.setAttribute("class", "text-start");
        name.innerHTML = extension + " " + fileData.name;

        newConainer.appendChild(name);

        const actions = document.createElement("div");
        actions.setAttribute("class", "col-2 text-end actions");

        const btnDown = document.createElement("button");
        btnDown.setAttribute("class", "btn btn-success");
        btnDown.innerHTML = `<i class="bi bi-cloud-download-fill"></i>`;
        actions.appendChild(btnDown);

        btnDown.addEventListener("click", () => {
            window.open(`/routes/getDocument/${fileData.id}/2`)
        });


        const restoredBtn = document.createElement("button");
        restoredBtn.setAttribute("class", "btn btn-primary");
        restoredBtn.innerHTML = `<i class="bi bi-arrow-repeat"></i>`;
        restoredBtn.title = "Restaurar";
        actions.appendChild(restoredBtn);

        restoredBtn.addEventListener("click", () => {
            const queryBack = new Provider("routes/backArchive/"+fileData.id, null, null, "GET", deletedMe, false, {file}, false, true);
            queryBack.operate();
        });

        file.appendChild(actions);
        files.appendChild(file);

    });
}

const queryGetFiles = new Provider("routes/getFiles/0", null, null, "GET", renderFiles, false);
queryGetFiles.operate();