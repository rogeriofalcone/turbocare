//AJAX Post function
function postJSON(url, postVars) {
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

var qry = {};


// variables ===================
qry.g_nTimeoutId;
qry.TableDiv = ''; //Use this to track which DIV we need to update later with LoadSubTables
qry.tcount = 0; //The current table count (to create unique ids)
// utility functions ===========

/*
	When someone enters an age, modify the DateBirth
	entry to match the age to the date.
*/
qry.AgePickUpdate = function(dom_obj){
	var Age = getElement('Age').value;
	if (Age == '') {
		return false;
	} else if (isNaN(Age)){
		getElement('Age').value = '';
	} else if (Age != qry.Age) {
		var Today = new Date();
		var DateBirth = new Date(Today.getFullYear() - Age, Today.getMonth(), Today.getDate());
		getElement('DateBirth').value = toISODate(DateBirth);
		qry.Age = Age;
		qry.DateBirth = toISODate(DateBirth);
	}
}
/*
	Open a date entry javascript box
*/
qry.DatePick = function(dom_obj){
	if ((dom_obj.type() == 'click') || (dom_obj.type()=='keydown' && (dom_obj.key()['string']=='KEY_ARROW_DOWN'))) {
//		if (dom_obj.type() == 'keydown') {
//			dom_obj.stop();
//		}
		Widget.pickDateTime(dom_obj.src().id);
	}
}
/*
	When a date has been entered, update
	the age box
*/
qry.DatePickUpdate = function(dom_obj){
	var DateBirth = isoDate((getElement("DateBirth").value).slice(0,10));
	getElement('DateBirth').value = toISODate(DateBirth);
	if (getElement('DateBirth').value != qry.DateBirth) {
		var Today = new Date();
		var diff = Today.getTime() - DateBirth.getTime();
		getElement('Age').value = parseInt((diff + 43200000)/(31557600000));
		qry.Age = getElement('Age').value;
		qry.DateBirth = toISODate(DateBirth);
	}
}
/*
	Collect variables from the form "f" (element node)
	make a postable query string
*/
qry.collectPostVars = function(f){
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
      	postVars+= f.elements[i].name +'='+ qry.multiselect_csv(f.elements[i].id);
      } else {
      	postVars+= f.elements[i].name +'='+ f.elements[i].options[f.elements[i].selectedIndex].value;
      }
    }
  }
  return postVars;
}

/*
	returns the PostVars for a select item
	a good way of testing if something has been selected.
*/
qry.checkSelect = function(elem) {
	var select = getElement(elem);
	var t = select.type;
	var postVars = '';
	if (t.indexOf('select') > -1){
		if (getNodeAttribute(select,'multiple') != null) {
			postVars+= select.name +'='+ qry.multiselect_csv(select.id);
		} else {
			postVars+= select.name +'='+ select.options[select.selectedIndex].value;
		}		
	}
	return postVars;
}

/*
	Scans over a multi-select list and puts the values in a csv
	NOTE: if you're getting errors, it couls be because the 
	Select list doesn't have an "id" attribute!
*/
qry.multiselect_csv = function(element_id){
	if (getElement(element_id) != null) {
		var nodes = getElement(element_id).childNodes;
		var csv = '';
		for (var i=0;i<nodes.length;i++){
			if (nodes[i].selected){
				csv += nodes[i].value +',';
			}
		}
		csv = csv.slice(0,csv.length-1);
		return csv;
	} else {
		return '';
	}
}
/*
	ChangeGroup: Create a query object, then serialize it into JSON format
	to transmit to the app server and save it to a file for future use
*/
qry.ChangeGroup = function(e) {
	var Group = getElement('Group').value;
	if (Group!='') {
		qry.toggle_message("Loading...");
		var postVars = 'Group='+Group;
		var d = postJSON('LoadReportList',postVars);
		d.addCallbacks(qry.UpdateReportList,qry.error_report);
	}
}
/*
	UpdateReportList: Update the report listing for a group
*/
qry.UpdateReportList = function(d) {
	qry.toggle_message("");
	var ReportFile = getElement('ReportFile');
	replaceChildNodes(ReportFile, null);
	for (var i=0; i<d.reports.length; i++) {
		ReportFile.appendChild(createDOM('OPTION',{'value':d.reports[i]},d.reports[i]));
	}
}
/*
	EditReport: Create a query object, then serialize it into JSON format
	to transmit to the app server and save it to a file for future use
*/
qry.EditReport = function(e) {
	var Group = getElement('Group').value;
	var ReportFile = getElement('ReportFile').value;
	if (Group!=''&&ReportFile!='') {
		qry.toggle_message("Loading...");
		var postVars = 'Group='+Group+'&ReportFile='+ReportFile;
		var d = postJSON('LoadSavedQuery',postVars);
		d.addCallbacks(def.RenderQueryEditor,qry.error_report);
	}
}

