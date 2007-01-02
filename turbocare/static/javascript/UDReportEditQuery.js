var def = {};
// variables ===================
def.g_nTimeoutId;
def.tables = null; // tables is the array of tables from the query definition

/*
	Render the query builder
	The query builder has one table entry - with columns
	and zero or more sub-table entries (each with their own columns)
*/
// The Show/Hide element (part of a column entry)
def.ElemShowHide = function() {
	return createDOM('DIV',{'class':'displayable'},"[Show/Hide]");
}
// The click and drag element (part of a column entry)
def.ElemDrag = function() {
	return createDOM('DIV',{'class':'draggable'},"[Click to drag]");
}
// The column name element (part of a column entry)
def.ElemColName = function(column) {
	return createDOM('DIV',{'style':'font-weight:bold'},column.ColName);
}
// The duplicate column element (part of a column entry)
def.ElemDuplicate = function() {
	return createDOM('DIV',null,createDOM('BUTTON',{'style':'font-size:10px','type':'button','name':'Duplicate','value':'Duplicate'},'Duplicate'));
}
// The From and To date filters (part of a column entry)
def.ElemFmToDate = function(table,column) {
	var tbl = createDOM('DIV',{'style':'display:table;text-align:left'});
	var fmRow = createDOM('DIV',{'style':'display:table-row'});
	var toRow = createDOM('DIV',{'style':'display:table-row'});
	var fmLbl = createDOM('DIV',{'style':'display:table-cell'},"Fm Date:");
	var fmData = createDOM('DIV',{'style':'display:table-cell'});
	var fmInput = createDOM('INPUT',{'class':'dateEntry','type':'text','name':'FromDate','size':'8','value':column.FromDate,'id':'FromDate'+table.TableID+column.ColName});
	fmData.appendChild(fmInput);
	appendChildNodes(fmRow,fmLbl,fmData);
	var toLbl = createDOM('DIV',{'style':'display:table-cell'},"To Date:");
	var toData = createDOM('DIV',{'style':'display:table-cell'});
	var toInput = createDOM('INPUT',{'class':'dateEntry','type':'text','name':'ToDate','size':'8','value':column.ToDate,'id':'ToDate'+table.TableID+column.ColName});
	toData.appendChild(toInput);
	appendChildNodes(toRow,toLbl,toData);
	appendChildNodes(tbl,fmRow,toRow);
	return tbl;
}
// Aggregated filter/method (part of a column entry)
def.ElemAggType = function(column) {
	var Opt = function(value,defValue) {
		if (value==defValue) {
			return null;
		} else {
			if (column.Aggregate==value) {
				return createDOM('OPTION',{'value':value,'checked':'checked'},value);
			} else {
				return createDOM('OPTION',{'value':value},value);
			}
		}
	}
	var sel = createDOM('SELECT',{'name':'Aggregate'});
	appendChildNodes(sel,Opt(column.Aggregate),Opt('Normal',column.Aggregate),
		Opt('GroupBy',column.Aggregate),Opt('Sum',column.Aggregate),Opt('Average',column.Aggregate),
		Opt('Minimum',column.Aggregate),Opt('Maximum',column.Aggregate),
		Opt('First',column.Aggregate),Opt('Last',column.Aggregate),Opt('Count',column.Aggregate));
	return createDOM('DIV',null,sel);
}
// Text field filter
def.ElemTextFilter = function(column){
	var div = createDOM('DIV',null);
	var inp = createDOM('INPUT', {'type':'text','name':'TextFilter','size':'10','value':column.TextFilter});
	appendChildNodes(div,"Filter:",inp);
	return div;
}
// Numeric field filter
def.ElemNumFilter = function(column){
	var tbl = createDOM('DIV',{'style':'display:table;text-align:left'});
	var GtRow = createDOM('DIV',{'style':'display:table-row'});
	var LtRow = createDOM('DIV',{'style':'display:table-row'});
	var GtLbl = createDOM('DIV',{'style':'display:table-cell'},"Greater than:");
	var GtData = createDOM('DIV',{'style':'display:table-cell'});
	var GtInput = createDOM('INPUT',{'type':'text','name':'GreaterThan','size':'5','value':column.GreaterThan});
	GtData.appendChild(GtInput);
	appendChildNodes(GtRow,GtLbl,GtData);
	var LtLbl = createDOM('DIV',{'style':'display:table-cell'},"Less than:");
	var LtData = createDOM('DIV',{'style':'display:table-cell'});
	var LtInput = createDOM('INPUT',{'type':'text','name':'LessThan','size':'5','value':column.LessThan});
	LtData.appendChild(LtInput);
	appendChildNodes(LtRow,LtLbl,LtData);
	appendChildNodes(tbl,GtRow,LtRow);
	return tbl;
	
}
// Boolean field filter
def.ElemBoolFilter = function(column) {
	var Opt = function(value,defVal) {
		if (value==defVal) {
			return null;
		} else {
			if (value==column.BoolFilter) {
				return createDOM('OPTION',{'value':value,'checked':'checked'},value);
			} else {
				return createDOM('OPTION',{'value':value},value);
			}
		}
	}
	var sel = createDOM('SELECT',{'name':'BoolFilter'});
	appendChildNodes(sel,Opt(column.BoolFilter),Opt('No Filter',column.BoolFilter),Opt('True',column.BoolFilter),
		Opt('False',column.BoolFilter));
	return createDOM('DIV',null,sel);	
}
// Extra filter options (NOT and Empty options)
def.ElemExtraFilter = function(column){
	var div = createDOM('DIV',null);
	if (column.NotFilter) {
		var chkNot = createDOM('INPUT', {'type':'checkbox','name':'NotFilter','value':'true', 'checked':'checked'});
	} else {
		var chkNot = createDOM('INPUT', {'type':'checkbox','name':'NotFilter','value':'true'});
	}
	if (column.NullFilter) {
		var chkNull = createDOM('INPUT', {'type':'checkbox','name':'NullFilter','value':'true', 'checked':'checked'});
	} else {
		var chkNull = createDOM('INPUT', {'type':'checkbox','name':'NullFilter','value':'true'});
	}
	appendChildNodes(div,chkNot,'Not', chkNull,'Is Empty');
	return div;
}
// Column sorting options
def.ElemSorting = function(column) {
	var Opt = function(value, defVal) {
		if (value==defVal) {
			return null;
		} else {
			if (column.Sorting==value) {
				return createDOM('OPTION',{'value':value,'checked':'checked'},value);
			} else {
				return createDOM('OPTION',{'value':value},value);
			}
		}
	}
	var sel = createDOM('SELECT',{'name':'Sorting'});
	appendChildNodes(sel,Opt(column.Sorting), Opt('No Sorting',column.Sorting),
		Opt('Ascending',column.Sorting),Opt('Descending',column.Sorting));
	return createDOM('DIV',null,sel);	
}
// Formatting, justification options (left, right or centre)
def.ElemJustification = function(column) {
	var Opt = function(value,checked) {
		if (checked) {
			return createDOM('OPTION',{'value':value,'checked':'checked'},value);
		} else {
			return createDOM('OPTION',{'value':value},value);
		}
	}
	var sel = createDOM('SELECT',{'name':'Justification'});
	if (column.Justification=='Left') {
		appendChildNodes(sel,Opt('Left',true),Opt('Right'),Opt('Centre'));
	} else if (column.Justification=='Right') {
		appendChildNodes(sel,Opt('Right',true),Opt('Left'),Opt('Centre'));
	} else {
		appendChildNodes(sel,Opt('Centre',true),Opt('Left'),Opt('Right'));
	}
	return createDOM('DIV',null,sel);	
}
// Formatting for numeric columns
def.ElemNumericFormat = function(column) {
	var Opt = function(value,defVal) {
		if (value==defVal) {
			return null;
		} else {
			if (column.NumericFormat==value) {
				return createDOM('OPTION',{'value':value,'checked':'checked'},value);
			} else {
				return createDOM('OPTION',{'value':value},value);
			}
		}
	}
	var sel = createDOM('SELECT',{'name':'NumericFormat'});
	appendChildNodes(sel,Opt(column.NumericFormat),Opt('12,34,567.12',column.NumericFormat),
		Opt('12,34,567.',column.NumericFormat),Opt('12,34 lakh',column.NumericFormat),
		Opt('12,345,678.12',column.NumericFormat),Opt('12,345,678.',column.NumericFormat),
		Opt('123.46%',column.NumericFormat),Opt('123456.',column.NumericFormat),
		Opt('123456.123456',column.NumericFormat));
	return createDOM('DIV',null,sel);	
}
// Formatting for date columns
def.ElemDateFormat = function(column) {
	var Opt = function(value,defVal) {
		if (value==defVal) {
			return null;
		} else {
			if (column.DateFormat==value) {
				return createDOM('OPTION',{'value':value,'checked':'checked'},value);
			} else {
				return createDOM('OPTION',{'value':value},value);
			}
		}
	}
	var sel = createDOM('SELECT',{'name':'DateFormat'});
	appendChildNodes(sel,Opt(column.DateFormat),Opt('YYYY-mm-dd (ISO)',column.DateFormat),
		Opt('YYYY-mm-dd HH:MM:SS (ISO)',column.DateFormat),Opt('dd/mm/YYYY',column.DateFormat),
		Opt('dd-mmm-YYYY',column.DateFormat),Opt('YYYY-mmm',column.DateFormat));
	return createDOM('DIV',null,sel);	
}
// The toggle column: used to show/hide a row of columns
def.ColRowToggle = function(table) {
	if (table.rowvisible) {
		var RowVisible = 'show-row';
	} else {
		var RowVisible = 'hide-row';
	}
	var col = createDOM('DIV',{'class':'tablecol mark-shown '+RowVisible,'style':'width:30px'});
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
def.ColLoadSubTables = function(table) {
	if (table.rowvisible) {
		var RowVisible = 'show-row';
	} else {
		var RowVisible = 'hide-row';
	}
	var col = createDOM('DIV',{'class':'tablecol mark-shown '+RowVisible,'style':'width:30px'});
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
def.ColRemoveTable = function(table) {
	if (table.rowvisible) {
		var RowVisible = 'show-row';
	} else {
		var RowVisible = 'hide-row';
	}
	var col = createDOM('DIV',{'class':'tablecol mark-shown '+RowVisible,'style':'width:30px'});
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
def.ColDateTime = function(table,column){
	if (column.colvisible) {
		var ColVisible = 'mark-shown';
	} else {
		var ColVisible = 'mark-hidden';
	}
	if (column.rowvisible) {
		var RowVisible = 'show-row';
	} else {
		var RowVisible = 'hide-row';
	}
	var col = createDOM('DIV',{'class':'tablecol '+ColVisible+' '+RowVisible,'id':table.TableID+'.'+column.ColName});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':column.ColName});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'DateTime'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':table.TableName});
	appendChildNodes(col,name,type,table,def.ElemShowHide(),def.ElemDrag(),def.ElemColName(column),
		def.ElemFmToDate(table,column),def.ElemExtraFilter(column),def.ElemAggType(column),def.ElemSorting(column),
		def.ElemDateFormat(column),def.ElemJustification(column),def.ElemDuplicate());
	return col;
}
// Text column
def.ColText = function(table,column){
	if (column.colvisible) {
		var ColVisible = 'mark-shown';
	} else {
		var ColVisible = 'mark-hidden';
	}
	if (column.rowvisible) {
		var RowVisible = 'show-row';
	} else {
		var RowVisible = 'hide-row';
	}
	var col = createDOM('DIV',{'class':'tablecol '+ColVisible+' '+RowVisible,'id':table.TableID+'.'+column.ColName});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':column.ColName});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'Text'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':table.TableName});
	appendChildNodes(col,name,table,type,def.ElemShowHide(),def.ElemDrag(),def.ElemColName(column),
		def.ElemTextFilter(column),def.ElemExtraFilter(column),def.ElemAggType(column),def.ElemSorting(column),
		def.ElemJustification(column),def.ElemDuplicate());
	return col;
}
// Numeric column
def.ColNumeric = function(table,column){
	if (column.colvisible) {
		var ColVisible = 'mark-shown';
	} else {
		var ColVisible = 'mark-hidden';
	}
	if (column.rowvisible) {
		var RowVisible = 'show-row';
	} else {
		var RowVisible = 'hide-row';
	}
	var col = createDOM('DIV',{'class':'tablecol '+ColVisible+' '+RowVisible,'id':table.TableID+'.'+column.ColName});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':column.ColName});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'Numeric'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':table.TableName});
	appendChildNodes(col,name,table,type,def.ElemShowHide(),def.ElemDrag(),def.ElemColName(column),
		def.ElemNumFilter(column),def.ElemExtraFilter(column),def.ElemAggType(column),
		def.ElemSorting(column),def.ElemNumericFormat(column),def.ElemJustification(column),def.ElemDuplicate());
	return col;
}
// Boolean column
def.ColBoolean = function(table,column){
	if (column.colvisible) {
		var ColVisible = 'mark-shown';
	} else {
		var ColVisible = 'mark-hidden';
	}
	if (column.rowvisible) {
		var RowVisible = 'show-row';
	} else {
		var RowVisible = 'hide-row';
	}
	var col = createDOM('DIV',{'class':'tablecol '+ColVisible+' '+RowVisible,'id':table.TableID+'.'+column.ColName});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':column.ColName});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'Boolean'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':table.TableName});
	appendChildNodes(col,name,table,type,def.ElemShowHide(),def.ElemDrag(),def.ElemColName(column),
		def.ElemBoolFilter(column),def.ElemExtraFilter(column),def.ElemAggType(column),
		def.ElemSorting(column),def.ElemJustification(column),def.ElemDuplicate());
	return col;
}
// Foreign Key column (these columns have no filtering enabled)
def.ColFK = function(table,column){
	if (column.colvisible) {
		var ColVisible = 'mark-shown';
	} else {
		var ColVisible = 'mark-hidden';
	}
	if (column.rowvisible) {
		var RowVisible = 'show-row';
	} else {
		var RowVisible = 'hide-row';
	}
	var col = createDOM('DIV',{'class':'tablecol '+ColVisible+' '+RowVisible,'id':table.TableID+'.'+column.ColName});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':column.ColName});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'ForeignKey'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':table.TableName});
	appendChildNodes(col,name,table,type,def.ElemShowHide(),def.ElemDrag(),def.ElemColName(column),
		def.ElemAggType(column),def.ElemSorting(column),def.ElemJustification(column),
		def.ElemNumericFormat(column),def.ElemDateFormat(column),def.ElemDuplicate());
	return col;
}
// Function column (these columns have no filtering enabled)
def.ColFunction = function(table,column){
	if (column.colvisible) {
		var ColVisible = 'mark-shown';
	} else {
		var ColVisible = 'mark-hidden';
	}
	if (column.rowvisible) {
		var RowVisible = 'show-row';
	} else {
		var RowVisible = 'hide-row';
	}
	var col = createDOM('DIV',{'class':'tablecol '+ColVisible+' '+RowVisible,'id':table.TableID+'.'+column.ColName});
	var name = createDOM('INPUT',{'type':'hidden','name':'ColName','value':column.ColName});
	var type = createDOM('INPUT',{'type':'hidden','name':'ColType','value':'Function'});
	var table = createDOM('INPUT',{'type':'hidden','name':'TableName','value':table.TableName});
	appendChildNodes(col,name,table,type,def.ElemShowHide(),def.ElemDrag(),def.ElemColName(column),
		def.ElemAggType(column),def.ElemSorting(column),def.ElemJustification(column),
		def.ElemNumericFormat(column),def.ElemDateFormat(column),def.ElemDuplicate());
	return col;
}
/*
	A row entry for a table item (either the main table or a sub table)
	Index: 	Index for the table in def.tables
	issub: 	boolean value - True means the table is a sub-table 
			(which has a show/hide option), otherwise, it is a main table
*/
def.RowTbl = function(Index,issub) {
	var tdef = def.tables[Index];
	var tablename = tdef.TableName;
	var cols = tdef.Columns;
	var tableid = tdef.TableID;
	// Display name
	if (issub) {
		if (tdef.JoinType == 'RelatedJoin') {
			var displayname = tdef.JoinName + ' ['+tdef.TableName+']';
		} else {
			var displayname = tdef.JoinName + ' ['+tdef.TableName+'.'+tdef.LinkColumn+']';
		}
	} else {
		var displayname = tdef.TableName;
	}
	//DOM stuff from here on in
	var qdef = createDOM('DIV',{'id':tableid,'class':'QryMkrTbl'});
	var tgrp = createDOM('DIV',{'class':'tablegroup'},displayname);
	qdef.appendChild(tgrp);
	if (tdef.rowvisible) {
		var tbl = createDOM('DIV',{'class':'tableitem show-row','id':'qdef'+tablename+count});
	} else {
		var tbl = createDOM('DIV',{'class':'tableitem hide-row','id':'qdef'+tablename+count});
	}
	appendChildNodes(tgrp,tbl);
	// Create the columns
	if (issub) {
		tbl.appendChild(def.ColRowToggle(tdef));
		tbl.appendChild(def.ColLoadSubTables(tdef));
		tbl.appendChild(def.ColRemoveTable(tdef));
	}
	for (var i=0;i<cols.length;i++) {
		if (cols[i].ColType == 'Text') {
			tbl.appendChild(def.ColText(tdef,cols[i]));
		} else if (cols[i].ColType == 'Numeric') {
			tbl.appendChild(def.ColNumeric(tdef,cols[i]));
		} else if (cols[i].ColType == 'DateTime') {
			tbl.appendChild(def.ColDateTime(tdef,cols[i]));
		} else if (cols[i].ColType == 'Boolean') {
			tbl.appendChild(def.ColBoolean(tdef,cols[i]));
		} else if (cols[i].ColType == 'ForeignKey') {
			tbl.appendChild(def.ColFK(tdef,cols[i]));
		} else if (cols[i].ColType == 'Function') {
			tbl.appendChild(def.ColFunction(tdef,cols[i]));
		}
	}
	tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'TableID','value':tdef.TableID}));
	tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'ParentTableID','value':tdef.ParentTableID}));
	if (tdef.TableName!=null) {
		tbl.appendChild(createDOM('INPUT',{'type':'hidden','name':'TableName','value':tdef.TableName}));
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
def.SubTable = function(Index) {
	// Create main sub table. 
	var tItem = createDOM('DIV',{'style':'display:table-row'});//The item we return
	var tGrp = createDOM('DIV',{'class':'tablegroup'});
	tItem.appendChild(tGrp);
	var mTbl = def.RowTbl(Index,true);
	var sTbls = def.GetSTIndexArray(def.tables[Index].TableID);
	// Create sub-sub tables
	for (var j=0;j<sTbls.length;j++) {
		mTbl.appendChild(def.SubTable(sTbls[j]));
	}
	tGrp.appendChild(mTbl);
	return tItem;
}
/*
	RenderQueryEditor: Rebuild the query definition for editing
*/
def.RenderQueryEditor = function(data){
	// Create main table. NOTE there should already be a "QueryDefinition" element on the template
	var qdef = getElement('QueryDefinition');
	//Do this next step to help with memory
	replaceChildNodes(qdef,null);
	// Remove any pre-existing table definitions
	if (data!=null && data.QD!=null) {
		def.tables = data.QD.Tables;
		// Find our master table index (most times, it'll be 0)
		var MT = def.GetMTIndex();
		var mTbl = def.RowTbl(MT,false);
		var sTbls = def.GetSTIndexArray(def.tables[MT].TableID);
		// Create sub tables
		for (var i=0;i<sTbls.length;i++) {
			mTbl.appendChild(def.SubTable(sTbls[i]));
		}
		swapDOM(qdef,mTbl);
		//The first render doesn't work, so a re-render is needed
		qry.toggle_message("Displaying Query Builder...");
		var d = callLater(1,qry.RedisplayTables);
	}
}
// Get the Master table from the definition
def.GetMTIndex = function() {
	for (var i=0; i<def.tables.length; i++) {
		if (def.tables[i].ParentTableID=='') {
			return i;
		}
	}
	return -1;
}

// Get Sub-Tables
def.GetSTIndexArray = function(TableID) {
	var ST = new Array();
	var Count = 0;
	for (var i=0; i<def.tables.length; i++) {
		if (def.tables[i].ParentTableID==TableID) {
			 ST[Count] = i;
			 Count++;
		}
	}
	return ST;
}
