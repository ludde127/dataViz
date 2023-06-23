function navigate(url) {
        console.log("Huh");
        document.location.href = url;
}

function toggleShow(elementId) {
        const element = document.getElementById(elementId);
        if (element.style.display === "none") {
                element.style.display = "inherit";
        } else {
                element.style.display = "none";
        }
}

function unixTimestampToDatetime(timestamp) {
        return new Date(timestamp * 1000) // Make it ms
}