/*
	Collect Query Variables:  Scan the DOM tree starting at id="QueryDefinition"
	for the desired query definition (tables, columns, filters, grouping, sorting, etc...)
*/
/*
	ParseColumn: Parse the information in a column box into an object
	el: 	The element which is the column (class=tablecol), 
*/
qry.ParseColumn = function(el){
	var obj = new Object(); // Create a new object to attach the column properties to
	// For every input in the column, create an object attribute
	var Inputs = getElementsByTagAndClassName('INPUT',null,el);
	for (var i=0;i<Inputs.length;i++) {
		if (Inputs[i].type=='checkbox') {
			obj[Inputs[i].name] = (Inputs[i].checked==true);
		} else {
			obj[Inputs[i].name] = Inputs[i].value;
		}
	}
	// For every select in the column, create an object attribute (note, only single selects are allowed)
	var Selects = getElementsByTagAndClassName('SELECT',null,el);
	for (var i=0;i<Selects.length;i++) {
		obj[Selects[i].name] = Selects[i].value;
	}
	// Check the class to see if the column is visible
	if (hasElementClass(el,"mark-hidden")) {
		obj.colvisible = false;
	} else {
		obj.colvisible = true;
	}
	// Check the class to see if the row is visible
	if (hasElementClass(el,"hide-row")) {
		obj.rowvisible = false;
	} else {
		obj.rowvisible = true;
	}
	return obj;
}
/*
	ParseTable: Parse the information in a table box into an object.
	el: 	The element which is the table (class=tableitem), 
*/
qry.ParseTable = function(el){
	var obj = new Object(); // Create a new object to attach the column properties to
	// For every input on the table, create an object attribute.  Make sure that the input is a direct child of the table.
	var Inputs = getElementsByTagAndClassName('INPUT',null,el);
	for (var i=0;i<Inputs.length;i++) {
		if (el.id == Inputs[i].parentNode.id) { //Make sure the node is a child node and not a child child node
			obj[Inputs[i].name] = Inputs[i].value;
		}
	}
	// Append the columns of the table as an array of objects
	var cols = new Array();
	var columns = getElementsByTagAndClassName('DIV','tablecol',el);
	for (var i=0;i<columns.length;i++) {
		cols[i] = qry.ParseColumn(columns[i]);
	}
	obj.Columns = cols;
	// Check the class to see if the row is visible
	if (hasElementClass(el,"hide-row")) {
		obj.rowvisible = false;
	} else {
		obj.rowvisible = true;
	}
	return obj;
}
/*
	ParseQuery: Parse the information in the query section into an object.
	el: 	The element which is the query DIV
	The query is an array of table query definitions
*/
qry.ParseQuery = function(el){
	var obj = new Object();
	var tbls = new Array();
	var tables = getElementsByTagAndClassName('DIV','tableitem',el);
	for (var i=0;i<tables.length;i++) {
		tbls[i] = qry.ParseTable(tables[i]);
	}
	obj.Tables = tbls;
	return obj;
}
/*
	SerializeQuery: Create a query object, then serialize it into JSON format
	to transmit to the app server and process it as a query
*/
qry.SerializeQuery = function() {
	qry.toggle_message("Running Query...");
	var QD = getElement("QueryDefinition");
	var query = qry.ParseQuery(QD);
	var data = serializeJSON(query);
	var postVars = 'Query='+data;
	var d = postJSON('ExecuteQuery',postVars);
	d.addCallbacks(rr.Render,qry.error_report);
}
/*
	SaveReport: Create a query object, then serialize it into JSON format
	to transmit to the app server and save it to a file for future use
*/
qry.SaveReport = function() {
	var ReportName = getElement('ReportName').value;
	if (ReportName==''||ReportName==null) {
		alert('You need to give the report a name');
		getElement('ReportName').focus();
	} else {
		qry.toggle_message("Saving Query...");
		var QD = getElement("QueryDefinition");
		var query = qry.ParseQuery(QD);
		var data = serializeJSON(query);
		var postVars = 'Query='+data+'&ReportName='+ReportName;
		var d = postJSON('SaveQuery',postVars);
		d.addCallbacks(qry.IsSaved,qry.error_report);
	}
}
/*
	IsSaved: Call back for SaveReport.  Informs the user on
	the status of the saving of the report definition
*/
qry.IsSaved = function(d) {
	qry.toggle_message("");
	alert(d.message);
}
// AJSON reactions ==================
qry.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	qry.toggle_message("");
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
qry.error_report = function(data){
	qry.toggle_message("ERROR");
	var d = callLater(5,qry.toggle_message);
}

