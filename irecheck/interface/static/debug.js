<<<<<<< HEAD
$(document).ready(function(){

    var intervalID = setInterval(dynamicUpdate, 1000);

    $("#decrement").click(function(){
        var counter = parseInt($("#counter").text(), 10);
        --counter;
        $("#counter").text(counter);
    });

    $("#increment").click(function(){
        var counter = parseInt($("#counter").text(), 10);
        ++counter;
        $("#counter").text(counter);
    });

    $("#sendFlask").click(function(){
        $.post("ros",
        {
            name: "Julian Blackwell",
            rosMessage: $("#textToFlask").val()
        },
        function(data, status){
            alert(data);
        });
    });

    $("#sendQTSay").click(function(){
        $.post("ros", 
        {
            name: "Julian Blackwell",
            rosMessage: "QTSAY",
            data: $("#QTSay").val()
        },
        function(data, status){
            //Callback here
        });
    });

    $(".langButton").click(function(){
        sendRobot("LANGUAGE", $(this).text());
    });

    $(".simButton").click(function(){
        sendRobot("SIM", $(this).text());
    });

    $(".stateButton").click(function(){
        sendRobot("STATE", $(this).text());
    });

});

function sendRobot(msg, toSend) {
    $.post("ros", 
    {
        rosMessage: msg,
        data: toSend
    }, function(data, status){
        //Callback here
    });
}

function dynamicUpdate() {
    $.get("debug/dynamic", function(data, status){
        if(data.newDynamico) {
=======
$(document).ready(function()***REMOVED***

    var intervalID = setInterval(dynamicUpdate, 1000);

    $("#decrement").click(function()***REMOVED***
        var counter = parseInt($("#counter").text(), 10);
        --counter;
        $("#counter").text(counter);
    ***REMOVED***);

    $("#increment").click(function()***REMOVED***
        var counter = parseInt($("#counter").text(), 10);
        ++counter;
        $("#counter").text(counter);
    ***REMOVED***);

    $("#sendFlask").click(function()***REMOVED***
        $.post("ros",
        ***REMOVED***
            name: "Julian Blackwell",
            rosMessage: $("#textToFlask").val()
        ***REMOVED***,
        function(data, status)***REMOVED***
            alert(data);
        ***REMOVED***);
    ***REMOVED***);

    $("#sendQTSay").click(function()***REMOVED***
        $.post("ros", 
        ***REMOVED***
            name: "Julian Blackwell",
            rosMessage: "QTSAY",
            data: $("#QTSay").val()
        ***REMOVED***,
        function(data, status)***REMOVED***
            //Callback here
        ***REMOVED***);
    ***REMOVED***);

    $(".langButton").click(function()***REMOVED***
        sendRobot("LANGUAGE", $(this).text());
    ***REMOVED***);

    $(".simButton").click(function()***REMOVED***
        sendRobot("SIM", $(this).text());
    ***REMOVED***);

    $(".stateButton").click(function()***REMOVED***
        sendRobot("STATE", $(this).text());
    ***REMOVED***);

***REMOVED***);

function sendRobot(msg, toSend) ***REMOVED***
    $.post("ros", 
    ***REMOVED***
        rosMessage: msg,
        data: toSend
    ***REMOVED***, function(data, status)***REMOVED***
        //Callback here
    ***REMOVED***);
***REMOVED***

function dynamicUpdate() ***REMOVED***
    $.get("debug/dynamic", function(data, status)***REMOVED***
        if(data.newDynamico) ***REMOVED***
>>>>>>> 8832a7b795d6e3fb29254763f5a2a25dadd29e4b
            $("<span>ARRIVED! </span>")
                .appendTo("#newDynamicoData")
                .css("color", "green")
                .fadeOut(3000);
            
            $("#historyLast10").html(data.latestHistory);
<<<<<<< HEAD
        }
        connectionStatus("#coreAval", data.coreAval);
        connectionStatus("#qtAval", data.qtAval);
        $("#debugScroll").append(data.newRobot);
    });
}

function connectionStatus(id, status) {
    if (status) {
        $(id).text("AVAILABLE").css("color", "green");
    } else {
        $(id).text("DISCONNECTED").css("color", "red");
    }
}
=======
        ***REMOVED***
        connectionStatus("#coreAval", data.coreAval);
        connectionStatus("#qtAval", data.qtAval);
        $("#debugScroll").append(data.newRobot);
    ***REMOVED***);
***REMOVED***

function connectionStatus(id, status) ***REMOVED***
    if (status) ***REMOVED***
        $(id).text("AVAILABLE").css("color", "green");
    ***REMOVED*** else ***REMOVED***
        $(id).text("DISCONNECTED").css("color", "red");
    ***REMOVED***
***REMOVED***
>>>>>>> 8832a7b795d6e3fb29254763f5a2a25dadd29e4b
