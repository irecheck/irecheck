// credits to sajjansarkar: http://jsfiddle.net/sajjansarkar/zgcgq8cg/
// and Ana Tudor: https://stackoverflow.com/questions/12813573/position-icons-into-circle
// https://css-tricks.com/snippets/sass/placing-items-circle/




function makeEllipse( idWrapper, imageList, a, b, delta) {
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
	for (var i = 0; i < noOfCircles; i++) {
		/* add to the wrapper */
		angle = currAngle * Math.PI/180
		translationY = Math.sin(angle)*b
		translationX = Math.cos(angle)*a
		wrapper.append(getGroupDiv(idWrapper + "-" + i, translationX, translationY, imageList[i]));
		/* increment the angle incrementer */
		currAngle = currAngle + degreeAngle;
	}

}

function makeEllipseExact( idWrapper, imageList, ellipseList) {
	var noOfCircles = imageList.length;
	/* equally divide 360 by the no of circles to be drawn */
	var degreeAngle = 360 / noOfCircles;
	/* get handle on the wrapper canvas */
	var wrapper = $("." + idWrapper + "-container");
	/* clear it first */
	wrapper.html("");
	/* initialize angle incrementer variable */
	// var currAngle = delta;
	/* draw each circle at the specified angle */
	for (var i = 0; i < noOfCircles; i++) {
		/* add to the wrapper */
		cordinate = ellipseList[i];
		translationY = cordinate[1];
		translationX = cordinate[0];
		wrapper.append(getGroupDiv(idWrapper + "-" + i, translationX, translationY, imageList[i]));
		/* increment the angle incrementer */
		// currAngle = currAngle + degreeAngle;
	}

}


/*
	Function returns a new DIV with the angles translation using CSS.
	It also applies a random color for fun.
	stole the CSS from :http://stackoverflow.com/questions/12813573/position-icons-into-circle
*/
function getGroupDiv(placeholderId, translationX, translationY, imageInfo) {
	var div = ""
	
	div += "<div id='" + placeholderId + "' class='placeholder' name='" + placeholderId +"' ";
	// div += "style='transform: rotate(" + currAngle + "deg) translate(" + translation + ") rotate(-" + currAngle + "deg);'>"
	div += "style='transform:  translate(" + translationX + "em, " + translationY + "em);'>"	
	if(imageInfo[0].length){
		div += "<img src='" + imageInfo[0] + "' width='100\%' alt='" + imageInfo[1] +"' ";
		div += "onClick='groupButtonClick(\""+ placeholderId +"\")' ondblclick='groupButtonDblClick(\""+ placeholderId +"\")' />"
	}
	else
		div += "<p>" + imageInfo[1] + "</p>";
		
	div += "</div>"
	
	return div
}



function getRandomColor() {
	var letters = '0123456789ABCDEF'.split('');
	var color = '#';
	for (var i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}



function makeCircularCommandList(idCommandsWrapper, commandsList, ellipseList) {
	var wrapper = $("." + idCommandsWrapper + "-container");
	wrapper.html("");
	
	for( var g_id = 0; g_id < commandsList.length; g_id++) {
		var color = commandsList[g_id][0];

		// var noOfCircles = commandsList[g_id][1].length;

		
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) {
			var id = idCommandsWrapper + "-" + g_id + "-" + c_id
			if (g_id + c_id < commandsList.length) {
				n = g_id + c_id; 
			} else {
				n = g_id + c_id - commandsList.length;
			}

			cordinate = ellipseList[n];
			translationY = cordinate[1];
			translationX = cordinate[0];
			commandsHTML = "";
			commandsHTML += "<div id='" + id + "' class='" + idCommandsWrapper + "-element" + "' name='" + id +"' ";
			commandsHTML += "style='background-color: " + color + "; transform:  translate(" + translationX + "em, " + translationY + "em);' ";
			commandsHTML += "onClick='commandButtonClick("+ g_id + "," + c_id +")' ";
			commandsHTML += ">";
			commandsHTML += commandsList[g_id][1][c_id][0];
			commandsHTML += "</div>";
			wrapper.append(commandsHTML);
			// currAngle = currAngle + degreeAngle;
		}
	}
}





function makeCommandList(idCommandsWrapper) {
	var wrapper = $("." + idCommandsWrapper + "-container");
	wrapper.html("");
	
	for( var g_id = 0; g_id < commandsList.length; g_id++) {
		var color = commandsList[g_id][0];
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) {
			var id = idCommandsWrapper + "-" + g_id + "-" + c_id
			commandsHTML = "";
			commandsHTML += "<div id='" + id + "' class='"  + "' name='" + id +"' " ; /*+ idCommandsWrapper + "-element" */
			commandsHTML += "style='background-color: " + color + "' ";
			commandsHTML += "onClick='commandButtonClick("+ g_id + "," + c_id +")' ";
			commandsHTML += ">";
			commandsHTML += commandsList[g_id][1][c_id][0];
			commandsHTML += "</div>";
			wrapper.append(commandsHTML);
		}
	}
}

