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
			var postVars = 'LocationID='+ID.value;
			document.location.href = 'LocationsEditor?'+postVars;
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
config.FkDivID = null;

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
		var d = postJSON('LocationsEditorQuickSearch',postVars);
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
	LocationGroups
	Similar to any related join type selection
*/
config.LocationGroups = function(e){
	config.toggle_message("Loading...");
	var postVars = 'LocationID='+getElement('LocationID').value;
	var d = postJSON('LocationsEditorGroupSelect',postVars);
	d.addCallbacks(config.RenderLocationGroups,config.error_report);
}
/* 	
	RenderLocationGroups box functions
*/
//Render the box
config.RenderLocationGroups = function(data){
	var AddResultRow = function(value){
		//Each row needs: id, text, and selected
		var row = createDOM('DIV',{'class':'divtable'});
		if (value.selected) {
			var Check = createDOM('INPUT',{'type':'checkbox', 'checked':'checked','value':value.id,'name':'LocationGroupID'});
		} else {
			var Check = createDOM('INPUT',{'type':'checkbox','value':value.id,'name':'LocationGroupID'});
		}
		var text = createDOM('INPUT',{'id':'LocationGroupName'+value.id,'type':'text','readonly':'readonly','value':value.text,'name':'LocationGroupName'});
		//replaceChildNodes(Check, value.text);
		row.appendChild(Check);
		row.appendChild(text);
		return row;
	}
	//Reset the message
	config.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'relatedjoin_dialog','style':'height:200px; overflow:auto'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'relatedjoin_shadow','style':'height:210px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:config.LocationGroups_remove()'},"Close");
	dialog.appendChild(close_link);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Make our listing
	var results = data.results;
	for (i=0; i<results.length; i++) {
		dialog.appendChild(AddResultRow(results[i]));
	}
	//Put our OK button at the end
	var btnRow = createDOM('DIV',{'style':'text-align:right'});
	btnRow.appendChild(createDOM('INPUT',{'name':'btnSelectGroups','id':'btnSelectGroups','type':'BUTTON','value':'OK'}));
	dialog.appendChild(btnRow);
	//Attach an event to the button
	connect('btnSelectGroups','onclick',config.LocationGroupsSelect);
}
config.LocationGroups_remove = function(){
	swapDOM('relatedjoin_dialog',null);
	swapDOM('relatedjoin_shadow',null);
}
config.LocationGroupsSelect = function(dom_obj){
	var dialog = getElement('relatedjoin_dialog');
	var groups = getElement('LocationGroups');
	//Clear our current groups listing
	replaceChildNodes(groups,null);
	var checkboxes = getElementsByTagAndClassName('INPUT',null,dialog);
	// For every input box line, append an entry to the groups
	for (i=0; i<checkboxes.length;i++) {
		if (checkboxes[i].checked) {
			var text = getElement('LocationGroupName'+checkboxes[i].value).value;
			var value = checkboxes[i].value;
			groups.appendChild(createDOM('LI',null,text));
			groups.appendChild(createDOM('INPUT',{'name':'LocationGroups','type':'hidden','value':value}));
		}
	}
	//Close the dialog
	config.LocationGroups_remove();
}
/*
	ForeignKey Select box
	
*/
config.FkSelect = function(e) {
	config.toggle_message("Loading...");
	if (e.src().id == 'btnParentDeptNrID') {
		config.FkDivID = 'ParentDeptNrID'; // The DIV where we want to render our results later
		var d = postJSON('LocationEditorParentDepartmentSelect',null);
	}
	d.addCallbacks(config.RenderFkSelect,config.error_report);	
}
/*
	Render the ForeignKey selection dialog
*/
config.RenderFkSelect = function(data){
	var AddResultRow = function(value){
		//Each row needs: id, text, and selected
		var row = createDOM('DIV',{'class':'listingrow'},value.text);
		var btn = createDOM('INPUT',{'type':'button','value':'Select','name':'FkButton'});
		var text = createDOM('INPUT',{'type':'hidden','readonly':'readonly','value':value.text,'name':'FkText'});
		var id = createDOM('INPUT',{'type':'hidden','value':value.id,'name':'FkID'});
		//replaceChildNodes(Check, value.text);
		replaceChildNodes(row,btn,value.text,text,id);
		return row;
	}
	//Reset the message
	config.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'fk_dialog','style':'height:200px; overflow:auto'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'fk_shadow','style':'height:210px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:config.FkSelect_remove()'},"Close");
	dialog.appendChild(close_link);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Create our SearchText box
	var SearchText = createDOM('INPUT',{'type':'text','name':'FkSearchText','id':'FkSearchText','value':''});
	dialog.appendChild(createDOM('BR',null));
	dialog.appendChild(SearchText);
	//Make our listing
	var SearchResults = createDOM('DIV',{'id':'FkResults'});
	dialog.appendChild(SearchResults);
	var results = data.results;
	for (i=0; i<results.length; i++) {
		SearchResults.appendChild(AddResultRow(results[i]));
	}
	//Attach the event to the buttons
	var Inputs = getElementsByTagAndClassName('INPUT',null,SearchResults);
	for (i=0;i<Inputs.length;i++){
		if (getNodeAttribute(Inputs[i],'type') == 'button') {
			connect(Inputs[i],'onclick',config.FkSelect_select);
		}
	}
	//Attach the update event to the search box
	connect(SearchText,'onkeydown',config.FkSelect_update);
	SearchText.focus();
	//We have a function name which we'll hide in the dialog box
	dialog.appendChild(createDOM('INPUT',{'type':'hidden','id':'FkFunction','value':data.function_name}));
}
//Remove the dialog box
config.FkSelect_remove = function(){
	swapDOM('fk_dialog',null);
	swapDOM('fk_shadow',null);
}
//Run a search to update the listing (usually to fine-tune the search results)
config.FkSelect_update = function(dom_obj){
	if ((dom_obj.key()['string']=='KEY_ENTER')&&(getElement('FkSearchText').value!='')) {
		config.toggle_message("Searching...");
		var postVars = 'SearchText='+getElement('FkSearchText').value;
		// The following line needs to point to the function which is used for the quick search in your context
		//alert(getElement('FkFunction').value);
		var d = postJSON(getElement('FkFunction').value,postVars);
		d.addCallbacks(config.RenderFkSelectUpdate,config.error_report);
	}
}
//Update the search results
config.RenderFkSelectUpdate = function(data){
	var AddResultRow = function(value){
		//Each row needs: id, text, and selected
		var row = createDOM('DIV',{'class':'listingrow'},value.text);
		var btn = createDOM('INPUT',{'type':'button','value':'Select','name':'FkButton'});
		var text = createDOM('INPUT',{'type':'hidden','readonly':'readonly','value':value.text,'name':'FkText'});
		var id = createDOM('INPUT',{'type':'hidden','value':value.id,'name':'FkID'});
		//replaceChildNodes(Check, value.text);
		replaceChildNodes(row,btn,value.text,text,id);
		return row;
	}
	//Reset the message
	config.toggle_message("");
	//Make our listing
	var SearchResults = getElement('FkResults');
	replaceChildNodes(SearchResults,null);
	var results = data.results;
	for (i=0; i<results.length; i++) {
		SearchResults.appendChild(AddResultRow(results[i]));
	}
	//Attach the event to the buttons
	var Inputs = getElementsByTagAndClassName('INPUT',null,SearchResults);
	for (i=0;i<Inputs.length;i++){
		if (getNodeAttribute(Inputs[i],'type') == 'button') {
			connect(Inputs[i],'onclick',config.FkSelect_select);
		}
	}
}
//Select and return an item from the list
config.FkSelect_select = function(dom_obj){
	var FkDiv = getElement(config.FkDivID);
	var elem = dom_obj.src().parentNode;
	var Inputs = getElementsByTagAndClassName('INPUT',null,elem);
	for (i=0; i<Inputs.length; i++){
		if (getNodeAttribute(Inputs[i],'name') == 'FkText') {
			var text = Inputs[i].value;
		} else if (getNodeAttribute(Inputs[i],'name') == 'FkID') {
			var ID = Inputs[i].value;
		}
	}
	replaceChildNodes(FkDiv,text,createDOM('INPUT',{'name':config.FkDivID,'type':'hidden','value':ID}));
	config.FkDivID = '';
	config.FkSelect_remove();
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
		if (results[i].type=='location') {
			QuickSearchResults.appendChild(AddResultRow('LocationsEditor','LocationID='+results[i].id,results[i].text));
		} else {
			QuickSearchResults.appendChild(AddResultRow('LocationsEditor','DepartmentID='+results[i].id,results[i].text));
		}
	}
}
/*
	ToggleDepartmentType: Show/Hide the mini edit form for department types
*/
config.ToggleDepartmentType = function(e){
	var el = getElement('EditTypeOptionsForm');
	if (el.style.display=='none') {
		// initialize the edit form (any previous unsaved changes are cancelled)
		var Type = getElement('Type');
		var opts = getElementsByTagAndClassName('OPTION',null,Type);
		forEach(opts, function(opt) {
			if (opt.value==Type.value) {
				getElement('TypeName').value = scrapeText(opt);
			}
		});
		getElement('TypeID').value = Type.value;
		el.style.display='';
	} else {
		el.style.display='none';
	}
}
/*
	SaveType: Save changes made to the department type
*/
config.SaveType = function(e){
	config.toggle_message("Saving...");
	var postVars = 'TypeID='+getElement('TypeID').value+'&TypeName='+getElement('TypeName').value+'&Operation=Save';
	var d = postJSON('LocationsEditorDepartmentTypeSave',postVars);
	d.addCallbacks(config.RenderTypes,config.error_report);
}
/*
	CancelType: Cancel changes made to the department type
*/
config.CancelType = function(e){
	config.toggle_message("Cancelling...");
	var postVars = 'Operation=Cancel';
	var d = postJSON('LocationsEditorDepartmentTypeSave',postVars);
	d.addCallbacks(config.RenderTypes,config.error_report);
}
/*
	NewType: Cancel changes made to the department type and set the record up to create a new entry
*/
config.NewType = function(e){
	getElement('TypeName').value = '';
	getElement('TypeID').value = '';
}
/*
	DeleteType: Request that the department type be deleted
*/
config.DeleteType = function(e){
	if (confirm('Are you sure you want to delete?')) {
		config.toggle_message("Deleting...");
		var postVars = 'TypeID='+getElement('TypeID').value+'&Operation=Delete';
		var d = postJSON('LocationsEditorDepartmentTypeSave',postVars);
		d.addCallbacks(config.RenderTypes,config.error_report);
	}
}
/*
	UnDeleteType: Request that the department type be un-deleted
*/
config.UnDeleteType = function(e){
	config.toggle_message("Deleting...");
	var postVars = 'TypeID='+getElement('TypeID').value+'&Operation=Un-Delete';
	var d = postJSON('LocationsEditorDepartmentTypeSave',postVars);
	d.addCallbacks(config.RenderTypes,config.error_report);
}
/*
	RenderTypes: Render an updated list of the Department types
*/
config.RenderTypes = function(d) {
	if (d.message!='') {
		config.toggle_message(d.message)
		var delay = callLater(8,config.toggle_message);
	} else {
		config.toggle_message('');
	}
	var Select = getElement('Type');
	replaceChildNodes(Select,null);
	forEach(d.results,function(result) {
		if (result.selected) {
			Select.appendChild(OPTION({'value':result.id,'selected':'selected'},result.name));
		} else {
			Select.appendChild(OPTION({'value':result.id},result.name));
		}
	});
	config.ToggleDepartmentType();
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
		if (getElement("btnEditLocationGroups")!=null) {
			connect("btnEditLocationGroups",'onclick',config.LocationGroups);
		}
		if (getElement("btnParentDeptNrID")!=null) {
			connect("btnParentDeptNrID",'onclick',config.FkSelect);
		}
		// buttons for the department type mini-form
		if (getElement("EditTypeOptions")!=null) {
			connect("EditTypeOptions",'onclick',config.ToggleDepartmentType);
		}
		if (getElement("btnSaveType")!=null) {
			connect("btnSaveType",'onclick',config.SaveType);
		}
		if (getElement("btnCancelType")!=null) {
			connect("btnCancelType",'onclick',config.CancelType);
		}
		if (getElement("btnAddNewType")!=null) {
			connect("btnAddNewType",'onclick',config.NewType);
		}
		if (getElement("btnDeleteType")!=null) {
			connect("btnDeleteType",'onclick',config.DeleteType);
		}
		if (getElement("btnUnDeleteType")!=null) {
			connect("btnUnDeleteType",'onclick',config.UnDeleteType);
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
	tbody.appendChild(StringEdit('LocationID','Location ID',''));
	//Create our dialog
	table.appendChild(tbody);
	dialog.appendChild(table);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Attach the button event
	getElement('dialog_ID').focus();
}
