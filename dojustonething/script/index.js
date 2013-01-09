$(document).ready(function() {
    $("#newthing_task").click(function() {
        window.newthing.lower_bound = window.benchmark.urgency;
        window.api("addtask", [window.newthing], thing_added);
        $("#compare_dialog").dialog("close");
    });

    $("#benchmark_task").click(function() {
        window.newthing.upper_bound = window.benchmark.urgency;
        window.api("addtask", [window.newthing], thing_added);
        $("#compare_dialog").dialog("close");
    });

    var compare = function() {
        var draw_button = function(selector, is_newthing_button) {
            if (is_newthing_button) {
                label = window.newthing.task;
            } else {
                label = window.benchmark.task;

            }
            $(selector).button({
                label: label,
                disabled: false
            });
        };
        draw_button("#newthing_task", true);
        draw_button("#benchmark_task", false);
        $(".comparison").addClass("comparison");
        $("#compare_dialog").dialog("open");
    };

    var thing_added = function(response) {
        if (response.success) {
            $("#thing-to-do").text(response.top_item);
        } else {
            window.newthing = response.newthing;
            window.benchmark = response.benchmark;
            compare();
        }
    };

    window.newthing_dialog = $("#newthing_dialog").dialog({
        buttons: { "Add": function() {
            var thingtodo = $("#newthing").val();
            window.api(
                "addtask",
                [{
                    task: thingtodo,
                    upper_bound: null,
                    lower_bound: null
                }],
                thing_added
            );
            $(this).dialog("close");
        } },
        height: 400,
        width: 450,
        autoOpen: false
    });

    window.compare_dialog = $("#compare_dialog").dialog({
        height: 400,
        width: 450,
        autoOpen: false
    });

    $("#addthing").click(function() {
        $("#newthing").text("");
        $("#newthing_dialog").dialog("open");
    });
});