function makeSpinner( idSpinnerWrapper) {
	var wrapper = $("#" + idSpinnerWrapper + "-container");
	wrapper.html("");

	commandsHTML = "<img src='static/images/spinner.gif'/>"
	wrapper.append(commandsHTML);
}


function hideEverything() {	
	for( var i = 0; i < infoList.length; i++) {
		$("#group-info-" + i).show();
		$("#group-text-" + i).show();
	}
	
	var idCommandsWrapper = "commands-list";

	for( var g_id = 0; g_id < commandsList.length; g_id++)
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) {
			var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
				$(id).hide();
		}
		
	hideSpinner();
	//$("#spinner-container").hide();
}


function showInfo() {
	var idCommandsWrapper = "commands-list";
	for( var g_id = 0; g_id < commandsList.length; g_id++)
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) {
			var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
				$(id).hide();
		}


	var visible = false;
	for( var g_id = 0; g_id < infoList.length; g_id++)
		if($("#group-text-" + g_id).is(":visible")) {
			visible = true;
			break;
		}
	
	if(visible)
		for( var g_id = 0; g_id < infoList.length; g_id++) {
			$("#group-info-" + g_id).hide();
			$("#group-text-" + g_id).hide();
		}
	else
		for( var g_id = 0; g_id < infoList.length; g_id++) {
			$("#group-info-" + g_id).show();
			$("#group-text-" + g_id).show();
		}
}



function groupButtonClick( placeholderId ) {
	var idCommandsWrapper = "commands-list";
	for( var g_id = 0; g_id < commandsList.length; g_id++)
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) {
			var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
				$(id).hide();
		}

	var visible = false;
	for( var g_id = 0; g_id < infoList.length; g_id++)
		if($("#group-text-" + g_id).is(":visible")) {
			visible = true;
			break;
		}
	
	var buttonId = placeholderId.split("-")[2];

	if(visible)
		for( var g_id = 0; g_id < infoList.length; g_id++) {
			if(g_id != buttonId) {
				$("#group-info-" + g_id).hide();
				$("#group-text-" + g_id).hide();
			}
		}

	$("#group-info-" + buttonId).toggle();
	$("#group-text-" + buttonId).toggle();
}


function groupButtonDblClick( placeholderId ) {
	for( var g_id = 0; g_id < infoList.length; g_id++) {
		$("#group-info-" + g_id).hide();
		$("#group-text-" + g_id).hide();
	}
	
	var idCommandsWrapper = "commands-list";
	var group_id = placeholderId.split("-")[2];
	for( var g_id = 0; g_id < commandsList.length; g_id++)
		if(g_id != group_id)
			for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) {
				var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
				$(id).hide();
			}

	g_id = group_id;
	for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) {
		var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
			$(id).toggle();
	}

}

// this will send data to flask
var busy = false;
function commandButtonClick( g_id, c_id) {
	if(busy) return;
	command = commandsList[g_id][1][c_id];
	busytime = command[2]*1000;
	$("#spinner-container").css('visibility', 'visible');
	busy = true;
	setCommandListOpacity("50%");
	setTimeout(hideSpinner, busytime);

	
	//alert(command);
	const url_path = "/woz";
	var xhttp = new XMLHttpRequest();

	// the data sent to flask
	var payload = { "group_id": g_id,
					"control_id": c_id,
					"command": command[1],
					"text": command[0],
					};
					
	$.ajax({
		type: "POST", // HTTP method POST or GET
		contentType: 'application/json; charset=utf-8', //content type
		url: url_path, //Where to make Ajax calls
		dataType:'json', // Data type, HTML, json etc.
		processData: false,
		data: JSON.stringify(payload), 
	}).done(
		function(data) {
			console.log(data);
		}
	);
	
}

function hideSpinner() {
	$("#spinner-container").css('visibility', 'hidden');
	setCommandListOpacity("100%");
	busy = false;
}

function setCommandListOpacity( opacity) {
	var idCommandsWrapper = "commands-list";

	for( var g_id = 0; g_id < commandsList.length; g_id++)
		for( var c_id = 0; c_id < commandsList[g_id][1].length; c_id++) {
			var id = "#" + idCommandsWrapper + "-" + g_id + "-" + c_id;
			$(id).css('opacity', opacity);
		}
}
