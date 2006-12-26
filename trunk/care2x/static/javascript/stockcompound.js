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

inv.loadLocations = function(id){
	if (hasParent("listing_row_"+id,"StockItemCompound") != true) {
		//Select the item (exclusive) make it the only orange item
		var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
		for (var i=0;i<elems.length;i++){
			swapElementClass(elems[i],"listingrow_item","listingrow");
		}
		swapElementClass("listing_row_"+id,"listingrow","listingrow_item");
		var item = getElement("listing_row_"+id);
		//Find the current CatalogItemID
		var elems = getElementsByTagAndClassName("input",null,item);
		for (var i=0;i<elems.length;i++){
			if (elems[i].name == "CatalogItemID"){
				var CatalogItemID = elems[i].value;
			}
		}
		var elems = getElementsByTagAndClassName("option",null,getElement("LocationName"));
		for (var i=0;i<elems.length;i++){
			if (elems[i].selected){
				var LocationID = elems[i].value;
			}
		}
		//Load the locations
		inv.toggle_message("Loading...");
	  	var d = postJSON("StockItemCompoundGetLocationsForItem","CatalogItemID="+CatalogItemID+"&LocationID="+LocationID);
	  	d.addCallbacks(inv.renderLocations,inv.error_report);
  	}
}

inv.removeItem = function(id){
	swapDOM(id,null);
}

inv.showStockItemCompound = function(id){
	var stockitemcompounds = getElement("StockItemCompound");
	//first, hide all other lines
	var elems = getElementsByTagAndClassName(null,"listingrowcontain_show",stockitemcompounds);
	if (elems.length > 0) {
		for (var i=0;i<elems.length;i++){
			swapElementClass(elems[i],"listingrowcontain_show","listingrowcontain");
			removeEmptyTextNodes(elems[i]);
			var sub_elems = getElementsByTagAndClassName(null, "listingrow", elems[i]);
			for (var j=0;j<sub_elems.length;j++){
				swapElementClass(sub_elems[j],"listingrow","listingrow_hidden");
			}
		}
	}
	//Now show our selected line
	var elem = getElement(id);
	if (getNodeAttribute(elem,"class") == null){
		alert('help me, i am stuck in the computer, let me out.');
	} else {
		swapElementClass(elem,"listingrowcontain","listingrowcontain_show");
		var elems = getElementsByTagAndClassName(null, "listingrow_hidden", elem);
		for (var i=0;i<elems.length;i++){
			swapElementClass(elems[i],"listingrow_hidden", "listingrow");
		}
	}
}

