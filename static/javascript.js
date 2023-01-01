setTimeout(() => {
    var resultbox = document.getElementById("messagebox");
    if (resultbox)
        resultbox.remove();
}, 5000);

// Multiselect allowed for dropdown lists.
$(document).ready(function() {
    $(".selectpicker").selectpicker();
});