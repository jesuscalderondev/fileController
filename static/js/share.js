const shareBtn = document.getElementById("btnSub");
const form = document.getElementById("form");

shareBtn.addEventListener("click", () => {
    shareBtn.disabled = true;


    const emails = document.getElementById("emails").value;
    const message = document.getElementById("message").value;

    const route = "routes/share";

    const body = {
        emails: emails,
        message: message,
        fileId : idFile
    }

    function sendMail(data) {
        console.log(data);
        form.reset();
    }

    const query = new Provider(route, body, shareBtn, "POST", sendMail, false, {}, false, true);
    query.operate();

});