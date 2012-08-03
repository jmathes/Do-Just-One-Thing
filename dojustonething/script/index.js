var add_thing = function() {
    $.ajax({url: "/api/add",
            success: function(result) {
                alert(result.foo);
            },
            error: function(result) {
                alert("addthing error");
            }
        });
};

$(document).ready(function() {
    $("#addthing").click(add_thing);
});
