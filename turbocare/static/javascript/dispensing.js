//Document wide variables
var barcode = {};//The barcode object
//The barcode value
barcode.CustomerID = ''; //Defined as 20 numeric characters followed by a enter key
barcode.StockItemID = '';//Defined as 22 numeric characters followed by a enter key
barcode.DispenseAll = '';//captures the text "dispenseall" followed by the enter key (needs to be lower case, no spaces)
//capture the keypress event.  We're looking for 20 consecutive numeric values
//followed by an enter key.  The enter key is captured by a separate function.
barcode.keypress = function(dom_obj){
	var DispenseAllText = 'dispenseall';
	if (dom_obj.modifier()['any'] == false){
		var key = dom_obj.key()['string'];
		if (isNaN(key)) {
			barcode.CustomerID = '';
			barcode.StockItemID = '';
			barcode.DispenseAll = barcode.DispenseAll + key;
		} else {
			barcode.CustomerID = barcode.CustomerID + key;
			barcode.StockItemID = barcode.StockItemID + key;
			barcode.DispenseAll = '';
		}
		if (barcode.CustomerID.length > 20) {
			barcode.CustomerID = '';
		}
		if (barcode.StockItemID.length > 22) {
			barcode.StockItemID = '';
		}
		if ((barcode.DispenseAll.length > 12) || (barcode.DispenseAll != DispenseAllText.slice(0,barcode.DispenseAll.length))) {
			barcode.DispenseAll = '';
		}
	} else {
		barcode.CustomerID = '';
		barcode.StockItemID = '';
	}
}
//Capture the enter key.  If our barcode is full when an enter key is pressed
//We are most likely entering a barcode.  At this point, we signal a barcode event!
barcode.keydown = function(dom_obj) {
	var DispenseAllText = 'dispenseall';
	if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.CustomerID.length==20)){
		signal(document,'customerid',barcode.CustomerID);
	} else if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.StockItemID.length==22)){
		signal(document,'stockitemid',barcode.StockItemID);
	} else if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.DispenseAll==DispenseAllText)){
		signal(document,'dispenseall','dispense all');
	} else if (dom_obj.key()['string']=='KEY_ENTER') {
		barcode.CustomerID = '';
		barcode.StockItemID = '';
		barcode.DispenseAll = '';
	}
}
/*
	Events for the barcode reader.  The connect operations are made at the bottom of the document
*/
//When a customerid event (custom event) is fired, we process it here
barcode.LoadCustomerID = function(dom_obj) {
	//Load the items available for the customer
  	var postVars = 'barcode='+barcode.CustomerID;
	barcode.CustomerID = '';
	obj.LoadDocs('LoadPatient',postVars);
//  	d = postJSON('LoadPatient',postVars);
//  	d.addCallbacks(obj.LoadPatient,obj.error_report);
}
//When a stockitemid event (custom event) is fired, we process it here
barcode.LoadStockItemID = function(dom_obj) {
	//check if the stock item id is available in the current items
	var ID = parseInt(barcode.StockItemID);
	var form = getElement('CustomerItems');
	var Inputs = getElementsByTagAndClassName('INPUT',null,form);
	for (i=0; i<Inputs.length; i++){
		if ((getNodeAttribute(Inputs[i],'name')=='StockItemId') && (Inputs[i].value == ID)){
			if (getNodeAttribute(Inputs[i],'class')=='row') {
				swapElementClass(Inputs[i],'row','row_go');
			} else {
				swapElementClass(Inputs[i],'row_lite','row_go');
			}
		}
	}
	barcode.StockItemID = '';
}
// The dipense all event is caught by another function!! obj.DispenseAll()

/*
	My custom shortcuts:
	1. Open a dialog box for entering a customer id
	2. Call the "dispense all" operation
*/
var shortcuts = {};//keyboard short cut operations
shortcuts.keypress = function(dom_obj){
	if ((dom_obj.modifier()['ctrl'] == true) && (dom_obj.key()['string'] == 'c')) {
		obj.renderCustomerIdDialog();
	} else if ((dom_obj.modifier()['ctrl'] == true) && (dom_obj.modifier()['alt'] == true) && (dom_obj.key()['string'] == 'd')) {
		var postVars = obj.collectPostVars(getElement('CustomerItems'));
		postVars = postVars + '&CustomerID='+obj.CustomerId;
		obj.LoadDocs('SaveReceiptItems',postVars);
	}
}
shortcuts.keydown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		//Perform a search
		if (getNodeAttribute(getElement('dialog_CustomerID'),'type') != null) {
			var customerid = getElement('dialog_CustomerID').value;
			obj.customeriddialog_remove();
			obj.LoadDocs('LoadPatient','barcode='+customerid);
		}
	}
}


