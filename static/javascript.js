$(document).ready(function() {
    // Get json supplied by Flask.
    var moves = appConfig.all_moves;

    // Multiselect allowed for dropdown lists.
    $(".selectpicker").selectpicker();

    // Add rows in training data view.
    $("#addBtn").click(function() {
        var options = "";

        // Loop through moves array and add select option for each element found.
        moves.forEach(element => {
            options += "<option value='" + element.id + "'>" + element.move_name + "</option>";
        });

        $("#selectedMoves").append("\
            <tr>\
                <td>\
                    <select name='selected_moves'>\
                        " + options +"\
                    </select>\
                </td>\
                <td>\
                    <input type='number' name='reps'>\
                </td>\
                <td>\
                    <input type='number' name='weights'>\
                </td>\
                <td>\
                <button type='button' class='btn btn-link' name='removeBtn'>Remove</button>\
                </td>\
            </tr>");
    });

    $("#trainingDataTable").on('click', 'button[name=removeBtn]', function () {
        $(this).closest('tr').remove();
    });
});
