$(document).ready(function(){

    $("#rawUD").hide();

    am4core.ready(function() {

        var intervalID = setInterval(dynamicUpdate, 1000);

    });

    $("#debug").click(function(){
        $.get("util", function(data, status){
            alert(data);
        });
    });

    $("#toRaw").click(function(){
        $("#visualData").hide();
        $("#rawUD").show();
        $.get("history/raw", function(data, status){
            $("#rawTable").html(data);
        });
    });

    $("#toVisual").click(function(){
        $("#rawUD").hide();
        $("#visualData").show();
    });

});

function dynamicUpdate() {
    $.get("history/dynamic", function(data, status){
        if(data.shouldUpdate) {
            var nWin = data.nSuccess;
            winLossChart(nWin, data.size - nWin);
            levelChart(data.levels);
            activityChart(data.activity);
            // $("#history").html(data.historyTable);
        }
    });
}

function activityChart(activity) {
    var activityChart = am4core.create("activityChart", am4charts.PieChart);

    var title = activityChart.titles.create();
    title.text = "Activites:"

    activityChart.data = [ {
        "activity": "STATIC",
        "number": activity[0]
    }, {
        "activity": "TILT",
        "number": activity[1]
    }, {
        "activity": "PRESSURE",
        "number": activity[2]
    }, {
        "activity": "KINEMATIC",
        "number": activity[3]
    }
    ];

    var activitySeries = activityChart.series.push(new am4charts.PieSeries());
    activitySeries.dataFields.value = "number";
    activitySeries.dataFields.category = "activity";

    activitySeries.slices.template.stroke = am4core.color("black");
    activitySeries.slices.template.strokeWidth = 2;
    activitySeries.slices.template.strokeOpactiy = 1;
}

function winLossChart(win, loss) {
    var winLossChart = am4core.create("winLossChart", am4charts.PieChart);

    winLossChart.data = [ {
        "result": "Win",
        "number": win
    }, {
        "result": "Fail",
        "number": loss
    }
    ];

    var winLossSeries = winLossChart.series.push(new am4charts.PieSeries());
    winLossSeries.dataFields.value = "number";
    winLossSeries.dataFields.category = "result";
}

function levelChart(levels) {
    var levelChart = am4core.create("levelChart", am4charts.PieChart);

    levelChart.data = [ {
        "level": 1,
        "number": levels[0]
    }, {
        "level": 2,
        "number": levels[1]
    }, {
        "level": 3,
        "number": levels[2]
    }, {
        "level": 4,
        "number": levels[3]
    }, {
        "level": 5,
        "number": levels[4]
    }
    ];

    var levelSeries = levelChart.series.push(new am4charts.PieSeries());
    levelSeries.dataFields.value = "number";
    levelSeries.dataFields.category = "level";
}