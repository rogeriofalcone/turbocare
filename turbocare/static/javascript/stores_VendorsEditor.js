/*
	IMPORT vars

import pick.*;
*/
//Document wide variables
var barcode = {};//The barcode object
//The barcode value
barcode.CustomerID = ''; //Defined as 20 numeric characters followed by a enter key
barcode.PatientID = '';//Defined as 18 numeric characters followed by a enter key
barcode.StockItemID = '';//Defined as 22 numeric characters followed by a enter key
barcode.CatalogItemID = '';//Defined as 16 numeric characters followed by a enter key
//capture the keypress event.  We're looking for 16 to 22 consecutive numeric values
//followed by an enter key.  The enter key is captured by a separate function.
barcode.keypress = function(dom_obj){
	if (dom_obj.modifier()['any'] == false){
		var key = dom_obj.key()['string'];
		if (isNaN(key)) {
			barcode.CustomerID = '';
			barcode.PatientID = '';
			barcode.StockItemID = '';
			barcode.CatalogItemID = '';
		} else {
			barcode.CustomerID = barcode.CustomerID + key;
			barcode.PatientID = barcode.PatientID + key;
			barcode.StockItemID = barcode.StockItemID + key;
			barcode.CatalogItemID = barcode.CatalogItemID + key;
		}
		if (barcode.StockItemID.length > 22) {
			barcode.StockItemID = '';
		}
		if (barcode.CustomerID.length > 20) {
			barcode.CustomerID = '';
		}
		if (barcode.PatientID.length > 18) {
			barcode.PatientID = '';
		}
		if (barcode.CatalogItemID.length > 16) {
			barcode.CatalogItemID = '';
		}
	} else {
		barcode.CustomerID = '';
		barcode.PatientID = '';
		barcode.StockItemID = '';
		barcode.CatalogItemID = '';
	}
}
//Capture the enter key.  If our barcode is full when an enter key is pressed
//We are most likely entering a barcode.  At this point, we signal a barcode event!
barcode.keydown = function(dom_obj) {
	if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.CustomerID.length==20)){
		//alert(barcode.CustomerID);
		signal(document,'customerid',barcode.CustomerID);
	} else if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.PatientID.length==18)){
		//alert(barcode.PatientID);
		signal(document,'patientid',barcode.PatientID);
	} else if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.StockItemID.length==22)){
		//alert(barcode.StockItemID);
		signal(document,'stockitemid',barcode.StockItemID);
	} else if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.CatalogItemID.length==16)){
		//alert(barcode.CatalogItemID);
		signal(document,'catalogitemID',barcode.CatalogItemID);
	} else if (dom_obj.key()['string']=='KEY_ENTER') {
		barcode.CustomerID = '';
		barcode.PatientID = '';
		barcode.StockItemID = '';
		barcode.CatalogItemID = '';
	}
}
/*
	Events for the barcode reader.  The connect operations are made at the bottom of the document
*/
//When a customerid event (custom event) is fired, we process it here
barcode.LoadCustomerID = function(dom_obj) {
	//Load the items available for the customer
  	//var postVars = 'CustomerID='+barcode.CustomerID;
	//barcode.CustomerID = '';
	//document.location.href = 'RegistrationPage1?'+postVars;
}
//When a PatientID event (custom event) is fired, we process it here
barcode.LoadPatientID = function(dom_obj) {
	//Load the items available for the customer
  	//var postVars = 'PatientID='+barcode.PatientID;
	//barcode.PatientID = '';
	//document.location.href = 'RegistrationPage1?'+postVars;
}
barcode.LoadCatalogItemID = function(dom_obj){
 	var postVars = 'CatalogItemID='+barcode.CatalogItemID;
	barcode.CatalogItemID = '';
	document.location.href = 'CatalogItemsEditor?'+postVars;
}
barcode.LoadStockItemID = function(dom_obj){
 	var postVars = 'StockItemID='+barcode.StockItemID;
	barcode.StockItemID = '';
	document.location.href = 'CatalogItemsEditor?'+postVars;
}

