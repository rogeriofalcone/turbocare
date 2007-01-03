function hasParent(el,parent_id) {
	var node = getElement(el);
	var ret_val = false;
	if (node==null) { return false; }
	while (node.parentNode != null) {
		if (node.parentNode.id == parent_id){
			ret_val = true;
		}
		node = node.parentNode;
	}
	return ret_val;
}
var barcode = {};//The barcode object
//The barcode value
barcode.CustomerID = ''; //Defined as 20 numeric characters followed by a enter key
barcode.PatientID = '';//Defined as 18 numeric characters followed by a enter key
//capture the keypress event.  We're looking for 20 consecutive numeric values
//followed by an enter key.  The enter key is captured by a separate function.
barcode.keypress = function(dom_obj){
	if (dom_obj.modifier()['any'] == false){
		var key = dom_obj.key()['string'];
		if (isNaN(key)) {
			barcode.CustomerID = '';
			barcode.PatientID = '';
		} else {
			barcode.CustomerID = barcode.CustomerID + key;
			barcode.PatientID = barcode.PatientID + key;
		}
		if (barcode.CustomerID.length > 20) {
			barcode.CustomerID = '';
		}
		if (barcode.PatientID.length > 18) {
			barcode.PatientID = '';
		}
	} else {
		barcode.CustomerID = '';
		barcode.PatientID = '';
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
	} else if (dom_obj.key()['string']=='KEY_ENTER') {
		barcode.CustomerID = '';
		barcode.PatientID = '';
	}
}
/*
	Events for the barcode reader.  The connect operations are made at the bottom of the document
*/
//When a customerid event (custom event) is fired, we process it here
barcode.LoadCustomerID = function(dom_obj) {
	//Load the items available for the customer
  	var postVars = 'CustomerID='+barcode.CustomerID;
	barcode.CustomerID = '';
	document.location.href = 'RegistrationPage1?'+postVars;
}
//When a PatientID event (custom event) is fired, we process it here
barcode.LoadPatientID = function(dom_obj) {
	//Load the items available for the customer
  	var postVars = 'PatientID='+barcode.PatientID;
	barcode.PatientID = '';
	document.location.href = 'RegistrationPage1?'+postVars;
}


/*
	My custom shortcuts:
	1. Open a dialog box for entering a customer id
*/
var shortcuts = {};//keyboard short cut operations
shortcuts.keypress = function(dom_obj){
	if ((dom_obj.modifier()['ctrl'] == true) && (dom_obj.key()['string'] == 'l')) {
		reg.renderCustomerIdDialog();
		dom_obj.stop();
	}
}
/*
    33: 'KEY_PAGE_UP',
    34: 'KEY_PAGE_DOWN',
    35: 'KEY_END',
    36: 'KEY_HOME',
    37: 'KEY_ARROW_LEFT',
    38: 'KEY_ARROW_UP',
    39: 'KEY_ARROW_RIGHT',
    40: 'KEY_ARROW_DOWN',
*/
shortcuts.keydown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		var el = dom_obj.target();
		//Perform a search
		if (el.id == 'SearchText' || el.id == 'SearchAddress') {
			var search_text = getElement('SearchText').value;
			var search_address = getElement('SearchAddress').value;
			if ((search_text + search_address) != ''){
				reg.Search();
			}
		} else if (el.id == 'dialog_CustomerID' && !isNaN(el.value)) {
			var postVars = 'CustomerID='+el.value;
			document.location.href = 'RegistrationPage1?'+postVars;			
		}
	} else if  (dom_obj.key()['string']=='KEY_ARROW_UP') {
		if (hasParent(dom_obj.target(),'SearchResults')) {
			dom_obj.stop()
			reg.NavigateResults(-1);
		}
	} else if  (dom_obj.key()['string']=='KEY_ARROW_DOWN') {
		dom_obj.stop();
		reg.NavigateResults(1);
	} else if  (dom_obj.key()['string']=='KEY_PAGE_UP') {
		if (hasParent(dom_obj.target(),'SearchResults')) {
			dom_obj.stop()
			reg.NavigateResults(-10);
		}
	} else if  (dom_obj.key()['string']=='KEY_PAGE_DOWN') {
		if (hasParent(dom_obj.target(),'SearchResults')) {
			dom_obj.stop()
			reg.NavigateResults(10);
		}
	} else if  (dom_obj.key()['string']=='KEY_HOME') {
		if (hasParent(dom_obj.target(),'SearchResults')) {
			dom_obj.stop()
			reg.NavigateResults('home');
		}
	} else if  (dom_obj.key()['string']=='KEY_END') {
		if (hasParent(dom_obj.target(),'SearchResults')) {
			dom_obj.stop()
			reg.NavigateResults('end');
		}
	}
}


