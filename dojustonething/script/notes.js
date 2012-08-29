var api = function(fname, args, success) {
    $.ajax({url: "/api/" + fname,
        type: "post",
        data: {args: JSON.stringify(args)},
        success: success,
        error: function(result) {
            alert("addthing error");
        }
    });
};
api.vars = {};


$(document).ready(function() {



    $("#addthing").click(function() {
        api.vars.a=3;
        api.vars.b=4;
        api.vars.c = 100;
        api("multiply", [api.vars.a, api.vars.b], function(result) {
            alert(api.vars.c + result);
            alert(api.vars.c + result + 1);
        });
    });


    function sayHello2() {
      var text = 0;
      var sayAlert = function() {
        text += 1;
        alert(text);
      };
      var sayAlert2 = function() {
        text += 2;
        alert(text);
      };
      return [sayAlert, sayAlert2];
    }

    var encloseda = sayHello2();
    var enclosed = encloseda[0];
    var enclosed2 = encloseda[1];
    enclosed();
    enclosed2();
    enclosed();
    enclosed2();

    // both = enclosed[0];
    // justb = enclosed[1];
    // alert(both());
    // alert(justb());
    // alert(both());
    // alert(justb());


    // possible issues:
    // syntax chars in strings
    // vars with weird scope
    // different kinds of subscope
    // subclosures?
    if(false) {
        $("#addthing").click(function() {
            var a=3;
            var b=4;
            var c = api.multiply(a, b);
            alert(c);
            alert(c+1);
            alert(api.multiply_by_4(c));
        });
    }
    // Pull var declarations to top
    if(false) {
        $("#addthing").click(function() {
            var a;
            var b;
            var c;
            a=3;
            b=4;
            c = api.multiply(a, b);
            alert(c);
            alert(c+1);
            alert(api.multiply_by_4(c));
        });
    }
    // Split logic up into subfunctions split by  api calls
    // The return value of each subfunction except the last is the args
    // to the API call and the name of the API call
    // The args to each subfunction except the first are the return value
    // of the API call; args to first are null
    if(false) {
        $("#addthing").click(function() {
            var a;
            var b;
            var c;
            var __api_subfunctions = [];
            __api_subfunctions.push(function() {
                a=3;
                b=4;
                return ["multiply", a, b];
            });
            __api_subfunctions.push(function(result) {
                c = result;
                alert(c);
                alert(c+1);
                return ["multiply_by_4", c];
            });
            __api_subfunctions.push(function(result) {
                alert(result);
            });
        });
    }
    // Give the subfunctions and everything their own closure
    // of the API call; args to first are null
    if(false) {
        $("#addthing").click(function() {
            var __api_encloser = function() {
                var a;
                var b;
                var c;
                var __api_subfunctions = [];
                __api_subfunctions.push(function() {
                    a=3;
                    b=4;
                    return ["multiply", a, b];
                });
                __api_subfunctions.push(function(result) {
                    c = result;
                    alert(c);
                    alert(c+1);
                    return ["multiply_by_4", c];
                });
                __api_subfunctions.push(function(result) {
                    alert(result);
                });
                return __api_subfunctions;
            };
            __api_subfunctions = __api_encloser();
        });
    }
    // Iterate through all the functions
    if(false) {
        $("#addthing").click(function() {
            var __api_encloser = function() {
                var a;
                var b;
                var c;
                var __api_subfunctions = [];
                __api_subfunctions.push(function(result) {
                    a=3;
                    b=4;
                    return ["multiply", [a, b]];
                });
                __api_subfunctions.push(function(result) {
                    c = result;
                    alert(c);
                    alert(c+1);
                    return ["multiply_by_4", [c]];
                });
                __api_subfunctions.push(function(result) {
                    alert(result);
                    return ["__done"];
                });
                return __api_subfunctions;
            };
            var __api_subfunctions = __api_encloser();
            var __result = [];
            var __i = 0;

            var __next_step = function(__result) {
                var __output = __api_subfunctions[__i](__result);
                if(__output[0] != "__done") {
                    $.ajax({url: "/api/" + __output[0],
                        type: "post",
                        data: {args: JSON.stringify(__output[1])},
                        success: function(result) {
                            __i += 1;
                            __next_step(__i, result);
                        },
                        error: function(result) {
                            alert("error! Add debug info?");
                        }
                    });

                }
            };
        });
    }

});