/*
	My custom shortcuts:
	1. Open a dialog box for entering a an id
*/
var shortcuts = {};//keyboard short cut operations
shortcuts.keypress = function(dom_obj){
	if ((dom_obj.modifier()['ctrl'] == true) && (dom_obj.key()['string'] == 'l')) {
		store.renderIdDialog();
	}
}
shortcuts.keydown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		var ID = getElement("dialog_ID");
		if ((ID != null) && (ID.value != null) && (ID.value != '')){
			//Load the items available for the customer
			store.idDialog_remove();
			var postVars = 'PurchaseOrderID='+ID.value;
			document.location.href = 'PurchaseOrdersEditor?'+postVars;
		}
	}
}

//AJAX Post function
function postJSON(url, postVars) {
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

var store = {};


// variables ===================
store.g_nTimeoutId;
store.FkDivID = ''; //Use this to track which DIV we need to update later
// utility functions ===========

/*
	When someone enters an age, modify the DateBirth
	entry to match the age to the date.
*/
store.AgePickUpdate = function(dom_obj){
	var Age = getElement('Age').value;
	if (Age == '') {
		return false;
	} else if (isNaN(Age)){
		getElement('Age').value = '';
	} else if (Age != store.Age) {
		var Today = new Date();
		var DateBirth = new Date(Today.getFullYear() - Age, Today.getMonth(), Today.getDate());
		getElement('DateBirth').value = toISODate(DateBirth);
		store.Age = Age;
		store.DateBirth = toISODate(DateBirth);
	}
}
/*
	Open a date entry javascript box
*/
store.DatePick = function(dom_obj){
	if ((dom_obj.type() == 'click') || (dom_obj.type()=='keydown' && (dom_obj.key()['string']=='KEY_ARROW_DOWN'))) {
//		if (dom_obj.type() == 'keydown') {
//			dom_obj.stop();
//		}
		Widget.pickDateTime(dom_obj.src().id);
	}
}
/*
	When a date has been entered, update
	the age box
*/
store.DatePickUpdate = function(dom_obj){
	var DateBirth = isoDate((getElement("DateBirth").value).slice(0,10));
	getElement('DateBirth').value = toISODate(DateBirth);
	if (getElement('DateBirth').value != store.DateBirth) {
		var Today = new Date();
		var diff = Today.getTime() - DateBirth.getTime();
		getElement('Age').value = parseInt((diff + 43200000)/(31557600000));
		store.Age = getElement('Age').value;
		store.DateBirth = toISODate(DateBirth);
	}
}
/*
	Collect variables from the form "f" (element node)
	make a postable query string
*/
store.collectPostVars = function(f){
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
      	postVars+= f.elements[i].name +'='+ store.multiselect_csv(f.elements[i].id);
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
store.checkSelect = function(elem) {
	var select = getElement(elem);
	var t = select.type;
	var postVars = '';
	if (t.indexOf('select') > -1){
		if (getNodeAttribute(select,'multiple') != null) {
			postVars+= select.name +'='+ store.multiselect_csv(select.id);
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
store.multiselect_csv = function(element_id){
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


// AJSON reactions ==================
store.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	store.toggle_message("");
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
store.error_report = function(data){
	store.toggle_message("ERROR");
	var d = callLater(5,store.toggle_message);
}

store.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

store.merge_hidden_inputs = function(parentid){
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
store.QuickSearch = function(dom_obj){
	if ((dom_obj.key()['string']=='KEY_ENTER')&&(getElement('QuickSearch').value!='')) {
		store.toggle_message("Searching...");
		var postVars = 'QuickSearchText='+getElement('QuickSearch').value;
		// The following line needs to point to the function which is used for the quick search in your context
		var d = postJSON('VendorsEditorQuickSearch',postVars);
		d.addCallbacks(store.RenderQuickSearch,store.error_report);
	}
}
/*
	CheckDelete: Confirm that the user wants to delete the record
*/
store.CheckDelete = function(dom_obj){
	if (!(confirm("Are you sure you want to delete the record?"))){
		dom_obj.stop();
	}
}
/*
	CheckAddNew: Confirm that the user wants to make a new record
*/
store.CheckAddNew = function(dom_obj){
	//if (!(confirm("Are you sure you want to continue?  Un-saved changes to the current record will be lost."))){
	//	dom_obj.stop();
	//}
}

/*
	CancelChanges:  basically, reload the page
*/
store.CancelChanges = function(dom_obj){
	location = "VendorsEditor?VendorID="+getElement("VendorID").value;
}
/*
	ForeignKey Select box
	
*/
store.FkSelect = function(dom_obj) {
	store.toggle_message("Loading...");
	if (dom_obj.src().id == 'btnPickCityID') {
		store.FkDivID = 'CityID';
		var d = postJSON('VendorsEditorCitySelect',null);
	}
	d.addCallbacks(store.RenderFkSelect,store.error_report);
}
/*
	Groups
	Similar to any related join type selection
*/
store.Groups = function(dom_obj){
	store.toggle_message("Loading...");
	var postVars = 'VendorID='+getElement('VendorID').value;
	// The following line needs to point to the function which is used for the quick search in your context
	var d = postJSON('VendorsEditorVendorSelect',postVars);
	d.addCallbacks(store.RenderGroups,store.error_report);
}
/*
	If the Quick Search has the default text:
		Enter Search Text
	Then clear the text on clicking the box
*/
store.QuickSearchClear = function(dom_obj){
	if (getElement('QuickSearch').value == 'Enter Search Text'){
		getElement('QuickSearch').value = '';
	}
}
/*
	Initial event configuration
*/
store.OpenOnLoad = function() {
	if (getElement('Name')!=null) {
		getElement('Name').focus();
	}
	//We have show/hide buttons (inputs with the hideUnHide class) which need to have "onclick" events added
	var toggleButtons = getElementsByTagAndClassName('INPUT',"hideUnHide",document);
	for (i=0;i<toggleButtons.length; i++){
		connect(toggleButtons[i],"onclick",store.ShowHide);
	}
	//We have some inputs with the  dateEntry class which want to have a date control added
	var dateInputs = getElementsByTagAndClassName('INPUT',"dateEntry",document);
	for (i=0;i<dateInputs.length; i++){
		connect(dateInputs[i],"onclick",store.DatePick);
		connect(dateInputs[i],"onkeydown",store.DatePick);
	}
	//Link the delItem buttons
	var delButtons = getElementsByTagAndClassName('INPUT',"delItem",document);
	for (i=0;i<delButtons.length; i++){
		connect(delButtons[i],"onclick",store.DeleteItem);
	}
}
/*
	To do Show/Hide, I give the button "name" the same value as the div "id" which I want to toggle
	to show/hide, I just read the button's name, get the DIV and read the "display" style and then
	toggle it.  I then set the value on the button to corrospond.
	NOTE: display is toggled between None and Table!!!!
*/
store.ShowHide = function(dom_obj){
	var btn = dom_obj.src();
	var div = getElement(btn.name);
	var disp = computedStyle(div,"display");
	if (disp == "none"){
		btn.value = "Hide";
		div.style.display = "table";
	} else {
		btn.value = "Edit";
		div.style.display = "none";
	}
}
/*
	Remove the item from the DOM.  This is an attempt to delete an item from a purchase order
	The server script will notice that the item is missing from the list and will then attempt to
	delete it, or mark it deleted.
*/
store.DeleteItem = function(dom_obj){
	if (confirm('Are you sure you want to try to delete the Item?')) {
		var elem = dom_obj.src().parentNode.parentNode;
		swapDOM(elem,null);
	}
}

/*
	AJSON Reactions to the above actions
*/

/* 	
	Render the Quick Search Results
*/
store.RenderQuickSearch = function(data){
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
	store.toggle_message("");
	//Make our results list
	var QuickSearchResults = getElement('QuickSearchResults');
	replaceChildNodes(QuickSearchResults,null);
	var results = data.results;
	QuickSearchResults.appendChild(AddResultRow(null,null,'There are '+results.length+' result(s)'));
	for (i=0; i<results.length; i++) {
		QuickSearchResults.appendChild(AddResultRow('VendorsEditor','VendorID='+results[i].id,results[i].text));
	}
}
/*
	Render the ForeignKey selection dialog
*/
store.RenderFkSelect = function(data){
	var AddResultRow = function(value){
		//Each row needs: id, text, and selected
		var row = createDOM('DIV',{'class':'listingrow'},value.text);
		var btn = createDOM('INPUT',{'type':'button','value':'Select','name':'FkButton'});
		var text = createDOM('INPUT',{'type':'hidden','readonly':'readonly','value':value.text,'name':'FkText'});
		var id = createDOM('INPUT',{'type':'hidden','value':value.id,'name':'FkID'});
		if (value.linkurl != null) {
			var link = createDOM('INPUT',{'type':'hidden','value':value.linkurl,'name':'FkLink'});
			replaceChildNodes(row,btn,value.text,text,id,link);
		} else {
			replaceChildNodes(row,btn,value.text,text,id);
		}
		return row;
	}
	//Reset the message
	store.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'fk_dialog','style':'height:200px; overflow:auto'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'fk_shadow','style':'height:210px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:store.FkSelect_remove()'},"Close");
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
			connect(Inputs[i],'onclick',store.FkSelect_select);
		}
	}
	//Attach the update event to the search box
	connect(SearchText,'onkeydown',store.FkSelect_update);
	SearchText.focus();
	//We have a function name which we'll hide in the dialog box
	dialog.appendChild(createDOM('INPUT',{'type':'hidden','id':'FkFunction','value':data.function_name}));
}
//Remove the dialog box
store.FkSelect_remove = function(){
	swapDOM('fk_dialog',null);
	swapDOM('fk_shadow',null);
}
//Run a search to update the listing (usually to fine-tune the search results)
store.FkSelect_update = function(dom_obj){
	if ((dom_obj.key()['string']=='KEY_ENTER')&&(getElement('FkSearchText').value!='')) {
		store.toggle_message("Searching...");
		var postVars = 'SearchText='+getElement('FkSearchText').value;
		// The following line needs to point to the function which is used for the quick search in your context
		//alert(getElement('FkFunction').value);
		var d = postJSON(getElement('FkFunction').value,postVars);
		d.addCallbacks(store.RenderFkSelectUpdate,store.error_report);
	}
}
//Update the search results
store.RenderFkSelectUpdate = function(data){
	var AddResultRow = function(value){
		//Each row needs: id, text, and selected
		var row = createDOM('DIV',{'class':'listingrow'},value.text);
		var btn = createDOM('INPUT',{'type':'button','value':'Select','name':'FkButton'});
		var text = createDOM('INPUT',{'type':'hidden','readonly':'readonly','value':value.text,'name':'FkText'});
		var id = createDOM('INPUT',{'type':'hidden','value':value.id,'name':'FkID'});
		if (value.linkurl != null) {
			var link = createDOM('INPUT',{'type':'hidden','value':value.linkurl,'name':'FkLink'});
			replaceChildNodes(row,btn,value.text,text,id,link);
		} else {
			replaceChildNodes(row,btn,value.text,text,id);
		}
		//replaceChildNodes(Check, value.text);
		return row;
	}
	//Reset the message
	store.toggle_message("");
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
			connect(Inputs[i],'onclick',store.FkSelect_select);
		}
	}
}
//Select and return an item from the list
store.FkSelect_select = function(dom_obj){
	var FkDiv = getElement(store.FkDivID);
	var elem = dom_obj.src().parentNode;
	var Url = '';
	var Inputs = getElementsByTagAndClassName('INPUT',null,elem);
	for (i=0; i<Inputs.length; i++){
		if (getNodeAttribute(Inputs[i],'name') == 'FkText') {
			var text = Inputs[i].value;
		} else if (getNodeAttribute(Inputs[i],'name') == 'FkID') {
			var ID = Inputs[i].value;
		} else if (getNodeAttribute(Inputs[i],'name') == 'FkLink') {
			Url = Inputs[i].value;
		}
	}
	if (Url != '') {
		var link = createDOM('A',{'href':Url},text);
		replaceChildNodes(FkDiv,link,createDOM('INPUT',{'name':store.FkDivID,'type':'hidden','value':ID}));
	} else {
		replaceChildNodes(FkDiv,text,createDOM('INPUT',{'name':store.FkDivID,'type':'hidden','value':ID}));
	}
	store.FkDivID = '';
	store.FkSelect_remove();
}
/* 	
	Vendor box functions
	(this is a typical RelatedJoin editor)
*/
//Render the box
store.RenderGroups = function(data){
	var AddResultRow = function(value){
		//Each row needs: id, text, and selected
		var row = createDOM('DIV',{'class':'divtable'});
		if (value.selected) {
			var Check = createDOM('INPUT',{'type':'checkbox', 'checked':'checked','value':value.id,'name':'GroupID'});
		} else {
			var Check = createDOM('INPUT',{'type':'checkbox','value':value.id,'name':'GroupID'});
		}
		var text = createDOM('INPUT',{'id':'GroupName'+value.id,'type':'text','readonly':'readonly','value':value.text,'name':'GroupName'});
		//replaceChildNodes(Check, value.text);
		row.appendChild(Check);
		row.appendChild(text);
		return row;
	}
	//Reset the message
	store.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'relatedjoin_dialog','style':'height:200px; overflow:auto'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'relatedjoin_shadow','style':'height:210px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:store.Groups_remove()'},"Close");
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
	connect('btnSelectGroups','onclick',store.GroupsSelect);
}
store.Groups_remove = function(){
	swapDOM('relatedjoin_dialog',null);
	swapDOM('relatedjoin_shadow',null);
}
store.GroupsSelect = function(dom_obj){
	var dialog = getElement('relatedjoin_dialog');
	var listing = getElement('Groups');
	//Clear our current listing
	replaceChildNodes(listing,null);
	var checkboxes = getElementsByTagAndClassName('INPUT',null,dialog);
	// For every input box line, append an entry
	for (i=0; i<checkboxes.length;i++) {
		if (checkboxes[i].checked) {
			var text = getElement('GroupName'+checkboxes[i].value).value;
			var value = checkboxes[i].value;
			listing.appendChild(createDOM('LI',null,text));
			listing.appendChild(createDOM('INPUT',{'name':'Groups','type':'hidden','value':value}));
			listing.appendChild(createDOM('INPUT',{'name':'GroupsCounter','type':'hidden','value':'1'}));
		}
	}
	//Close the dialog
	store.Groups_remove();
}

