/*
	Notes on hacking this javascript:
	Customize:
		renderItemOptions
		selectItemOption
		moveItem
*/

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

inv.loadItemOptions = function(id){
	if (hasParent("listing_row_"+id,"FinalItems") != true) {
		//Select the item (exclusive) make it the only orange item
		var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
		for (var i=0;i<elems.length;i++){
			swapElementClass(elems[i],"listingrow_item","listingrow");
		}
		swapElementClass("listing_row_"+id,"listingrow","listingrow_item");
		//Load the item options
		inv.toggle_message("Loading...");
	  	var d = postJSON("GetItemOptions","ItemId="+id);
	  	d.addCallbacks(inv.renderItemOptions,inv.error_report);
  	}
}

inv.removeItem = function(id){
	var item = getElement(id);
	//find and remove item options info from the item
	var elems = getElementsByTagAndClassName("input",null,item);
	for (var i=0;i<elems.length;i++){
		if (elems[i].name == 'ItemOption'){
			var ItemOptionId = elems[i].value;
			elems[i].value = "";
		}
		if (elems[i].name == 'QuotePrice'){
			elems[i].value = "";
		}
	}
	var itemoption = getElement('itemoption_'+ItemOptionId);
	var items = getElement("Items");
	items.appendChild(item.cloneNode(true));
	swapDOM(item,null);
	swapDOM("closelink_"+id,null);
	//remove the ItemOption section from the Final item list if they have no more items
	var elems = getElementsByTagAndClassName(null,"listingrow",itemoption);
	if (elems.length == 0){
		swapDOM(itemoption,null);
	}
}

inv.showItemOption = function(id){
	var finalitems = getElement("FinalItems");
	//first, hide all other item option lines
	var elems = getElementsByTagAndClassName(null,"listingrowcontain_show",finalitems);
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

inv.hideItemOption = function(id){
	elem = getElement(id);
	for (var i=1;i<elem.childNodes.length;i++){
		makeInvisible(elem.childNodes[i]);
	}
}

inv.moveItem = function(){
	var finalitems = getElement("FinalItems");
	//get the item option
	var elems = getElementsByTagAndClassName(null,"listingrow_itemoption",document);
	var itemoption = elems[0];
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_itemoption","listingrow");
	}
	//get the item
	var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
	if (elems.length < 1) {
		alert('There is a problem with the javascript.');
	}
	var item = elems[0];
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_item","listingrow");
	}
	if ((itemoption == null) || (item == null)){
		alert("First, choose a item and a item option.");
	} else {
		//look for item option in final item list
		var itemoption_final = getElement("Final_"+itemoption.id);
		var linkdiv = createDOM('DIV',{'id':'closelink_'+item.id, 'class':'listingrow'});
		var closelink = createDOM('A',{'href':'javascript:inv.removeItem("'+item.id+'")'}, "Remove");
		linkdiv.appendChild(closelink);
		if (getNodeAttribute(itemoption_final,"class") == null) {
			elems = getElementsByTagAndClassName("input",null,itemoption);
			for (i=0;i<elems.length;i++){
				if (elems[i].name == "itemoptionname"){
					var ItemOptionName = elems[i].value;
				}
			}
			var itemoption_final = createDOM('DIV',{'id':'Final_'+itemoption.id, 'class':'listingrowcontain', 'onclick':'inv.showItemOption("Final_'+itemoption.id+'")'},ItemOptionName);
			itemoption_final.appendChild(linkdiv);
			itemoption_final.appendChild(item.cloneNode(true));
			swapDOM(item,null);
			finalitems.appendChild(itemoption_final);
		} else {
			itemoption_final.appendChild(linkdiv);
			itemoption_final.appendChild(item.cloneNode(true));
			swapDOM(item,null);
		}
		//show our current final item option line
		inv.showItemOption('Final_'+itemoption.id);
		inv.clearItemOptions();
	}
}

inv.selectItemOption = function(id){
	//deselect any previous item option and select current item option
	var elems = getElementsByTagAndClassName(null,"listingrow_itemoption",document);
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_itemoption","listingrow");
	}
	itemoption = getElement("itemoption_"+id);
	swapElementClass(itemoption,"listingrow","listingrow_itemoption");
	//Find the current StockLocationID which we call the ItemOptionID
	for (var i=0;i<itemoption.childNodes.length;i++){
		if (itemoption.childNodes[i].name == 'ItemOptionID'){
			var ItemOptionID =itemoption.childNodes[i].value;
		}
	}	
	//find the selected item and update the ItemOptionID
	var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
	var item = elems[0];
	if (getNodeAttribute(item,"class") == "listingrow_item"){
		elems = getElementsByTagAndClassName("input",null,item);
		for (var i=0;i<elems.length;i++){
			if (elems[i].name == 'ItemOptionID'){
				elems[i].value = ItemOptionID;
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

inv.clearItemOptions = function() {
	var ItemOptions = createDOM('DIV',{'id':'ItemOptions', 'style':'overflow:auto;'});
	swapDOM('ItemOptions',ItemOptions);
}
inv.renderItemOptions = function(data){
	var tr = function(label, data){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',data);
		row.appendChild(label);
		row.appendChild(data);
		return row;
	}
	var itemoptionDiv = function(record){
		var br = createDOM('BR',null);
		var div = createDOM('DIV',{'class':'listingrow','id':'itemoption_'+record.id, 'ondblclick':'inv.selectItemOption('+record.id+')'});
		var itemoptionname = createDOM('INPUT',{'type':'hidden', 'name':'itemoptionname', 'value':record.Name});
		var itemoptionid = createDOM('INPUT',{'type':'hidden', 'name':'ItemOptionID', 'value':record.id});
		var unitprice = createDOM('INPUT',{'type':'hidden', 'name':'UnitPrice', 'value':record.UnitPrice});
		var table = createDOM('TABLE',{'class':'minimal'});
		var tbody = createDOM('TBODY',null);
		appendChildNodes(tbody, tr("Name",record.Name), tr("Expire date","Rs. " + record.ExpireDate));
		table.appendChild(tbody);
		div.appendChild(itemoptionname);
		div.appendChild(itemoptionid);
		div.appendChild(unitprice);
		div.appendChild(table);
		return div;
	}
	inv.toggle_message();
	var ItemOptions = createDOM('DIV',{'id':'ItemOptions', 'style':'overflow:auto;'});
	for (var i=0; i<data.items.length;i++){
		var record = data.items[i];
		if (record.Status != 'deleted'){
			ItemOptions.appendChild(itemoptionDiv(record));
		}
	}
	swapDOM('ItemOptions',ItemOptions);
}

