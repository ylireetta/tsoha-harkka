setTimeout(() => {
    var resultbox = document.getElementById("messagebox");
    if (resultbox)
        resultbox.remove();
}, 5000);


function toggleVisibility(elementId) {
    var element = document.getElementById(elementId);

    // Display is <empty string> on the first click. Make display block in that case, also.
    element.style.display === "none" || element.style.display === "" 
        ? element.style.display = "block" 
        : element.style.display = "none"
}