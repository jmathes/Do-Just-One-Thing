$(document).ready(function() {
    window.task_id = -1;
    $("#newthing_task").click(function() {
        window.newthing.lower_bound = window.benchmark.urgency;
        window.api("add_task", [window.newthing], thing_added);
        $("#compare_dialog").dialog("close");
    });

    $("#benchmark_task").click(function() {
        window.newthing.upper_bound = window.benchmark.urgency;
        window.api("add_task", [window.newthing], thing_added);
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
            show_next_task(response.top_item);
        } else {
            window.newthing = response.newthing;
            window.benchmark = response.benchmark;
            compare();
        }
    };

    var show_next_task = function(thing) {
        window.task_id = thing['id'];
        $("#thing-to-do").text(thing['task']);
    };

    window.newthing_dialog = $("#newthing_dialog").dialog({
        buttons: { "Add": function() {
            var thingtodo = $("#newthing").val();
            window.api(
                "add_task",
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
        $("#newthing").attr("value", "");
        $("#newthing_dialog").dialog("open");
    });
    $("#delaything").click(function() {
        window.api(
            "delay_task",
            [window.task_id],
            show_next_task
        );
    });
    $("#didthing").click(function() {
        window.api(
            "did_task",
            [window.task_id],
            show_next_task
        );
    });

    window.api(
        "get_next_task",
        [],
        show_next_task
        );
});

