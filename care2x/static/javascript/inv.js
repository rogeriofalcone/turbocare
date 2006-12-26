function postJSON(url, postVars) {
	inv.toggle_message("Sending request...");
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
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
inv.OverlayManager = new YAHOO.widget.OverlayManager();
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

inv.clearAllFormFields = function(parentid){
	elems = getElementsByTagAndClassName('input',null,parentid);
	for (var i=0;i<elems.length;i++){
		elems[i].value = "";
	}
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

inv.merge_hidden_inputs = function(parentid){
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

inv.deleteObj = function(){
	var Result = function(data){
		inv.toggle_message("");
		alert(data.result_msg);
		if (data.result != 0) {
			inv.openObjView(inv.cur_def.Read);
		}
	}
	if (inv.cur_def.id != null) {
		if (confirm("Are you sure you want to delete?")) {
			inv.toggle_message("Deleting...");
			url = inv.cur_def.Del;
		 	var d = postJSON(url,'id='+inv.cur_def.id);
		  	d.addCallback(Result);		
		}
	}
}

inv.undeleteObj = function(){
	var Result = function(data){
		inv.toggle_message("");
		alert(data.result_msg);
		if (data.result != 0) {
			inv.openObjView(inv.cur_def.Read);
		}
	}
	if (inv.cur_def.id != null){
		inv.toggle_message("Un-Deleting...");
		url = inv.cur_def.UnDel;
	 	var d = postJSON(url,'id='+inv.cur_def.id);
	  	d.addCallback(Result);		
	}
}

inv.openObjForm = function(url){
	if (url != null){
		inv.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(inv.renderObjForm);
	} else {
		inv.renderObjForm();
	}
}

inv.openObjView = function(url){
	if (url != null){
		inv.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(inv.renderObjView);
	} else {
		inv.renderObjView();
	}
}

inv.openObjSearch = function(url){
	if (url != null){
		inv.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(inv.SearchBox);
	} else {
		inv.SearchBox();
	}
}

inv.openObjListing = function(url,dest){
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

inv.openObj = function(url){
	if (url != null){
		inv.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(inv.loadDef);
	} else {
		inv.loadDef();
	}
}
// render fields ================
inv.fieldBoolEdit = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',null);
  	var b =  createDOM('SELECT',{'name':field.name,'id':field.id});
	var t =  createDOM('OPTION',{'value':1},'True');
  	var f =  createDOM('OPTION',{'value':0},'False');
  	if (field.data) {
  		setNodeAttribute(t,'selected','selected');
  	} else {
  	  	setNodeAttribute(f,'selected','selected');
  	}
  	b.appendChild(t);b.appendChild(f);
  	data.appendChild(b);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldStringEdit = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',null);
	var edit = createDOM('INPUT',{'type':'text','name':field.name,'value':field.data,'id':field.id});
	data.appendChild(edit);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldStringROEdit = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',field.data);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldTextEdit = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',null);
	var edit = createDOM('TEXTAREA',{'type':'text', 'name':field.name, 'id':field.id,'rows':field.attr.rows},field.data);
	data.appendChild(edit);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldEnumEdit = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',null);
  	var options =  createDOM('SELECT',{'name':field.name,'id':field.id});
  	for (i=0;i<field.options.length;i++){
		var option =  createDOM('OPTION',{'value':field.options[i]},field.options[i]);
		if (field.data == field.options[i]){
			setNodeAttribute(option,'selected','selected');
		}
		options.appendChild(option);
	}
	data.appendChild(options);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldCurrencyEdit = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',null);
	var edit = createDOM('INPUT',{'type':'text','name':field.name,'value':field.data,'id':field.id});
	data.appendChild(edit);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldNumericEdit = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',null);
	var edit = createDOM('INPUT',{'type':'text','name':field.name,'value':field.data,'id':field.id});
	data.appendChild(edit);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldDateTimeEdit = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',null);
	var span = createDOM('SPAN',{'class':'date_time_widget'});
	var edit = createDOM('INPUT',{'type':'text','name':field.name,'value':field.data,'id':field.id, 'readonly':'1'});
	var link = createDOM('A',{'href':'javascript:Widget.pickDateTime("'+field.id+'")','title':'Pick date time'});
	var link_img = createDOM('IMG',{'border':'0','src':'/static/images/cal.png'});
	link.appendChild(link_img);
	span.appendChild(edit);
	span.appendChild(link);
	data.appendChild(span);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;	
}

inv.fieldHiddenEdit = function(field){
	var hidden = createDOM('INPUT',{'type':'hidden','name':field.name,'value':field.data,'id':field.id});
	return hidden
}

inv.fieldForeignKeyEdit_onchange = function(field_num){
	var renderResult = function(data){
		inv.toggle_message("");
		if (inv.cur_def.Fields[data.field_num].attr.edit_url != null){
			var edit_url = inv.cur_def.Fields[data.field_num].attr.edit_url;
		} else {
			var edit_url = inv.cur_def.Edit;
		}
		var link = createDOM('A',{'href':'javascript:inv.openObjForm(\''+edit_url+'?id='+data.record.id+'\')'},'<<Edit');
		if (data.record.id == null)  {
			var text = createDOM('DIV',{'id':data.field_id},data.display);
		} else {
			var text = createDOM('DIV',{'id':data.field_id},data.display,link);
		}
		swapDOM(data.field_id,text);
	}
	var field = inv.cur_def.Fields[field_num];
	var url = field.attr.lookupUrl;
	var id_field = field.id;
	var field_id = field.id + '_display';
	var full_url = url+'?Id='+eval('document.ObjForm.'+id_field+'.value')+'&field_id='+field_id+'&field_num='+field_num;
  	var d = loadJSONDoc(full_url);
  	d.addCallbacks(renderResult,inv.error_report);	
}
inv.fieldForeignKeyEdit_update = function(field_num){
	//alert(inv.cur_def.Fields[field_num].name);
	//create a search field list of "name" followed by "label"
	var field = inv.cur_def.Fields[field_num];
	if (getNodeAttribute('fk_form_'+field.id+'_srch','name') == null){
		inv.fieldForeignKeyEdit_srch(field_num);
	} else {
		if (getNodeAttribute('fk_select_'+field.id,'id') != null){
			eval('document.ObjForm.'+field.id+'.value=document.ObjForm.fk_select_'+field.id+'.value');
		}
		inv.fieldForeignKeyEdit_remove(field_num);
		inv.fieldForeignKeyEdit_onchange(field_num);
	}
}
inv.fieldForeignKeyEdit_get_srchresult = function(data){
	inv.toggle_message("");
	var field = inv.cur_def.Fields[data.field_num];
	var srch_result_id = field.id+'_srch_results'
	var select = createDOM('SELECT',{'class':'foreignkey;','size':'5','id':'fk_select_'+field.id, 'ondblclick':'inv.fieldForeignKeyEdit_update('+data.field_num+')'});
	for(var i = 0; i < data.results.length;i++){
		if (data.results[i].text != ''){
			var option = createDOM('OPTION',{'value':data.results[i].id}, data.results[i].text);
		} else {
			var option = createDOM('OPTION',{'value':data.results[i].id}, data.results[i].Name + ', ' + data.results[i].Description);
		}
		select.appendChild(option);
	}
	var br = createDOM('BR',null);
	var pick_link = 'document.ObjForm.'+field.id+'.value=document.ObjForm.fk_select_'+field.id+'.value';
	var btnPick = createDOM('BUTTON',{'name':'btnPick', 'type':'button', 'onclick':'inv.fieldForeignKeyEdit_update('+data.field_num+')'}, 'Pick');
	replaceChildNodes(srch_result_id,select,br,btnPick);
}
inv.fieldForeignKeyEdit_post_srchresult = function(field_num){
	var field = inv.cur_def.Fields[field_num];
	var url = field.attr.srchUrl;
	var form_name = 'fk_form_'+field.id+'_srch';
  	var postVars =inv.collectPostVars(eval('document.'+form_name));
  	var d = postJSON(url,postVars+'&field_num='+field_num);
  	d.addCallbacks(inv.fieldForeignKeyEdit_get_srchresult,inv.error_report);
  	return false;
}
inv.fieldForeignKeyEdit_remove = function(field_num){
	var srch_field_id = inv.cur_def.Fields[field_num].id+'_srch';
	replaceChildNodes(srch_field_id,null);
}
inv.fieldForeignKeyEdit_srch = function(field_num){
	var StringEdit = function(name, label){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','name':name});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	var url = inv.cur_def.SrchLink;
	var srch_field_id = inv.cur_def.Fields[field_num].id + '_srch';
	var srch_fields = inv.cur_def.Fields[field_num].attr.srchFields;
	var submit_link = 'inv.fieldForeignKeyEdit_post_srchresult('+field_num+')';
	var form = createDOM('FORM',{'onsubmit':'return false;', 'name':'fk_form_'+srch_field_id,'id':'fk_form_'+srch_field_id, 'class':'tableform'});
	var table = createDOM('TABLE',null);
	var tablebody = createDOM('TBODY',null);
	for(var i = 0; i < srch_fields.length;i++){
		tablebody.appendChild(StringEdit(srch_fields[i].name,srch_fields[i].label));
	}
	var br = createDOM('BR',null);
	var srch_results = createDOM('DIV',{'id':srch_field_id+'_results'});//creates a field like: inv.cur_def.Fields[i].id + '_srch_results'
	var close_link = createDOM('A',{'href':'javascript:inv.fieldForeignKeyEdit_remove('+field_num+')'},"Close");
	var submit_btn = createDOM('BUTTON',{'name':'btnSubmit', 'value':'Search', 'type':'submit', 'onclick':submit_link}, 'Search');
	table.appendChild(tablebody);
	form.appendChild(close_link);
	form.appendChild(table);
	form.appendChild(submit_btn);
	replaceChildNodes(srch_field_id,form,br,srch_results);
}
inv.fieldForeignKeyEdit = function(field,num){
	var update_js = 'inv.fieldForeignKeyEdit_update('+num+')';
	var row = createDOM('TR',null);
	var label = createDOM('TD',null);
	var update_link = createDOM('A',{'href':'javascript:'+update_js},field.label);
	label.appendChild(update_link);
	var data = createDOM('TD',null);
	var hidden = createDOM('INPUT',{'type':'hidden', 'name':field.name, 'value':field.data, 'id':field.id},field.data);
	if (field.attr.edit_url != null){
		var edit_url = field.attr.edit_url;
	} else {
		var edit_url = inv.cur_def.Edit;
	}
	var link = createDOM('A',{'href':'javascript:inv.openObjForm(\''+edit_url+'?id=' + field.data + '\')'}, '  <<Edit');
	if ((field.data == null) || (field.data == ''))  {
		var disp_text = createDOM('DIV',{'id':field.id+'_display'},field.init_display);
	} else {
		var disp_text = createDOM('DIV',{'id':field.id+'_display'},field.init_display,link);
	}
	var br = createDOM('BR',null);
	var disp_srch_box = createDOM('DIV',{'id':field.id+'_srch'});
	data.appendChild(hidden);
	data.appendChild(disp_text);
	data.appendChild(disp_srch_box);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldMultiJoinEdit_update = function(field_num){
	var tableRow = function(record,editLink){
		var row = createDOM('TR',null);
		var col1 = createDOM('TD',null);
		var col2 = createDOM('TD',record.listing);
		var link = createDOM('A',{'href':'javascript:inv.openObjForm(\''+editLink+'?id='+record.id+'\')'},'Edit>>');
		col1.appendChild(link);
		row.appendChild(col1);
		row.appendChild(col2); 
		return row;
	}
	var makeTable = function(data){
		inv.toggle_message("");
		var field = inv.cur_def.Fields[data.field_num];
		var table = createDOM('TABLE',{'class':'listing','id':field.id+'_listing_table'});
		var tbody = createDOM('TBODY',null);
		for (var i=0;i<data.col_items.length;i++){
			tbody.appendChild(tableRow(data.col_items[i],field.attr.linkUrl));
		}
		table.appendChild(tbody);
		replaceChildNodes(field.id+'_listing',table);
	}
	var removeTable = function(field_num){
		var field = inv.cur_def.Fields[field_num];
		replaceChildNodes(field.id+'_listing',null);
	}
	var setDisplay_apply = function(data){
		inv.toggle_message("");
		var field = inv.cur_def.Fields[data.field_num];
		var disp_text = createDOM('DIV',{'id':field.id+'_display'},data.dislpay);
		swapNodes(field.id+'_display',disp_text);
	}
	var setDisplay = function(field_num){
		var field = inv.cur_def.Fields[field_num];
		var full_url = field.attr.displayUrl+'?Id='+inv.cur_def.id+'&ColName='+field.name+'&field_num='+field_num;
  		var d = loadJSONDoc(full_url);
	  	d.addCallbacks(setDisplay_apply,inv.error_report);			
	}
	var getTableData = function(field_num){
		inv.toggle_message("Loading..."); 
		field = inv.cur_def.Fields[field_num];
		var full_url = field.attr.listUrl+'?Id='+inv.cur_def.id+'&ColName='+field.name+'&field_num='+field_num;
  		var d = loadJSONDoc(full_url);
	  	d.addCallbacks(makeTable,inv.error_report);	
	}
	var field = inv.cur_def.Fields[field_num];
	if (getNodeAttribute(field.id+'_listing_table','class') == null){
		getTableData(field_num);
		setDisplay(field_num);
	} else {
		removeTable(field_num);
		setDisplay(field_num);
	}
}
inv.fieldMultiJoinEdit = function(field,num){
	var update_js = 'inv.fieldMultiJoinEdit_update('+num+')';
	var row = createDOM('TR',null);
	var label = createDOM('TD',null);
	var update_link = createDOM('A',{'href':'javascript:'+update_js},field.label);
	label.appendChild(update_link);
	var data = createDOM('TD',null);
	var disp_text = createDOM('DIV',{'id':field.id+'_display'},field.data);
	var br = createDOM('BR',null);
	var disp_listing = createDOM('DIV',{'id':field.id+'_listing'});
	data.appendChild(disp_text);
	data.appendChild(disp_listing);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldRelatedJoinEdit_close = function(field_num){
	var field = inv.cur_def.Fields[field_num];
	replaceChildNodes(field.id+'_select',null);
}
inv.fieldRelatedJoinEdit_load_srch_right = function(data){
	inv.toggle_message("");
	var field = inv.cur_def.Fields[data.field_num];
	var items = data.results;
	for (var i=0;i<items.length;i++){
		var option = createDOM('OPTION',{'value':items[i].id},items[i].text);
		if (i == 0) {
			replaceChildNodes(field.id+'_select_list_right',option);
		} else {
			appendChildNodes(field.id+'_select_list_right',option);
		}
	}
}
inv.fieldRelatedJoinEdit_load_select_left = function(data){
	inv.toggle_message("");
	var field = inv.cur_def.Fields[data.field_num];
	var items = data.rel_items;
	for (var i=0;i<items.length;i++){
		var option = createDOM('OPTION',{'color':'black', 'value':items[i].id},items[i].text);
		if (i == 0) {
			replaceChildNodes(field.id+'_select_list_left',option);
		} else {
			appendChildNodes(field.id+'_select_list_left',option);
		}
	}
	inv.fieldRelatedJoinEdit_setDisplay(data.field_num);
}
inv.fieldRelatedJoinEdit_post_select_left = function(field_num){
	inv.toggle_message("Loading...");
	field = inv.cur_def.Fields[field_num];
	var full_url = field.attr.listUrl+'?Id='+inv.cur_def.id+'&field_num='+field_num;
	var d = loadJSONDoc(full_url);
  	d.addCallbacks(inv.fieldRelatedJoinEdit_load_select_left,inv.error_report);			
}
inv.fieldRelatedJoinEdit_remove_option_items = function(field_num){
	var field = inv.cur_def.Fields[field_num];
	var nodes = getElement(field.id+'_select_list_left').childNodes;
	for (var i=0;i<nodes.length;i++){
	 	if (nodes[i].selected){
	 		appendChildNodes(field.id+'_select_list_right',nodes[i]);
	 		i--; //decrement counter when item is removed since nodes.length is updated to one less value.
	 	}
	}
	return false;
}
inv.fieldRelatedJoinEdit_copy_option_items = function(field_num){
	var field = inv.cur_def.Fields[field_num];
	var nodes = getElement(field.id+'_select_list_right').childNodes;
	for (var i=0;i<nodes.length;i++){
	 	if (nodes[i].selected) {
	 		appendChildNodes(field.id+'_select_list_left',nodes[i]);
	 		i--; //decrement counter when item is removed since nodes.length is updated to one less value.
	 	}
	}
	return false;
}
inv.fieldRelatedJoinEdit_save_option_items = function(field_num){
	var field = inv.cur_def.Fields[field_num];
	var url = field.attr.saveUrl;
	var nodes = getElement(field.id+'_select_list_left').childNodes;
	for (var i=0;i<nodes.length;i++){
	 	nodes[i].selected = true;
	}
	if (nodes.length == 0) {
	  	var d = postJSON(url,'field_num='+field_num+'&id='+inv.cur_def.id);
	  	d.addCallbacks(inv.fieldRelatedJoinEdit_load_select_left,inv.error_report);
	} else {
		var form_name = field.id+'_select_form_left';
		var csv = inv.multiselect_csv(field.id+'_select_list_left');
		var postVars =inv.collectPostVars(eval('document.'+form_name))
		var d = postJSON(url,postVars+'&field_num='+field_num+'&id='+inv.cur_def.id+'&new_option_select='+csv);
		d.addCallbacks(inv.fieldRelatedJoinEdit_load_select_left,inv.error_report);
	 }
  	return false;
}
inv.fieldRelatedJoinEdit_srch_option_items = function(field_num){
	var field = inv.cur_def.Fields[field_num];
	var url = field.attr.srchUrl;
	var form_name = field.id+'_srch_form_right';
  	var postVars =inv.collectPostVars(eval('document.'+form_name));
  	var d = postJSON(url,postVars+'&field_num='+field_num+'&id='+inv.cur_def.id);
  	d.addCallbacks(inv.fieldRelatedJoinEdit_load_srch_right,inv.error_report);
  	return false;
}
inv.fieldRelatedJoinEdit_setDisplay_apply = function(data){
	inv.toggle_message("");
	var field = inv.cur_def.Fields[data.field_num];
	var disp_text = createDOM('DIV',{'id':field.id+'_display'},data.display);
	swapDOM(field.id+'_display',disp_text);
}
inv.fieldRelatedJoinEdit_setDisplay = function(field_num){
	inv.toggle_message("Loading...");
	var field = inv.cur_def.Fields[field_num];
	var full_url = field.attr.displayUrl+'?Id='+inv.cur_def.id+'&field_num='+field_num;
	var d = loadJSONDoc(full_url);
  	d.addCallbacks(inv.fieldRelatedJoinEdit_setDisplay_apply,inv.error_report);			
}
inv.fieldRelatedJoinEdit_update = function(field_num){
	var close = function(field_num){
		var field = inv.cur_def.Fields[field_num];
		replaceChildNodes(field.id+'_select',null);
	}
	var makeEdit = function(field_num){
		var StringEdit = function(name, label){
			var row = createDOM('TR',null);
			var label = createDOM('TD',label);
			var data = createDOM('TD',null);
			var edit = createDOM('INPUT',{'type':'text','name':name});
			data.appendChild(edit);
		  	row.appendChild(label);
		  	row.appendChild(data);
		  	return row;
		}
		var field = inv.cur_def.Fields[field_num];
			//Main table
		var table = createDOM('TABLE',{'class':'minimal','id':field.id+'_select_table'});
		var tbody = createDOM('TBODY',null);
		var row = createDOM('TR',null);
		var col1 = createDOM('TD',null);
		var col2 = createDOM('TD',null);
			//Selected items
		var table_left = createDOM('TABLE',{'class':'minimal','id':field.id+'_select_table_left'});
		var tbody_left = createDOM('TBODY',null);
		var row1_left = createDOM('TR',null);
		var col1_left = createDOM('TD',null);
		var row2_left = createDOM('TR',null);
		var col2_left = createDOM('TD',null);
		var form_left = createDOM('FORM',{'onsubmit':'return false;', 'name':field.id+'_select_form_left', 'class':'tableform', 'id':field.id+'_select_form_left'});
		var save_btn = createDOM('BUTTON',{'name':'btnSave', 'value':'Save', 'type':'submit', 'onclick':'inv.fieldRelatedJoinEdit_save_option_items('+field_num+')'}, 'Save');
		var delete_btn = createDOM('BUTTON',{'name':'btnDelete', 'value':'Delete', 'type':'submit', 'onclick':'inv.fieldRelatedJoinEdit_remove_option_items('+field_num+')'}, 'Delete');
		var select_left = createDOM('SELECT',{'multiple':'multiple', 'size':'11', 'class':'relatedjoin','name':'option_select', 'id':field.id+'_select_list_left', 'ondblclick':'inv.fieldRelatedJoinEdit_remove_option_items('+field_num+')'});
		col2_left.appendChild(delete_btn);
		col2_left.appendChild(save_btn);
		col1_left.appendChild(select_left);
		row1_left.appendChild(col1_left);
		row2_left.appendChild(col2_left);
		tbody_left.appendChild(row1_left);
		tbody_left.appendChild(row2_left);
		table_left.appendChild(tbody_left);
		form_left.appendChild(table_left); //<------------- This is the main object here
			//Selectable items
		var table_right = createDOM('TABLE',{'class':'minimal','id':field.id+'_select_table_right'});
		var tbody_right = createDOM('TBODY',null);
		var row1_right = createDOM('TR',null);
		var col1_right = createDOM('TD',null);
		var row2_right = createDOM('TR',null);
		var col2_right = createDOM('TD',null);
		var row3_right = createDOM('TR',null);
		var col3_right = createDOM('TD',null);
				//search
		var form_srch = createDOM('FORM',{'onsubmit':'return false;', 'name':field.id+'_srch_form_right', 'class':'tableform', 'id':field.id+'_srch_form_right'});
		var table_srch = createDOM('TABLE',{'class':'minimal'});
		var tbody_srch = createDOM('TBODY',null);
		for (var i=0;i<field.attr.srchFields.length;i++){
			tbody_srch.appendChild(StringEdit(field.attr.srchFields[i].name,field.attr.srchFields[i].label));
		}
		var row_srch = createDOM('TR',null);
		var col_srch = createDOM('TD',null);
		var btn_srch = createDOM('BUTTON',{'name':'btnSrch', 'value':'Search', 'type':'submit', 'onclick':'inv.fieldRelatedJoinEdit_srch_option_items('+field_num+')'}, 'Search');
		col_srch.appendChild(btn_srch);
		row_srch.appendChild(col_srch);
		tbody_srch.appendChild(row_srch);
		table_srch.appendChild(tbody_srch);
		form_srch.appendChild(table_srch);
		col1_right.appendChild(form_srch);
				//list box
		var select_right = createDOM('SELECT',{'multiple':'multiple', 'size':'5', 'class':'relatedjoin','name':'option_select', 'id':field.id+'_select_list_right','ondblclick':'inv.fieldRelatedJoinEdit_copy_option_items('+field_num+')'});
		col2_right.appendChild(select_right);
				//buttons
		var select_btn = createDOM('BUTTON',{'name':'btnSelect', 'value':'Copy', 'type':'submit', 'onclick':'inv.fieldRelatedJoinEdit_copy_option_items('+field_num+')'}, 'Select');
		var cancel_btn = createDOM('BUTTON',{'name':'btnCancel', 'value':'Cancel', 'type':'submit', 'onclick':'inv.fieldRelatedJoinEdit_close('+field_num+')'}, 'Cancel');
		col3_right.appendChild(cancel_btn);
		col3_right.appendChild(select_btn);
		var form_right = createDOM('FORM',{'onsubmit':'return false;', 'name':field.id+'_select_form_right', 'class':'tableform', 'id':field.id+'_select_form_right'});
		row1_right.appendChild(col1_right);
		row2_right.appendChild(col2_right);
		row3_right.appendChild(col3_right);
		tbody_right.appendChild(row1_right);
		tbody_right.appendChild(row2_right);
		tbody_right.appendChild(row3_right);
		table_right.appendChild(tbody_right);
		form_right.appendChild(table_right);
			//final appends
		col1.appendChild(form_left);
		col2.appendChild(form_right);
		row.appendChild(col1);
		row.appendChild(col2);
		tbody.appendChild(row);
		table.appendChild(tbody);
		replaceChildNodes(field.id+'_select',table);
	}
	var field = inv.cur_def.Fields[field_num];
	if (getNodeAttribute(field.id+'_select_table','class') == null){
		makeEdit(field_num);
		inv.fieldRelatedJoinEdit_post_select_left(field_num);
	} else {
		close(field_num);
		inv.fieldRelatedJoinEdit_setDisplay(field_num);
	}
}
inv.fieldRelatedJoinEdit = function(field, num){
	var update_js = 'inv.fieldRelatedJoinEdit_update('+num+')';
	var row = createDOM('TR',null);
	var label = createDOM('TD',null);
	var update_link = createDOM('A',{'href':'javascript:'+update_js},field.label);
	label.appendChild(update_link);
	var data = createDOM('TD',null);
	var disp_text = createDOM('DIV',{'id':field.id+'_display'},field.data);
	var br = createDOM('BR',null);
	var disp_listing = createDOM('DIV',{'id':field.id+'_select'});
	data.appendChild(disp_text);
	data.appendChild(disp_listing);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldDisplay = function(field) {
	var display = createDOM('DIV',{'class':field.attr.css_class,'id':field.id},field.data);
	if (getNodeAttribute(field.id,'class') == null){
		document.body.appendChild(display);
	} else {
		swapDOM(field.id,display);
	}
  	return null;	
}

inv.fieldBoolView = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	if (field.data) {
		var data = createDOM('TD','True');
	} else {
		var data = createDOM('TD','False');
	}
  	row.appendChild(label);
  	row.appendChild(data);
	return row;
}

inv.fieldStringView = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',field.data);
  	row.appendChild(label);
  	row.appendChild(data);
	return row;
}

inv.fieldStringROView = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',field.data);
  	row.appendChild(label);
  	row.appendChild(data);
  	return row;
}

inv.fieldTextView = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',{'style':'width:'+field.attr.cols*8+'px'},field.data);
  	row.appendChild(label);
  	row.appendChild(data);
	return row;
}

inv.fieldEnumView = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',field.data);
  	row.appendChild(label);
  	row.appendChild(data);
	return row;
}

inv.fieldCurrencyView = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',field.data);
  	row.appendChild(label);
  	row.appendChild(data);
	return row;
}

