//AJAX Post function
function postJSON(url, postVars) {
	config.toggle_message("Sending request...");
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

var config = {};
config.ClassEdit = false; // If we've edited the classification name, then set this true
config.TypeEdit = false; // If we've edited the type name, then set this true
config.classifications = null; // The object which contains the classifications.  Initialized only after first AJAX operation
config.ethnicorigtypes = null; // The object which contains the types.  Initialized only after first AJAX operation
// The following vars are used for Cancel operations
config.TypeName = null;
config.TypeID = null;
config.ClassName = null;
config.ClassID = null;
config.TypeDeleted = null;
config.ClassDeleted = null;

config.collectPostVars = function(f){
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
      	postVars+= f.elements[i].name +'='+ config.multiselect_csv(f.elements[i].id);
      } else {
      	postVars+= f.elements[i].name +'='+ f.elements[i].options[f.elements[i].selectedIndex].value;
      }
    }
  }
  return postVars;
}

config.multiselect_csv = function(element_id){
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

config.clearAllFormFields = function(parentid){
	elems = getElementsByTagAndClassName('input',null,parentid);
	for (var i=0;i<elems.length;i++){
		elems[i].value = "";
	}
}

// AJSON reactions ==================
config.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	config.toggle_message("");
	if (data.message != null) {
		var display = createDOM('DIV',{'class':'displaymsg','id':'last_result_msg'},data.message);
		if (getNodeAttribute('last_result_msg','class') == null){
			document.body.appendChild(display);
		} else {
			swapDOM(field.id,display);
		}
	}
	var d = callLater(5,remove_message);
}
config.error_report = function(data){
	config.toggle_message("ERROR (Authentication, Network connection, or Server Error)");
	var d = callLater(8,config.toggle_message);
}

config.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

