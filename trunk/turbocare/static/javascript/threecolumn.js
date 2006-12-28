function postJSON(url, postVars) {
	inv.toggle_message("Sending request...");
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
}

function hasParent(id,parent_id) {
	var node = getElement(id);
	var ret_val = false;
	while (node.parentNode != null) {
		if (node.parentNode.id == parent_id){
			ret_val = true;
		}
		node = node.parentNode;
	}
	return ret_val;
}

var inv = {};

// variables ===================
inv.g_nTimeoutId;
inv.MAX_HISTORY_LENGTH = 20;
inv.history = [];
inv.cur_def = null;
inv.list_def = null; //This is like cur_def except that it is used when we need to choose items from another object.
inv.list_dest = null; //This is a string element id where a listing should be located in the web page
inv.list_inputs = []; //This is an array of label name pairs for input fields
//inv.OverlayManager = new YAHOO.widget.OverlayManager();
// utility functions ===========
inv.addHistory = function(entry)
{
    inv.history[inv.history.length]  = entry;
    if(inv.history.length > inv.MAX_HISTORY_LENGTH)
    {
        var h= inv.history.shift();
    }
}

inv.historyBack = function()
{
    if(inv.history.length==1) return;
    var step = inv.history.pop(); //pop the current view first..
    step = inv.history.pop(); //get the previous view

    switch(step['view'])
    {
       case 'renderObjForm':
        inv.renderObjForm(step['def']);
        break;
       case 'renderObjView':
        inv.openObjView(step['def'].Read+'?id='+step['def'].id);
        break;
       case 'renderListing':
        inv.renderListing(step['def']);
        break;
//       case 'add':
//        inv.historyBack();
//        break;
    }
}

inv.collectPostVars = function(f)
{
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
      	postVars+= f.elements[i].name +'='+ inv.multiselect_csv(f.elements[i].id);
      } else {
      	postVars+= f.elements[i].name +'='+ f.elements[i].options[f.elements[i].selectedIndex].value;
      }
    }
  }
  return postVars;
}

inv.multiselect_csv = function(element_id){
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

// AJSON reactions ==================
inv.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	inv.toggle_message("");
	if (data.result_msg != null) {
		var display = createDOM('DIV',{'class':'displaymsg','id':'last_result_msg'},data.result_msg);
		if (getNodeAttribute('last_result_msg','class') == null){
			document.body.appendChild(display);
		} else {
			swapDOM(field.id,display);
		}
	}
	var d = callLater(5,remove_message);
	if (data.result == 1) {
		inv.openObjView(inv.cur_def.Read+'?id='+data.id);
	} else {
		inv.historyBack();
	}
}

inv.error_report = function(data){
	inv.toggle_message("");
	alert('ERROR: ' + data);
}

inv.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

// AJSON actions ====================
inv.saveForm = function(url){
	inv.toggle_message("Saving...");
  	var postVars =inv.collectPostVars(document.ObjForm);
  	var d = postJSON(url,postVars);
  	d.addCallbacks(inv.updated,inv.error_report);
  	return false;
}

inv.saveData = function(url,vars){
	inv.toggle_message("Saving...");
  	var d = postJSON(url,vars);
  	d.addCallbacks(inv.updated,inv.error_report);
}

inv.loadVendors = function(id){
	if (hasParent("listing_row_"+id,"PurchaseOrders") != true) {
		//Select the item (exclusive) make it the only orange catalog item
		var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
		for (var i=0;i<elems.length;i++){
			swapElementClass(elems[i],"listingrow_item","listingrow");
		}
		swapElementClass("listing_row_"+id,"listingrow","listingrow_item");
		//Load the vendors
		inv.toggle_message("Loading...");
	  	var d = postJSON("PurchaseOrderGetVendorsForItem","CatalogItemId="+id);
	  	d.addCallbacks(inv.renderVendors,inv.error_report);
  	}
}

