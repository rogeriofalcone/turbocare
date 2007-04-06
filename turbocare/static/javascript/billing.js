//Document wide variables
var isEmpty = true;//If no current record is loaded, then true, otherwise, false
var barcode = {};//The barcode object
//The barcode value
barcode.value = '';
//capture the keypress event.  We're looking for 20 consecutive numeric values
//followed by an enter key.  The enter key is captured by a separate function.
barcode.keypress = function(dom_obj){
	if (dom_obj.modifier()['any'] == false){
		var key = dom_obj.key()['string'];
		if (isNaN(key)) {
			barcode.value = '';
		} else {
			barcode.value = barcode.value + key;
		}
		if (barcode.value.length > 20) {
			barcode.value = '';
		}
	} else {
		barcode.value = '';
	}
}
//Capture the enter key.  If our barcode is full when an enter key is pressed
//We are most likely entering a barcode.  At this point, we signal a barcode event!
barcode.keydown = function(dom_obj) {
	if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.value.length==20)){
		signal(document,'barcode',barcode.value);
	} else if (dom_obj.key()['string']=='KEY_ENTER') {
		barcode.value = '';
	}
}
//When a barcode event (custom event) is fired, we process it here
barcode.load = function(obj) {
	//load the billing customer
	billing.OpenPatient("LoadPatient?barcode="+barcode.value);
	barcode.value = '';
}

/*
	My custom shortcuts:
	1. Open a dialog box for entering a customer id
*/
var shortcuts = {};//keyboard short cut operations
shortcuts.keypress = function(obj){
	if ((obj.modifier()['ctrl'] == true) && (obj.key()['string'] == 'c')) {
		billing.renderCustomerIdDialog();
	}
}
shortcuts.keydown = function(obj){
	if (obj.key()['string']=='KEY_ENTER') {
		//Grab the entered key and try to open the customer record
		var elem = getElement('customerid_dialog');
		if (getNodeAttribute(elem,'class') == 'dialogbox'){
			//Grab the first input box and take the value
			var customerid = getElementsByTagAndClassName('INPUT',null,elem)[0].value;
			billing.customeriddialog_remove();
			if (customerid != '') {
				billing.OpenPatient("LoadPatient?barcode="+customerid);
			}
		}
	}
}

//AJAX Post function
function postJSON(url, postVars) {
	billing.toggle_message("Sending request...");
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

var billing = {};


// variables ===================
billing.g_nTimeoutId;
billing.CustomerId = '';
billing.ReceiptId = '';
billing.EncounterId = '';
billing.list_def = '';
billing.Mode = 'View';//Other options: Update, Append, Remove
billing.EditMode = '';//The RowID for the receipt item currently being edited
billing.TempQty = '';//When a record is in edit mode, temporarily record the original value in case we cancel the edit
billing.TempLocation = '';//When a record is in edit mode, temporarily record the original value in case we cancel the edit
billing.IsBookletPrinting = false;
// utility functions ===========

billing.collectPostVars = function(f){
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
      	postVars+= f.elements[i].name +'='+ billing.multiselect_csv(f.elements[i].id);
      } else {
      	postVars+= f.elements[i].name +'='+ f.elements[i].options[f.elements[i].selectedIndex].value;
      }
    }
  }
  return postVars;
}

billing.multiselect_csv = function(element_id){
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

billing.clearAllFormFields = function(parentid){
	elems = getElementsByTagAndClassName('input',null,parentid);
	for (var i=0;i<elems.length;i++){
		elems[i].value = "";
	}
}
/*
	Searches the current receipt item row
	for the specified Input box and returns the
	value.  Otherwise, it returns false.
*/
billing.getReceiptItemInputVal = function(row,name) {
	var Inputs = getElementsByTagAndClassName('INPUT',null,row);
	for (j=0; j<Inputs.length; j++){
		if (getNodeAttribute(Inputs[j],'name') == name) {
			return Inputs[j].value;
		}
	}//end of for-loop
	return false;
}
// Like the above, except that it sets the value.
billing.setReceiptItemInputVal = function(row,name,value) {
	var Inputs = getElementsByTagAndClassName('INPUT',null,row);
	for (j=0; j<Inputs.length; j++){
		if (getNodeAttribute(Inputs[j],'name') == name) {
			Inputs[j].value = value;
			return Inputs[j].value;
		}
	}//end of for-loop
	return false;
}
/*
	Checks all receipt items.  If any of the items has been modified
	then the function returns true, otherwise false.
*/
billing.IsModified = function(){
	var Inputs = getElementsByTagAndClassName('INPUT',null,'receipt');
	for (i=0; i<Inputs.length; i++){
		if (getNodeAttribute(Inputs[i],'name') == 'IsModified') {
			if (Inputs[i].value == 'true'){
				return true;
			}
		}
	}
	return false;
}
// AJSON reactions ==================
billing.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	billing.toggle_message("");
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
billing.DoBookletPrinting = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	billing.toggle_message("");
	if (data.result_msg != null) {
		var display = createDOM('DIV',{'class':'displaymsg','id':'last_result_msg'},data.result_msg);
		if (getNodeAttribute('last_result_msg','class') == null){
			document.body.appendChild(display);
		} else {
			swapDOM(field.id,display);
		}
	}
	var d = callLater(5,remove_message);
	billing.BookletPrint();
}
billing.DoBookletPrintingError = function(data){
	billing.toggle_message("ERROR");
	var d = callLater(5,billing.toggle_message);
	billing.BookletPrint();
}
billing.error_report = function(data){
	billing.toggle_message("ERROR");
	var d = callLater(5,billing.toggle_message);
}

billing.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

