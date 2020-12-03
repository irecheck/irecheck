// credits to sajjansarkar: http://jsfiddle.net/sajjansarkar/zgcgq8cg/
// and Ana Tudor: https://stackoverflow.com/questions/12813573/position-icons-into-circle
// https://css-tricks.com/snippets/sass/placing-items-circle/




function makeCircle( idWrapper, imageList, translation, delta) ***REMOVED***
	var noOfCircles = imageList.length;
	/* equally divide 360 by the no of circles to be drawn */
	var degreeAngle = 360 / noOfCircles;
	/* get handle on the wrapper canvas */
	var wrapper = $("." + idWrapper + "-container");
	/* clear it first */
	wrapper.html("");
	/* initialize angle incrementer variable */
	var currAngle = delta;
	/* draw each circle at the specified angle */
	for (var i = 0; i < noOfCircles; i++) ***REMOVED***
		/* add to the wrapper */
		wrapper.append(getGroupDiv(idWrapper + "-" + i, currAngle, translation, imageList[i]));
		/* increment the angle incrementer */
		currAngle = currAngle + degreeAngle;
	***REMOVED***

***REMOVED***


/*
	Function returns a new DIV with the angles translation using CSS.
	It also applies a random color for fun.
	stole the CSS from :http://stackoverflow.com/questions/12813573/position-icons-into-circle
*/
function getGroupDiv(placeholderId, currAngle, translation, imageInfo) ***REMOVED***
	var div = ""
	
	div += "<div id='" + placeholderId + "' class='placeholder' name='" + placeholderId +"' ";
	div += "style='transform: rotate(" + currAngle + "deg) translate(" + translation + ") rotate(-" + currAngle + "deg);'>"
		
	if(imageInfo[0].length)***REMOVED***
		div += "<img src='" + imageInfo[0] + "' width='100\%' alt='" + imageInfo[1] +"' ";
		div += "onClick='groupButtonClick(\""+ placeholderId +"\")' ondblclick='groupButtonDblClick(\""+ placeholderId +"\")' />"
	***REMOVED***
	else
		div += "<p>" + imageInfo[1] + "</p>";
		
	div += "</div>"
	
	return div
***REMOVED***



function getRandomColor() ***REMOVED***
	var letters = '0123456789ABCDEF'.split('');
	var color = '#';
	for (var i = 0; i < 6; i++) ***REMOVED***
		color += letters[Math.floor(Math.random() * 16)];
	***REMOVED***
	return color;
***REMOVED***



function makeCircularCommandList(idCommandsWrapper, commandsList, translation, delta) ***REMOVED***
	var wrapper = $("." + idCommandsWrapper + "-container");
	wrapper.html("");
	
	for( var g_id = 0; g_id < commandsList.length; g_id++) ***REMOVED***
		var color = commandsList[g_id][0];

		var noOfCircles = commandsList[g_id][1].length;
		var degreeAngle = 360.0 / 10.0;
		var currAngle =  360/commandsList.length * g_id + delta; //delta;
		
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) ***REMOVED***
			var id = idCommandsWrapper + "-" + g_id + "-" + c_id
			commandsHTML = "";
			commandsHTML += "<div id='" + id + "' class='" + idCommandsWrapper + "-element" + "' name='" + id +"' "
			commandsHTML += "style='background-color: " + color + "; transform: rotate(" + currAngle + "deg) translate(" + translation + ") rotate(-" + currAngle + "deg);' "
			commandsHTML += "onClick='commandButtonClick("+ g_id + "," + c_id +")' ";
			commandsHTML += ">";
			commandsHTML += commandsList[g_id][1][c_id][0];
			commandsHTML += "</div>";
			wrapper.append(commandsHTML);
			currAngle = currAngle + degreeAngle;
		***REMOVED***
	***REMOVED***
***REMOVED***








function makeCommandList(idCommandsWrapper) ***REMOVED***
	var wrapper = $("." + idCommandsWrapper + "-container");
	wrapper.html("");
	
	for( var g_id = 0; g_id < commandsList.length; g_id++) ***REMOVED***
		var color = commandsList[g_id][0];
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) ***REMOVED***
			var id = idCommandsWrapper + "-" + g_id + "-" + c_id
			commandsHTML = "";
			commandsHTML += "<div id='" + id + "' class='"  + "' name='" + id +"' " ; /*+ idCommandsWrapper + "-element" */
			commandsHTML += "style='background-color: " + color + "' ";
			commandsHTML += "onClick='commandButtonClick("+ g_id + "," + c_id +")' ";
			commandsHTML += ">";
			commandsHTML += commandsList[g_id][1][c_id][0];
			commandsHTML += "</div>";
			wrapper.append(commandsHTML);
		***REMOVED***
	***REMOVED***
***REMOVED***