//AJAX Post function
function postJSON(url, postVars) {
	reg.toggle_message("Sending request...");
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

var reg = {};


// variables ===================
reg.g_nTimeoutId;
reg.CustomerId = '';
// utility functions ===========

reg.collectPostVars = function(f){
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
      	postVars+= f.elements[i].name +'='+ reg.multiselect_csv(f.elements[i].id);
      } else {
      	postVars+= f.elements[i].name +'='+ f.elements[i].options[f.elements[i].selectedIndex].value;
      }
    }
  }
  return postVars;
}

reg.multiselect_csv = function(element_id){
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

reg.clearAllFormFields = function(parentid){
	elems = getElementsByTagAndClassName('input',null,parentid);
	for (var i=0;i<elems.length;i++){
		elems[i].value = "";
	}
}

// AJSON reactions ==================
reg.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	reg.toggle_message("");
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
reg.error_report = function(data){
	reg.toggle_message("ERROR");
	var d = callLater(5,reg.toggle_message);
}

reg.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

reg.merge_hidden_inputs = function(parentid){
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
	Call the search procedure and return the results below
*/
reg.Search = function(){
	var SearchText = getElement('SearchText').value;
	var SearchAddress = getElement('SearchAddress').value;
	reg.toggle_message("Searching...");
  	var postVars = 'SearchText='+SearchText+'&SearchAddress='+SearchAddress;
  	var d = postJSON('RegistrationSearch',postVars);
  	d.addCallbacks(reg.RenderSearchResults,reg.error_report);
}

/*
	There are two parameters: customer_id and receipt_id, which are two
	DIVs which might contain numbers.  If they do, then we want to load
	them when the page finishes loading.  Otherwise, do nothing.
*/
reg.OpenOnLoad = function() {
	if (getElement('SearchText')!=null) {
		getElement('SearchText').focus();
	}
}

/*
	NavigateResults: Move up and down the list of results
	n: The number of records to move: 1, 10, -1, -10, 'home', 'end'
		if the record is on the first and we need to navigate "up" then we'll go to the bottom of the list
		if we're at the end, and we need to navigate "down" then we'll go to the top of the list
*/
reg.NavigateResults = function(n){
	var curResult = getElementsByTagAndClassName('LI','itemSelected','SearchResults');
	if (curResult.length==0) {
		var results = getElementsByTagAndClassName('LI',null,'SearchResults');
		addElementClass(results[0],'itemSelected');
		results[0].firstChild.focus();
	} else if (n=='home') {
		// Clear previous selected item
		for (var i=0;i<curResult.length;i++) {
			removeElementClass(curResult[i],'itemSelected');
		}
		var results = getElementsByTagAndClassName('LI',null,'SearchResults');
		addElementClass(results[0],'itemSelected');
		results[0].firstChild.focus();
	} else if (n=='end') {
		// Clear previous selected item
		for (var i=0;i<curResult.length;i++) {
			removeElementClass(curResult[i],'itemSelected');
		}
		var results = getElementsByTagAndClassName('LI',null,'SearchResults');
		addElementClass(results[results.length-1],'itemSelected');
		results[results.length-1].firstChild.focus();
	} else if (!isNaN(n)) {
		//Move up/down by 1 or by 10
		// Clear previous selected item
		for (var i=0;i<curResult.length;i++) {
			removeElementClass(curResult[i],'itemSelected');
		}
		var RowNum = parseInt(curResult[0].id.slice(4)); //Our current row number (hidden in the id)
		var results = getElementsByTagAndClassName('LI',null,'SearchResults');
		if (RowNum+n > results.length-1) { // We're scrolling past the end
			if (RowNum==results.length-1) { // If we're at the end, go to the start
				addElementClass(results[0],'itemSelected');
				results[0].firstChild.focus();
			} else { // If we're not at the end, then go to the end
				addElementClass(results[results.length-1],'itemSelected');
				results[results.length-1].firstChild.focus();			
			}
		} else if (RowNum+n < 0) {// We're scrolling past the start
			if (RowNum==0) { // If we're at the start, go to the end
				addElementClass(results[results.length-1],'itemSelected');
				results[results.length-1].firstChild.focus();			
			} else { // If we're not at the start, go to the start
				addElementClass(results[0],'itemSelected');
				results[0].firstChild.focus();
			}
		} else {// Scroll the results
			var newRow = RowNum+parseInt(n);
			addElementClass('row_'+newRow,'itemSelected');
			getElement('row_'+newRow).firstChild.focus();
		}
	}
}
/*
	SelectResult: Search for the result with the 'itemSelected' class in the "SearchResults" DIV
		then load that item
*/
reg.SelectResult = function() {
	var curResult = getElementsByTagAndClassName('LI','itemSelected','SearchResults');
	if (curResult.length>0) {
		 location = getElementsByTagAndClassName('LI','itemSelected',curResult[0])[0].href;
	}
}
/* 	Call back from Ajax call initiated by reg.OpenSearch()
	data comes from "controllers_reg.py"->"LoadPatient"
	
	Patient/customer data and receipt information is loaded in this step
*/
reg.RenderSearchResults = function(data){
	var HREF = function(ID){
		var elem = createDOM('A',{'style':'padding-right:10px','href':'RegistrationPage1?PatientID='+ID},'Select');
		return elem;
	}
	var AddResultRow = function(result,row){
		var Display = result.text;
		var ID = result.id;
		var row = createDOM('LI',{'id':'row_'+row});
		replaceChildNodes(row, HREF(ID),Display);
		return row;
	}
	//Reset the message
	reg.toggle_message("");
	//If there is an url_var object, then we want to load the registration document right away
	if (data.url_var) {
		document.location.href = 'RegistrationPage1?'+data.url_var;
	}
	var RecordCount = data.result_count;
	var results = data.results;
	//Make the list of pending items
	var listing = getElement('SearchResults');
	Items = 0;
	replaceChildNodes(listing,RecordCount+' record(s) found');
	for (i=0; i<results.length; i++){
		listing.appendChild(AddResultRow(results[i],i));
	}
	//Change pending items title
	var title = getElement('PendingItemsTitle');
	replaceChildNodes(title,Items + " Pending Items");
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
//Connect our buttons to events -- need to do this on document load
connect(window, 'onload', function(){
	connect('btnSearch','onclick',reg.Search);
	});
//Connect on onload for the document to open the document using javascript
connect(window, 'onload', reg.OpenOnLoad);
/*
	Small dialog box, for entering the customer id
*/
reg.customeriddialog_remove = function(){
	swapDOM('customerid_dialog',null);
	swapDOM('customerid_shadow',null);
}
reg.renderCustomerIdDialog = function(){
	var StringEdit = function(name, label, value){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','name':name,'id':'dialog_'+name, 'value':value});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	reg.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'customerid_dialog','style':'height:70px'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'customerid_shadow','style':'height:80px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:reg.customeriddialog_remove()'},"Close");
	dialog.appendChild(close_link);
	//The main table
	var table = createDOM('TABLE',{'class':'regular'});
	var tbody = createDOM('TBODY',null);
	// Add field
	tbody.appendChild(StringEdit('CustomerID','Customer ID',''));
	//Create our dialog
	table.appendChild(tbody);
	dialog.appendChild(table);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Attach the button event
	connect('dialog_CustomerID','onkeydown',shortcuts.keydown);
	getElement('dialog_CustomerID').focus();
}