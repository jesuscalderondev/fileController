function formatCurrency(number) {

    const parts = number.split(",");
    let intPart = "";
    if (number.length > 0) {
        const clean = parts[0].split('.').join('');

        let counter = 0;
        for (let index = clean.length - 1; index >= 0; index--) {

            const element = clean[index];
            counter++;
            intPart = element + intPart;
            if (counter % 3 == 0 && index > 0) {
                intPart = "." + intPart;
            }
        }
    }

    return intPart;
}

function formatDate(dateString){
    const date = new Date(dateString);

    const monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    const day = date.getDate();
    const month = monthNames[date.getMonth()];
    const year = date.getFullYear();

    return `${day} de ${month} de ${year}`
}