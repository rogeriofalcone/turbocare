//AJAX Post function
function postJSON(url, postVars) {
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
}

var qry = {};

/*
	Collect variables from the form "f" (element node)
	make a postable query string
*/
qry.collectPostVars = function(f){
  var postVars='';
  for(var i=0; i<f.elements.length;i++)
  {
    var t = f.elements[i].type;
    if(t.indexOf('text') > -1 )
    {
      if(postVars!='') postVars+='&';
      postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].value);
    }
    if(t.indexOf('hidden') > -1 )
    {
      if(postVars!='') postVars+='&';
      postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].value);
    }
    if(t.indexOf('select') > -1)
    {
      if(postVars!='') postVars+='&';
      if (getNodeAttribute(f.elements[i],'multiple') != null) {
      	postVars+= f.elements[i].name +'='+ qry.multiselect_csv(f.elements[i].id);
      } else {
      	postVars+= f.elements[i].name +'='+ f.elements[i].options[f.elements[i].selectedIndex].value;
      }
    }
  }
  return postVars;
}

/*
	returns the PostVars for a select item
	a good way of testing if something has been selected.
*/
qry.checkSelect = function(elem) {
	var select = getElement(elem);
	var t = select.type;
	var postVars = '';
	if (t.indexOf('select') > -1){
		if (getNodeAttribute(select,'multiple') != null) {
			postVars+= select.name +'='+ qry.multiselect_csv(select.id);
		} else {
			postVars+= select.name +'='+ select.options[select.selectedIndex].value;
		}		
	}
	return postVars;
}

/*
	Scans over a multi-select list and puts the values in a csv
	NOTE: if you're getting errors, it couls be because the 
	Select list doesn't have an "id" attribute!
*/
qry.multiselect_csv = function(element_id){
	if (getElement(element_id) != null) {
		var nodes = getElement(element_id).childNodes;
		var csv = '';
		for (var i=0;i<nodes.length;i++){
			if (nodes[i].selected){
				csv += nodes[i].value +',';
			}
		}
		csv = csv.slice(0,csv.length-1);
		return csv;
	} else {
		return '';
	}
}
/*
	ChangeGroup: Create a query object, then serialize it into JSON format
	to transmit to the app server and save it to a file for future use
*/
qry.ChangeGroup = function(e) {
	var Group = getElement('Group').value;
	if (Group!='') {
		qry.toggle_message("Loading...");
		var postVars = 'Group='+Group;
		var d = postJSON('LoadReportList',postVars);
		d.addCallbacks(qry.UpdateReportList,qry.error_report);
	}
}
/*
	UpdateReportList: Update the report listing for a group
*/
qry.UpdateReportList = function(d) {
	qry.toggle_message("");
	var ReportFile = getElement('ReportFile');
	replaceChildNodes(ReportFile, null);
	for (var i=0; i<d.reports.length; i++) {
		ReportFile.appendChild(createDOM('OPTION',{'value':d.reports[i]},d.reports[i]));
	}
}
/*
	EditReport: Create a query object, then serialize it into JSON format
	to transmit to the app server and save it to a file for future use
*/
qry.EditReport = function(e) {
	var Group = getElement('Group').value;
	var ReportFile = getElement('ReportFile').value;
	if (Group!=''&&ReportFile!='') {
		qry.toggle_message("Loading...");
		var postVars = 'Group='+Group+'&ReportFile='+ReportFile;
		var d = postJSON('LoadSavedQuery',postVars);
		d.addCallbacks(def.RenderQueryEditor,qry.error_report);
	}
}

// AJSON reactions ==================
qry.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	qry.toggle_message("");
	if (data.result_msg != null) {
		var display = createDOM('DIV',{'class':'displaymsg','id':'last_result_msg'},data.result_msg);
		if (getNodeAttribute('last_result_msg','class') == null){
			document.body.appendChild(display);
		} else {
			swapDOM(field.id,display);
		}
	}
	var d = callLater(5,remove_message);
}
qry.error_report = function(data){
	qry.toggle_message("ERROR");
	var d = callLater(5,qry.toggle_message);
}

qry.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}


//Configure our events using the Mochikit signal library
/*
	Initial event configuration
*/
qry.OpenOnLoad = function() {
	connect("Group","onclick",qry.ChangeGroup);
	connect("ReportFile","ondblclick",qry.RunReport);
}
//Connect on onload for the document to open the document using javascript
connect(window, 'onload', qry.OpenOnLoad);
