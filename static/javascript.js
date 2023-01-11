// This is needed so that flash messages are removed after a period of time!
setTimeout(() => {
    var resultbox = document.getElementById("messagebox");
    if (resultbox)
        resultbox.remove();
}, 5000);

$(document).ready(function() {
    if (localStorage.getItem("show-comments") && localStorage.getItem("show-comments") == getNumber(window.location.pathname)) {
        // We have previously clicked the comment button, so keep showing comment rows.
        $("#show-hide-comments").attr("aria-expanded", "true");
        $("#hiddendiv").attr("class", "collapse show");
    }

    $("#show-hide-comments").click(function() {
        localStorage.getItem("show-comments") 
            ? localStorage.removeItem("show-comments")
            : localStorage.setItem("show-comments", getNumber(window.location.pathname));
    });

    function getNumber(str) {
        return str.replace( /^\D+/g, '');
    };
});