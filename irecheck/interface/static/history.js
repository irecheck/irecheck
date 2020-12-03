$(document).ready(function()***REMOVED***

    $("#rawUD").hide();

    am4core.ready(function() ***REMOVED***

        var intervalID = setInterval(dynamicUpdate, 1000);

    ***REMOVED***);

    $("#debug").click(function()***REMOVED***
        $.get("util", function(data, status)***REMOVED***
            alert(data);
        ***REMOVED***);
    ***REMOVED***);

    $("#toRaw").click(function()***REMOVED***
        $("#visualData").hide();
        $("#rawUD").show();
        $.get("history/raw", function(data, status)***REMOVED***
            $("#rawTable").html(data);
        ***REMOVED***);
    ***REMOVED***);

    $("#toVisual").click(function()***REMOVED***
        $("#rawUD").hide();
        $("#visualData").show();
    ***REMOVED***);

***REMOVED***);

function dynamicUpdate() ***REMOVED***
    $.get("history/dynamic", function(data, status)***REMOVED***
        if(data.shouldUpdate) ***REMOVED***
            var nWin = data.nSuccess;
            winLossChart(nWin, data.size - nWin);
            levelChart(data.levels);
            activityChart(data.activity);
            // $("#history").html(data.historyTable);
        ***REMOVED***
    ***REMOVED***);
***REMOVED***

function activityChart(activity) ***REMOVED***
    var activityChart = am4core.create("activityChart", am4charts.PieChart);

    var title = activityChart.titles.create();
    title.text = "Activites:"

    activityChart.data = [ ***REMOVED***
        "activity": "STATIC",
        "number": activity[0]
    ***REMOVED***, ***REMOVED***
        "activity": "TILT",
        "number": activity[1]
    ***REMOVED***, ***REMOVED***
        "activity": "PRESSURE",
        "number": activity[2]
    ***REMOVED***, ***REMOVED***
        "activity": "KINEMATIC",
        "number": activity[3]
    ***REMOVED***
    ];

    var activitySeries = activityChart.series.push(new am4charts.PieSeries());
    activitySeries.dataFields.value = "number";
    activitySeries.dataFields.category = "activity";

    activitySeries.slices.template.stroke = am4core.color("black");
    activitySeries.slices.template.strokeWidth = 2;
    activitySeries.slices.template.strokeOpactiy = 1;
***REMOVED***

function winLossChart(win, loss) ***REMOVED***
    var winLossChart = am4core.create("winLossChart", am4charts.PieChart);

    winLossChart.data = [ ***REMOVED***
        "result": "Win",
        "number": win
    ***REMOVED***, ***REMOVED***
        "result": "Fail",
        "number": loss
    ***REMOVED***
    ];

    var winLossSeries = winLossChart.series.push(new am4charts.PieSeries());
    winLossSeries.dataFields.value = "number";
    winLossSeries.dataFields.category = "result";
***REMOVED***

function levelChart(levels) ***REMOVED***
    var levelChart = am4core.create("levelChart", am4charts.PieChart);

    levelChart.data = [ ***REMOVED***
        "level": 1,
        "number": levels[0]
    ***REMOVED***, ***REMOVED***
        "level": 2,
        "number": levels[1]
    ***REMOVED***, ***REMOVED***
        "level": 3,
        "number": levels[2]
    ***REMOVED***, ***REMOVED***
        "level": 4,
        "number": levels[3]
    ***REMOVED***, ***REMOVED***
        "level": 5,
        "number": levels[4]
    ***REMOVED***
    ];

    var levelSeries = levelChart.series.push(new am4charts.PieSeries());
    levelSeries.dataFields.value = "number";
    levelSeries.dataFields.category = "level";
***REMOVED***