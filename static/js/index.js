const images = document.getElementById("images");
const indicators = document.getElementById("indicators");

function renderEvent(data) {
    const eventData = data.data.event;
    console.log(data.data.event);
    let index;


    eventData.medias.forEach(img => {

        let textTitle = null;
        let href = null;
        let textLink = null;

        const item = document.createElement("div");
        item.setAttribute("class", "carousel-item");

        const indicator = document.createElement("button");
        indicator.setAttribute("data-bs-target", "#carousel");
        indicator.setAttribute("data-bs-slide-to", "" + eventData.medias.indexOf(img));

        const info = document.createElement("div");
        info.setAttribute("class", "carousel-caption d-none d-md-block");
        
        const title = document.createElement("h1");
        const description = document.createElement("p");
        const link = document.createElement("a");
        link.setAttribute("class", "btn btn-primary semi-circle");
        
        index = eventData.medias.indexOf(img);

        switch (index) {
            case 0:
                console.log(index);
                
                item.classList.add("active");
                indicator.classList.add("active");
                indicator.setAttribute("aria-current", true);
                textTitle = eventData.name;
                description.innerHTML = eventData.description;
                href = "#moreInfo";
                textLink = "Saber más";
                break;
            case 1:
                textTitle = "Adquiere tu carnet";
                description.innerHTML = "Hazte con tu carnet para tener acceso a la variedad de actividades y ponencias.";
                textLink =  "Adquirir - <span class='bi bi-bag-heart'></span>";
                href = "/pricesPhases";
                break;
            default:
                textTitle = "Defecto";
        }
        link.setAttribute("href", href)
        link.innerHTML = textLink;
        title.innerHTML = "<b>" + textTitle + "</b>";

        title.setAttribute("class", "entry-left-ob");
        description.setAttribute("class", "entry-right-ob");

        info.appendChild(title);
        info.appendChild(description);
        info.appendChild(link);

        item.appendChild(info);

        indicators.appendChild(indicator);

        const source = document.createElement("img");
        source.src = production + "sources/" + img.route;
        source.alt = "Una imagen de portada";
        source.setAttribute("class", "d-block w-100");

        item.appendChild(source);
        images.appendChild(item);
    });
}

const test = document.getElementById("texto-animado");

writeText("Si estamos en fase de prueba de funciones visuales", test)

function writeText(text, container, index=0) {
    
    if (index < text.length) {
        setTimeout(() => {
            container.innerHTML += text[index];

            writeText(text, container, index+1);
        }, 50);
        
    }
}

const eventQuery = new Provider("admin/getEventCurrent", null, null, "GET", renderEvent, null, {}, null);
eventQuery.operate();