//AJAX Post function
function postJSON(url, postVars) {
	obj.toggle_message("Sending request...");
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

var obj = {};


// variables ===================
obj.g_nTimeoutId;
obj.CustomerId = '';
obj.deferreds = null;
// utility functions ===========

obj.collectPostVars = function(f){
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
      	postVars+= f.elements[i].name +'='+ obj.multiselect_csv(f.elements[i].id);
      } else {
      	postVars+= f.elements[i].name +'='+ f.elements[i].options[f.elements[i].selectedIndex].value;
      }
    }
  }
  return postVars;
}

obj.multiselect_csv = function(element_id){
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

obj.clearAllFormFields = function(parentid){
	elems = getElementsByTagAndClassName('input',null,parentid);
	for (var i=0;i<elems.length;i++){
		elems[i].value = "";
	}
}

// AJSON reactions ==================
obj.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	obj.toggle_message("");
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
obj.error_report = function(data){
	obj.toggle_message("ERROR");
	var d = callLater(5,obj.toggle_message);
}

obj.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

obj.merge_hidden_inputs = function(parentid){
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
	All ajson actions wrapped in one function
	I need this because I have a deferred that gets called every minute
	name: either - LoadPatient, GetListOfCustomers, SaveReceiptItems
	postVars: if we're posting vars, then the variables to post
	
*/
obj.LoadDocs = function(name,postVars){
	//cancel any pending events and reset
	if (obj.deferreds != null) {
		//This even is normally the timer event which goes every minute (or two minutes)
		//If this is not cancelled, then I will get extra timer events.
		obj.deferreds.cancel();
	}
	//configure new events
	if (name == 'LoadPatient') {
		obj.toggle_message("Loading data...");
		var d1 = postJSON('LoadPatient',postVars);
		var d2 = loadJSONDoc('GetListOfCustomers');
		// a list of deferreds
		var list = new DeferredList([d1, d2], false, false, true);
		list.addCallback(function (resultList) {
			if ( ! resultList[0][0] || ! resultList[1][0])  {
				obj.error_report();
			} else  {
				obj.RenderPendingItems(resultList[1][1]);
				obj.LoadPatient(resultList[0][1]);
                        }
		});
		obj.deferreds = list;
	} else if (name == 'SaveReceiptItems') {
		obj.toggle_message("Saving data...");
		var d1 = postJSON('SaveReceiptItems',postVars);
		var d2 = loadJSONDoc('GetListOfCustomers');
		// a list of deferreds
		var list = new DeferredList([d1, d2], false, false, true);
		list.addCallback(function (resultList) {
			if ( ! resultList[0][0] || ! resultList[1][0])  {
				obj.error_report();
			} else  {
				obj.RenderPendingItems(resultList[1][1]);
				obj.LoadPatient(resultList[0][1]);
                        }
		});
		obj.deferreds = list;	
	} else {
		obj.toggle_message("Loading listing...");
		var d2 = loadJSONDoc('GetListOfCustomers');
		d2.addCallbacks(obj.RenderPendingItems,obj.error_report);
		obj.deferreds = d2;
	}
}
/*
	Dispense one item of the items listed
	1. Find the receipt item id for the row
	2. Send the request to the server
	3. Reload the customer's information (should be 1 item less)
*/
obj.DispenseLine = function(btn){
	var elem = btn.src();
	var col = elem.parentNode;
	var Inputs = getElementsByTagAndClassName('INPUT',null,col);
	for (i=0; i<Inputs.length; i++){
		if (getNodeAttribute(Inputs[i],'name') == 'ReceiptItemId') {
			var ReceiptItemId = Inputs[i].value;
		}
	}
	var postVars = 'CustomerID='+obj.CustomerId+'&Counter=1&ReceiptItemId='+ReceiptItemId;
	obj.LoadDocs('SaveReceiptItems',postVars);
}
/*
	Dispense all items listed
	1. Send the entire form's data
	2. Send the request to the server
*/
obj.DispenseAll = function(){
	var postVars = obj.collectPostVars(getElement('CustomerItems'));
	postVars = postVars + '&CustomerID='+obj.CustomerId;
	obj.LoadDocs('SaveReceiptItems',postVars);
}

/*
	There is 1 parameter: customer_id located in a div
	If there is an id there, then call "OpenPatient" to load that patient's data
	Initiate the function to reload the pending items list
*/
obj.OpenOnLoad = function() {
	var elem = getElement('customer_id');
	var CustomerID = scrapeText(elem);
	if (CustomerID != '') {
		var postVars = 'barcode='+CustomerID;
		obj.LoadDocs('LoadPatient',postVars);
//		d = postJSON('LoadPatient',postVars);
//		d.addCallbacks(obj.LoadPatient,obj.error_report);
	} else {
		obj.LoadDocs('GetListOfCustomers',postVars);
//	obj.LoadPendingItems();
	}
}
/*
	Pending Items List:  This list is reloaded every minute.
	Don't know what happens when this event coincides with
	another Ajson event?
*/
obj.LoadPendingItems = function(){
	obj.LoadDocs('GetListOfCustomers','');
}
/*
	AJSON Reactions to the above actions
*/

/* 
	Patient/customer data and receipt information is loaded in this step
*/
obj.LoadPatient = function(data){
	var ColName = function(text){
		var col = createDOM('DIV',{'style':'text-align: left; padding-left:4px'},text);
		return col;
	}
	var ColQuantity = function(text) {
		var col = createDOM('DIV',{'style':'text-align: right; padding-left:4px'},text);
		return col;
	}
	var ColBatch = function(text) {
		var col = createDOM('DIV',{'style':'text-align: left; padding-left:4px;','class':'clear'},text);
		return col;
	}
	var ColButton = function(ReceiptItemId, StockItemId) {
		var col = createDOM('DIV',{'style':'text-align: right; padding-left:4px;','class':'clear'});
		var button = createDOM('INPUT',{'type':'BUTTON', 'name':'Dispense', 'value':'Dispense'});
		var receiptitemid = createDOM('INPUT',{'type':'HIDDEN', 'name':'ReceiptItemId', 'value':ReceiptItemId});
		var stockitemid = createDOM('INPUT',{'type':'HIDDEN', 'name':'StockItemId', 'value':StockItemId});
		var counter = createDOM('INPUT',{'type':'HIDDEN', 'name':'Counter', 'value':'1'});
		appendChildNodes(col, button, receiptitemid, stockitemid,counter);
		return col;
	}
	var AddReceiptItemRow = function(ReceiptItem,Paid){
		var ReceiptItemId = ReceiptItem.receiptitem_id;
		var StockItemId = ReceiptItem.stockitem_id;
		var Quantity = ReceiptItem.quantity;
		var Name = ReceiptItem.name;
		var BatchNumber = ReceiptItem.batch_number;
		if (Paid) {
			var row = createDOM('DIV',{'id':ReceiptItemId,'class':'row'});
		} else {
			var row = createDOM('DIV',{'id':ReceiptItemId,'class':'row_lite'});
		}
		appendChildNodes(row,ColName(Name),ColQuantity(Quantity),ColBatch(BatchNumber),ColButton(ReceiptItemId,StockItemId));
		return row;
	}
	var AddButtonRow = function() {
		var row = createDOM('DIV',{'id':'dispenseallrow','style':'margin-top:2px', 'class':'row'});
		var col_button = createDOM('INPUT',{'type':'BUTTON','style':'font-size:100%', 'name':'DispenseAll', 'value':'Dispense All'});
		row.appendChild(createDOM('DIV',{'class':'clear'},' '));
		row.appendChild(createDOM('DIV',{'class':'clear'},' '));
		row.appendChild(createDOM('DIV',{'class':'clear'},' '));
		row.appendChild(createDOM('DIV',{'style':'text-align:right', 'class':'clear'},col_button));
		return row;
	}
	var AddTitle = function(CustomerName){
		var elem = getElement('CurrentItemsTitle');
		var Title = 'Current items for: ' + CustomerName;
		replaceChildNodes(elem,Title);
	}
	var AddCustomerInformation = function(CustomerInfo, Name){
		var info = getElement('CurrentItemsTitle');
		var Title = 'Current items for: ' + Name;
		replaceChildNodes(info,Title);
		info.appendChild(createDOM('LI',null,'Status: '+CustomerInfo.encounter_class));
		if (CustomerInfo.encounter_class_id == 'inpatient') { //include inpatient information, otherwise, skip it
			if (CustomerInfo.is_discharged){
				info.appendChild(createDOM('LI',null,'Is Discharged'));
				info.appendChild(createDOM('LI',null,'Was discharged on '+CustomerInfo.discharge_datetime));
			} else {
				info.appendChild(createDOM('LI',null,'Is Admitted'));
			}
		}
		info.appendChild(createDOM('LI',null,'Payment type: '+CustomerInfo.name));
		info.appendChild(createDOM('LI',null,CustomerInfo.firm+', '+CustomerInfo.number));
	}
	//Reset the message
	obj.toggle_message("");
	var PaidReceiptItems = data.paid_items;
	var UnpaidReceiptItems = data.unpaid_items;
	var CustomerInfo = data.encounter;
	var Name = data.customer_name;
	//Load our global variable
	obj.CustomerId = data.customerid;
	//Make the Customer info box
	AddCustomerInformation(CustomerInfo,Name);
	//Modify our title line
	//AddTitle(Name);
	//Make the item list
	var table = getElement('CustomerItemsTable');
	replaceChildNodes(table,null);
	for (i=0; i<PaidReceiptItems.length; i++){
		table.appendChild(AddReceiptItemRow(PaidReceiptItems[i],true));
	}
	for (i=0; i<UnpaidReceiptItems.length; i++){
		table.appendChild(AddReceiptItemRow(UnpaidReceiptItems[i],false));
	}
	if (PaidReceiptItems.length + UnpaidReceiptItems.length > 0) {
		table.appendChild(AddButtonRow());
	}
	//Connect events after DOM objects created
	//Connect button events
	var Inputs = getElementsByTagAndClassName('INPUT',null,table);
	for (j=0; j<Inputs.length; j++){
		if (getNodeAttribute(Inputs[j],'value') == 'Dispense') {
			connect(Inputs[j],'onclick',obj.DispenseLine);
		} else if (getNodeAttribute(Inputs[j],'value') == 'Dispense All') {
			connect(Inputs[j],'onclick',obj.DispenseAll);
		}
	}
}

/* 
	Patient/customer data and receipt information is loaded in this step
*/
obj.RenderPendingItems = function(data){
	var AddCustomerRow = function(CustomerId,CustomerInfo,CustomerItems){
		var Name = CustomerInfo.name;
		var row = createDOM('DIV',{'id':CustomerId,'class':'ListItemRow'},Name + ' with ' + CustomerItems.length + ' items');
		for (j=0; j<CustomerItems.length; j++){
			if (CustomerItems[j].paid) {
				row.appendChild(createDOM('LI',null,CustomerItems[j].name));
			} else {
				row.appendChild(createDOM('LI',{'class':'lite'},CustomerItems[j].name));
			}
		}
		return row;
	}
	//Reset the message
	obj.toggle_message("");
	var CustomerIDs = data.customer_ids;
	var CustomerInfo = data.customer_info;
	var CustomerItems = data.customer_items;
	//Make the list of pending items
	var listing = getElement('PendingItems');
	Items = 0;
	replaceChildNodes(listing,null);
	for (i=0; i<CustomerIDs.length; i++){
		Items = Items + CustomerItems[CustomerIDs[i]].length;
		listing.appendChild(AddCustomerRow(CustomerIDs[i],CustomerInfo[CustomerIDs[i]],CustomerItems[CustomerIDs[i]]));
	}
	//Change pending items title
	var title = getElement('PendingItemsTitle');
	replaceChildNodes(title,Items + " Pending Items");
	//After one minute call the procedure again
	var d = callLater(60,obj.LoadPendingItems);
	obj.deferreds = d;
}


//Configure our events using the Mochikit signal library
/* DEFINE OUR EVENT FUNCTIONS */
connect(document,'onkeydown', barcode.keydown);
connect(document,'onkeypress', barcode.keypress);
connect(document,'customerid', barcode.LoadCustomerID);
connect(document,'stockitemid', barcode.LoadStockItemID);
connect(document,'dispenseall', obj.DispenseAll);

//custom short-cuts
connect(document,'onkeypress',shortcuts.keypress);
connect(document,'onkeydown', shortcuts.keydown);
//Connect our buttons to events -- need to do this on document load
/*connect(window, 'onload', function(){
	connect('btnSearch','onclick',obj.Save);
	connect('btnEdit','onclick',obj.Edit);
	connect('btnAppend','onclick',obj.Append);
	connect('btnPrint','onclick',obj.Print);
	connect('btnCancel','onclick',obj.Cancel);
	connect('btnNew','onclick',obj.New);
	connect('btnPay','onclick',obj.renderPayment);
	});*/
//Connect on onload for the document to open the document using javascript
connect(window, 'onload', obj.OpenOnLoad);


/*
	Small dialog box, for entering the customer id
*/

obj.customeriddialog_remove = function(){
	swapDOM('customerid_dialog',null);
	swapDOM('customerid_shadow',null);
}
obj.renderCustomerIdDialog = function(){
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
	obj.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'customerid_dialog','style':'height:70px'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'customerid_shadow','style':'height:80px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:obj.customeriddialog_remove()'},"Close");
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
	getElement('dialog_CustomerID').focus();
}
