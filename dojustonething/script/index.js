$(document).ready(function() {
    window.dialog = $("#dialog").dialog({
        buttons: { "Add": function() {
            console.log($("#newthing").val());
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

