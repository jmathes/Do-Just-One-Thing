$(document).ready(function() {
    var compare = function(newthing, benchmark) {
        var draw_button = function(selector, newthing, benchmark,
                                is_newthing_button) {
            if (is_newthing_button) {
                label = newthing.task;
            } else {
                label = benchmark.task;

            }
            $(selector).button({
                label: label,
                disabled: false
            });
            $(selector).click(function() {
                if (is_newthing_button) {
                    newthing.lower_bound = benchmark.urgency;
                } else {
                    newthing.upper_bound = benchmark.urgency;
                }
            });
            window.api("addtask", [newthing], thing_added);
            $("#compare_dialog").dialog("close");

        };
        draw_button("#newthing_task", newthing, benchmark, true);
        draw_button("#benchmark_task", newthing, benchmark, false);
        $(".comparison").addClass("comparison");
        $("#compare_dialog").dialog("open");
    };

    var thing_added = function(response) {
        console.log(response);
        if (response.success) {
            $("#thing-to-do").text(response.top_item);
        } else {
            console.log(response);
            compare(response.newthing, response.benchmark);
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

