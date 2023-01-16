$(document).ready(function() {
    var obs = new MutationObserver(function(mutations) {
        // mutations = basically an array of occurred mutations in the document.
        // Iterate through them to access the element we just added.

        mutations.forEach(oneMutation => {
            if (oneMutation.type === "childList") {
                var addedNodes = oneMutation.addedNodes;
                
                // Loop to find added table row.
                addedNodes.forEach(oneNode => {
                    if (oneNode.tagName === "TR") {
                        var children = oneNode.childNodes;

                        children.forEach(rowChild => {
                            if (rowChild.firstElementChild && rowChild.firstElementChild.tagName == "SELECT") {
                                // We found the added select list!
                                // Get id number of added element (basically select list id).
                                var addedElementId = parseNumberFromString(rowChild.firstElementChild.id);
                                var selectedValue = rowChild.firstElementChild.value;

                                var parentRow = $(rowChild.firstElementChild).parent().parent();
                                // Finally, get previous max weights from provided data.
                                setTableDefaultInput(selectedValue, addedElementId, parentRow);
                            }
                        });
                    }
                });
            }
        });
    });
    obs.observe(document, {attributes: false, childList: true, characterData: false, subtree:true});
    
    // Get json supplied by Flask.
    var moves = appConfig.all_moves;
    var maxWeights = appConfig.max_weights;
    var templates = appConfig.templates;

    var options = "";

    // Loop through moves array and add select option for each element found. This is used when adding new table rows.
    moves.forEach(element => {
        options += "<option value='" + element.id + "'>" + element.move_name + "</option>";
    });

    // When adding new table rows, use this variable as part of element id.
    var nextIndex = 1;

    // Add rows in training data view.
    $("#add-btn").click(function() {
        addTableRow();
    });

    $("#clear-btn").click(function() {
        $("#selected-moves").find("tr").remove();
    });

    $("body").on("change", ".move-select", function() {
        var parentRow = $(this).parent().parent();

        var selectedMoveId = parseInt($(this).val());
        var selectionIdNumber = parseNumberFromString(this.id);

        setTableDefaultInput(selectedMoveId, selectionIdNumber, parentRow);
    });

    $("#training-data-table").on("click", "button[name=remove-btn]", function() {
        $(this).closest("tr").remove();
    });

    $("#info-btn").tooltip().attr("title", "Moves that have been removed from the database will not be added to new training sessions.");

    $("#select-template").click(function() {
        // When this button is clicked, use the selected template as base for workout.
        // I.e., add each move in template as new row to data table. If template includes multiple sets of the same move, add rows.
        // Clear previous rows, if any.
        $("#selected-moves").find("tr").remove();
        
        var selectedTemplateId = parseInt($("#users-templates").val());

        // One template is basically a collection of move rows, connected by a common template id.
        var selectedTemplateRows = templates.filter(function(item) {
            return parseInt(item.id) === selectedTemplateId;
        });

        // Add however many table rows are needed and adjust move selections.
        selectedTemplateRows.forEach(row => {
            if (row.visible) {
                var number_of_sets = row.number_of_sets;
                
                for (var i = 1; i <= number_of_sets; i++) {
                    var indexToAdd = nextIndex;
                    addTableRow();
                    $("#select" + indexToAdd).val(row.move_id).change();
                }
            }
        });

    });

    function setTableDefaultInput(selectedMoveId, selectionIdNumber, parentRow) {
        var matchingRepsInput = parentRow.find("input[id='reps" + selectionIdNumber +"']");
        var matchingWeightsInput = parentRow.find("input[id='weights" + selectionIdNumber +"']");
    
        if (matchingRepsInput && matchingWeightsInput) {
            var finalReps = 1;
            var finalWeights = 0;

            var previousSet = maxWeights.filter(function(item) {
                return (parseInt(item.id) === parseInt(selectedMoveId));
            });
    
            if (previousSet.length > 0) {
                var previousData = previousSet[0]; // Returned an array, so get first object.
    
                finalReps = parseInt(previousData["reps"]);
                finalWeights = parseFloat(previousData["weights"]);
            }

            matchingRepsInput.val(finalReps);
            matchingWeightsInput.val(finalWeights);
        }
    };

    function parseNumberFromString(str) {
        return parseInt(str.replace( /^\D+/g, ''));
    };

    function addTableRow() {
        $("#selected-moves").append("\
            <tr>\
                <td class='col-6'>\
                    <select class='move-select form-control' name='selected-moves' id='select" + nextIndex + "'>\
                        " + options +"\
                    </select>\
                </td>\
                <td class='col-6'>\
                    <input type='number' class='form-control' name='reps' id='reps" + nextIndex +"' min='1' required>\
                </td>\
                <td class='col-6'>\
                    <input type='number' class='form-control' name='weights' id='weights" + nextIndex + "' min='0' step=0.25 required>\
                </td>\
                <td class='col-6'>\
                    <button type='button' class='btn btn-link' name='remove-btn'>Remove</button>\
                </td>\
            </tr>");

            nextIndex++;
    };
});
