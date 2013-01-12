if (!window.api) {
    window.api = function(fname, args, success) {
        $.ajax({url: "/api/" + fname,
            type: "post",
            data: {args: JSON.stringify(args)},
            success: success,
            error: function(result) {
                console.log(result);
                alert("Something went wrong. Sorry");
            }
        });
    };
}
