const logs = document.getElementById("logs");
const download = document.getElementById("download");

function renderlogs(data) {

    const logsData = data.data.logs;

    if(logsData.length > 0){
        const btnDow = document.createElement("a");
        btnDow.setAttribute("href", "downloadHistory");
        btnDow.setAttribute("class", "btn btn-success col-6 m-3");
        btnDow.innerHTML = `Descargar excel <i class="bi bi-file-earmark-excel-fill"></i>`

        download.appendChild(btnDow);
    }

    logsData.forEach(logData => {
        const log = document.createElement("div");

        let extension = null;

        switch (logData.extension) {
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

        log.setAttribute("class", "file row");

        const newConainer = document.createElement("div");

        newConainer.setAttribute("class", "center-vertical col-8")
        log.appendChild(newConainer);

        const name = document.createElement("div");
        name.setAttribute("class", "text-start");
        name.innerHTML = extension + " " + logData.name;

        newConainer.appendChild(name);

        const hour = document.createElement("div");
        hour.setAttribute("class", "col-2 text-center");
        hour.innerHTML = logData.date;

        log.appendChild(hour);

        const actions = document.createElement("div");
        actions.setAttribute("class", "col-2 text-center");
        actions.innerHTML = logData.action;

        log.appendChild(actions);
        logs.appendChild(log);

    });
}

const queryGetLogs = new Provider("routes/getLogs", null, null, "GET", renderlogs, false);
queryGetLogs.operate();