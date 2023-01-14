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
    var max_weights = appConfig.max_weights;
    var templates = appConfig.templates;

    var options = "";

    // Loop through moves array and add select option for each element found. This is used when adding new table rows.
    moves.forEach(element => {
        options += "<option value='" + element.id + "'>" + element.move_name + "</option>";
    });

    // When adding new table rows, use this variable as part of element id.
    var nextIndex = 1;

    // Multiselect allowed for dropdown lists.
    $(".selectpicker").selectpicker();

    // Add rows in training data view.
    $("#addBtn").click(function() {
        addTableRow();
    });

    $("#clearBtn").click(function() {
        $("#selectedMoves").find("tr").remove();
    });

    $("body").on("change", ".moveSelect", function() {
        var parentRow = $(this).parent().parent();

        var selectedMoveId = parseInt($(this).val());
        var selectionIdNumber = parseNumberFromString(this.id);

        setTableDefaultInput(selectedMoveId, selectionIdNumber, parentRow);
    });

    $("#trainingDataTable").on("click", "button[name=removeBtn]", function() {
        $(this).closest("tr").remove();
    });

    $("#infoBtn").tooltip().attr("title", "Moves that have been removed from the database will not be added to new training sessions.");

    $("#selectTemplate").click(function() {
        // When this button is clicked, use the selected template as base for workout.
        // I.e., add each move in template as new row to data table. If template includes multiple sets of the same move, add rows.
        // Clear previous rows, if any.
        $("#selectedMoves").find("tr").remove();
        
        var selectedTemplateId = parseInt($("#usersTemplates").val());

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

            var previousSet = max_weights.filter(function(item) {
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
        $("#selectedMoves").append("\
            <tr>\
                <td>\
                    <select class='moveSelect' name='selected_moves' id='select" + nextIndex + "'>\
                        " + options +"\
                    </select>\
                </td>\
                <td>\
                    <input type='number' name='reps' id='reps" + nextIndex +"' min='1' required>\
                </td>\
                <td>\
                    <input type='number' name='weights' id='weights" + nextIndex + "' min='0' step=0.25 required>\
                </td>\
                <td>\
                <button type='button' class='btn btn-link' name='removeBtn'>Remove</button>\
                </td>\
            </tr>");

            nextIndex++;
    };
});