function makeSpinner( idSpinnerWrapper) ***REMOVED***
	var wrapper = $("#" + idSpinnerWrapper + "-container");
	wrapper.html("");

	commandsHTML = "<img src='static/images/spinner.gif'/>"
	wrapper.append(commandsHTML);
***REMOVED***


function hideEverything() ***REMOVED***	
	for( var i = 0; i < infoList.length; i++) ***REMOVED***
		$("#group-info-" + i).hide();
		$("#group-text-" + i).hide();
	***REMOVED***
	
	var idCommandsWrapper = "commands-list";

	for( var g_id = 0; g_id < commandsList.length; g_id++)
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) ***REMOVED***
			var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
				$(id).hide();
		***REMOVED***
		
	hideSpinner();
	//$("#spinner-container").hide();
***REMOVED***


function showInfo() ***REMOVED***
	var idCommandsWrapper = "commands-list";
	for( var g_id = 0; g_id < commandsList.length; g_id++)
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) ***REMOVED***
			var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
				$(id).hide();
		***REMOVED***


	var visible = false;
	for( var g_id = 0; g_id < infoList.length; g_id++)
		if($("#group-text-" + g_id).is(":visible")) ***REMOVED***
			visible = true;
			break;
		***REMOVED***
	
	if(visible)
		for( var g_id = 0; g_id < infoList.length; g_id++) ***REMOVED***
			$("#group-info-" + g_id).hide();
			$("#group-text-" + g_id).hide();
		***REMOVED***
	else
		for( var g_id = 0; g_id < infoList.length; g_id++) ***REMOVED***
			$("#group-info-" + g_id).show();
			$("#group-text-" + g_id).show();
		***REMOVED***
***REMOVED***



function groupButtonClick( placeholderId ) ***REMOVED***
	var idCommandsWrapper = "commands-list";
	for( var g_id = 0; g_id < commandsList.length; g_id++)
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) ***REMOVED***
			var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
				$(id).hide();
		***REMOVED***

	var visible = false;
	for( var g_id = 0; g_id < infoList.length; g_id++)
		if($("#group-text-" + g_id).is(":visible")) ***REMOVED***
			visible = true;
			break;
		***REMOVED***
	
	var buttonId = placeholderId.split("-")[2];

	if(visible)
		for( var g_id = 0; g_id < infoList.length; g_id++) ***REMOVED***
			if(g_id != buttonId) ***REMOVED***
				$("#group-info-" + g_id).hide();
				$("#group-text-" + g_id).hide();
			***REMOVED***
		***REMOVED***

	$("#group-info-" + buttonId).toggle();
	$("#group-text-" + buttonId).toggle();
***REMOVED***


function groupButtonDblClick( placeholderId ) ***REMOVED***
	for( var g_id = 0; g_id < infoList.length; g_id++) ***REMOVED***
		$("#group-info-" + g_id).hide();
		$("#group-text-" + g_id).hide();
	***REMOVED***
	
	var idCommandsWrapper = "commands-list";
	var group_id = placeholderId.split("-")[2];
	for( var g_id = 0; g_id < commandsList.length; g_id++)
		if(g_id != group_id)
			for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) ***REMOVED***
				var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
				$(id).hide();
			***REMOVED***

	g_id = group_id;
	for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) ***REMOVED***
		var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
			$(id).toggle();
	***REMOVED***

***REMOVED***

// this will send data to flask
var busy = false;
var busyTime = 10000;
function commandButtonClick( g_id, c_id) ***REMOVED***
	if(busy) return;

	$("#spinner-container").css('visibility', 'visible');
	busy = true;
	setCommandListOpacity("50%");
	setTimeout(hideSpinner, busyTime);

	command = commandsList[g_id][1][c_id];
	//alert(command);
	const url_path = "/woz";
	var xhttp = new XMLHttpRequest();

	// the data sent to flask
	var payload = ***REMOVED*** "group_id": g_id,
					"control_id": c_id,
					"command": command [1],
					"text": command[0],
					***REMOVED***;

					
	$.ajax(***REMOVED***
		type: "POST", // HTTP method POST or GET
		contentType: 'application/json; charset=utf-8', //content type
		url: url_path, //Where to make Ajax calls
		dataType:'json', // Data type, HTML, json etc.
		processData: false,
		data: JSON.stringify(payload), 
	***REMOVED***).done(
		function(data) ***REMOVED***
			console.log(data);
		***REMOVED***
	);
	
***REMOVED***

function hideSpinner() ***REMOVED***
	$("#spinner-container").css('visibility', 'hidden');
	setCommandListOpacity("100%");
	busy = false;
***REMOVED***

function setCommandListOpacity( opacity) ***REMOVED***
	var idCommandsWrapper = "commands-list";

	for( var g_id = 0; g_id < commandsList.length; g_id++)
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) ***REMOVED***
			var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
			$(id).css('opacity', opacity);
		***REMOVED***
***REMOVED***