inv.fieldNumericView = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',field.data);
  	row.appendChild(label);
  	row.appendChild(data);
	return row;
}

inv.fieldDateTimeView = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',field.data);
  	row.appendChild(label);
  	row.appendChild(data);
	return row;
}

inv.fieldForeignKeyView = function(field){
	var row = createDOM('TR',null);
	var label = createDOM('TD',field.label);
	var data = createDOM('TD',field.init_display);
  	row.appendChild(label);
  	row.appendChild(data);
	return row;
}

inv.fieldMultiJoinView = function(field,num){
	return inv.fieldMultiJoinEdit(field,num);
}

inv.fieldRelatedJoinView = function(field,num){
	return inv.fieldRelatedJoinEdit(field,num);
}

inv.buttonSave = function(link){
	var button = createDOM('BUTTON',{'name':'btnSave', 'value':'Save', 'onclick':'inv.saveForm("'+link+'")'}, 'Save');
	return button
}

inv.buttonCancel = function(link){
	var button = createDOM('BUTTON',{'name':'btnCancel', 'value':'Cancel', 'type':'reset', 'onclick':'inv.historyBack()'}, 'Cancel');
	return button
}

inv.buttonEdit = function(link){
	var button = createDOM('BUTTON',{'name':'btnEdit', 'value':'Edit', 'onclick':'inv.openObjForm("'+link+'")'},'Edit');
	return button
}

