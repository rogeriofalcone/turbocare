/*
	My custom shortcuts:
	1. Open a dialog box for entering a an id
*/
var shortcuts = {};//keyboard short cut operations
shortcuts.keypress = function(e){
	if ((e.modifier()['ctrl'] == true) && (e.key()['string'] == 'l')) {
		e.stop();
		config.renderIdDialog();
	}
}
shortcuts.keydown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		var ID = getElement("dialog_ID");
		if ((ID != null) && (ID.value != null) && (ID.value != '')){
			//Load the items available for the customer
			config.idDialog_remove();
			var postVars = 'AddressID='+ID.value;
			document.location.href = 'AddressesEditor?'+postVars;
		}
	}
}

//AJAX Post function
function postJSON(url, postVars) {
	config.toggle_message("Sending request...");
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
}

//Funky redraw function
function redraw(){
	resizeBy(-1,0);
	resizeBy(1,0);
}

var config = {};


/*
	Open a date entry javascript box
*/
config.DatePick = function(dom_obj){
	if ((dom_obj.type() == 'click') || (dom_obj.type()=='keydown' && (dom_obj.key()['string']=='KEY_ARROW_DOWN'))) {
		if (dom_obj.type() == 'keydown') {
			dom_obj.stop();
		}
		Widget.pickDateTime("DateEdit");
	}
}

config.collectPostVars = function(f){
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
      	postVars+= f.elements[i].name +'='+ encodeURIComponent(config.multiselect_csv(f.elements[i].id));
      } else {
      	postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].options[f.elements[i].selectedIndex].value);
      }
    }
  }
  return postVars;
}

config.multiselect_csv = function(element_id){
	var nodes = getElement(element_id).childNodes;
	var csv = '';
	for (var i=0;i<nodes.length;i++){
	 	if (nodes[i].selected){
	 		csv += nodes[i].value +',';
	 	}
	}
	csv = csv.slice(0,csv.length-1);
	return csv;
}

config.clearAllFormFields = function(parentid){
	elems = getElementsByTagAndClassName('input',null,parentid);
	for (var i=0;i<elems.length;i++){
		elems[i].value = "";
	}
}

// AJSON reactions ==================
config.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	config.toggle_message("");
	if (data.message != null) {
		var display = createDOM('DIV',{'class':'displaymsg','id':'last_result_msg'},data.message);
		if (getNodeAttribute('last_result_msg','class') == null){
			document.body.appendChild(display);
		} else {
			swapDOM(field.id,display);
		}
	}
	var d = callLater(5,remove_message);
}
config.error_report = function(data){
	config.toggle_message("ERROR");
	var d = callLater(5,config.toggle_message);
}

config.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

config.merge_hidden_inputs = function(parentid){
//Take all inputs under the parent and for any hidden input with a visible input having the same name
//Copy the value to the visible input and remove the hidden input from DOM
	var inputs = getElementsByTagAndClassName('INPUT',null,parentid);
	for (i=0;i<inputs.length;i++){
		if (getNodeAttribute(inputs[i],'type') == 'hidden') {
			for (j=0;j<inputs.length;j++){
				if (getNodeAttribute(inputs[i],'name') == getNodeAttribute(inputs[j],'name') && (getNodeAttribute(inputs[j],'type')!='hidden')) {
					//copy the value from the hidden field to the visible field
					inputs[j].value = inputs[i].value;
					//change the name of the hidden field
					inputs[i].name = inputs[i].name + '_remove';
				}
			}
		}
	}
}
// AJSON actions ====================
/*
	Quick search
	Search for Items which match the entered text
*/
config.QuickSearch = function(dom_obj){
	if ((dom_obj.key()['string']=='KEY_ENTER')&&(getElement('QuickSearch').value!='')) {
		config.toggle_message("Searching...");
		var postVars = 'QuickSearchText='+getElement('QuickSearch').value;
		// The following line needs to point to the function which is used for the quick search in your context
		var d = postJSON('AddressesEditorQuickSearch',postVars);
		d.addCallbacks(config.RenderQuickSearch,config.error_report);
	}
}
/*
	If the Quick Search has the default text:
		Enter Search Text
	Then clear the text on clicking the box
*/
config.QuickSearchClear = function(dom_obj){
	if (getElement('QuickSearch').value == 'Enter Search Text'){
		getElement('QuickSearch').value = '';
	}
}
/*
	Set the focus on the name field
*/
config.OpenOnLoad = function() {
	if (getElement('Name')!=null) {
		getElement('Name').focus();
	}
}


/* 	
	RenderQuickSearch: Render the Quick Search Results
*/
config.RenderQuickSearch = function(data){
	var AddResultRow = function(URL,PostVar,Text){
		var row = createDOM('LI',null);
		if (URL!=null) {
			var A = createDOM('A',{'href':URL+'?'+PostVar},Text);
		} else {
			var A = Text;
		}
		replaceChildNodes(row, A);
		return row;
	}
	//Reset the message
	config.toggle_message("");
	//Make our results list
	var QuickSearchResults = getElement('QuickSearchResults');
	replaceChildNodes(QuickSearchResults,null);
	var results = data.results;
	QuickSearchResults.appendChild(AddResultRow(null,null,'There are '+results.length+' result(s)'));
	for (i=0; i<results.length; i++) {
		QuickSearchResults.appendChild(AddResultRow('AddressesEditor','AddressID='+results[i].id,results[i].text));
	}
}


//custom short-cuts
connect(document,'onkeypress',shortcuts.keypress);
connect(document,'onkeydown', shortcuts.keydown);
//Connect our buttons/fields to events -- need to do this on document load

connect(window, 'onload', function(){
		if (getElement("QuickSearch")!=null) {
			connect("QuickSearch",'onkeydown',config.QuickSearch);
			connect("QuickSearch",'onclick',config.QuickSearchClear);
		}
	if (getElement('btnDelete')!=null){
		connect('btnDelete','onclick',function(e) {
			if (!confirm('Are you sure you want to delete?')) {
				e.stop();
			}
		});
	}
});
//Connect on onload for the document to open the document using javascript
connect(window, 'onload', config.OpenOnLoad);

/*
	Small dialog box, to enter an id for direct loading
*/
config.idDialog_remove = function(){
	swapDOM('id_dialog',null);
	swapDOM('id_shadow',null);
}
config.renderIdDialog = function(){
	var StringEdit = function(name, label, value){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','name':name,'id':'dialog_ID', 'value':value});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	config.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'id_dialog','style':'height:70px'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'id_shadow','style':'height:80px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:config.idDialog_remove()'},"Close");
	dialog.appendChild(close_link);
	//The main table
	var table = createDOM('TABLE',{'class':'regular'});
	var tbody = createDOM('TBODY',null);
	// Add field
	tbody.appendChild(StringEdit('AddressID','Address ID',''));
	//Create our dialog
	table.appendChild(tbody);
	dialog.appendChild(table);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Attach the button event
	getElement('dialog_ID').focus();
}