billing.merge_hidden_inputs = function(parentid){
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
billing.saveForm = function(url){
	billing.toggle_message("Saving...");
  	var postVars =billing.collectPostVars(document.receiptform);
  	var d = postJSON(url,postVars);
  	d.addCallbacks(billing.LoadPatient,billing.error_report);
}

billing.saveData = function(url,vars){
	billing.toggle_message("Saving...");
  	var d = postJSON(url,vars);
  	d.addCallbacks(billing.updated,billing.error_report);
}

billing.deleteObj = function(){
	var Result = function(data){
		billing.toggle_message("");
		alert(data.result_msg);
		if (data.result != 0) {
			billing.openObjView(billing.cur_def.Read);
		}
	}
	if (billing.cur_def.id != null) {
		if (confirm("Are you sure you want to delete?")) {
			billing.toggle_message("Deleting...");
			url = billing.cur_def.Del;
			var d = postJSON(url,'id='+billing.cur_def.id);
			d.addCallback(Result);		
		}
	}
}
billing.Save = function(){
	billing.saveForm('SaveReceipt');
}
billing.Edit = function(){
	if (billing.EditMode != '') {
		if (confirm('Not all changes are saved, do you want to save?')) {
			billing.Save();
		}
	} else {
		if (billing.Mode != 'Edit') {
			billing.Mode = 'Edit';
			//Update buttons
			updateNodeAttributes('btnSave',{'class':''});
			updateNodeAttributes('btnCancel',{'class':''});
		} else {
			//Search for all rows and reset there style
			var ReceiptRows = getElementsByTagAndClassName('DIV','row','receipt');
			for (i=0; i<ReceiptRows.length; i++){
				updateNodeAttributes(ReceiptRows[i],{'style':'background-color:transparent'});
				var ReceiptButtons = getElementsByTagAndClassName('INPUT',null,ReceiptRows[i]);
				for (j=0; j<ReceiptButtons.length; j++){
					updateNodeAttributes(ReceiptButtons[j],{'style':'display:none'});
				}
			}
			billing.Mode = 'View';
			//Update buttons
			updateNodeAttributes('btnSave',{'class':'invisible'});
			updateNodeAttributes('btnCancel',{'class':'invisible'});
		}
	}
}

billing.Append = function(){
	if (billing.CustomerId != '') {	
		if (confirm("Are you sure you want to add new items?")) {
			billing.toggle_message("Loading...");
			var d = loadJSONDoc('CustomerAddReceipt?id='+billing.CustomerId+'&ReceiptID='+billing.ReceiptId);
			d.addCallbacks(billing.pickList,billing.error_report);
		}
	} else {
		alert('You need to select a customer first');
	}
}
billing.Print = function(data){
	if (data.receiptid == billing.ReceiptId) {
		//In this situation, the data variable is an updated receipt entry which we should load
		billing.LoadPatient(data);
		//Now continue with the printing...
		if (confirm("Do you want to print a receipt?")) {
			billing.toggle_message("Printing...");
			var d = loadJSONDoc('BillingPrintReceipt?ReceiptID='+billing.ReceiptId);
			d.addCallbacks(billing.DoBookletPrinting,billing.DoBookletPrintingError);
		} else {
			billing.BookletPrint();
		}
	} else {
		if (confirm("Do you want to print a receipt?")) {
			billing.toggle_message("Printing...");
			var d = loadJSONDoc('BillingPrintReceipt?ReceiptID='+billing.ReceiptId);
			d.addCallbacks(billing.DoBookletPrinting,billing.DoBookletPrintingError);
		} else {
			billing.BookletPrint();
		}
	}
}
billing.BookletPrint = function(){
	if (billing.IsBookletPrinting) {
		if (confirm("Do you want to print a booklet label?")) {
			billing.toggle_message("Printing Booklet Label...");
			var d = loadJSONDoc('BillingPrintBookletLabel?ReceiptID='+billing.ReceiptId);
			d.addCallbacks(billing.updated,billing.error_report);
		}
	}
}
/*
	Change the mode to viewing and reload the receipt
*/
billing.Cancel = function(){
	//Search for all rows and reset there style
	var ReceiptRows = getElementsByTagAndClassName('DIV','row','receipt');
	for (i=0; i<ReceiptRows.length; i++){
		updateNodeAttributes(ReceiptRows[i],{'style':'background-color:transparent'});
		var ReceiptInputs = getElementsByTagAndClassName('INPUT',null,ReceiptRows[i]);
		for (j=0; j<ReceiptInputs.length; j++){
			updateNodeAttributes(ReceiptInputs[j],{'style':'display:none'});
		}
	}
	billing.Mode = 'View';
	//Update buttons
	updateNodeAttributes('btnSave',{'class':'invisible'});
	updateNodeAttributes('btnCancel',{'class':'invisible'});
	billing.OpenPatient('LoadPatient?ReceiptID='+billing.ReceiptId);
}
/*
	Take the curent line and set it into edit mode:
	1. Show the save and cancel buttons
	2. Hide the edit button
	3. Set the EditMode, TempQty and TempLocation variables
	4. Show the Qty edit box and the location drop down.
*/
billing.EditLine = function(row){
	//Show the Save and Cancel buttons, hide the Edit button
	var ReceiptButtons = getElementsByTagAndClassName('INPUT',null,row);
	for (j=0; j<ReceiptButtons.length; j++){
		if ((ReceiptButtons[j].value == 'Update') || (ReceiptButtons[j].value == 'Cancel')){
			updateNodeAttributes(ReceiptButtons[j],{'style':'display:block'});
		} else {
			updateNodeAttributes(ReceiptButtons[j],{'style':'display:none'});
		}
	}//end of for-loop
	//Show the select box
	var Select = getElementsByTagAndClassName('SELECT',null,row);
	for (j=0; j<Select.length; j++){
		if (getNodeAttribute(Select[j],'name') == 'StockLocationId') {
			updateNodeAttributes(Select[j],{'style':'display:block'});
			billing.TempLocation = Select[j].value;
		}
	}//end of for-loop
	//Show the Quantity box and Get the ReceiptItemID
	var Inputs = getElementsByTagAndClassName('INPUT',null,row);
	for (j=0; j<Inputs.length; j++){
		if (getNodeAttribute(Inputs[j],'name') == 'Qty') {
			updateNodeAttributes(Inputs[j],{'style':'display:block'});
			billing.TempQty = Inputs[j].value;
			var qty_box = Inputs[j];
		} else if (getNodeAttribute(Inputs[j],'name') == 'ReceiptItemId') {
			billing.EditMode = Inputs[j].value;
		}
	}//end of for-loop
	qty_box.focus();
	var d = callLater(1,redraw);
}
/*
	Delete the selected row:  Send the receipt item id to the server
	function to attempt to delete the row.  The receipt is reloaded...
	that's where you can confirm if a row is deleted or not.
*/
billing.DeleteLine = function(row){
	billing.toggle_message("Attempting to delete...");
  	var postVars = 'ReceiptItemID='+billing.getReceiptItemInputVal(row,'ReceiptItemId');
  	var d = postJSON('DeleteReceiptItem',postVars);
  	d.addCallbacks(billing.LoadPatient,billing.error_report);
  	return false;	
}
billing.New = function(){
	if (billing.CustomerId != '') {
		if (confirm("Are you sure you want to make a new bill?")) {
			billing.toggle_message("Loading...");
			var d = loadJSONDoc('CustomerAddReceipt?id='+billing.CustomerId);
			d.addCallbacks(billing.pickList,billing.error_report);
		}
	} else {
		alert('You need to select a customer first');
	}
}
billing.OpenPatient = function(url){
	if (url != null){
		if (billing.IsModified()) {
			if (confirm("Changes were made but not saved!  DISCARD changes?")) {
				billing.toggle_message("Loading...");
				var d = loadJSONDoc(url);
				d.addCallbacks(billing.LoadPatient,billing.error_report);
			}
		} else {
			billing.toggle_message("Loading...");
			var d = loadJSONDoc(url);
			d.addCallbacks(billing.LoadPatient,billing.error_report);
		}
	}
}
billing.OpenAppend = function(){
	if (confirm("Are you sure you want to add new items?")) {
		billing.toggle_message("Loading...");
		var d = loadJSONDoc('CustomerAddReceipt?id='+billing.CustomerId+'&ReceiptID='+billing.ReceiptId);
		d.addCallbacks(billing.pickList,billing.error_report);
	}
}
/*
	There are two parameters: customer_id and receipt_id, which are two
	DIVs which might contain numbers.  If they do, then we want to load
	them when the page finishes loading.  Otherwise, do nothing.
*/
billing.OpenOnLoad = function() {
	var customer_id = scrapeText(getElement('customer_id'));
	var receipt_id = scrapeText(getElement('receipt_id'));
	if (receipt_id != '') {
		billing.OpenPatient('LoadPatient?ReceiptID='+receipt_id);
	} else if (customer_id != '') {
		billing.OpenPatient('LoadPatient?barcode='+customer_id);
	}
}
/*
	When all the bill editing is done, and the payment is collected, then we need
	to mark the bill as paid and record how much was taken.  This calls the 
	server function to perform the payment saving.
*/
billing.Pay = function(CashAmt,CashNotes,InsrAmt,InsrNotes,TotalCashAmt){
	billing.toggle_message("Applying payment...");
	var urlvars = '?ReceiptID='+billing.ReceiptId+'&CashAmt='+CashAmt+'&CashNotes='+CashNotes+'&InsrAmt='+InsrAmt+'&InsrNotes='+InsrNotes+'&TotalCashAmt='+TotalCashAmt;
	var d = loadJSONDoc('MakeReceiptPayment'+urlvars);
	d.addCallbacks(billing.Print,billing.error_report);
}
/*
	AJSON Reactions to the above actions
*/

/* 	Call back from Ajax call initiated by billing.OpenPatient(url)
	data comes from "controllers_billing.py"->"LoadPatient"
	
	Patient/customer data and receipt information is loaded in this step
*/
billing.LoadPatient = function(data){
	var HiddenFields = function(receiptitemid, catalogitemid, stocklocationid, unitprice, ismodified){
		var col = createDOM('DIV',{'style':'display:none'});
		var receiptid = createDOM('INPUT',{'type':'hidden', 'name':'ReceiptId', 'value':billing.ReceiptId});
		var receiptitemid = createDOM('INPUT',{'type':'hidden', 'name':'ReceiptItemId', 'value':receiptitemid});
		var customerid = createDOM('INPUT',{'type':'hidden', 'name':'CustomerId', 'value':billing.CustomerId});
		var catalogitemid = createDOM('INPUT',{'type':'hidden', 'name':'CatalogItemId', 'value':catalogitemid});
		var encounterid = createDOM('INPUT',{'type':'hidden', 'name':'EncounterId', 'value':billing.EncounterId});
		var stocklocationid = createDOM('INPUT',{'type':'hidden', 'name':'StockLocationIDset', 'value':stocklocationid});
		var unitprice = createDOM('INPUT',{'type':'hidden', 'name':'UnitPrice', 'value':unitprice});
		var counter = createDOM('INPUT',{'type':'hidden', 'name':'Counter', 'value':'1'});
		var ismodified = createDOM('INPUT',{'type':'hidden', 'name':'IsModified', 'value':ismodified});
		appendChildNodes(col,receiptid, receiptitemid, customerid, catalogitemid, encounterid, stocklocationid, unitprice, counter, ismodified);
		return col;
	}
	var ColOne = function(text){
		//Special function to detect a BookletPrinting item
		if (text.toLowerCase()=="booklet printing") {
			billing.IsBookletPrinting = true;
		}
		var col = createDOM('DIV',{'class':'w40', 'name':'col1'},text);
		return col;
	}
	var ColTwo = function(text) {
		var col = createDOM('DIV',{'name':'col2','style':'text-align:right'},text);
		var ed = createDOM('INPUT',{'name':'Qty', 'size':'5', 'style':'display:none', 'value':text});
		col.appendChild(ed);
		return col;
	}
	var ColThree = function(text) {
		var col = createDOM('DIV',{'name':'col3','style':'text-align:right'},text);
		return col;
	}
	var ColFour = function(text) {
		var col = createDOM('DIV',{'class':'w15','name':'col4','style':'text-align:right'},text);
		return col;
	}
	var listbox = function(def,name,Options) {
		var select = createDOM('SELECT',{'name':name,'style':'display:none'});
		for (var i in Options){
			if (Options[i] == def) {
				var Option = createDOM('OPTION',{'value':i, 'selected':'selected'},Options[i]);
			} else {
				var Option = createDOM('OPTION',{'value':i},Options[i]);
			}
			select.appendChild(Option);
		}
		return select;
	}
	var ColFive = function(text, LocationOptions) {
		var col = createDOM('DIV',{'class':'w25','name':'col5'},text);
		col.appendChild(listbox(text,'StockLocationId',LocationOptions));
		return col;
	}
	var ColButtons = function() {
		var col = createDOM('DIV',{'class':'last'});
		col.appendChild(createDOM('INPUT',{'type':'button', 'style':'display:none','name':'col6ed', 'value':'Edit'}));
		col.appendChild(createDOM('INPUT',{'type':'button', 'style':'display:none','name':'col6sv', 'value':'Update'}));		
		col.appendChild(createDOM('INPUT',{'type':'button', 'style':'display:none','name':'col6cn', 'value':'Cancel'}));
		col.appendChild(createDOM('INPUT',{'type':'button', 'style':'display:none','name':'col6dl', 'value':'Delete'}));
		return col;
	}
	var AddReceiptRow = function(ReceiptItem){
		var RowID = 'ri_'+ReceiptItem.receiptitemid;
		var Location = ReceiptItem.locationname;
		var Total = ReceiptItem.qty * ReceiptItem.unitprice;
		if (ReceiptItem.ismodified == 'true') {
			var row = createDOM('DIV',{'id':RowID,'name':'receiptrow','style':'background-color:pink', 'receiptid':ReceiptItem.receiptitemid, 'class':'row'});
		} else {
			var row = createDOM('DIV',{'id':RowID,'name':'receiptrow','receiptid':ReceiptItem.receiptitemid, 'class':'row'});
		}
		row.appendChild(HiddenFields(ReceiptItem.receiptitemid, ReceiptItem.catalogitemid, ReceiptItem.stocklocationid, ReceiptItem.unitprice, ReceiptItem.ismodified));
		row.appendChild(ColOne(ReceiptItem.description));
		row.appendChild(ColTwo(ReceiptItem.qty));
		row.appendChild(ColThree(ReceiptItem.unitprice));
		row.appendChild(ColFour(Total));
		row.appendChild(ColFive(Location,ReceiptItem.locationoptions));
		row.appendChild(ColButtons());
		return row;
	}
	var AddColumnHeadings = function(){
		var row = createDOM('DIV',{'class':'rowtitle'});
		var col1 = createDOM('DIV',{'class':'w40'},'Item');
		var col2 = createDOM('DIV',null,'Qty');
		var col3 = createDOM('DIV',null,'Unit cost');
		var col4 = createDOM('DIV',{'class':'w15'},'Total');
		var col5 = createDOM('DIV',{'class':'w25'},'Location');
		var col6 = createDOM('DIV',{'class':'last'});
		appendChildNodes(row,col1,col2,col3,col4,col5,col6);
		return row;
	}
	var AddReceiptTotal = function(total) {
		var row = createDOM('DIV',{'class':'rowtotal'});
		var col1 = createDOM('DIV',{'class':'w40','style':'text-align:right'},'Total:');
		var col2 = createDOM('DIV',null);
		var col3 = createDOM('DIV',null);
		var col4 = createDOM('DIV',{'id':'receipt_total','style':'text-align:right'},total);
		var col5 = createDOM('DIV',{'class':'w25'});
		var col6 = createDOM('DIV',{'class':'last'});
		appendChildNodes(row,col1,col2,col3,col4,col5,col6);
		return row;
	}
	var AddTitle = function(text){
		var title = createDOM('DIV',{'class':'title'},text);
		return title;
	}
	var AddHistory = function(History){
		var history = createDOM('DIV',{'id':'history','class':'menuright'},'History information');
		for (i=0; i<History.length;i++){
			var item = createDOM('LI',{'class':'menuitem'}, History[i].description);
			var ReceiptID = createDOM('INPUT',{'type':'hidden', 'name':'receiptid', 'value':History[i].receiptid});
			item.appendChild(ReceiptID);
			history.appendChild(item);
		}
		return history;
	}
	var AddBillingInfo = function(Financial){
		var financial = createDOM('DIV',{'id':'customer_info','class':'infoboxright'},'Billing information');
		financial.appendChild(createDOM('LI',{'id':'insurance_type','style':'display:none'},Financial.type));
		financial.appendChild(createDOM('INPUT',{'id':'curr_receipt_paid','type':'hidden','value':Financial.curr_receipt_paid}));
		financial.appendChild(createDOM('INPUT',{'id':'balance_amt','type':'hidden','value':Financial.balance_amt}));
		financial.appendChild(createDOM('INPUT',{'id':'is_curr_receipt_in_balance','type':'hidden','value':Financial.is_curr_receipt_in_balance}));
		financial.appendChild(createDOM('LI',null,Financial.name));
		financial.appendChild(createDOM('LI',null,Financial.firm));
		financial.appendChild(createDOM('LI',null,Financial.number));
		financial.appendChild(createDOM('LI',null,Financial.all_receipts));
		financial.appendChild(createDOM('LI',null,Financial.all_payments));
		financial.appendChild(createDOM('LI',null,Financial.balance));
		return financial;
	}
	//Reset the message
	billing.toggle_message("");
	//Reset Booklet Printing
	billing.IsBookletPrinting = false;
	var ReceiptItems = data.receipt_items;
	var ReceiptHistory = data.receipt_history;
	var Financial = data.financial;
	//Load our global variables
	billing.CustomerId = data.customerid;
	billing.ReceiptId = data.receiptid;
	billing.EncounterId = data.encounterid;
	//Make the receipt
	var Receipt = createDOM('DIV',{'id':'receipt', 'class':'main'});
	Receipt.appendChild(AddTitle('Receipt for '+data.customer_name+' (ID:'+data.customerid+'), ' + data.receipt_status));
	var ReceiptTable = createDOM('DIV',{'class':'billtable'});
	ReceiptTable.appendChild(AddColumnHeadings());
	var total = 0;
	for (i=0; i<ReceiptItems.length; i++){
		total = total + ReceiptItems[i].qty * ReceiptItems[i].unitprice;
		ReceiptTable.appendChild(AddReceiptRow(ReceiptItems[i]));
	}
	ReceiptTable.appendChild(AddReceiptTotal(total));
	Receipt.appendChild(ReceiptTable);
	swapDOM('receipt',Receipt);
	//Make the history box
	swapDOM('history',AddHistory(ReceiptHistory));
	//Customer billing info box
	swapDOM('customer_info',AddBillingInfo(Financial));
	//Connect events after DOM objects created
	//Connect Receipt item rows events
	var ReceiptRows = getElementsByTagAndClassName('DIV','row','receipt');
	for (i=0; i<ReceiptRows.length; i++){
		connect(ReceiptRows[i],'onclick',billing.ReceiptItemToggle);
		var ReceiptButtons = getElementsByTagAndClassName('INPUT',null,ReceiptRows[i]);
		for (j=0; j<ReceiptButtons.length; j++){
			if (getNodeAttribute(ReceiptButtons[j],'value') == 'Edit') {
				connect(ReceiptButtons[j],'onclick',billing.ReceiptItemEditMode);
			} else if (getNodeAttribute(ReceiptButtons[j],'value') == 'Update') {
				connect(ReceiptButtons[j],'onclick',billing.ReceiptItemUpdate);
			} else if (getNodeAttribute(ReceiptButtons[j],'value') == 'Cancel') {
				connect(ReceiptButtons[j],'onclick',billing.ReceiptItemCancel);
			} else if (getNodeAttribute(ReceiptButtons[j],'value') == 'Delete') {
				connect(ReceiptButtons[j],'onclick',billing.ReceiptItemDelete);
			}
		}
	}
	//Sometimes we load a receipt without assigned locations, so the program auto assigns and then marks the records modfied
	//So we need to go into edit mode.
	if (billing.IsModified() && (billing.Mode == 'View')) {
		billing.Edit();
	} else if (( !billing.IsModified()) && (billing.Mode == 'Edit')){
		billing.Edit();
	}
	//Connect Receipt History events
	var HistoryRows = getElementsByTagAndClassName('LI',null,'history');
	for (i=0; i<HistoryRows.length; i++){
			connect(HistoryRows[i],'ondblclick',billing.ReceiptItemOnClickLoad);		
	}
	//If the Customer has no credit, then hide the refund button
	if (getElement('balance_amt').value>=0) {
		getElement('btnRefund').style.display = 'none';
	} else {
		getElement('btnRefund').style.display = '';
	}
}
/*
	Go through the entire receipt and recalculate the totals for each line, and the grand total
	for the receipt
*/
billing.CalcTotals = function(){
	var Total = 0.0;
	var rows = getElementsByTagAndClassName('DIV','row','receipt');
	for (i=0; i<rows.length; i++) {
		//Calc the total for the row
		var RowTotal = billing.getReceiptItemInputVal(rows[i],'Qty') * billing.getReceiptItemInputVal(rows[i],'UnitPrice');
		Total = Total + RowTotal;
		//Update the display value for total
		var divs = getElementsByTagAndClassName('DIV',null,rows[i]);
		for (j=0; j<divs.length; j++) {
			if (getNodeAttribute(divs[j],'name') == 'col4') {
				replaceChildNodes(divs[j], RowTotal);
				break;
			}
		}
	}
	//Update the grand total at the bottom
	replaceChildNodes('receipt_total', Total);
}
// Receipt line event functions
/*
	When a mouse goes over a receipt line, then we:
	1. Check the "Mode" var,
		Also check the EditMode var
	2. Highlight the line
	3. Show the Edit link
	4. Check if any other record is in EditMode and confirm the Update/cancel of that record
*/
billing.ReceiptItemToggle = function(obj){
	if (billing.Mode == 'Edit') {
		if (billing.EditMode == '') {
			//Search for all rows and reset there style
			var ReceiptRows = getElementsByTagAndClassName('DIV','row','receipt');
			for (i=0; i<ReceiptRows.length; i++){
				updateNodeAttributes(ReceiptRows[i],{'style':'background-color:transparent'});
				var Inputs = getElementsByTagAndClassName('INPUT',null,ReceiptRows[i]);
				for (j=0; j<Inputs.length; j++){
					if ((Inputs[j].value == 'Edit') || (Inputs[j].value == 'Delete')) {
						updateNodeAttributes(Inputs[j],{'style':'display:none'});
					} else if ((Inputs[j].name == 'IsModified') && (Inputs[j].value == 'true')) {
						updateNodeAttributes(ReceiptRows[i],{'style':'background-color:pink'});
					}
				}
			}
			//display the selected row
			var elem = obj.src();
			updateNodeAttributes(elem,{'style':'background-color:yellow'});
			var ReceiptButtons = getElementsByTagAndClassName('INPUT',null,elem);
			for (j=0; j<ReceiptButtons.length; j++){
				if ((ReceiptButtons[j].value == 'Edit') || (ReceiptButtons[j].value == 'Delete')) {
					updateNodeAttributes(ReceiptButtons[j],{'style':'display:block'});
				}
			}
		}
	}
}
/*
	Call the billing.EditMode function with the current row element
*/
billing.ReceiptItemEditMode = function(obj){
	if (billing.Mode == 'Edit') {
		if (billing.EditMode == '') {
			var elem = obj.src();
			var row = elem.parentNode.parentNode;
			billing.EditLine(row);
		}//end of if (billing.EditMode =='')
	}
}
/*
	Call the billing.DeleteLine function with the current row element
*/
billing.ReceiptItemDelete = function(obj){
	if (billing.Mode == 'Edit') {
		if (billing.EditMode == '') {
			if (confirm("Are you sure you want to delete?")) {
				var elem = obj.src();
				var row = elem.parentNode.parentNode;
				billing.DeleteLine(row);
			}
		}//end of if (billing.EditMode =='')
	}
}
/*
	Receipt item update:
	1. Make sure the row was in edit mode and the right row is selected
	2. Update the record to reflect the new values, change the IsModified to "true"
	3. Hide the edit fields, and the update and cancel buttons, and show the delete and edit buttons
*/
billing.ReceiptItemUpdate = function(obj){
	if (billing.Mode == 'Edit') {
		var elem = obj.src();
		var row = elem.parentNode.parentNode;
		if (billing.EditMode == billing.getReceiptItemInputVal(row,'ReceiptItemId')) {
			//We'll find our select box, then we'll update the current location id and name
			var Select = getElementsByTagAndClassName('SELECT',null,row);
			for (j=0; j<Select.length; j++){
				if (getNodeAttribute(Select[j],'name') == 'StockLocationId') {
					//Get the text
					var LocationNode = Select[j].parentNode;
					var Options = getElementsByTagAndClassName('OPTION',null,LocationNode);
					var NewText = 'No LocaTION';
					for (i=0; i<Options.length; i++){
						if (getNodeAttribute(Options[i],'value') == Select[j].value){
							NewText = scrapeText(Options[i]);
							break;
						}
					}
					//Update the Node
					replaceChildNodes(LocationNode, NewText, Select[j]);
					updateNodeAttributes(Select[j],{'style':'display:none'});
				}
			}//end of for-loop
			//Reset the inputs visibility
			var Inputs = getElementsByTagAndClassName('INPUT',null,row);
			for (j=0; j<Inputs.length; j++){
				if ((Inputs[j].value == 'Edit') || (Inputs[j].value == 'Delete')) {
					updateNodeAttributes(Inputs[j],{'style':'display:block'});
				} else if ((Inputs[j].value == 'Update') || (Inputs[j].value == 'Cancel')) {
					updateNodeAttributes(Inputs[j],{'style':'display:none'});
				} else if (getNodeAttribute(Inputs[j],'name') == 'Qty') {
					//Update the Quantity edit field, in the same manner as the select box
					var qtyNode = Inputs[j].parentNode;
					//Validate the quantity entry
					if (isNaN(Inputs[j].value)) {
						Inputs[j].value = 0; //If it's not a number, then set the quantity to zero
					}
					var NewText = Inputs[j].value;
					replaceChildNodes(qtyNode,NewText, Inputs[j]);
					updateNodeAttributes(Inputs[j],{'style':'display:none'});
				} else if (getNodeAttribute(Inputs[j],'name') == 'IsModified') {
					Inputs[j].value = 'true';
				}
			}//end of for loop
			billing.EditMode = '';
			billing.CalcTotals();
		}//end of if (billing.EditMode =='')
	}
}
/*
	Receipt item cancel:
	1. Make sure the row was in edit mode (quit if it isn't)
	2. Return the receipt row to it's initial value, billing.TempQty and billing.TempLocation
	3. Hide the inputs
	4. Hide the Update and cancel buttons and show the Edit and Delete buttons
*/
billing.ReceiptItemCancel = function(obj){
	if (billing.Mode == 'Edit') {
		var elem = obj.src();
		var row = elem.parentNode.parentNode;
		if (billing.EditMode == billing.getReceiptItemInputVal(row,'ReceiptItemId')) {
			var Select = getElementsByTagAndClassName('SELECT',null,row);
			for (j=0; j<Select.length; j++){
				if (getNodeAttribute(Select[j],'name') == 'StockLocationId') {
					updateNodeAttributes(Select[j],{'style':'display:none'});
					Select[j].value = billing.TempLocation;
				}
			}//end of for-loop
			//Reset the inputs visibility
			var Inputs = getElementsByTagAndClassName('INPUT',null,row);
			for (j=0; j<Inputs.length; j++){
				if ((Inputs[j].value == 'Edit') || (Inputs[j].value == 'Delete')) {
					updateNodeAttributes(Inputs[j],{'style':'display:block'});
				} else if ((Inputs[j].value == 'Update') || (Inputs[j].value == 'Cancel')) {
					updateNodeAttributes(Inputs[j],{'style':'display:none'});
				} else if (getNodeAttribute(Inputs[j],'name') == 'Qty') {
					updateNodeAttributes(Inputs[j],{'style':'display:none'});
					Inputs[j].value = billing.TempQty;
				}
			}
			//Undo the edit mode
			billing.EditMode = '';
		}//end of if (billing.EditMode ==...)
	}
}
/*
	Receipt item load:
	1. Make sure that nothing is in edit mode (otherwise exit)
	2. Attempt to load the selected receipt item
*/
billing.ReceiptItemOnClickLoad = function(obj){
	if (billing.Mode == 'View') {
		var Inputs = getElementsByTagAndClassName('INPUT',null,obj.src());
		for (i=0;i<Inputs.length;i++) {
			if (getNodeAttribute(Inputs[i],'name') == 'receiptid') {
				var receiptid = Inputs[i].value;
				break;
			}
		}
		billing.OpenPatient("LoadPatient?ReceiptID="+receiptid);
	}
}

//Configure our events using the Mochikit signal library
/* DEFINE OUR EVENT FUNCTIONS */
connect(document,'onkeydown', barcode.keydown);
connect(document,'onkeypress', barcode.keypress);
connect(document,'barcode', barcode.load);
//custom short-cuts
connect(document,'onkeypress',shortcuts.keypress);
connect(document,'onkeydown', shortcuts.keydown);
//Connect our buttons to events -- need to do this on document load
connect(window, 'onload', function(){
	connect('btnSave','onclick',billing.Save);
	connect('btnEdit','onclick',billing.Edit);
	connect('btnAppend','onclick',billing.Append);
	connect('btnPrint','onclick',billing.Print);
	connect('btnCancel','onclick',billing.Cancel);
	connect('btnNew','onclick',billing.New);
	connect('btnPay','onclick',billing.renderPayment);
	connect('btnRefund','onclick',billing.renderRefund);
	});
//Connect on onload for the document to open the document using javascript
connect(window, 'onload', billing.OpenOnLoad);

/*
	Pick list for choosing items for a new bill
	==========================
	1. Copy and paste the code into the javascript for the page
	2. Copy CustomerAddReceipt from "controllers_billing.py" 
*/

billing.pickList_move = function(elemid){
	var def = billing.list_def;
	var div = getElement(elemid);
	var left = getElement('pick_list_qry_result_'+def.Name);
	var right = getElement('pick_list_res_'+def.Name);
	var parent = getElement(div.parentNode);
	if (left == parent){
		appendChildNodes(right,div);
	} else {
		appendChildNodes(left,div);
	}
}
billing.pickList_getData = function(data){
	billing.toggle_message("");
	var def = billing.list_def;
	var results = getElement('pick_list_res_'+def.Name);
	for(var i = 0; i < data.results.length;i++){
		var chkbox = createDOM('INPUT',{'name':'row_select', 'type':'checkbox', 'checked':'checked', 'onclick':'billing.pickList_move("pick_list_row_data_'+data.items[i].id+'")'});
		var marker = createDOM('DIV',{'name':'input_marker'});
		var result = createDOM('DIV',{'class':'listingrow','id':'pick_list_row_data_'+data.items[i].id}, chkbox);
		if (data.results[i].text != '') {
			result.appendChild(createDOM('LABEL', {'style':'font-variant:small-caps; text-decoration:underline;'},'  '+data.results[i].text));
		} else {
			result.appendChild(createDOM('LABEL', {'style':'font-variant:small-caps; text-decoration:underline;'},'  '+data.results[i].Name + ', ' + data.results[i].Description));
		}
		result.appendChild(marker);
		var table = createDOM('TABLE',{'class':'minimal'});
		var tbody = createDOM('TBODY',null);
		for (var j in data.items[i]) {
			var l = -1;
			for (var k = 0; k<def.Inputs.length; k++){
				if (def.Inputs[k].name == j){
					l = k;
					break;
				}
			}
			if (l>-1) {
				var label = createDOM('LABEL','    '+def.Inputs[l].label+' ');
				if (def.Inputs[l].type == "DateTime") {
					var input = createDOM('SPAN',{'class':'date_time_widget'});
					var edit = createDOM('INPUT',{'type':'text','id':'datetime_left_'+j+'_'+i, 'name':def.Inputs[l].name,'value':eval('data.items[i].'+j), 'readonly':'1'});
					var link = createDOM('A',{'href':'javascript:Widget.pickDateTime("datetime_left_'+l+'_'+i+'")','title':'Pick date time'});
					var link_img = createDOM('IMG',{'border':'0','src':'/static/images/cal.png'});
					link.appendChild(link_img);
					appendChildNodes(input, edit, link);
				} else {
					var input = createDOM('INPUT',{'type':'text', 'size':def.Inputs[l].attr.length, 'name':def.Inputs[l].name, 'id':'pick_list_row_'+data.items[i].id+def.Inputs[l].name, 'value':eval('data.items[i].'+j)},'  ');
				}
				var td1 = createDOM('TD',null);
				td1.appendChild(label);
				var td2 = createDOM('TD',null);
				td2.appendChild(input);
				var row = createDOM('TR',null);
				appendChildNodes(row,td1,td2);
				tbody.appendChild(row);
			} else {
				var input = createDOM('INPUT',{'type':'hidden', 'name':j, 'value':eval('data.items[i].'+j)});
				result.appendChild(input);
			}
		}
		table.appendChild(tbody);
		result.insertBefore(table,marker);
		removeElement(marker);
		results.appendChild(result);
	}
	if (def.SrchNow == true){
		billing.pickList_postsearch();
	}
}

billing.pickList_getsearch = function(data){
	billing.toggle_message("");
	var def = billing.list_def;
	var results = createDOM('DIV',{'id':'pick_list_qry_result_'+def.Name});
	for(var i = 0; i < data.results.length;i++){
		var chkbox = createDOM('INPUT',{'name':'row_select', 'type':'checkbox', 'onclick':'billing.pickList_move("pick_list_row_'+data.items[i].id+'")'});
		var result = createDOM('DIV',{'class':'listingrow','id':'pick_list_row_'+data.items[i].id}, chkbox);
		if (data.results[i].text != '') {
			result.appendChild(createDOM('LABEL', {'style':'font-variant:small-caps; text-decoration:underline;'},'  '+data.results[i].text));
		} else {
			result.appendChild(createDOM('LABEL', {'style':'font-variant:small-caps; text-decoration:underline;'},'  '+data.results[i].Name + ', ' + data.results[i].Description));
		}
		//additional inputs
		var table = createDOM('TABLE',{'class':'minimal'});
		var tbody = createDOM('TBODY',null);
		for (var j = 0; j<def.Inputs.length; j++){
			var label = createDOM('LABEL','    '+def.Inputs[j].label+' ');
			if (def.Inputs[j].type == "DateTime") {
				var input = createDOM('SPAN',{'class':'date_time_widget'});
				var edit = createDOM('INPUT',{'type':'text','id':'datetime_left_'+j+'_'+i, 'name':def.Inputs[j].name,'value':'', 'readonly':'1'});
				var link = createDOM('A',{'href':'javascript:Widget.pickDateTime("datetime_left_'+j+'_'+i+'")','title':'Pick date time'});
				var link_img = createDOM('IMG',{'border':'0','src':'/static/images/cal.png'});
				link.appendChild(link_img);
				appendChildNodes(input, edit, link);
			} else {
				var input = createDOM('INPUT',{'type':'text', 'size':def.Inputs[j].attr.length, 'name':def.Inputs[j].name},'  ');
			}
			var td1 = createDOM('TD',null);
			td1.appendChild(label);
			var td2 = createDOM('TD',null);
			td2.appendChild(input);
			var row = createDOM('TR',null);
			appendChildNodes(row,td1,td2);
			tbody.appendChild(row);
		}
		table.appendChild(tbody);
		result.appendChild(table);
		for (var j in data.items[i]) {
			var input = createDOM('INPUT',{'type':'hidden', 'name':j, 'value':eval('data.items[i].'+j)});
			result.appendChild(input);
		}
		results.appendChild(result);
	}
	swapDOM('pick_list_qry_result_'+def.Name,results);
	//Go through and merge the values of hidden inputs with the visible inputs
	var rows = getElementsByTagAndClassName(null,'listingrow','pick_list_qry_result_'+def.Name);
	for (i=0;i<rows.length;i++){
		billing.merge_hidden_inputs(rows[i]);
	}
}
billing.pickList_postList = function(url,url_vars){
	var def = billing.list_def;
	var form = 'pick_list_res_'+def.Name;
	var node = getElement(form);
	var data = "";
	var data_item = "";
	for (var i=0;i<node.childNodes.length;i++){
		var item = node.childNodes[i];
		var values = formContents(node.childNodes[i]);
		var data_part = "";
		for (var j=0;j<values[0].length;j++){
			var name = values[0][j];
			var value = values[1][j];
			data_part += '"'+name+'":"'+value+'", ';
		}
		data_item += '{'+data_part.slice(0,-2)+'}, ';
	}
	data = '['+data_item.slice(0,-2)+']';
	billing.toggle_message("Loading...");
	if (def.NoAjax == true){
		if (url_vars != '') {
			location = url+'?'+url_vars+'&data='+data;
		} else {
			location = url+'?data='+data;
		}
 		//location.eval(url+'?data='+data);
 	} else {
		if (url_vars != '') {
		  	var d = postJSON(url,url_vars+'&data='+data);
		} else {
			var d = postJSON(url,'data='+data);
		}
 		d.addCallbacks(billing.updated,billing.error_report);
	 	billing.pickList_remove();
	  	return false;	
 	}
}
billing.pickList_postdata = function(){
	var def = billing.list_def;
	if (def.DataUrl != ''){
		var url = def.DataUrl;
		billing.toggle_message("Loading...");
	  	var d = postJSON(url,'id='+def.id);
	 	d.addCallbacks(billing.pickList_getData,billing.error_report);
	} else {
		if (def.SrchNow == true){
			billing.pickList_postsearch();
		}
	}
  	return false;
}
billing.pickList_postsearch = function(){
	var def = billing.list_def;
	var url = def.SrchUrl;
	var form = 'pick_list_qry_form_'+def.Name;
	billing.toggle_message("Loading...");
  	var postVars = billing.collectPostVars(eval('document.'+form));
  	var d = postJSON(url,postVars);
 	d.addCallbacks(billing.pickList_getsearch,billing.error_report);
  	return false;
}
billing.pickList_remove = function(){
	swapDOM('pick_list_'+billing.list_def.Name,null);
	swapDOM('pick_list_shadow_'+billing.list_def.Name,null);
}
billing.pickList = function(def){
	var GroupSelect = function(field){
		var row = createDOM('TR',null);
		var label = createDOM('TD',field.label);
		var data = createDOM('TD',null);
		var select = createDOM('SELECT',{'multiple':'multiple', 'size':'4', 'class':'groupselect','name':field.name, 'id':field.id+'_group_select'});
		for (var i=0;i<field.attr.Groups.length;i++){
			var option =  createDOM('OPTION',{'value':field.attr.Groups[i]},field.attr.Groups[i]);
			select.appendChild(option);
		}
		data.appendChild(select);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	var StringEdit = function(name, label){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','name':name,'id':'listing_srch_'+name});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	var StringEditRO = function(name, label, value){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','name':name,'id':'listing_srch_'+name, 'value':value, 'readonly':'1'});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	var StringHidden = function(name, value){
		var edit = createDOM('INPUT',{'type':'hidden','name':name,'id':'listing_srch_'+name, 'value':value});
	  	return edit;
	}
	billing.toggle_message("");
	billing.list_def = def;
	//This is the big div box that surrounds the entire selection process
	var pick_list = createDOM('DIV',{'class':'pick_list','id':'pick_list_'+def.Name});
	var shadow = createDOM('DIV',{'class':'pick_list_shadow','id':'pick_list_shadow_'+def.Name});
	//The following table is used to format the data selection process into 2 columns
	var table = createDOM('TABLE',{'class':'regular'});
	var tbody = createDOM('TBODY',null);
	var row = createDOM('TR',null);
	var left = createDOM('TD',null);
	var right = createDOM('TD',null);
	//This is the left side div
	var list_qry = createDOM('DIV',{'class':'pick_list_col', 'id':'pick_list_qry_'+def.Name});
	var close_link = createDOM('A',{'href':'javascript:billing.pickList_remove()'},"Close");
	var br = createDOM('BR',null);
	var title = createDOM('H3',def.Label);
	var form_qry = createDOM('FORM',{'onsubmit':'return false;', 'class':'tableform', 'name':'pick_list_qry_form_'+def.Name, 'id':'pick_list_qry_form_'+def.Name});
	var table_qry = createDOM('TABLE',{"class":"minimal"});
	var tbody_qry = createDOM('TBODY',null);
	for (var i=0; i<def.FieldsSrch.length; i++){
		switch(def.FieldsSrch[i].type) {
			case 'String':
				tbody_qry.appendChild(StringEdit(def.FieldsSrch[i].name,def.FieldsSrch[i].label));
			break;
			case 'StringRO':
				tbody_qry.appendChild(StringEditRO(def.FieldsSrch[i].name,def.FieldsSrch[i].label,def.FieldsSrch[i].data));
			break;
			case 'Hidden':
				form_qry.appendChild(StringHidden(def.FieldsSrch[i].name,def.FieldsSrch[i].data));
			break;
			case 'MultiSelect':
				tbody_qry.appendChild(GroupSelect(def.FieldsSrch[i]));
			break;
		}
	}
	table_qry.appendChild(tbody_qry);
	var submit_url = 'billing.pickList_postsearch("listing_form_'+def.Name+'","'+def.SrchUrl+'")';
	var btn_row = createDOM('TR',null);
	var btn_col = createDOM('TD',null);
	var submit_btn = createDOM('BUTTON',{'name':'btnSubmit', 'value':'Search', 'type':'submit', 'onclick':submit_url}, 'Search');
	btn_col.appendChild(submit_btn);
	btn_row.appendChild(btn_col);
	tbody_qry.appendChild(btn_row);
	form_qry.appendChild(table_qry);
	list_qry.appendChild(close_link);
	list_qry.appendChild(br);
	list_qry.appendChild(title);
	list_qry.appendChild(br);
	list_qry.appendChild(form_qry);
	var list_qry_res = createDOM('DIV',{'id':'pick_list_qry_result_'+def.Name});
	list_qry.appendChild(list_qry_res);
	left.appendChild(list_qry);
	//Now the right side result box
	var list_res = createDOM('DIV',{'class':'pick_list_col', 'id':'pick_list_res_'+def.Name});
	var post_url = 'billing.pickList_postList("'+def.Url+'","'+def.UrlVars+'")';
	var submit_res_btn = createDOM('BUTTON',{'name':'btnSubmit', 'value':'Save', 'type':'submit', 'onclick':post_url}, 'Save and Close');
	right.appendChild(submit_res_btn);
	right.appendChild(br);
	right.appendChild(list_res);
	row.appendChild(left);
	row.appendChild(right);
	tbody.appendChild(row);
	table.appendChild(tbody);
	pick_list.appendChild(table);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(pick_list);
	billing.pickList_postdata();
//	new Draggable('pick_list_'+def.Name);
}

//Remove our payment dialog box
billing.payment_remove = function(){
	swapDOM('paymentbox',null);
	swapDOM('paymentshadow',null);
}
/*
	Call the billing.Pay() function with variables we pull
	from our payment dialog, and close the dialog
*/
billing.payment_post = function() {
	var Inputs = getElementsByTagAndClassName('INPUT',null,'paymentbox');
	for (i=0; i<Inputs.length; i++) {
		var Name = getNodeAttribute(Inputs[i],'name');
		if (Name == 'CashAmt') {
			var CashAmt = Inputs[i].value;
		} else if (Name == 'CashNotes') {
			var CashNotes = Inputs[i].value;
		} else if (Name == 'InsrAmt') {
			var InsrAmt = Inputs[i].value;
		} else if (Name == 'InsrNotes') {
			var InsrNotes = Inputs[i].value;
		}
	}
	var TotalCashAmt = getElement('payment_TotalCashAmt').value;
	if (TotalCashAmt < 0) {
		alert('Cannot pay a negative amount (to return money, use the refund button)');
		TotalCashAmt = 0;
		getElement('payment_TotalCashAmt').value = TotalCashAmt;
	}
	if (confirm('Continue with customer making a payment for Rs. '+TotalCashAmt+'?  This operation cannot be un-done.')) {
		billing.payment_remove();
		billing.Pay(CashAmt,CashNotes,InsrAmt,InsrNotes, TotalCashAmt);
	}
}
billing.renderPayment = function(obj){
	var StringEdit = function(name, label, value){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','size':'12','name':name,'id':'payment_'+name, 'value':value});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	var StringEditRO = function(name, label, value){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','size':'12','name':name,'id':'payment_'+name, 'value':value, 'readonly':'1'});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	var StringHidden = function(name, value){
		var edit = createDOM('INPUT',{'type':'hidden','name':name,'id':'payment_'+name, 'value':value});
	  	return edit;
	}
	billing.toggle_message("");
	if (billing.IsModified()) {
		alert("First save the record before making a payment");
	} else {
		//This is the big div box that surrounds the entire selection process
		var dialog = createDOM('DIV',{'style':'width:300px;height:400px','class':'dialogbox','id':'paymentbox'});
		var shadow = createDOM('DIV',{'style':'width:310px;height:410px','class':'dialogbox_shadow','id':'paymentshadow'});
		//Close link
		var close_link = createDOM('A',{'href':'javascript:billing.payment_remove()'},"Close");
		dialog.appendChild(close_link);
		//The main table
		//alert('hi');
		var table = createDOM('TABLE',{'class':'regular'});
		var tbody = createDOM('TBODY',null);
		// Get the receipt Total
		var Total = scrapeText('receipt_total');
		// Get the insurance information
		var InsrType = scrapeText('insurance_type');
		// Get the current receipt payment
		var CurrPayment = getElement('curr_receipt_paid').value;
		// Get current customer balance
		var Balance = getElement('balance_amt').value;
		if (getElement('is_curr_receipt_in_balance').value=='true') {
			Balance = parseFloat(Balance) - parseFloat(Total) + parseFloat(CurrPayment);
		}
		// Figure out how much the customer needs to pay
		// Add fields
		tbody.appendChild(createDOM('TD',{'colspan':'2'},'Complete Balance Owing (past and current)'));
		tbody.appendChild(StringEditRO('PrevBalance','Previous Balance (Rs)',Balance));
		tbody.appendChild(StringEditRO('CurrBalance','Current Balance (Rs)',''));
		tbody.appendChild(StringEdit('TotalCashAmt','Customer Payment (Rs)',''));
		tbody.appendChild(createDOM('TD',{'colspan':'2'},'Current Receipt Information'));
		if (InsrType == 'self_pay') {
			var editamt = StringEditRO('CashAmt','Self pay amount',Total);
			tbody.appendChild(editamt);
			tbody.appendChild(StringEdit('CashNotes','Self pay notes',''));
			tbody.appendChild(StringEditRO('InsrAmt','Insurance amount','0.0'));
			tbody.appendChild(StringEditRO('InsrNotes','Insurance notes',''));
		} else {
			var editamt = StringEdit('CashAmt','Self pay amount','0.0');
			tbody.appendChild(editamt);
			tbody.appendChild(StringEdit('CashNotes','Self pay notes',''));
			tbody.appendChild(StringEditRO('InsrAmt','Insurance amount',Total));
			tbody.appendChild(StringEdit('InsrNotes','Insurance notes',''));
		}
		tbody.appendChild(StringEditRO('CurrPaid','Already Paid (Rs)',CurrPayment));
		var btn_row = createDOM('TR',null);
		var btn_col = createDOM('TD',null);
		var submit_btn = createDOM('BUTTON',{'id':'btnPayDialog', 'name':'btnPayDialog', 'value':'Pay', 'type':'submit'},'Pay');
		tbody.appendChild(submit_btn);
		//Create our dialog
		table.appendChild(tbody);
		dialog.appendChild(table);
		document.body.appendChild(shadow);
		setOpacity(shadow,0.5);
		document.body.appendChild(dialog);
		//Calculate totals
		billing.paymentUpdate();
		//Attach the button event
		connect('btnPayDialog','onclick', billing.payment_post);
		connect('payment_CashAmt','onblur',billing.paymentUpdate);
		getElement('payment_CashAmt').focus();
	}
}
/*
	If the Cash contribution to the receipt changes
	then we need to update the Total Cash Payment field
*/
billing.paymentUpdate = function(dom_obj){
	// Get variables for caculation
	var InsrType = scrapeText('insurance_type');
	var Total = scrapeText('receipt_total');
	var CashAmt = getElement('payment_CashAmt');
	var InsrAmt = getElement('payment_InsrAmt');
	// Update the Insurance amount field and fix the Cash amount field if incorrect values are entered
	if (((parseFloat(CashAmt.value) + parseFloat(InsrAmt.value)) < parseFloat(Total))&&(InsrType!='self_pay')){
		InsrAmt.value = parseFloat(Total)-parseFloat(CashAmt.value);
	} else if (((parseFloat(CashAmt.value) + parseFloat(InsrAmt.value)) < Total)&&(InsrType=='self_pay')) {
		CashAmt.value = Total;
	}
	var PrevBalance = getElement('payment_PrevBalance').value;
	var CurrPayment = getElement('curr_receipt_paid').value;
	// Calculate the current balance
	var CurrBalance = getElement('payment_CurrBalance');
	var TotalCashAmt =  getElement('payment_TotalCashAmt');
	if (InsrType=='self_pay') {
		CurrBalance.value = parseFloat(Total) - parseFloat(CurrPayment);
	} else {
		CurrBalance.value = 0.0
	}
	TotalCashAmt.value = parseFloat(PrevBalance) + parseFloat(CurrBalance.value);
	if (TotalCashAmt.value < 0) {
		TotalCashAmt.value = 0;
	}
}
//Remove our payment dialog box
billing.refund_remove = function(){
	swapDOM('refundbox',null);
	swapDOM('refundshadow',null);
}
/*
	Call the billing.Pay() function with variables we pull
	from our payment dialog, and close the dialog
*/
billing.refund_post = function() {
	var CashAmt = getElement('refund_CashAmt').value;
	if (isNaN(CashAmt)) {
		alert("The value entered needs to be numeric, but it doesn't look numeric");
	} else if (CashAmt<=0) {
		alert("Cannot refund zero or less, operation CANCELLED");
	} else if (confirm('Are you sure you want to refund the customer for Rs. '+CashAmt+'?  This operation cannot be un-done.')) {
		billing.refund_remove();
		location = 'BillingRefund?CashAmt='+CashAmt+'&ReceiptID='+billing.ReceiptId;
	}
}
/*
	renderRefund: Create a dialog box for making a refund.
*/
billing.renderRefund = function (e){
	var StringEdit = function(name, label, value){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','size':'12','name':name,'id':'refund_'+name, 'value':value});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	billing.toggle_message("");
	var MaxRefund = -parseFloat(getElement('balance_amt').value);
	if (billing.IsModified()) {
		alert("First save the record before making a refund");
	} else if (MaxRefund <= 0) {
		alert("Not enough credit to perform a refund.  Operation CANCELLED.");
	} else {
		//This is the big div box that surrounds the entire selection process
		var dialog = createDOM('DIV',{'style':'width:300px;height:100px','class':'dialogbox','id':'refundbox'});
		var shadow = createDOM('DIV',{'style':'width:310px;height:110px','class':'dialogbox_shadow','id':'refundshadow'});
		//Close link
		var close_link = createDOM('A',{'href':'javascript:billing.refund_remove()'},"Close");
		dialog.appendChild(close_link);
		//The main table
		var table = createDOM('TABLE',{'class':'regular'});
		var tbody = createDOM('TBODY',null);
		// Add fields
		tbody.appendChild(StringEdit('CashAmt','Refund Amount (Rs)',MaxRefund));
		var btn_row = createDOM('TR',null);
		var btn_col = createDOM('TD',null);
		var submit_btn = createDOM('BUTTON',{'id':'btnRefundDialog', 'name':'btnRefundDialog', 'value':'Refund', 'type':'submit'},'Refund');
		tbody.appendChild(submit_btn);
		//Create our dialog
		table.appendChild(tbody);
		dialog.appendChild(table);
		document.body.appendChild(shadow);
		setOpacity(shadow,0.5);
		document.body.appendChild(dialog);
		//Attach the button event
		connect('btnRefundDialog','onclick', billing.refund_post);
		getElement('refund_CashAmt').focus();
	}
}
/*
	Small dialog box, for entering the customer id
*/
billing.customeriddialog_remove = function(){
	swapDOM('customerid_dialog',null);
	swapDOM('customerid_shadow',null);
}
billing.renderCustomerIdDialog = function(){
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
	billing.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'customerid_dialog','style':'height:70px'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'customerid_shadow','style':'height:80px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:billing.customeriddialog_remove()'},"Close");
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