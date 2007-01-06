function postJSON(url, postVars) {
	um.toggle_message("Sending request...");
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

var um = {};

um.collectPostVars = function(f)
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
      	postVars+= f.elements[i].name +'='+ um.multiselect_csv(f.elements[i].id);
      } else {
      	postVars+= f.elements[i].name +'='+ f.elements[i].options[f.elements[i].selectedIndex].value;
      }
    }
  }
  return postVars;
}

um.multiselect_csv = function(element_id){
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
um.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	um.toggle_message("");
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
		um.openObjView(um.cur_def.Read+'?id='+data.id);
	} else {
		um.historyBack();
	}
}

um.error_report = function(data){
	um.toggle_message("");
	alert('ERROR: ' + data);
}

um.toggle_message = function(message){
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
um.saveForm = function(url){
	um.toggle_message("Saving...");
  	var postVars =um.collectPostVars(document.ObjForm);
  	var d = postJSON(url,postVars);
  	d.addCallbacks(um.updated,um.error_report);
  	return false;
}

um.saveData = function(url,vars){
	um.toggle_message("Saving...");
  	var d = postJSON(url,vars);
  	d.addCallbacks(um.updated,um.error_report);
}

um.loadVendors = function(id){
	if (hasParent("listing_row_"+id,"PurchaseOrders") != true) {
		//Select the item (exclusive) make it the only orange catalog item
		var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
		for (var i=0;i<elems.length;i++){
			swapElementClass(elems[i],"listingrow_item","listingrow");
		}
		swapElementClass("listing_row_"+id,"listingrow","listingrow_item");
		//Load the vendors
		um.toggle_message("Loading...");
	  	var d = postJSON("PurchaseOrderGetVendorsForItem","CatalogItemId="+id);
	  	d.addCallbacks(um.renderVendors,um.error_report);
  	}
}

um.removeItem = function(id){
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

um.showPOVendor = function(id){
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

um.hidePOVendor = function(id){
	elem = getElement(id);
	for (var i=1;i<elem.childNodes.length;i++){
		makeInvisible(elem.childNodes[i]);
	}
}

um.moveItem = function(){
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
		var closelink = createDOM('A',{'href':'javascript:um.removeItem("'+catalogitem.id+'")'}, "Remove");
		linkdiv.appendChild(closelink);
		if (getNodeAttribute(vendor_po,"class") == null) {
			elems = getElementsByTagAndClassName("input",null,vendor);
			for (i=0;i<elems.length;i++){
				if (elems[i].name == "vendorname"){
					var VendorName = elems[i].value;
				}
			}
			var vendor_po = createDOM('DIV',{'id':'PO_'+vendor.id, 'class':'listingrowcontain', 'onclick':'um.showPOVendor("PO_'+vendor.id+'")'},VendorName);
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
		um.showPOVendor('PO_'+vendor.id);
		um.clearVendors();
	}
}

um.selectVendor = function(id){
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

um.openListing = function(url,dest){
	//This also does a search like above
	//url: Where to get the data; dest: where to place the result object, defaults to main location
	if (dest != null){
		um.list_dest = dest;
	} else {
		um.list_dest = null;
	}
	if (url != null){
		um.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(um.renderListing);
	}
}

um.openPickList = function(url){
	if (url != null){
		um.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(um.pickList);
	}
}

// load view/form data =========

um.clearVendors = function() {
	var vendors = createDOM('DIV',{'id':'vendors', 'style':'overflow:auto;'});
	swapDOM('vendors',vendors);
}
um.renderVendors = function(data){
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
		var div = createDOM('DIV',{'class':'listingrow','id':'vendor_'+record.id, 'ondblclick':'um.selectVendor('+record.id+')'});
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
	um.toggle_message();
	var vendors = createDOM('DIV',{'id':'vendors', 'style':'overflow:auto;'});
	for (var i=0; i<data.items.length;i++){
		var record = data.items[i];
		if (record.Status != 'deleted'){
			vendors.appendChild(vendorDiv(record));
		}
	}
	swapDOM('vendors',vendors);
}

connect(document,'onload',um.OnLoad);