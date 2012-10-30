$(document).ready(function() {
    var thing_added = function(response) {
        console.log(response);
        if (response.success) {
            $("#thing-to-do").text(response.top_item);
        } else {
            alert("Compare to " + response.compare_to);
        }
    };

    window.dialog = $("#dialog").dialog({
        buttons: { "Add": function() {
            var thingtodo = $("#newthing").val();
            window.api("addtask", [thingtodo], thing_added);
            $(this).dialog("close");
        } },
        height: 400,
        width: 450,
        autoOpen: false
    });

    $("#addthing").click(function() {
        // window.api("multiply", [3, 4], function(result) {
        //     alert(result);
        // });
        $("#dialog").dialog("open");
    });
});