inv.buttonNavNext = function(link){

}

inv.buttonNavPrev = function(link){

}

inv.buttonNavFirst = function(link){

}

inv.buttonNavLast = function(link){

}
//Tabber fields

inv.tabberCreate = function(field,IsEdit){
	var row = createDOM('TR',null);
	var data = createDOM('TD',{'colspan':2});
	var tabber = createDOM('DIV',{"class":"tabber"});
	//for (var i=0;i<field.
  	row.appendChild(data);
	return row;
}


// load view/form data =========

// render object ===============
inv.displayObj = function(obj){
	replaceChildNodes('dom_obj',obj);
}

inv.renderObjForm = function(def){
	inv.toggle_message("");
	if (def != null){
	  	inv.addHistory({'view':'renderObjForm','def':def});
	  	inv.cur_def = def;
	} else {
		def = inv.cur_def;
	}
	if (def.id != null){
		var IdNum = " (" + def.id + ")";
	} else {
		var IdNum = "";
	}
  	var ObjForm = createDOM('DIV',null);
  	var menubar = createDOM('DIV',{'id':'menubar','class':'yuimenubar'});
  	var title = createDOM('H3',{'style':'text-align:left'},def.Label+IdNum);
	var form = createDOM('FORM',{'class':'tableform','action':'', 'name':'ObjForm', 'onsubmit':'return false;'});
	var table = createDOM('TABLE',{'class':'tableform'});
	var tablebody = createDOM('TBODY',null);
	var fields = def.Fields;
	for(var i = 0; i < fields.length;i++){
		switch(fields[i].type) {
			case 'Bool':
			var row = inv.fieldBoolEdit(fields[i]);
			break;
			case 'String':
			var row = inv.fieldStringEdit(fields[i]);
			break;
			case 'StringRO':
			var row = inv.fieldStringROEdit(fields[i]);
			break;
			case 'Text':
			var row = inv.fieldTextEdit(fields[i]);
			break;
			case 'Numeric':
			var row = inv.fieldNumericEdit(fields[i]);
			break;
			case 'Enum':
			var row = inv.fieldEnumEdit(fields[i]);
			break;
			case 'Currency':
			var row = inv.fieldCurrencyEdit(fields[i]);
			break;
			case 'Numeric':
			var row = inv.fieldNumericEdit(fields[i]);
			break;
			case 'DateTime':
			var row = inv.fieldDateTimeEdit(fields[i]);
			break;
			case 'Hidden':
			var hidden_field = inv.fieldHiddenEdit(fields[i]);
			form.appendChild(hidden_field);
			break;
			case 'ForeignKey':
			var row = inv.fieldForeignKeyEdit(fields[i],i);
			break;
			case 'MultiJoin':
			var row = inv.fieldMultiJoinEdit(fields[i],i);
			break;
			case 'RelatedJoin':
			var row = inv.fieldRelatedJoinEdit(fields[i],i);
			break;
			case 'Display':
			var row = inv.fieldDisplay(fields[i]);
			break;
			default:			
			var row = inv.fieldStringEdit(fields[i]);
		}
		if ((fields[i].type != 'Hidden') && (fields[i].type != 'Display')){
			tablebody.appendChild(row);
		}
	}
	table.appendChild(tablebody);
	form.appendChild(table);
	form.appendChild(inv.buttonCancel(''));
	form.appendChild(inv.buttonSave(def.Save));
	ObjForm.appendChild(menubar);
	ObjForm.appendChild(title);
	ObjForm.appendChild(form);
	inv.displayObj(ObjForm);
  	inv.ObjMenuBar(inv.cur_def);
}