//Configure our events using the Mochikit signal library
/* DEFINE OUR EVENT FUNCTIONS */
connect(document,'onkeydown', barcode.keydown);
connect(document,'onkeypress', barcode.keypress);
connect(document,'customerid', barcode.LoadCustomerID);
connect(document,'patientid', barcode.LoadPatientID);
//custom short-cuts
connect(document,'onkeypress',shortcuts.keypress);
connect(document,'onkeydown', shortcuts.keydown);
//Connect our buttons/fields to events -- need to do this on document load

connect(window, 'onload', function(){
		if (getElement("QuickSearch")!=null) {
			connect("QuickSearch",'onkeydown',store.QuickSearch);
			connect("QuickSearch",'onclick',store.QuickSearchClear);
		}
		if (getElement("btnPickCityID")!=null) {
			connect("btnPickCityID",'onclick',store.FkSelect);
		}
		if (getElement("btnEditGroups")!=null) {
			connect("btnEditGroups",'onclick',store.Groups);
		}
		if (getElement("btnCancel")!=null){
			// cancel changes by reloading the page ** This is not a proper cancel
			connect("btnCancel",'onclick',store.CancelChanges);
		}
		if (getElement("btnDelete")!=null){
			connect("btnDelete",'onclick',store.CheckDelete);
		}
		if (getElement("btnAddNew")!=null){
			connect("btnAddNew",'onclick',store.CheckAddNew);
		}
});
//Connect on onload for the document to open the document using javascript
connect(window, 'onload', store.OpenOnLoad);


/*
	Small dialog box, for entering the customer id
*/
store.idDialog_remove = function(){
	swapDOM('id_dialog',null);
	swapDOM('id_shadow',null);
}
store.renderIdDialog = function(){
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
	store.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'id_dialog','style':'height:70px'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'id_shadow','style':'height:80px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:store.idDialog_remove()'},"Close");
	dialog.appendChild(close_link);
	//The main table
	var table = createDOM('TABLE',{'class':'regular'});
	var tbody = createDOM('TBODY',null);
	// Add field
	tbody.appendChild(StringEdit('CatalogItemID','Catalog Item ID',''));
	//Create our dialog
	table.appendChild(tbody);
	dialog.appendChild(table);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Attach the button event
	getElement('dialog_ID').focus();
}

