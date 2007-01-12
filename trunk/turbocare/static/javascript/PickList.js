/*
	Pick list javascript
	
	Dependencies:
		- Mochikit 1.3 (or higher)
		- Need to use the Mochikit Signal Events system
		
	Example:
		In the javascript of your page, you need the following code:
			pick.openPickList("UrlForSetupData");
				
		In the server side you will need two scripts:
			Script #1:
			UrlForSetupData:  This sends data to the script defining how to setup the display, and selection options
				@expose(format='json')
				def PurchaseOrderCreateNewStep1(self, data='', **kw):
					if data != '':
						raise cherrypy.HTTPRedirect('PurchaseOrderCreateNewStep2?data='+data)
					result_msg = ''
					id=''
					Name = dict(id="qri_Name", name="Name", label="Name", type="String", attr=dict(length=25), data='')
					IsSelectable = dict(id="qri_IsSelectable", name="IsSelectable", label="IsSelectable", type="Hidden", attr=dict(length=25), data='true')
					InvGrpStockNames = []
					for item in model.InvGrpStock.select():
						InvGrpStockNames.append(item.Name)
					SrchCatalogGroups = dict(id="po_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect", attr=dict(Groups=InvGrpStockNames), data='')
					return dict(id=id, Name='PurchaseOrderCreateNewStep1', Label='Select items from catalog',\
						FieldsSrch=[Name, SrchCatalogGroups,IsSelectable], Inputs=[], SrchUrl='CatalogItemSearch', \
						DataUrl='', Url='PurchaseOrderCreateNewStep1', UrlVars='', result_msg=result_msg, \
						SrchNow=False, NoAjax=True)
			Description:
				id:			The javascript ID of the box (behind the scenes programming uses)
				Name:		The javascript name of the box (behind the scenes programming uses)
				Label:		This is displayed near the top of the entry form
				FieldsSrch:	These are the fields (defined earlier) which are included in the form sent to the "SrchUrl" for the query
				Inputs:		When you want extra input boxes on the record, create them here.  They are dictionaries:
				SrchUrl:		The URL which the program calls (using ajson) to get the options to choose from
				DataUrl:		? Not being used?
				Url:			The URL which the script posts the final results to when the "Save and Close" button is pressed
				UrlVars:		Extra URL variables which are posted during the "Save and Close"
				result_msg:	The current operations result message (if you want to tell the user something important about the search)
				SrchNow:		True: when the form is loaded, it will call the "SrchUrl" without delay to display a default set of values
							False: The user needs to press the Search button to get some options to choose from
				NoAjax:		True: The result of the post operation (Save and Close) will attempt to load a page into the browser
							False: The result of Save and Close will be done through Ajax (ajson in this case)
				JsonFunction:	If NoAjax = False, and we want to do a special call back to do DOM manipulation, then
							Add a function which will be used as a callback for the final rendering of our results.
			Script #2:
			ScriptForSaveAndClose:	This script will handle the final results of the Pick list
*/

pick = {};
pick.def = ''; //Data structure definition for our pick list

/*
	Utility functions
*/

pick.error_report = function(data){
	pick.toggle_message("");
	alert('ERROR: ' + data);
}

pick.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

pick.merge_hidden_inputs = function(parentid){
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

pick.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	pick.toggle_message("");
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
/*
	Open a date entry javascript box
*/
pick.DatePick = function(dom_obj){
	if ((dom_obj.type() == 'click') || (dom_obj.type()=='keydown' && (dom_obj.key()['string']=='KEY_ARROW_DOWN'))) {
		Widget.pickDateTime(dom_obj.src().id);
	}
}
pick.collectPostVars = function(f)
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
      	postVars+= f.elements[i].name +'='+ encodeURIComponent(pick.multiselect_csv(f.elements[i].id));
      } else {
      	postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].options[f.elements[i].selectedIndex].value);
      }
    }
  }
  return postVars;
}