config.merge_hidden_inputs = function(parentid){
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
/*
	PickClassification: Choose a new classification
*/
config.PickClassification = function(e){
	var doPick = true;
	if (config.ClassEdit||config.TypeEdit) {
		if (!confirm('Some changes are un-saved, do you want to proceed?')) {
			doPick = false;
		}
	}
	if (doPick) {
		var el = e.target();
		if (el.value!=null) {
			config.toggle_message('Loading...');
			config.ClassID = el.value;
			config.ClassName = scrapeText(el);
			getElement('EditClassificationName').value = config.ClassName;
			getElement('EditClassificationID').value = config.ClassID;
			var d = postJSON('EthnicOriginsEditorSelectClass','ClassID='+config.ClassID);
			d.addCallbacks(config.RenderForms,config.error_report);
		}
	}
}
/*
	CancelClass: Cancel any changes to the object
*/
config.CancelClass = function(e){
	var Cancel = function() {
		getElement('EditClassificationName').value = config.ClassName;
		getElement('EditClassificationID').value = config.ClassID;			
		getElement('EditTypeName').value = config.TypeName;
		getElement('EditTypeID').value = config.TypeID;			
		// Re-render the types list
		var select = getElement('EthnicOrigType');
		replaceChildNodes(select,null); // clear the select list
		// populate the select list
		forEach(config.ethnicorigtypes,function(type) {
			if (type.selected!=null) {
				select.appendChild(OPTION({'value':type.id,'selected':'selected'},type.name));
			} else {
				select.appendChild(OPTION({'value':type.id},type.name));
			}
		});
		config.ClassEdit = false;
		config.TypeEdit = false;
	}
	if (config.ClassEdit||config.TypeEdit) {
		if (confirm('Are you sure you want to cancel the changes?')) {
			Cancel();
		}
	} else {
		Cancel();
	}
	config.EditClassLabel();
	config.EditTypeLabel();
}
/*
	AddNewClass: Create a new blank entry for saving
*/
config.AddNewClass = function(e){
	var AddNew = function() {
		getElement('EditClassificationName').value = '';
		getElement('EditClassificationID').value = '';			
		getElement('EditTypeName').value = '';
		getElement('EditTypeID').value = '';			
		// remove the types list
		var select = getElement('EthnicOrigType');
		replaceChildNodes(select,null); // clear the select list
		config.ClassEdit = false;
		config.TypeEdit = false;
		getElement('EditClassificationName').focus();
	}
	if (config.ClassEdit||config.TypeEdit) {
		if (confirm('Some changes are un-saved, do you want to proceed?')) {
			AddNew();
		}
	} else {
		AddNew();
	}
	config.EditClassLabel();
	config.EditTypeLabel();
}
/*
	DeleteClass: Attempt to delete the currently selected item
*/
config.DeleteClass = function(e){
	var ClassID = getElement('EditClassificationID').value;
	if (ClassID!='') {
		if (confirm('Are you sure you want to delete?')) {
			var d = postJSON('EthnicOriginsEditorSaveClass','Operation=Delete&ClassID='+ClassID);
			d.addCallbacks(config.RenderForms,config.error_report);
		}
	}
}
/*
	UnDeleteClass: Attempt to un-delete the currently selected item
*/
config.UnDeleteClass = function(e){
	var ClassID = getElement('EditClassificationID').value;
	if (ClassID!='') {
		var d = postJSON('EthnicOriginsEditorSaveClass','Operation=Un-Delete&ClassID='+ClassID);
		d.addCallbacks(config.RenderForms,config.error_report);
	}
}
/*
	SaveClass: Attempt to update/create the item
*/
config.SaveClass = function(e){
	var ClassID = getElement('EditClassificationID').value;
	var ClassName = getElement('EditClassificationName').value;
	var d = postJSON('EthnicOriginsEditorSaveClass','Operation=Save&ClassID='+ClassID+'&ClassName='+ClassName);
	d.addCallbacks(config.RenderForms,config.error_report);
}
// Types Events
/*
	PickEthnicOrigType: Choose a new type
*/
config.PickEthnicOrigType = function(e){
	var doPick = true;
	if (config.TypeEdit) {
		if (!confirm('Some changes are un-saved, do you want to proceed?')) {
			doPick = false;
		}
	}
	if (doPick) {
		var el = e.target();
		if (el.value!=null) {
			config.TypeID = el.value;
			config.TypeName = scrapeText(el);
			getElement('EditTypeName').value = config.TypeName;
			getElement('EditTypeID').value = config.TypeID;
			config.TypeEdit = false;
		}
	}
	config.EditTypeLabel();
}
/*
	CancelType: Cancel any changes to the object
*/
config.CancelType = function(e){
	var Cancel = function(){
		getElement('EditTypeName').value = config.TypeName;
		getElement('EditTypeID').value = config.TypeID;			
		config.TypeEdit = false;
	}
	if (config.TypeEdit) {
		if (confirm('Are you sure you want to cancel the changes?')) {
			Cancel();
		}
	} else {
		Cancel();
	}
	config.EditTypeLabel();
}
/*
	AddNewType: Create a new blank entry for saving
*/
config.AddNewType = function(e){
	var AddNew = function() {
		getElement('EditTypeName').value = '';
		getElement('EditTypeID').value = '';			
		config.ClassEdit = false;
		getElement('EditTypeName').focus();
	}
	if (config.TypeEdit) {
		if (confirm('Some changes are un-saved, do you want to proceed?')) {
			AddNew();
		}
	} else {
		AddNew();
	}
	config.EditTypeLabel();
}
/*
	DeleteType: Attempt to delete the currently selected item
*/
config.DeleteType = function(e){
	var ClassID = getElement('EditClassificationID').value;
	var TypeID = getElement('EditTypeID').value;
	if (TypeID!='') {
		if (confirm('Are you sure you want to delete?')) {
			var d = postJSON('EthnicOriginsEditorSaveType','Operation=Delete&ClassID='+ClassID+'&TypeID='+TypeID);
			d.addCallbacks(config.RenderForms,config.error_report);
		}
	}
}
/*
	UnDeleteType: Attempt to un-delete the currently selected item
*/
config.UnDeleteType = function(e){
	var ClassID = getElement('EditClassificationID').value;
	var TypeID = getElement('EditTypeID').value;
	if (TypeID!='') {
		var d = postJSON('EthnicOriginsEditorSaveType','Operation=Un-Delete&ClassID='+ClassID+'&TypeID='+TypeID);
		d.addCallbacks(config.RenderForms,config.error_report);
	}
}
/*
	SaveType: Attempt to update/create the item
*/
config.SaveType = function(e){
	var ClassID = getElement('EditClassificationID').value;
	var TypeID = getElement('EditTypeID').value;
	var TypeName = getElement('EditTypeName').value;
	if (ClassID!='') {
		var d = postJSON('EthnicOriginsEditorSaveType','Operation=Save&ClassID='+ClassID+'&TypeName='+TypeName+'&TypeID='+TypeID);
		d.addCallbacks(config.RenderForms,config.error_report);
	}
}
/*
	RenderForms: Display the results of our action
*/
config.RenderForms = function(d){
	// Display any result message, or at least remove any existing message.
	if (d.message!=null) {
		config.toggle_message(d.message);
		var msg = callLater(8,config.toggle_message);
	} else {config.toggle_message('');}
	// Re-render the classifications list
	if (d.classifications!=null) {
		config.classifications = d.classifications;
		var select = getElement('Classification');
		replaceChildNodes(select,null); // clear the select list
		// populate the select list
		forEach(config.classifications,function(classif) {
			if (classif.selected!=null) {
				select.appendChild(OPTION({'value':classif.id,'selected':'selected'},classif.name));
			} else {
				select.appendChild(OPTION({'value':classif.id},classif.name));
			}
		});
	}
	// Re-render the types list
	if (d.ethnicorigtypes!=null) {
		config.ethnicorigtypes = d.ethnicorigtypes;
		var select = getElement('EthnicOrigType');
		replaceChildNodes(select,null); // clear the select list
		// populate the select list
		forEach(config.ethnicorigtypes,function(type) {
			if (type.selected!=null) {
				select.appendChild(OPTION({'value':type.id,'selected':'selected'},type.name));
			} else {
				select.appendChild(OPTION({'value':type.id},type.name));
			}
		});
	}
	// Selected Classification
	if (d.EditClassName!=null) {
		config.ClassName = d.EditClassName;
		getElement('EditClassificationName').value = config.ClassName;
		config.ClassEdit = false;
	}
	if (d.EditClassID!=null) {
		config.ClassID = d.EditClassID;
		getElement('EditClassificationID').value = config.ClassID;		
		config.ClassEdit = false;
	}
	// Selected type
	if (d.EditTypeName!=null) {
		config.TypeName = d.EditTypeName;
		getElement('EditTypeName').value = config.TypeName;
		config.TypeEdit = false;
	}
	if (d.EditTypeID!=null) {
		config.TypeID = d.EditTypeID;
		getElement('EditTypeID').value = config.TypeID;		
		config.TypeEdit = false;
	}
	config.EditClassLabel();
	config.EditTypeLabel();
}
/*
	EditClassLabel: Set the label to show if the class is in edit mode or create new mode
*/
config.EditClassLabel = function() {
	var el = getElement('ClassEditLabel');
	if (getElement('EditClassificationID').value=='') {
		replaceChildNodes(el,'Selected Classification (New Entry)');
	} else {
		replaceChildNodes(el,'Selected Classification (Edit Mode)');
	}
}
/*
	EditTypeLabel: Set the label to show if the type is in edit mode or create new mode
*/
config.EditTypeLabel = function() {
	var el = getElement('TypeEditLabel');
	if (getElement('EditTypeID').value=='') {
		replaceChildNodes(el,'Selected Type (New Entry)');
	} else {
		replaceChildNodes(el,'Selected Type (Edit Mode)');
	}
}
/*
	Set the focus on the classification name field
*/
config.OpenOnLoad = function() {
	connect('Classification','onclick',config.PickClassification);
	connect('btnSaveClass','onclick',function(e) { signal(document,'SaveClass'); });
	connect('btnCancelClass','onclick',config.CancelClass);
	connect('btnAddNewClass','onclick',config.AddNewClass);
	connect('btnDeleteClass','onclick',config.DeleteClass);
	connect('btnUnDeleteClass','onclick',config.UnDeleteClass);
	connect('EditClassificationName','onkeydown',function(e) {
		if (e.key()['string']=='KEY_ENTER') {
			e.stop();
			signal(document,'SaveClass');
		} else if (!config.ClassEdit) {
			config.ClassEdit = true;
		}
		});
	connect(document,'SaveClass',config.SaveClass);
	//===================
	connect('EthnicOrigType','onclick',config.PickEthnicOrigType);
	connect('btnSaveType','onclick',function(e) { signal(document,'SaveType'); });
	connect('btnCancelType','onclick',config.CancelType);
	connect('btnAddNewType','onclick',config.AddNewType);
	connect('btnDeleteType','onclick',config.DeleteType);
	connect('btnUnDeleteType','onclick',config.UnDeleteType);
	connect('EditTypeName','onkeydown',function(e) {
		if (e.key()['string']=='KEY_ENTER') {
			e.stop();
			signal(document,'SaveType');
		} else if (!config.TypeEdit) {
			config.TypeEdit = true;
		}
		});
	connect(document,'SaveType',config.SaveType);
	// Initialize our variables
	config.TypeName = getElement('EditTypeName').value;
	config.TypeID = getElement('EditTypeID').value;
	config.ClassName = getElement('EditClassificationName').value;
	config.ClassID = getElement('EditClassificationID').value;
	config.TypeDeleted = getElement('btnUnDeleteType').style.display == 'none';
	config.ClassDeleted = getElement('btnUnDeleteClass').style.display == 'none';
	if (getElement('EditClassificationName')!=null) {
		getElement('EditClassificationName').focus();
	}
}


//Connect on onload for the document to open the document using javascript
connect(window, 'onload', config.OpenOnLoad);