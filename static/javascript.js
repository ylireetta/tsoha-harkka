// This is needed so that flash messages are removed after a period of time!
setTimeout(() => {
    var resultbox = document.getElementById("messagebox");
    if (resultbox)
        resultbox.remove();
}, 5000);