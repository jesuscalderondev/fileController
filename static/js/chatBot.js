const conversation = document.getElementById("files");

function formatText(text) {
    // Detectar dos asteriscos y reemplazar con <b>
    text = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

    text = text.replace(/\*(.*?)\./g, '<li>$1</li><br>');


    return text;
}


function writeText(text, container, index=0) {
    
    if (index < text.length) {
        setTimeout(() => {
            container.innerHTML = formatText(((index > 0) ? container.innerHTML : "")+ text[index]);

            writeText(text, container, index+1);
        }, 10);
        
    }
}

function questionAi(data) {
    const answer = data.data.answer;

    console.log(answer);

    const file = document.createElement("div");
    file.setAttribute("class", "row text-start bg-primary p-1 text-white mb-2 message-bubble2");
    file.innerHTML = writeText(answer, file);
    conversation.appendChild(file);
}
const question = document.getElementById("question");
const btnSub = document.getElementById("submit");

form.addEventListener("submit", (event) => {

    event.preventDefault();

    const file = document.createElement("div");
    file.setAttribute("class", "row text-end bg-white p-1 text-dark mb-2 message-bubble1");
    file.innerHTML = question.value;

    conversation.appendChild(file);

    const formdata = {
        "question": question.value
    };

    const query = new Provider("routes/questionAi", formdata, btnSub, "POST", questionAi, false);
    query.operate();

    form.reset()


});