qry.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

qry.merge_hidden_inputs = function(parentid){
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
// Show/Hide the query definition section
qry.ToggleQueryDefinition = function(){
	var elem = getElement('QueryDefinition');
	if (elem.style.display != 'none') {
		elem.style.display = 'none';
	} else {
		elem.style.display = 'block';
		qry.toggle_message("Re-displaying Query...");
		var d = callLater(1,qry.RedisplayTables);
	}
	//toggleElementClass(elem,'invisible');
}
// AJSON actions ====================

/*
	When the user selects a table from the list, then we
	send a request to load the definition.  Later, we render
	it.
*/
qry.SelectTable = function(dom_obj){
	var table = getElement('TableName').value;
	qry.toggle_message("Loading...");
	var postVars = 'tablename='+table;
	var d = postJSON('GetTableDefinition',postVars);
	d.addCallbacks(qry.RenderQueryBuilder,qry.error_report);
}
/*
	LoadSubTables: Load multijoin or related join tables
	beneath the current table.
*/
qry.LoadSubTables = function(dom_obj){
	// This many (4) parent nodes to get to the insertion point for this table
	var table = dom_obj.src().parentNode.parentNode.parentNode.parentNode;
	qry.TableDiv = table;
	var d = getElementsByTagAndClassName('INPUT', null,table);
	for (var i=0; i<d.length;i++){
		if (d[i].name == 'TableName') {
			var tablename = d[i].value;
			break;
		}
	}
	qry.toggle_message("Loading sub tables...");
	var postVars = 'tablename='+tablename;
	var d = postJSON('GetSubTables',postVars);
	d.addCallbacks(qry.RenderSubTables,qry.error_report);
}
/*
	RemoveTable: Remove the table from the query screen (and all sub-tables)
*/
qry.RemoveTable = function(dom_obj){
	dom_obj.stop();
	var ok = confirm('Are you sure you want to remove the table (and sub-tables)?');
	if (ok) {
		// This many (6) parent nodes to get to the very top of the insertion point
		var table = dom_obj.src().parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
		swapDOM(table,null);
	}
}

/*
	AJSON Reactions to the above actions
*/


/*
	Render the query builder
	The query builder has one table entry - with columns
	and zero or more sub-table entries (each with their own columns)
*/
// The Show/Hide element (part of a column entry)
qry.ElemShowHide = function() {
	return createDOM('DIV',{'class':'displayable'},"[Show/Hide]");
}
// The click and drag element (part of a column entry)
qry.ElemDrag = function() {
	return createDOM('DIV',{'class':'draggable'},"[Click to drag]");
}
// The column name element (part of a column entry)
qry.ElemColName = function(name) {
	return createDOM('DIV',{'style':'font-weight:bold'},name);
}
// The From and To date filters (part of a column entry)
qry.ElemFmToDate = function(tablename,colname) {
	var tbl = createDOM('DIV',{'style':'display:table;text-align:left'});
	var fmRow = createDOM('DIV',{'style':'display:table-row'});
	var toRow = createDOM('DIV',{'style':'display:table-row'});
	var fmLbl = createDOM('DIV',{'style':'display:table-cell'},"Fm Date:");
	var fmData = createDOM('DIV',{'style':'display:table-cell'});
	var fmInput = createDOM('INPUT',{'class':'dateEntry','type':'text','name':'FromDate','size':'8','value':'','id':'FromDate'+tablename+colname});
	fmData.appendChild(fmInput);
	appendChildNodes(fmRow,fmLbl,fmData);
	var toLbl = createDOM('DIV',{'style':'display:table-cell'},"To Date:");
	var toData = createDOM('DIV',{'style':'display:table-cell'});
	var toInput = createDOM('INPUT',{'class':'dateEntry','type':'text','name':'ToDate','size':'8','value':'','id':'ToDate'+tablename+colname});
	toData.appendChild(toInput);
	appendChildNodes(toRow,toLbl,toData);
	appendChildNodes(tbl,fmRow,toRow);
	return tbl;
}
// Aggregated filter/method (part of a column entry)
qry.ElemAggType = function() {
	var Opt = function(value) {
		return createDOM('OPTION',{'value':value},value);
	}
	var sel = createDOM('SELECT',{'name':'Aggregate'});
	appendChildNodes(sel,Opt('Normal'),Opt('GroupBy'),Opt('Sum'),Opt('Average'),Opt('Minimum'),Opt('Maximum'),
		Opt('First'),Opt('Last'),Opt('Count'));
	return createDOM('DIV',null,sel);
}
// Text field filter
qry.ElemTextFilter = function(){
	var div = createDOM('DIV',null);
	var inp = createDOM('INPUT', {'type':'text','name':'TextFilter','size':'10','value':''});
	appendChildNodes(div,"Filter:",inp);
	return div;
}
// Numeric field filter
qry.ElemNumFilter = function(){
	var tbl = createDOM('DIV',{'style':'display:table;text-align:left'});
	var GtRow = createDOM('DIV',{'style':'display:table-row'});
	var LtRow = createDOM('DIV',{'style':'display:table-row'});
	var GtLbl = createDOM('DIV',{'style':'display:table-cell'},"Greater than:");
	var GtData = createDOM('DIV',{'style':'display:table-cell'});
	var GtInput = createDOM('INPUT',{'type':'text','name':'GreaterThan','size':'5','value':''});
	GtData.appendChild(GtInput);
	appendChildNodes(GtRow,GtLbl,GtData);
	var LtLbl = createDOM('DIV',{'style':'display:table-cell'},"Less than:");
	var LtData = createDOM('DIV',{'style':'display:table-cell'});
	var LtInput = createDOM('INPUT',{'type':'text','name':'LessThan','size':'5','value':''});
	LtData.appendChild(LtInput);
	appendChildNodes(LtRow,LtLbl,LtData);
	appendChildNodes(tbl,GtRow,LtRow);
	return tbl;
	
}
// Boolean field filter
qry.ElemBoolFilter = function() {
	var Opt = function(value,checked) {
		if (checked) {
			return createDOM('OPTION',{'value':value,'checked':'checked'},value);
		} else {
			return createDOM('OPTION',{'value':value},value);
		}
	}
	var sel = createDOM('SELECT',{'name':'BoolFilter'});
	appendChildNodes(sel,Opt('No Filter',true),Opt('True'),Opt('False'));
	return createDOM('DIV',null,sel);	
}
// Extra filter options (NOT and Empty options)
qry.ElemExtraFilter = function(){
	var div = createDOM('DIV',null);
	var chkNot = createDOM('INPUT', {'type':'checkbox','name':'NotFilter','value':'true'});
	var chkNull = createDOM('INPUT', {'type':'checkbox','name':'NullFilter','value':'true'});
	appendChildNodes(div,chkNot,'Not', chkNull,'Is Empty');
	return div;
}
// Column sorting options
qry.ElemSorting = function() {
	var Opt = function(value,checked) {
		if (checked) {
			return createDOM('OPTION',{'value':value,'checked':'checked'},value);
		} else {
			return createDOM('OPTION',{'value':value},value);
		}
	}
	var sel = createDOM('SELECT',{'name':'Sorting'});
	appendChildNodes(sel,Opt('No Sorting',true),Opt('Ascending'),Opt('Descending'));
	return createDOM('DIV',null,sel);	
}
// Formatting, justification options (left, right or centre)
qry.ElemJustification = function(just) {
	var Opt = function(value,checked) {
		if (checked) {
			return createDOM('OPTION',{'value':value,'checked':'checked'},value);
		} else {
			return createDOM('OPTION',{'value':value},value);
		}
	}
	var sel = createDOM('SELECT',{'name':'Justification'});
	if (just=='Left') {
		appendChildNodes(sel,Opt('Left',true),Opt('Right'),Opt('Centre'));
	} else if (just=='Right') {
		appendChildNodes(sel,Opt('Right',true),Opt('Left'),Opt('Centre'));
	} else {
		appendChildNodes(sel,Opt('Centre',true),Opt('Left'),Opt('Right'));
	}
	return createDOM('DIV',null,sel);	
}
// Formatting for numeric columns
qry.ElemNumericFormat = function() {
	var Opt = function(value,checked) {
		if (checked) {
			return createDOM('OPTION',{'value':value,'checked':'checked'},value);
		} else {
			return createDOM('OPTION',{'value':value},value);
		}
	}
	var sel = createDOM('SELECT',{'name':'NumericFormat'});
	appendChildNodes(sel,Opt('12,34,567.12',true),Opt('12,34,567.'),Opt('12,34 lakh'),Opt('12,345,678.12'),
		Opt('12,345,678.'),Opt('123.46%'),Opt('123456.'),Opt('123456.123456'));
	return createDOM('DIV',null,sel);	
}
// Formatting for date columns
qry.ElemDateFormat = function() {
	var Opt = function(value,checked) {
		if (checked) {
			return createDOM('OPTION',{'value':value,'checked':'checked'},value);
		} else {
			return createDOM('OPTION',{'value':value},value);
		}
	}
	var sel = createDOM('SELECT',{'name':'DateFormat'});
	appendChildNodes(sel,Opt('YYYY-mm-dd (ISO)',true),Opt('YYYY-mm-dd HH:MM:SS (ISO)'),Opt('dd/mm/YYYY'),Opt('dd-mmm-YYYY'),Opt('YYYY-mmm'));
	return createDOM('DIV',null,sel);	
}
// The toggle column: used to show/hide a row of columns
qry.ColRowToggle = function() {
	var col = createDOM('DIV',{'class':'tablecol mark-shown show-row','style':'width:30px'});
	var row = createDOM('DIV',{'class':'rowdisplay'});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'RowDisplay'});
	appendChildNodes(row,DIV(null,'S'),DIV(null,'H'),DIV(null,'W'),DIV(null,'---'),DIV(null,'H'),DIV(null,'I'),DIV(null,'D'));
	// The following code is not used for anything, but I couldn't get the page to render correctly without it... so it's filler
	var sel = createDOM('SELECT',null);
	appendChildNodes(sel,OPTION(null,'ONE'),OPTION(null,'TWO'));
	var opts = LI({'style':'display:none'},sel);
	appendChildNodes(col,type,row,opts);
	return col;
}
// Load sub-tables for the current table
qry.ColLoadSubTables = function() {
	var col = createDOM('DIV',{'class':'tablecol mark-shown show-row','style':'width:30px'});
	var row = createDOM('DIV',{'class':'loadsubtables'});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'LoadSubTables'});
	appendChildNodes(row,DIV(null,'L'),DIV(null,'O'),DIV(null,'A'),DIV(null,'D'),DIV(null,'--'),DIV(null,'S'),DIV(null,'B'));
	// The following code is not used for anything, but I couldn't get the page to render correctly without it... so it's filler
	var sel = createDOM('SELECT',null);
	appendChildNodes(sel,OPTION(null,'ONE'),OPTION(null,'TWO'));
	var opts = LI({'style':'display:none'},sel);
	appendChildNodes(col,type,row,opts);
	return col;
}
// Remove the table and all sub-tables from the page
qry.ColRemoveTable = function() {
	var col = createDOM('DIV',{'class':'tablecol mark-shown show-row','style':'width:30px'});
	var row = createDOM('DIV',{'class':'removetable'});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'RemoveTable'});
	appendChildNodes(row,DIV(null,'R'),DIV(null,'E'),DIV(null,'M'),DIV(null,'O'),DIV(null,'V'),DIV(null,'E'));
	// The following code is not used for anything, but I couldn't get the page to render correctly without it... so it's filler
	var sel = createDOM('SELECT',null);
	appendChildNodes(sel,OPTION(null,'ONE'),OPTION(null,'TWO'));
	var opts = LI({'style':'display:none'},sel);
	appendChildNodes(col,type,row,opts);
	return col;
}
// Date/time column
qry.ColDateTime = function(tablename,colname,count){
	var col = createDOM('DIV',{'class':'tablecol mark-shown show-row','id':tablename+'.'+colname+count});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':colname});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'DateTime'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':tablename});
	appendChildNodes(col,name,type,table,qry.ElemShowHide(),qry.ElemDrag(),qry.ElemColName(colname),
		qry.ElemFmToDate(tablename,colname),qry.ElemExtraFilter(),qry.ElemAggType(),qry.ElemSorting(),
		qry.ElemDateFormat(),qry.ElemJustification('Left'));
	return col;
}
// Text column
qry.ColText = function(tablename,colname,count){
	var col = createDOM('DIV',{'class':'tablecol mark-shown show-row','id':tablename+'.'+colname+count});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':colname});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'Text'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':tablename});
	appendChildNodes(col,name,table,type,qry.ElemShowHide(),qry.ElemDrag(),qry.ElemColName(colname),
		qry.ElemTextFilter(),qry.ElemExtraFilter(),qry.ElemAggType(),qry.ElemSorting(),qry.ElemJustification('Left'));
	return col;
}
// Numeric column
qry.ColNumeric = function(tablename,colname,count){
	var col = createDOM('DIV',{'class':'tablecol mark-shown show-row','id':tablename+'.'+colname+count});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':colname});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'Numeric'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':tablename});
	appendChildNodes(col,name,table,type,qry.ElemShowHide(),qry.ElemDrag(),qry.ElemColName(colname),
		qry.ElemNumFilter(),qry.ElemExtraFilter(),qry.ElemAggType(),qry.ElemSorting(),qry.ElemNumericFormat(),
		qry.ElemJustification('Right'));
	return col;
}
// Boolean column
qry.ColBoolean = function(tablename,colname,count){
	var col = createDOM('DIV',{'class':'tablecol mark-shown show-row','id':tablename+'.'+colname+count});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':colname});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'Boolean'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':tablename});
	appendChildNodes(col,name,table,type,qry.ElemShowHide(),qry.ElemDrag(),qry.ElemColName(colname),
		qry.ElemBoolFilter(),qry.ElemExtraFilter(),qry.ElemAggType(),qry.ElemSorting(),qry.ElemJustification('Right'));
	return col;
}
// Foreign Key column (these columns have no filtering enabled)
qry.ColFK = function(tablename,colname,count){
	var col = createDOM('DIV',{'class':'tablecol mark-shown show-row','id':tablename+'.'+colname+count});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':colname});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'ForeignKey'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':tablename});
	appendChildNodes(col,name,table,type,qry.ElemShowHide(),qry.ElemDrag(),qry.ElemColName(colname),
		qry.ElemAggType(),qry.ElemSorting(),qry.ElemJustification('Left'),qry.ElemNumericFormat(),qry.ElemDateFormat());
	return col;
}
// Function column (these columns have no filtering enabled)
qry.ColFunction = function(tablename,colname,count){
	var col = createDOM('DIV',{'class':'tablecol mark-shown show-row','id':tablename+'.'+colname+count});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':colname});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'Function'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':tablename});
	appendChildNodes(col,name,table,type,qry.ElemShowHide(),qry.ElemDrag(),qry.ElemColName(colname),
		qry.ElemAggType(),qry.ElemSorting(),qry.ElemJustification('Left'),qry.ElemNumericFormat(),qry.ElemDateFormat());
	return col;
}
/*
	A row entry for a table item (either the main table or a sub table)
	tdef: 	table definition object
	issub: 	boolean value - True means the table is a sub-table 
			(which has a show/hide option), otherwise, it is a main table
	count:	The table number (needed for multiple tables)
*/
qry.RowTbl = function(tdef,issub, parentid) {
	var tablename = tdef.TableName;
	var cols = tdef.Cols;
	if (parentid!=null&&issub) {
		var tableid = parentid+'QD'+tablename+qry.tcount;
	} else {
		var tableid = 'QueryDefinition';
	}
	// Display name
	if ((tdef.LinkColumn!=null)&& (tdef.AltName != null) && (tdef.JoinName!=null) && (tdef.JoinType!=null)) {
		if (tdef.JoinType == 'RelatedJoin') {
			var displayname = tdef.AltName + ' ['+tablename+']';
		} else {
			var displayname = tdef.AltName + ' ['+tablename+'.'+tdef.LinkColumn+']';
		}
	} else {
		var displayname = tablename;
	}
	//DOM stuff from here on in
	var qdef = createDOM('DIV',{'id':tableid,'class':'QryMkrTbl'});
	var tgrp = createDOM('DIV',{'class':'tablegroup'},displayname);
	qdef.appendChild(tgrp);
	var tbl = createDOM('DIV',{'class':'tableitem show-row','id':'qdef'+tablename+count});
	appendChildNodes(tgrp,tbl);
	// Create the columns
	if (issub) {
		tbl.appendChild(qry.ColRowToggle());
		tbl.appendChild(qry.ColLoadSubTables());
		tbl.appendChild(qry.ColRemoveTable());
	}
	for (var i=0;i<cols.length;i++) {
		if (cols[i].Type == 'Text') {
			tbl.appendChild(qry.ColText(tablename,cols[i].Name,count));
		} else if (cols[i].Type == 'Numeric') {
			tbl.appendChild(qry.ColNumeric(tablename,cols[i].Name,count));
		} else if (cols[i].Type == 'DateTime') {
			tbl.appendChild(qry.ColDateTime(tablename,cols[i].Name,count));
		} else if (cols[i].Type == 'Boolean') {
			tbl.appendChild(qry.ColBoolean(tablename,cols[i].Name,count));
		} else if (cols[i].Type == 'ForeignKey') {
			tbl.appendChild(qry.ColFK(tablename,cols[i].Name,count));
		} else if (cols[i].Type == 'Function') {
			tbl.appendChild(qry.ColFunction(tablename,cols[i].Name,count));
		}
	}
	tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'TableID','value':tableid}));
	tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'ParentTableID','value':parentid}));
	if (tablename!=null) {
		tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'TableName','value':tablename}));
	}
	if (tdef.ParentTable!=null) {
		tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'ParentTable','value':tdef.ParentTable}));
	}
	if (tdef.LinkColumn!=null) {
		tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'LinkColumn','value':tdef.LinkColumn}));
	}
	if (tdef.JoinType!=null) {
		tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'JoinType','value':tdef.JoinType}));
	}
	if (tdef.JoinName!=null) {
		tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'JoinName','value':tdef.JoinName}));
	}
	return qdef;
}
/*
	SubTable: Render any sub tables or sub-sub tables, etc...
*/
qry.SubTable = function(data, parentid) {
	// Create main sub table. 
	var tItem = createDOM('DIV',{'style':'display:table-row'});//The item we return
	var tGrp = createDOM('DIV',{'class':'tablegroup'});
	tItem.appendChild(tGrp);
	var mTbl = qry.RowTbl(data.TableDef,true, parentid);
	var sTbls = data.SubTables;
	// Create sub-sub tables
	var num = sTbls.length;
	for (var j=0;j<sTbls.length;j++) {
		mTbl.appendChild(qry.SubTable(sTbls[j],mTbl.id));
	}
	tGrp.appendChild(mTbl);
	return tItem;
}
/*
	RenderQueryBuilder: The all important query builder DOM code
*/
qry.RenderQueryBuilder = function(data){
	// Rendering takes a long time on occasion, so change our label
	qry.toggle_message('Rendering (this can take a long time)...');
	// Create main table. NOTE there should already be a "QueryDefinition" element on the template
	var qdef = getElement('QueryDefinition');
	qry.tcount = 0;
	//Do this next step to help with memory
	replaceChildNodes(qdef,null);
	// Remove any pre-existing table definitions
	if (data!=null && data.TableDef!=null) {
		var mTbl = qry.RowTbl(data.TableDef,false,null);
		var sTbls = data.SubTables;
		// Create sub tables
		//alert(sTbls.length);
		for (var i=0;i<sTbls.length;i++) {
			mTbl.appendChild(qry.SubTable(sTbls[i],mTbl.id));
		}
		swapDOM(qdef,mTbl);
		//The first render doesn't work, so a re-render is needed
		qry.toggle_message("Displaying Query Builder...");
		var d = callLater(1,qry.RedisplayTables);
	}
}
/*
	RenderSubTables: When a user wants to view the sub-tables of a table
	they select the table.  This function will render the sub-tables at the
	appropriate element.
*/
qry.RenderSubTables = function(data) {
	// Rendering takes a long time on occasion, so change our label
	qry.toggle_message('Rendering (this can take a long time)...');
	// Our sub-table location is saved in the qry.TableDiv variable
	var cTbl = qry.TableDiv; //current table
	// Remove any existing child tables (if we're reloading them)
	var removesubtable = getElementsByTagAndClassName('DIV',"removetable",cTbl);
	for (var i=0;i<removesubtable.length; i++){
		if (removesubtable[i].parentNode.parentNode.parentNode.parentNode.id!=cTbl.id) {
			var table = removesubtable[i].parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
			swapDOM(table,null);
		}
	}
	if (data!=null && data.SubTables!=null) {
		var sTbls = data.SubTables;
		// Create sub tables
		for (var i=0;i<sTbls.length;i++) {
			cTbl.appendChild(qry.SubTable(sTbls[i],cTbl.id));
		}
		//The first render doesn't work, so a re-render is needed
		qry.RedisplayTables(cTbl);
	}
	qry.toggle_message('');
}
// Call the RedisplayTables function with a message indicating what is being done
qry.CallRedisplayTables = function() {
	qry.toggle_message("Re-displaying Query Builder...");
	var d = callLater(1,qry.RedisplayTables);
}
/*
	RedisplayTables: Attempts to fix any bugs with the display or 
	events on the tables due to javascript or DOM quircks.
	It seems that Firefox 3 doesn't require the mandatory redisplay.
	You can edit the code appropriately to remove this.  NOTE: you'll
	need to attach the events at another location if you remove this.
*/
qry.RedisplayTables = function(el){
	if (el==null) {
		el = document;
	}
	var parents = getElementsByTagAndClassName('DIV', 'tableitem',el);
	//var num = parents.length;
	for (var j=0; j<parents.length; j++){
		//qry.toggle_message('Redrawing table ' + j + ' of ' + num);
	       var d = getElementsByTagAndClassName('DIV', 'draggable',parents[j]);
	       var clones = new Array(d.length);
		for (var i=0;i<d.length;i++){
			var clone = d[i].parentNode.cloneNode(true);
			clones[i] = clone;
		}
		// Clone the non-draggable items
		var FirstClones = new Array();
		var d = getElementsByTagAndClassName('DIV', 'rowdisplay',parents[j]);
		for (var i=0;i<d.length;i++){
			var clone = d[i].parentNode.cloneNode(true);
			FirstClones[i] = clone;
		}
		var SecondClones = new Array();
		var d1 = getElementsByTagAndClassName('DIV', 'loadsubtables',parents[j]);
		for (var i=0;i<d1.length;i++){
			var clone = d1[i].parentNode.cloneNode(true);
			SecondClones[i] = clone;
		}
		var ThirdClones = new Array();
		var d1 = getElementsByTagAndClassName('DIV', 'removetable',parents[j]);
		for (var i=0;i<d1.length;i++){
			var clone = d1[i].parentNode.cloneNode(true);
			ThirdClones[i] = clone;
		}
		// Clone all the inputs for the table item
		var InputClones = new Array();
		var Inputs = getElementsByTagAndClassName('INPUT',null,parents[j]);
		var inputcount = 0;
		for (var i=0;i<Inputs.length;i++) {
			if (parents[j].id == Inputs[i].parentNode.id) { //Make sure the node is a child node and not a child child node
				var clone = Inputs[i].cloneNode(true);
				InputClones[inputcount] = clone;
				inputcount++;
			}
		}
		// Replace all the draggable items
		replaceChildNodes(parents[j],null);
		// Re-Add non draggable items
		for (var i=0;i<FirstClones.length;i++){
			parents[j].appendChild(FirstClones[i]);
		}	
		for (var i=0;i<SecondClones.length;i++){
			parents[j].appendChild(SecondClones[i]);
		}	
		for (var i=0;i<ThirdClones.length;i++){
			parents[j].appendChild(ThirdClones[i]);
		}	
		// Re-Add draggable items
		for (var i=0;i<clones.length;i++){
			parents[j].appendChild(clones[i]);
		}
		// Re-Add input items
		for (var i=0;i<InputClones.length;i++){
			parents[j].appendChild(InputClones[i]);
		}
		
		// reconnect the drag event
	       var d = getElementsByTagAndClassName('DIV', 'draggable',parents[j]);
	       for (var i=0;i<d.length;i++){
			connect(d[i], 'onmousedown', Drag.start);
		}
		//  reconnect the column display event
		var d = getElementsByTagAndClassName('DIV', 'displayable',parents[j]);
		forEach(d,
		    function(elem) {
			connect(elem, 'onclick', ColDisplay.toggle);
		    });
		//  reconnect the row display event
		var d = getElementsByTagAndClassName('DIV', 'rowdisplay',parents[j]);
		forEach(d,
		    function(elem) {
			connect(elem, 'onclick', RowDisplay.toggle);
		    });
		var dateInputs = getElementsByTagAndClassName('INPUT',"dateEntry",parents[j]);
		for (var i=0;i<dateInputs.length; i++){
			connect(dateInputs[i],"onclick",qry.DatePick);
			connect(dateInputs[i],"onkeydown",qry.DatePick);
			connect(dateInputs[i],"onblur",validate.DateValidate);
		}
		var loadsubtables = getElementsByTagAndClassName('DIV',"loadsubtables",parents[j]);
		for (i=0;i<loadsubtables.length; i++){
			connect(loadsubtables[i],"onclick",qry.LoadSubTables);
		}
		var removetable = getElementsByTagAndClassName('DIV',"removetable",parents[j]);
		for (i=0;i<removetable.length; i++){
			connect(removetable[i],"onclick",qry.RemoveTable);
		}
	}
	qry.toggle_message('Ready');
	var d = callLater(1,qry.toggle_message);
	
}
//Configure our events using the Mochikit signal library
/*
	Initial event configuration
*/
qry.OpenOnLoad = function() {
	//We have some inputs with the  dateEntry class which want to have a date control added
	connect("Group","onclick",qry.ChangeGroup);
	connect("ReportFile","ondblclick",qry.EditReport);
	var dateInputs = getElementsByTagAndClassName('INPUT',"dateEntry",document);
	for (i=0;i<dateInputs.length; i++){
		connect(dateInputs[i],"onclick",qry.DatePick);
		connect(dateInputs[i],"onkeydown",qry.DatePick);
	}
}
//Connect our buttons/fields to events -- need to do this on document load
connect(window, 'onload', function(){
		if (getElement("TableName")!=null){
			connect("TableName",'onchange',qry.SelectTable);
		}
});
//Connect on onload for the document to open the document using javascript
connect(window, 'onload', qry.OpenOnLoad);