inv.removeItem = function(id){
	var catalogitem = getElement(id);
	//find and remove vendor info from the catalog item
	var elems = getElementsByTagAndClassName("input",null,catalogitem);
	for (var i=0;i<elems.length;i++){
		if (elems[i].name == 'Vendor'){
			var VendorId = elems[i].value;
			elems[i].value = "";
		}
		if (elems[i].name == 'QuotePrice'){
			elems[i].value = "";
		}
	}
	var vendor_po = getElement('PO_vendor_'+VendorId);
	var catalogitems = getElement("CatalogItems");
	catalogitems.appendChild(catalogitem.cloneNode(true));
	swapDOM(catalogitem,null);
	swapDOM("closelink_"+id,null);
	//remove the Vendor section from the Purchase order list if they have no more items
	var elems = getElementsByTagAndClassName(null,"listingrow",vendor_po);
	if (elems.length == 0){
		swapDOM(vendor_po,null);
	}
}

inv.showPOVendor = function(id){
	var purchaseorders = getElement("PurchaseOrders");
	//first, hide all other Purchase order vendor lines
	var elems = getElementsByTagAndClassName(null,"listingrowcontain_show",purchaseorders);
	if (elems.length > 0) {
		for (var i=0;i<elems.length;i++){
			swapElementClass(elems[i],"listingrowcontain_show","listingrowcontain");
			//removeEmptyTextNodes(elems[i]);
			//var sub_elems = getElementsByTagAndClassName(null, "listingrow", elems[i]);
			var sub_elems = getElementsByTagAndClassName('DIV',null, elems[i]);
			for (var j=0;j<sub_elems.length;j++){
				//alert(sub_elems[j].id);
				//swapElementClass(sub_elems[j],"listingrow","listingrow_hidden");
				setNodeAttribute(sub_elems[j],'style','display:none');
			}
		}
	}
	//Now show our selected line
	var elem = getElement(id);
	if (getNodeAttribute(elem,"class") == null){
		alert('help me, i am stuck in the computer, let me out.');
	} else {
		swapElementClass(elem,"listingrowcontain","listingrowcontain_show");
		//var elems = getElementsByTagAndClassName(null, "listingrow_hidden", elem);
		var elems = getElementsByTagAndClassName('DIV',null, elem);
		for (var i=0;i<elems.length;i++){
			//	alert(elems[j].id);
			//swapElementClass(elems[i],"listingrow_hidden", "listingrow");
			setNodeAttribute(elems[i],'style','display:block');
		}
	}
}

inv.hidePOVendor = function(id){
	elem = getElement(id);
	for (var i=1;i<elem.childNodes.length;i++){
		makeInvisible(elem.childNodes[i]);
	}
}

inv.moveItem = function(){
	var purchaseorders = getElement("PurchaseOrders");
	//get the vendor
	var elems = getElementsByTagAndClassName(null,"listingrow_vendor",document);
	var vendor = elems[0];
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_vendor","listingrow");
	}
	//get the catalogitem
	var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
	if (elems.length < 1) {
		alert('There is a problem with the javascript.');
	}
	var catalogitem = elems[0];
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_item","listingrow");
	}
	if ((vendor == null) || (catalogitem == null)){
		alert("First, choose a catalog item and a vendor.");
	} else {
		//look for vendor in purchase order list
		var vendor_po = getElement("PO_"+vendor.id);
		var linkdiv = createDOM('DIV',{'id':'closelink_'+catalogitem.id, 'class':'listingrow'});
		var closelink = createDOM('A',{'href':'javascript:inv.removeItem("'+catalogitem.id+'")'}, "Remove");
		linkdiv.appendChild(closelink);
		if (getNodeAttribute(vendor_po,"class") == null) {
			elems = getElementsByTagAndClassName("input",null,vendor);
			for (i=0;i<elems.length;i++){
				if (elems[i].name == "vendorname"){
					var VendorName = elems[i].value;
				}
			}
			var vendor_po = createDOM('DIV',{'id':'PO_'+vendor.id, 'class':'listingrowcontain', 'onclick':'inv.showPOVendor("PO_'+vendor.id+'")'},VendorName);
			vendor_po.appendChild(linkdiv);
			vendor_po.appendChild(catalogitem.cloneNode(true));
			swapDOM(catalogitem,null);
			purchaseorders.appendChild(vendor_po);
		} else {
			vendor_po.appendChild(linkdiv);
			vendor_po.appendChild(catalogitem.cloneNode(true));
			swapDOM(catalogitem,null);
		}
		//show our current po vendor line
		inv.showPOVendor('PO_'+vendor.id);
		inv.clearVendors();
	}
}

