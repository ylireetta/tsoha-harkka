// This is needed so that flash messages are removed after a period of time!
setTimeout(() => {
    var resultbox = document.getElementById("messagebox");
    if (resultbox)
        resultbox.remove();
}, 5000);

$(document).ready(function() {
    var nextIndex = 1;

    if (localStorage.getItem("show-comments") && localStorage.getItem("show-comments") == getNumber(window.location.pathname)) {
        // We have previously clicked the comment button, so keep showing comment rows.
        $("#show-hide-comments").attr("aria-expanded", "true");
        $("#hiddendiv").attr("class", "collapse show");
    }

    $("#show-hide-comments").click(function() {
        localStorage.getItem("show-comments") == getNumber(window.location.pathname)
            ? localStorage.removeItem("show-comments")
            : localStorage.setItem("show-comments", getNumber(window.location.pathname));
    });

    $("#submit-template").click(function() {
        // If the user submits the form without clicking the button that adds table rows, trigger that click here.
        if ($("#selection-data tr").length < 1)
            $("#finalize-selection").trigger("click");
    });

    function getNumber(str) {
        return str.replace( /^\D+/g, '');
    };

    $("#finalize-selection").click(function() {
        // Get selected move ids from dropdown select and pair them with move names.
        var selectedIds = $("#selected-moves").val();
        
        if (selectedIds) {
            var selectedText = [];
        
            $("#selected-moves option:selected").each(function() {
                var selText = $(this).text();
                selectedText.push(selText);
            });
    
            $.each(selectedIds, function(i, val) {
                addTableRow(selectedText[i], val);
            });
        }
    });

    $("#selection-data").on("click", "button[name=remove-row]", function() {
        $(this).closest("tr").remove();
    });

    function addTableRow(moveName, moveId) {
        $("#selection-data").append("\
            <tr>\
                <td>\
                    <input type='hidden' name='selected-move-id' value='" + moveId + "'>" + moveName + "\
                </td>\
                <td>\
                    <input type='number' name='sets' id='sets" + nextIndex +"' min='1' value='1' required>\
                </td>\
                <td>\
                <button type='button' class='btn btn-link' name='remove-row'>Remove</button>\
                </td>\
            </tr>");

            nextIndex++;
    };
});