/*
	My custom shortcuts:
	1. Open a dialog box for entering a an id
*/

//AJAX Post function
function toggle_message(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

function postJSON(url, postVars) {
    toggle_message("Sending request...");
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
}


RenderError = function(d) {
	toggle_message("ERROR");
	var d = callLater(5,toggle_message);
}

LoadPatient = function(){
	alert("A patient would be loaded here");
}

LoadBeds = function(){
	var WardID = getElement("room").value;
  	var d = postJSON("LoadBeds","RoomID="+WardID);
  	d.addCallbacks(RenderBeds,RenderError);	
}

RenderBeds = function(d){
	var SelectOption = function(value, label, selected){
		if (selected){
			return  createDOM('OPTION',{'value':value, "selected":"selected"},label);
		} else {
			return createDOM('OPTION',{'value':value},label);
		}
	}
	toggle_message('');
	var Beds = getElement("bed");
	replaceChildNodes("bed",null);
	var First = true;
	forEach(d.beds,function(bed) {
		if (First) {
			Beds.appendChild(SelectOption(bed.value, bed.label, true));
			First = false;
		} else {
			Beds.appendChild(SelectOption(bed.value, bed.label, false));
		}
	});
}

function LoadRooms(){
	var WardID = getElement("ward").value;
  	var d = postJSON("LoadRooms","WardID="+WardID);
  	d.addCallbacks(RenderRooms,RenderError);	
}

RenderRooms = function(d){
	var SelectOption = function(value, label, selected){
		if (selected){
			return  createDOM('OPTION',{'value':value, "selected":"selected"},label);
		} else {
			return createDOM('OPTION',{'value':value},label);
		}
	}
	toggle_message('');
	var Rooms = getElement("room");
	replaceChildNodes("room",null);
	var First = true;
	forEach(d.rooms,function(room) {
		if (First) {
			Rooms.appendChild(SelectOption(room.value, room.label, true));
			First = false;
		} else {
			Rooms.appendChild(SelectOption(room.value, room.label, false));
		}
	});
	LoadBeds();
}

function ConnectEvents(){
	if (getElement("ward")!=null) {
		connect("ward",'onclick',LoadRooms);
	}
	if (getElement("room")!=null) {
		connect("room",'onclick',LoadBeds);
	}
	if (getElement("bed")!=null) {
		connect("bed",'onclick',LoadPatient);
	}
}

/*
	Add the OnClick events to the ward, room and bed select lists.
*/
connect(window, 'onload', ConnectEvents);

