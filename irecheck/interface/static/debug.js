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
            $("<span>ARRIVED! </span>")
                .appendTo("#newDynamicoData")
                .css("color", "green")
                .fadeOut(3000);
            
            $("#historyLast10").html(data.latestHistory);
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