pick.multiselect_csv = function(element_id){
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
/*
	Main functions
*/

/*
	Load the data for our pick list
*/
pick.openPickList = function(url){
	if (url != null){
		pick.toggle_message("Loading...");
		var d = loadJSONDoc(url);
		d.addCallbacks(pick.pickList,pick.error_report);
	}
}

/*
	Move an element from the options listing to the chosen listing
*/
pick.pickList_move = function(dom_obj){
	var def = pick.def; 
	var div = dom_obj.src().parentNode;
	var left = getElement('pick_list_qry_result_'+def.Name);
	var right = getElement('pick_list_res_'+def.Name);
	var parent = getElement(div.parentNode);
	if (left == parent){
		appendChildNodes(right,div);
	} else {
		appendChildNodes(left,div);
	}
}
pick.pickList_getData = function(data){
	pick.toggle_message("");
	var def = pick.def;
	var results = getElement('pick_list_res_'+def.Name);
	for(var i = 0; i < data.results.length;i++){
		var chkbox = createDOM('INPUT',{'name':'row_select', 'type':'checkbox', 'checked':'checked'});// 'onclick':'pick.pickList_move("pick_list_row_data_'+data.items[i].id+'")'
		connect(chkbox,'onclick',pick.pickList_move);
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
					var edit = createDOM('INPUT',{'type':'text','id':'datetime_left_'+j+'_'+i, 'name':def.Inputs[j].name,'value':'', 'readonly':'1'});
					appendChildNodes(input, edit, "[<<click box]");
					connect(edit,'onclick',pick.DatePick);
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
	// Attach our onclick event to the checkbox
	var inputs = getElementsByTagAndClassName('INPUT',null,results);
	for (i=0;i<inputs.length;i++){
		if (getNodeAttribute(inputs[i],'type')=="checkbox"){
			connect(inputs[i],'onclick',pick.pick_list_move);
		}
	}
	if (def.SrchNow == true){
		pick.pickList_postsearch();
	}
}
/*
	Display Search results
*/
pick.pickList_getsearch = function(data){
	pick.toggle_message("");
	var def = pick.def;
	var results = createDOM('DIV',{'id':'pick_list_qry_result_'+def.Name});
	for(var i = 0; i < data.results.length;i++){
		var chkbox = createDOM('INPUT',{'name':'row_select', 'type':'checkbox'});// 'onclick':'pick.pickList_move("pick_list_row_'+data.items[i].id+'")'
		connect(chkbox,'onclick',pick.pickList_move);
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
				appendChildNodes(input, edit, "[<<click box]");
				connect(edit,'onclick',pick.DatePick);
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
		// Hidden inputs: these are the full db records (un-modified)
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
		pick.merge_hidden_inputs(rows[i]);
	}
}
/*
	Send the selected Items to the server for processing
*/
pick.pickList_postList = function(dom_obj){
	var def = pick.def;
	var form = 'pick_list_res_'+def.Name;
	var node = getElement(form);
	var data = new Array();
	for (var i=0;i<node.childNodes.length;i++){
		var item = node.childNodes[i];
		var values = formContents(node.childNodes[i]);
		var data_part = new Object();
		for (var j=0;j<values[0].length;j++){
			var name = values[0][j];
			var value = encodeURIComponent(values[1][j].replace('"','\\"','g'));
			data_part[name] = value;
		}
		data[i] = data_part;
	}
	pick.toggle_message("Loading...");
	//alert(serializeJSON(data));
	if (def.NoAjax == true){
 		location = def.Url+'?data='+serializeJSON(data);
 	} else {
		if (def.UrlVars != '') {
		  	var d = postJSON(def.Url,def.UrlVars+'&data='+serializeJSON(data));
		} else {
			var d = postJSON(def.Url,'data='+serializeJSON(data));
		}
		if (def.JsonFunction != null && def.JsonFunction != '') {
			d.addCallbacks(eval(def.JsonFunction),pick.error_report);
		} else {
			d.addCallbacks(pick.updated,pick.error_report);
		}
	 	pick.pickList_remove();
	  	return false;	
 	}
}
pick.pickList_postdata = function(){
	var def = pick.def;
	if (def.DataUrl != ''){
		var url = def.DataUrl;
		pick.toggle_message("Loading...");
	  	var d = postJSON(url,'id='+def.id);
	 	d.addCallbacks(pick.pickList_getData,pick.error_report);
	} else {
		if (def.SrchNow == true){
			pick.pickList_postsearch();
		}
	}
  	return false;
}
/*
	Send the search request to the server
*/
pick.pickList_postsearch = function(dom_obj){
	var def = pick.def;
	var url = def.SrchUrl;
	var form = 'pick_list_qry_form_'+def.Name;
	pick.toggle_message("Loading...");
  	var postVars = pick.collectPostVars(eval('document.'+form));
  	var d = postJSON(url,postVars);
 	d.addCallbacks(pick.pickList_getsearch,pick.error_report);
  	return false;
}
/*
	Close the PickList
*/
pick.pickList_remove = function(){
	swapDOM('pick_list_'+pick.def.Name,null);
	swapDOM('pick_list_shadow_'+pick.def.Name,null);
}
/*
	Create the display for the pick list
*/
pick.pickList = function(def){
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
	pick.toggle_message("");
	pick.def = def;
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
	var close_link = createDOM('A',{'href':'javascript:pick.pickList_remove()'},"Close");
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
	//This is the "Search" button to get our list of options
	var btn_row = createDOM('TR',null);
	var btn_col = createDOM('TD',null);
	var submit_btn = createDOM('BUTTON',{'name':'btnSubmit', 'value':'Search', 'type':'submit'}, 'Search');
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
	// This is our save and close button
	var submit_res_btn = createDOM('BUTTON',{'name':'btnSubmit', 'value':'Save', 'type':'submit'}, 'Save and Close');
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
	pick.pickList_postdata();
	// Connect our button click events
	connect(submit_res_btn,'onclick',pick.pickList_postList);
	connect(submit_btn,'onclick',pick.pickList_postsearch);
//	new Draggable('pick_list_'+def.Name);
}

/*
	EXPORT symbols from the file

export *;
*/