inv.makeItem = function(){
	var stockitemcompounds = getElement("StockItemCompound");
	//get the location
	var elems = getElementsByTagAndClassName(null,"listingrow_location",document);
	var location = elems[0];
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_location","listingrow");
	}
	//get the compound item
	var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
	item = elems[0];
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_item","listingrow");
	}
	//get the Quantity we want to produce
	var elem = getElement("TotalQty");
	var QtyTotal = parseInt(elem.value);
	if ((location == null) || (item == null) || (! (QtyTotal>0))){
		alert("First, choose a item and a location and set the quantity to a suitable value.");
	} else {
		//look for location in purchase order list
		var stockitemcompound_old = getElement("stockitemcompound_"+location.id+"_"+item.id);
		var linkdiv = createDOM('DIV',{'id':'closelink_'+location.id+"_"+item.id, 'class':'listingrow'});
		var closelink = createDOM('A',{'href':'javascript:inv.removeItem("stockitemcompound_'+location.id+'_'+item.id+'")'}, "Remove");
		linkdiv.appendChild(closelink);
		//Get Variables to form our title line
		elems = getElementsByTagAndClassName("input",null,location);
		for (i=0;i<elems.length;i++){
			if (elems[i].name == "Product"){
				var Product = elems[i].value;
			}
			if (elems[i].name == "QtyAvailable"){
				var QtyAvailable = elems[i].value;
			}
		}
		elems = getElementsByTagAndClassName("input",null,item);
		for (i=0;i<elems.length;i++){
			if (elems[i].name == "Qty"){
				var UnitQty = elems[i].value;
				var QtyRequested = QtyTotal * parseInt(UnitQty);
			}
		}
		//Calculate the default amount to transfer from the selected location
		if (QtyRequested>parseInt(QtyAvailable)){
			var qty = QtyAvailable;
		} else {
			var qty = QtyRequested;
		}
		//Create our new entry for the far right column
		var qtytransfer = createDOM('INPUT',{'type':'text', 'size':'9', 'name':'TransferQty', 'value':qty});
		//The "counter" is used when posting to determine if there are multiple records or only one record
		var counter = createDOM('INPUT',{'type':'hidden', 'name':'counter', 'value':'1'});
		var totalqty = createDOM('INPUT',{'type':'hidden', 'name':'TotalQty', 'value':QtyTotal});
		var divtitle = createDOM('DIV',null);
		appendChildNodes(divtitle,"Use ", qtytransfer," of " + Product + " to make " + QtyTotal + " items (" + QtyRequested + " needed)");
		var stockitemcompound = createDOM('DIV',{'id':"stockitemcompound_"+location.id+"_"+item.id, 'class':'listingrowcontain', 'onclick':'inv.showStockItemCompound("stockitemcompound_'+location.id+'_'+item.id+'")'},divtitle);
		var clone = item.cloneNode(true);
		clone.id = clone.id + "_copy";
		appendChildNodes(stockitemcompound,linkdiv,clone,location, counter, totalqty);
		stockitemcompounds.appendChild(stockitemcompound);
		//Any existing entry will be replaced by this one
		if (getNodeAttribute(stockitemcompound_old,"class") != null) {
			swapDOM(stockitemcompound_old, stockitemcompound);
		}
		//show our current po vendor line
		inv.showStockItemCompound('stockitemcompound_'+location.id+'_'+item.id);
		inv.clearLocations();
	}
}

inv.selectLocation = function(id){
	//deselect any previous location and select current location
	var elems = getElementsByTagAndClassName(null,"listingrow_location",document);
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_location","listingrow");
	}
	var location = getElement("location_"+id);
	swapElementClass(location,"listingrow","listingrow_location");
}

// load view/form data =========
inv.clearLocations = function() {
	var locations = createDOM('DIV',{'id':'Locations', 'style':'overflow:auto;'});
	swapDOM('Locations',locations);
}
inv.renderLocations = function(data){
	var tr = function(label, data){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',data);
		row.appendChild(label);
		row.appendChild(data);
		return row;
	}
	var locationDiv = function(record){
		var br = createDOM('BR',null);
		var link = "inv.selectLocation('"+record.StockLocationID+"')";
		var div = createDOM('DIV',{'class':'listingrow','id':'location_'+record.StockLocationID, 'ondblclick':link});
		var  stocklocationid = createDOM('INPUT',{'type':'hidden', 'name':'StockLocationID', 'value':record.StockLocationID});
		var product = createDOM('INPUT',{'type':'hidden', 'name':'Product', 'value':record.Product});
		var qtyavailable = createDOM('INPUT',{'type':'hidden', 'name':'QtyAvailable', 'value':record.LocationQty});
		var table = createDOM('TABLE',{'class':'minimal'});
		var tbody = createDOM('TBODY',null);
		appendChildNodes(tbody, tr("Name",record.Product + " from " + record.Name), tr("Quantity",record.LocationQty),tr("Expire date",record.ExpireDate));
		table.appendChild(tbody);
		appendChildNodes(div,stocklocationid,product,qtyavailable,table);
		return div;
	}
	var errorDiv = function(){
		var br = createDOM('BR',null);
		var div = createDOM('DIV',{'class':'listingrow_error','id':'location_error'});
		appendChildNodes(div,"No applicable stock found at this location!  Either transfer stock from another location, or, if no more stock exists, create a purchase order.");
		return div;
	}
	inv.toggle_message();
	var locations = createDOM('DIV',{'id':'Locations', 'style':'overflow:auto;'});
	for (var i=0; i<data.items.length;i++){
		var record = data.items[i];
		locations.appendChild(locationDiv(record));
	}
	if (data.items.length == 0){
		locations.appendChild(errorDiv());
	}
	swapDOM('Locations',locations);
}