inv.renderObjView = function(def){
	inv.toggle_message("");
	if (def != null){
	  	inv.addHistory({'view':'renderObjView','def':def});
	  	inv.cur_def = def;
	} else {
		def = inv.cur_def;
	}
 	if (def.id != null){
		var IdNum = " (" + def.id + ")";
	} else {
		var IdNum = "";
	}
  	var ObjView = createDOM('DIV',null);
  	var title = createDOM('H3',{'style':'text-align:left'},def.Label+IdNum);
  	var br = createDOM('BR',null);
  	var menubar = createDOM('DIV',{'id':'menubar','class':'yuimenubar'});
	var table = createDOM('TABLE',{'class':'tableform'});
	var tablebody = createDOM('TBODY',null);
	var fields = def.Fields;
	for(var i = 0; i < fields.length;i++){
		switch(fields[i].type) {
			case 'Bool':
			var row = inv.fieldBoolView(fields[i]);
			break;
			case 'String':
			var row = inv.fieldStringView(fields[i]);
			break;
			case 'StringRO':
			var row = inv.fieldStringROView(fields[i]);
			break;
			case 'Text':
			var row = inv.fieldTextView(fields[i]);
			break;
			case 'Numeric':
			var row = inv.fieldNumericView(fields[i]);
			break;
			case 'Enum':
			var row = inv.fieldEnumView(fields[i]);
			break;
			case 'Currency':
			var row = inv.fieldCurrencyView(fields[i]);
			break;
			case 'Numeric':
			var row = inv.fieldNumericView(fields[i]);
			break;
			case 'DateTime':
			var row = inv.fieldDateTimeView(fields[i]);
			break;
			case 'Hidden':
			//var hidden_field = inv.fieldHiddenEdit(fields[i]);
			break;
			case 'ForeignKey':
			var row = inv.fieldForeignKeyView(fields[i],i);
			break;
			case 'MultiJoin':
			var row = inv.fieldMultiJoinView(fields[i],i);
			break;
			case 'RelatedJoin':
			var row = inv.fieldRelatedJoinView(fields[i],i);
			break;
			case 'Display':
			var row = inv.fieldDisplay(fields[i]);
			break;
			default:			
			var row = inv.fieldStringView(fields[i]);
		}
		if ((fields[i].type != 'Hidden') && (fields[i].type != 'Display')){
			tablebody.appendChild(row);
		}
	}
	table.appendChild(tablebody);
	btnRow = createDOM('TR',null);
	btnCol = createDOM('TD',null);
	btnCol.appendChild(inv.buttonCancel(''));
	btnCol.appendChild(inv.buttonEdit(def.Edit+'?id='+def.id));
	btnRow.appendChild(btnCol);
	table.appendChild(btnRow);
	ObjView.appendChild(menubar);
	ObjView.appendChild(title);
	ObjView.appendChild(table);
	inv.displayObj(ObjView);
  	inv.ObjMenuBar(inv.cur_def);
}