inv.selectVendor = function(id){
	//deselect any previous vendor and select current vendor
	var elems = getElementsByTagAndClassName(null,"listingrow_vendor",document);
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_vendor","listingrow");
	}
	vendor = getElement("vendor_"+id);
	swapElementClass(vendor,"listingrow","listingrow_vendor");
	//Find the current quote price
	for (var i=0;i<vendor.childNodes.length;i++){
		if (vendor.childNodes[i].name == 'QuotePrice'){
			var QuotePrice = vendor.childNodes[i].value;
		}
		if (vendor.childNodes[i].name == 'id'){
			var VendorId = vendor.childNodes[i].value;
		}
	}	
	//find the selected catalog item and change the quote price
	var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
	var catalogitem = elems[0];
	if (getNodeAttribute(catalogitem,"class") == "listingrow_item"){
		elems = getElementsByTagAndClassName("input",null,catalogitem);
		for (var i=0;i<elems.length;i++){
			if (elems[i].name == 'QuotePrice'){
				elems[i].value = QuotePrice;
			}
			if (elems[i].name == 'Vendor'){
				elems[i].value = VendorId;
			}
		}
	}
}

inv.openListing = function(url,dest){
	//This also does a search like above
	//url: Where to get the data; dest: where to place the result object, defaults to main location
	if (dest != null){
		inv.list_dest = dest;
	} else {
		inv.list_dest = null;
	}
	if (url != null){
		inv.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(inv.renderListing);
	}
}

inv.openPickList = function(url){
	if (url != null){
		inv.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(inv.pickList);
	}
}

// load view/form data =========

inv.clearVendors = function() {
	var vendors = createDOM('DIV',{'id':'vendors', 'style':'overflow:auto;'});
	swapDOM('vendors',vendors);
}
inv.renderVendors = function(data){
	var tr = function(label, data){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',data);
		row.appendChild(label);
		row.appendChild(data);
		return row;
	}
	var vendorDiv = function(record){
		var br = createDOM('BR',null);
		var div = createDOM('DIV',{'class':'listingrow','id':'vendor_'+record.id, 'ondblclick':'inv.selectVendor('+record.id+')'});
		var vendorname = createDOM('INPUT',{'type':'hidden', 'name':'vendorname', 'value':record.Name + ", " + record.Description});
		var vendorid = createDOM('INPUT',{'type':'hidden', 'name':'id', 'value':record.id});
		var quoteprice = createDOM('INPUT',{'type':'hidden', 'name':'QuotePrice', 'value':record.Price});
		var table = createDOM('TABLE',{'class':'minimal'});
		var tbody = createDOM('TBODY',null);
		appendChildNodes(tbody, tr("Name",record.Name + ", " + record.Description), tr("Ranking",record.Ranking), tr("Product",record.Product), tr("Price","Rs. " + record.Price), tr("Notes",record.Notes), tr("Valid starting",record.ValidOn));
		table.appendChild(tbody);
		div.appendChild(vendorname);
		div.appendChild(vendorid);
		div.appendChild(quoteprice);
		div.appendChild(table);
		return div;
	}
	inv.toggle_message();
	var vendors = createDOM('DIV',{'id':'vendors', 'style':'overflow:auto;'});
	for (var i=0; i<data.items.length;i++){
		var record = data.items[i];
		if (record.Status != 'deleted'){
			vendors.appendChild(vendorDiv(record));
		}
	}
	swapDOM('vendors',vendors);
}

