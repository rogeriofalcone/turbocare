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
		var d = postJSON('StockTransferRequestsEditorQuickSearch',postVars);
		d.addCallbacks(store.RenderQuickSearch,store.error_report);
	}
}
/*
	AddItems - calls the pick.OpenPickList function to search for and populate the
	purchase order with more catalog items
*/
store.AddItems = function(dom_obj){
	var ID = getElement('StockTransferRequestID').value;
	pick.openPickList("StockTransferRequestsEditorAddItemsStep1?StockTransferRequestID="+ID);
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
	if (!(confirm("Are you sure you want to continue?  Un-saved changes to the current record will be lost."))){
		dom_obj.stop();
	}
}

/*
	CancelChanges:  basically, reload the page
*/
store.CancelChanges = function(dom_obj){
	location = "StockTransferRequestsEditor?StockTransferRequestID="+getElement("StockTransferRequestID").value;
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
	//Link the "Fill request" buttons
	var transferButtons = getElementsByTagAndClassName('INPUT',"FillRequest",document);
	for (i=0;i<transferButtons.length; i++){
		connect(transferButtons[i],"onclick",store.FillRequest);
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
	FillRequest:  Perform a StockTransfer for the StockTransferRequestItem
*/
store.FillRequest = function(dom_obj){
	//Get the StockTransferRequestItemID
	var ItemID = null;
	var Item = dom_obj.src().parentNode.parentNode;
	var Inputs = getElementsByTagAndClassName('INPUT',null,Item);
	for (i=0;i<Inputs.length;i++) {
		if (getNodeAttribute(Inputs[i],'name')=='ItemID') {
			var ItemID = Inputs[i].value;
		}
	}
	if (ItemID!=null){
		location = 'StockTransfersEditor?StockTransferRequestItemID='+ItemID;
	} else {
		alert('Error with the data in the page');
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
		QuickSearchResults.appendChild(AddResultRow('StockTransferRequestsEditor','StockTransferRequestID='+results[i].id,results[i].text));
	}
}
/*
	RenderAddItems:	
		After selecting new Items, we display their 
		Inputs on the entry form.  If you re-use this
		code, you'll need to do lots of customization
*/
store.RenderAddItems = function(data){
	var ChkBox = function(name, value) {
		var col = createDOM('DIV',{'style':'display:table-cell;border-top:1px solid gray'});
		var sel = createDOM('SELECT',{'name':name});
		if (value=='True'){
			sel.appendChild(createDOM('OPTION',{'value':'True','selected':'selected'},'True'));
			sel.appendChild(createDOM('OPTION',{'value':'False'},'False'));
		} else {
			sel.appendChild(createDOM('OPTION',{'value':'False','selected':'selected'},'False'));
			sel.appendChild(createDOM('OPTION',{'value':'True'},'True'));		
		}
		col.appendChild(sel);
		return col;
	}
	var Col = function(name,value) {
		var col = createDOM('DIV',{'style':'display:table-cell;border-top:1px solid gray'});
		var fld = createDOM('INPUT',{'name':name,'type':'text','value':value});
		col.appendChild(fld);
		return col;
	}
	var ColSize = function(name,value,size) {
		var col = createDOM('DIV',{'style':'display:table-cell;border-top:1px solid gray'});
		var fld = createDOM('INPUT',{'name':name,'type':'text','value':value,'size':size});
		col.appendChild(fld);
		return col;
	}
	var ROCol = function(text,name,value) {
		var col = createDOM('DIV',{'style':'display:table-cell;border-top:1px solid gray'},text);
		var fld = createDOM('INPUT',{'name':name,'type':'hidden','value':value});
		var counter = createDOM('INPUT',{'name':'ItemCounter','type':'hidden','value':'1'});
		col.appendChild(fld);
		col.appendChild(counter);
		return col;
	}
	var Row = function(d){
		var row = createDOM('DIV',{'style':'display:table-row'});
		var delCol = createDOM('DIV',{'style':'display:table-cell'});
		var Delete = createDOM('INPUT',{'type':'button','name':'Delete','value':'Delete','class':'delItem'});
		delCol.appendChild(Delete);
		replaceChildNodes(row,ROCol(d.ItemName,'ItemID',d.ItemID), ColSize('ItemQty',d.ItemQty,6),
			ColSize('ItemPurchaseOrderID',d.ItemPurchaseOrderID,5), Col('ItemNotes',d.ItemNotes), 
			ChkBox('ItemIsOnOrder',d.ItemIsOnOrder), ChkBox('ItemIsTransferred',d.ItemIsTransferred), delCol);
		connect(Delete,'onclick',store.DeleteItem);
		return row;
	}
	store.toggle_message("");
	// Get the location where we want to append the new items
	var Items = getElement("Items");
	var results = data.results;
	for (i=0;i<results.length;i++) {
		Items.appendChild(Row(results[i]));
	}
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
		if (getElement("btnAddItems")!=null) {
			connect("btnAddItems",'onclick',store.AddItems);
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