inv.SearchBox_view = function(){
	if (eval('document.'+inv.cur_def.Name+'SearchBoxFormSelect.'+inv.cur_def.Name+'SearchBoxSelect.value')!=null) {
		inv.openObjView(inv.cur_def.Read+'?id='+eval('document.'+inv.cur_def.Name+'SearchBoxFormSelect.'+inv.cur_def.Name+'SearchBoxSelect.value'));
		inv.SearchBox_remove();
	}
}
inv.SearchBox_getsearch = function(data){
	inv.toggle_message("");
	var form = createDOM('FORM',{'class':'tableform','name':inv.cur_def.Name+'SearchBoxFormSelect','id':inv.cur_def.Name+'SearchBoxFormSelect'});
	var select = createDOM('SELECT',{'class':'foreignkey;','size':'5','id':inv.cur_def.Name+'SearchBoxSelect', 'ondblclick':'inv.SearchBox_view()'});
	//alert(data.results.length);
	for(var i = 0; i < data.results.length;i++){
		if (data.results[i].text != ''){
			var option = createDOM('OPTION',{'value':data.results[i].id}, data.results[i].text);
		} else {
			var option = createDOM('OPTION',{'value':data.results[i].id}, data.results[i].Name + ', ' + data.results[i].Description);
		}
		select.appendChild(option);
	}
	var br = createDOM('BR',null);
	var btnPick = createDOM('BUTTON',{'name':'btnPick', 'type':'button', 'onclick':'inv.SearchBox_view()'}, 'Pick');
	form.appendChild(select);
	form.appendChild(br);
	form.appendChild(btnPick);
	replaceChildNodes(inv.cur_def.Name+'SearchBox_results',form);
}
inv.SearchBox_postsearch = function(){
	inv.toggle_message("Loading...");
	var url = inv.cur_def.SrchUrl;
	var form_name = inv.cur_def.Name+'SearchBoxForm';
  	var postVars =inv.collectPostVars(eval('document.'+form_name));
  	var d = postJSON(url,postVars);
  	d.addCallbacks(inv.SearchBox_getsearch,inv.error_report);
  	return false;
}
inv.SearchBox_remove = function(){
	swapDOM(inv.cur_def.Name+'SearchBox',null);
}
inv.SearchBox_create = function(){
	var StringEdit = function(name, label,num){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','name':name,'id':inv.cur_def.Name+'SearchBoxFormField'+num});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	var url = inv.cur_def.SrchLink;
	var srch_fields = inv.cur_def.FieldsSrch;
	var submit_link = 'inv.SearchBox_postsearch()';
	var SearchBox = createDOM('DIV',{'class':'SearchBox','id':inv.cur_def.Name+'SearchBox'});
	var form = createDOM('FORM',{'onsubmit':'return false;', 'name':inv.cur_def.Name+'SearchBoxForm','id':inv.cur_def.Name+'SearchBoxForm', 'class':'tableform'});
	var table = createDOM('TABLE',null);
	var tablebody = createDOM('TBODY',null);
	for(var i = 0; i < srch_fields.length;i++){
		tablebody.appendChild(StringEdit(srch_fields[i].name,srch_fields[i].label,i));
	}
	var br = createDOM('BR',null);
	var row_btn = createDOM('TR',null);
	var col_btn = createDOM('TD',{'colspan':2});
	row_btn.appendChild(col_btn);
	tablebody.appendChild(row_btn);
	var row_results = createDOM('TR',null);
	var results = createDOM('TD',{'colspan':2, 'id':inv.cur_def.Name+'SearchBox_results'});
	row_results.appendChild(results);
	tablebody.appendChild(row_results);
	var close_link = createDOM('A',{'href':'javascript:inv.SearchBox_remove()'},"Close");
	var submit_btn = createDOM('BUTTON',{'name':'btnSubmit', 'value':'Search', 'type':'submit', 'onclick':submit_link}, 'Search');
	col_btn.appendChild(submit_btn);
	table.appendChild(tablebody);
	form.appendChild(close_link);
	form.appendChild(table);
	SearchBox.appendChild(form);
	if (getNodeAttribute(inv.cur_def.Name+'SearchBox','class') == null){
		document.body.appendChild(SearchBox);
	} else {
		swapDOM(inv.cur_def.Name+'SearchBox',SearchBox);
	}
	//new Effect.BlindDown(inv.cur_def.Name+'SearchBox',{duration: 2.0});
	eval('document.'+inv.cur_def.Name+'SearchBoxForm.'+inv.cur_def.Name+'SearchBoxFormField0.focus()');
}
inv.SearchBox = function(def){
	inv.toggle_message("");
	if (def != null) {
	  	inv.cur_def = def;
	}
	//var js_link = 'javascript:inv.SearchBox_create()';
	//var link = createDOM('A',{'href':js_link},inv.cur_def.Label);
  	//inv.displayObj(link);
  	inv.SearchBox_create();  	
}

inv.Listing_getsearch = function(data){
	inv.toggle_message("");
	if (inv.listing_dest == null){
		var def = inv.cur_def;
	} else {
		var def = inv.listing_def;
	}
	var results = createDOM('DIV',null);
	for(var i = 0; i < data.results.length;i++){
		var editlink = createDOM('A',{'href':'javascript:inv.openObjForm("'+def.Edit+'?id='+data.items[i].id+'")'},'  Edit  ');
		if (data.results[i].text != '') {
			var result = createDOM('DIV',{'class':'listingrow','id':'listingrow_'+data.items[i].id}, editlink, data.results[i].text);
		} else {
			var result = createDOM('DIV',{'class':'listingrow','id':'listingrow_'+data.items[i].id}, editlink, data.results[i].Name + ', ' + data.results[i].Description);
		}
		for (var j in data.items[i]) {
			var input = createDOM('INPUT',{'type':'hidden', 'name':j, 'value':eval('data.items[i].'+j)});
			result.appendChild(input);
		}
		//additional inputs
		for (var j = 0; j<inv.list_inputs.length; j++){
			var label = createDOM('LABEL',inv.list_inputs[j].label);
			var input = createDOM('INPUT',{'type':'text', 'name':inv.list_inputs[j].name});
			result.appendChild(label);
			result.appendChild(input);
		}
		results.appendChild(result);
	}
	replaceChildNodes('listing_result_'+def.Name,results);
	//for(var i = 0; i < data.results.length;i++){	
	//	new Draggable('listingrow_'+data.items[i].id,{revert:true, ghosting:true});
	//}
}
inv.Listing_postsearch = function(){
	if (inv.list_dest == null) {
		var def = inv.cur_def;
	} else {
		var def = inv.list_def;
	}
	var url = def.SrchUrl;
	var form = 'listing_form_'+def.Name;
	inv.toggle_message("Loading...");
  	var postVars = inv.collectPostVars(eval('document.'+form));
  	var d = postJSON(url,postVars);
 	d.addCallbacks(inv.Listing_getsearch,inv.error_report);
  	return false;
}
inv.Listing_remove = function(){
	if (inv.list_dest == null) {
		swapDOM('listing_'+inv.cur_def.Name,null);
	} else {
		removeChildNodes(inv.list_dest,null);
	}
}
inv.renderListing = function(def){
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
	var HiddenEdit = function(name, data){
		var edit = createDOM('INPUT',{'type':'hidden','name':name,'id':'listing_srch_'+name, 'value':data});
	  	return edit;
	}
	inv.toggle_message("");
	var is_cur = false;
	if (def != null) {
	  	if (inv.list_dest == null) {
	  		inv.addHistory({'view':'renderListing','def':def});
	  		inv.cur_def = def;
	  		is_cur = true;
	  	} else {
	  		inv.list_def = def;
	  	}
	} else {
		def = inv.cur_def;
		is_cur = true;	
	}
	var listing = createDOM('DIV',{'class':'listing','id':'listing_'+def.Name});
  	var menubar = createDOM('DIV',{'id':'menubar','class':'yuimenubar'});
	var close_link = createDOM('A',{'href':'javascript:inv.Listing_remove()'},"Close");
	var br = createDOM('BR',null);
	var title = createDOM('H3',def.Label);
	var form = createDOM('FORM',{'onsubmit':'return false;', 'class':'tableform', 'name':'listing_form_'+def.Name, 'id':'listing_form_'+def.Name});
	var table = createDOM('TABLE',null);
	var tbody = createDOM('TBODY',null);
	for (var i=0; i<def.FieldsSrch.length; i++){
		switch(def.FieldsSrch[i].type) {
			case 'String':
				tbody.appendChild(StringEdit(def.FieldsSrch[i].name,def.FieldsSrch[i].label));
			break;
			case 'StringRO':
				tbody.appendChild(StringEdit(def.FieldsSrch[i].name,def.FieldsSrch[i].label));
			break;
			case 'MultiSelect':
				tbody.appendChild(GroupSelect(def.FieldsSrch[i]));
			break;
			case 'Hidden':
				form.appendChild(HiddenEdit(def.FieldsSrch[i].name,def.FieldsSrch[i].data));
			break;
		}
	}
	table.appendChild(tbody);
	var submit_url = 'inv.Listing_postsearch("listing_form_'+def.Name+'","'+def.SrchUrl+'")';
	var btn_row = createDOM('TR',null);
	var btn_col = createDOM('TD',{'colspan':'2'});
	var submit_btn = createDOM('BUTTON',{'name':'btnSubmit', 'value':'Search', 'type':'submit', 'onclick':submit_url}, 'Search');
	var sep = createDOM('LABEL',null,"    ");
	var clear_btn = createDOM('BUTTON',{'name':'btnClear', 'value':'Clear', 'type':'submit', 'onclick':'inv.clearAllFormFields("listing_form_'+def.Name+'")'}, 'Clear Search');
	appendChildNodes(btn_col,submit_btn,sep,clear_btn);
	btn_row.appendChild(btn_col);
	tbody.appendChild(btn_row);
	table.appendChild(tbody);
	form.appendChild(table);
	listing.appendChild(menubar);
	listing.appendChild(close_link);
	listing.appendChild(br);
	listing.appendChild(title);
	listing.appendChild(br);
	listing.appendChild(form);
	var list_result = createDOM('DIV',{'id':'listing_result_'+def.Name});
	listing.appendChild(list_result);
	if (inv.list_dest == null) {
		inv.displayObj(listing);
	} else {
		swapDOM(inv.list_dest,listing);
	}
	inv.ObjMenuBar(def);
	inv.Listing_postsearch('listing_form_'+def.Name, def.SrchUrl);
}

inv.pickList_move = function(elemid){
	var def = inv.list_def;
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
inv.pickList_getData = function(data){
	inv.toggle_message("");
	var def = inv.list_def;
	var results = getElement('pick_list_res_'+def.Name);
	for(var i = 0; i < data.results.length;i++){
		var chkbox = createDOM('INPUT',{'name':'row_select', 'type':'checkbox', 'checked':'checked', 'onclick':'inv.pickList_move("pick_list_row_data_'+data.items[i].id+'")'});
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
		inv.pickList_postsearch();
	}
}

inv.pickList_getsearch = function(data){
	inv.toggle_message("");
	var def = inv.list_def;
	var results = createDOM('DIV',{'id':'pick_list_qry_result_'+def.Name});
	for(var i = 0; i < data.results.length;i++){
		var chkbox = createDOM('INPUT',{'name':'row_select', 'type':'checkbox', 'onclick':'inv.pickList_move("pick_list_row_'+data.items[i].id+'")'});
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
		inv.merge_hidden_inputs(rows[i]);
	}
}
inv.pickList_postList = function(url,url_vars){
	var def = inv.list_def;
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
	inv.toggle_message("Loading...");
	//alert(data);
	if (def.NoAjax == true){
 		location = url+'?data='+data;
 		//location.eval(url+'?data='+data);
 	} else {
		if (url_vars != '') {
		  	var d = postJSON(url,url_vars+'&data='+data);
		} else {
			var d = postJSON(url,'data='+data);
		}
 		d.addCallbacks(inv.updated,inv.error_report);
	 	inv.pickList_remove();
	  	return false;	
 	}
}
inv.pickList_postdata = function(){
	var def = inv.list_def;
	if (def.DataUrl != ''){
		var url = def.DataUrl;
		inv.toggle_message("Loading...");
	  	var d = postJSON(url,'id='+def.id);
	 	d.addCallbacks(inv.pickList_getData,inv.error_report);
	} else {
		if (def.SrchNow == true){
			inv.pickList_postsearch();
		}
	}
  	return false;
}
inv.pickList_postsearch = function(){
	var def = inv.list_def;
	var url = def.SrchUrl;
	var form = 'pick_list_qry_form_'+def.Name;
	inv.toggle_message("Loading...");
  	var postVars = inv.collectPostVars(eval('document.'+form));
  	var d = postJSON(url,postVars);
 	d.addCallbacks(inv.pickList_getsearch,inv.error_report);
  	return false;
}
inv.pickList_remove = function(){
	swapDOM('pick_list_'+inv.list_def.Name,null);
	swapDOM('pick_list_shadow_'+inv.list_def.Name,null);
}
inv.pickList = function(def){
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
	inv.toggle_message("");
	inv.list_def = def;
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
	var close_link = createDOM('A',{'href':'javascript:inv.pickList_remove()'},"Close");
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
	var submit_url = 'inv.pickList_postsearch("listing_form_'+def.Name+'","'+def.SrchUrl+'")';
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
	var post_url = 'inv.pickList_postList("'+def.Url+'","'+def.UrlVars+'")';
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
	inv.pickList_postdata();
//	new Draggable('pick_list_'+def.Name);
}

inv.loadDef = function(def){
	inv.toggle_message("");
	if (def != null){
	  	inv.cur_def = def;
	}
  	inv.ObjTreeView();
}

inv.AppMenu = function(url){
	var RenderSubMenu = function(menu_item,num){
		var Menu = new YAHOO.widget.Menu("submenu_"+num);
		var menus = menu_item.menu;
	    for (var i=0;i<menus.length;i++){
	    	if (menus[i].menu == null){
	    		Menu.addItem(RenderSubMenuItem(menus[i]));
	    	} else {
	    		Menu.addItem(RenderSubMenu(menus[i],num*10+i));
	    	}
	    }
		Menu.mouseOverEvent.subscribe(inv.onSubmenuMouseOver,Menu,true);
		Menu.mouseOutEvent.subscribe(inv.onSubmenuMouseOut,Menu,true);
		inv.OverlayManager.register(Menu);
	    var MenuItem = new YAHOO.widget.MenuItem(menu_item.label, { url:menu_item.url, submenu: Menu});
		MenuItem.mouseOverEvent.subscribe(inv.onMenuBarItemMouseOver,MenuItem,true);
		MenuItem.mouseOutEvent.subscribe(inv.onMenuBarItemMouseOut,MenuItem,true);
	    return MenuItem;
	}
	var RenderSubMenuItem = function(menu_item){
		var MenuItem = new YAHOO.widget.MenuItem(menu_item.label, { url:menu_item.url});
		MenuItem.mouseOverEvent.subscribe(inv.onMenuBarItemMouseOver);
		MenuItem.mouseOutEvent.subscribe(inv.onMenuBarItemMouseOut);
		return MenuItem;
	}
	var Render = function(data){
		var menus = data.menu;
	    var Menu = new YAHOO.widget.Menu("appmenu",{ visible: true, position: "static"});
		Menu.mouseOverEvent.subscribe(inv.onMenuBarMouseOver,Menu,true);
	    for (var i=0;i<menus.length;i++){
	    	if (menus[i].menu == null){
	    		Menu.addItem(RenderSubMenuItem(menus[i]));
	    	} else {
	    		Menu.addItem(RenderSubMenu(menus[i],i));
	    	}
	    }
	    Menu.render('app_menu');
		inv.toggle_message("");
	    Menu.show();
	}
	YAHOO.util.Event.addListener(document,"mousedown",inv.onDocumentMouseDown);
	inv.toggle_message("Loading...");
  	var d = postJSON(url);
  	d.addCallbacks(Render,inv.error_report);
  	return false;	
}

// "mouseover" event handler for the root menu
inv.onMenuBarMouseOver = function(p_sType, p_aArguments, p_oMenu) {
	if(inv.g_nTimeoutId) {
		window.clearTimeout(inv.g_nTimeoutId);
	}
}
// "mouseover" event handler for each submenu
inv.onSubmenuMouseOver = function(p_sType, p_aArguments, p_oMenu) {
	if(inv.g_nTimeoutId) {
		window.clearTimeout(inv.g_nTimeoutId);
	}
}
// "mouseout" event handler for each submenu
inv.onSubmenuMouseOut = function(p_sType, p_aArguments, p_oMenu) {
	function hideMenu() {
		p_oMenu.hide();
	}
	if(inv.g_nTimeoutId) {
		window.clearTimeout(inv.g_nTimeoutId);
	}
	inv.g_nTimeoutId = window.setTimeout(hideMenu, 750);
}
// "mousedown" handler for the document
inv.onDocumentMouseDown = function(p_oEvent) {
	inv.OverlayManager.hideAll();
}
// "mouseover" handler for each item in the menu bar
inv.onMenuBarItemMouseOver = function(p_sType, p_aArguments, p_oMenu) {
	var oActiveItem = this.parent.activeItem;
	// Hide any other submenus that might be visible
	if(oActiveItem && oActiveItem != this) {
		this.parent.clearActiveItem();
	}
	// Select and focus the current MenuItem instance
	this.cfg.setProperty("selected", true);
	this.focus();
	// Show the submenu for this instance
	var oSubmenu = this.cfg.getProperty("submenu");
	if(oSubmenu) {
		oSubmenu.show();
	}
}
// "mouseout" handler for each item in the menu bar
inv.onMenuBarItemMouseOut = function(p_sType, p_aArguments, p_oMenu) {
	this.cfg.setProperty("selected", false);
	var oSubmenu = this.cfg.getProperty("submenu");
	if(oSubmenu) {
		var oDOMEvent = p_aArguments[0],
		oRelatedTarget = YAHOO.util.Event.getRelatedTarget(oDOMEvent);
		if(!(oRelatedTarget == oSubmenu.element || this._oDom.isAncestor(oSubmenu.element, oRelatedTarget))) {
			oSubmenu.hide();
		}
	}
}
inv.ObjMenuBar = function(def){
	var RenderSubMenu = function(menu_item,num){
		var Menu = new YAHOO.widget.Menu("objmenu_"+num);
		var menus = menu_item.menu;
	    for (var i=0;i<menus.length;i++){
	    	if (menus[i].menu == null){
	    		Menu.addItem(RenderSubMenuItem(menus[i]));
	    	} else {
	    		Menu.addItem(RenderSubMenu(menus[i],num*10+i));
	    	}
	    }
		Menu.mouseOverEvent.subscribe(inv.onSubmenuMouseOver,Menu,true);
		Menu.mouseOutEvent.subscribe(inv.onSubmenuMouseOut,Menu,true);
		inv.OverlayManager.register(Menu);
	    var MenuItem = new YAHOO.widget.MenuBarItem(menu_item.label, { url:menu_item.url, submenu: Menu});
		MenuItem.mouseOverEvent.subscribe(inv.onMenuBarItemMouseOver,MenuItem,true);
		MenuItem.mouseOutEvent.subscribe(inv.onMenuBarItemMouseOut,MenuItem,true);
	    return MenuItem;
	}
	var RenderSubMenuItem = function(menu_item){
		var MenuItem = new YAHOO.widget.MenuItem(menu_item.label, { url:menu_item.url});
		MenuItem.mouseOverEvent.subscribe(inv.onMenuBarItemMouseOver);
		MenuItem.mouseOutEvent.subscribe(inv.onMenuBarItemMouseOut);
		return MenuItem;
	}
	var Render = function(data){
		var menus = data.menu;
	    var Menu = new YAHOO.widget.MenuBar("objmenu");
		Menu.mouseOverEvent.subscribe(inv.onMenuBarMouseOver,Menu,true);
	    for (var i=0;i<menus.length;i++){
	    	if (menus[i].menu == null){
	    		Menu.addItem(RenderSubMenuItem(menus[i]));
	    	} else {
	    		Menu.addItem(RenderSubMenu(menus[i],i));
	    	}
	    }
	    Menu.render('menubar');
		inv.toggle_message("");
	}
	inv.toggle_message("Loading...");
  	var d = postJSON(def.MenuBar);
  	d.addCallbacks(Render,inv.error_report);
  	return false;	
}

inv.ObjTreeRemove = function(){
	setNodeAttribute("app_treeview_td","width",null);
	replaceChildNodes("app_treeview",null);
}
inv.ObjTreeView = function(){
	var RemoveTreeView = function() {
		setNodeAttribute("app_treeview_td","width",null);
		replaceChildNodes("app_treeview",null);
	}
	var MakeChildNodes = function(parent,data){
		for (var i=0;i<data.nodes.length;i++){
			var node_def = {label:data.nodes[i].label, href:data.nodes[i].href};
			var node = new YAHOO.widget.MenuNode(node_def, parent, false);
			if (data.nodes[i].nodes != null) {
				//node.labelStyle = "emLabel";
				MakeChildNodes(node,data.nodes[i]);
			} else {
				//node.labelStyle = "emLabel";//"emLabel";
			}
		}
	}
	var Render = function(data) {
		inv.toggle_message("");
		var tree = new YAHOO.widget.TreeView("app_treeview"); 
		var root = tree.getRoot();
		var close_node = new YAHOO.widget.MenuNode({label:"Close", href:"javascript:inv.ObjTreeRemove();"}, root, false);
		for (var i=0;i<data.nodes.length;i++){
			var node_def = {label:data.nodes[i].label, href:data.nodes[i].href};
			var node = new YAHOO.widget.MenuNode(node_def, root, false);
			if (data.nodes[i].nodes != null) {
				//node.labelStyle = "emLabel";
				MakeChildNodes(node,data.nodes[i]);
			} else {
				//node.labelStyle = "emLabel";
			}
		}
		tree.draw();
	}
	if (inv.cur_def.TreeView != null) {
		setNodeAttribute("app_treeview_td","width","25%");
		inv.toggle_message("Loading...");
		var d = postJSON(inv.cur_def.TreeView);
		d.addCallbacks(Render,inv.error_report);
	} else {
		RemoveTreeView();	
	}
	return false;
}
