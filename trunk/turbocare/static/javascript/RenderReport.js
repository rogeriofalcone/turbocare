rr = {}

rr.Dfn = null;
rr.Data = null;
rr.NumericFmt = '12,34,567.12'; //default numeric format (changes to the very first number format in the definition)
rr.isDefaultSet = false; //checks to see if the above default is set
rr.PrintPreviewWindow = null;
// Show/hide a message for the user
rr.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}
/*
	HideDetails & ShowDetails:
	Show/Hide All Report detail sections
*/
rr.HideDetails = function() {
	var rows = getElementsByTagAndClassName('DIV','rowdisplay','RenderReport');
	for (var i=0; i<rows.length;i++) {
		var el = rows[i];
		var tbl = el.nextSibling;
		while (!hasElementClass(tbl,'tDetail')){
			tbl = tbl.nextSibling;
		}
		if (!hasElementClass(tbl,'invisible')) {
			addElementClass(tbl,'invisible');
		}
	}
}
rr.ShowDetails = function() {
	var rows = getElementsByTagAndClassName('DIV','rowdisplay','RenderReport');
	for (var i=0; i<rows.length;i++) {
		var el = rows[i];
		var tbl = el.nextSibling;
		while (!hasElementClass(tbl,'tDetail')){
			tbl = tbl.nextSibling;
		}
		if (hasElementClass(tbl,'invisible')) {
			removeElementClass(tbl,'invisible');
		}
	}
}
/*
	RemoveHiddenSections: Upon request, remove any hidden sections from DOM
*/
rr.RemoveHiddenSections = function() {
	var rows = getElementsByTagAndClassName('DIV','rowdisplay','RenderReport');
	for (var i=0; i<rows.length;i++) {
		var el = rows[i];
		var tbl = el.nextSibling;
		while (!hasElementClass(tbl,'tDetail')){
			tbl = tbl.nextSibling;
		}
		if (hasElementClass(tbl,'invisible')) {
			swapDOM(tbl.previousSibling,null);
			swapDOM(tbl,null);
			//removeElementClass(tbl,'invisible');
		}
	}
}
/*
	Render: Call RenderReport (I use this to force the displaying of a message)
	RenderReport: Render the report
	d: the ajson object which is returned
	d.Data and d.Dfn
	
	The function requires a DIV labelled with the id="RenderReport" to place the report
	results there.
	If the d object is null, but we already have a definition and data, then re-render that
*/
rr.Render = function(d){
	rr.toggle_message('Rendering Report...');
	if (d!=null) {
		rr.Dfn = d.Dfn;
		rr.Data = d.Data;
	}
	if (rr.Data!=null) {
		var RenderFlat = getElement('RenderFlat');
		if (RenderFlat==null) {
			var d = callLater(1,rr.RenderReport);
		} else {
			//alert(RenderFlat.checked);
			if (RenderFlat.checked == true) {
				var d = callLater(1,rr.RenderFlatReport);
			} else {
				var d = callLater(1,rr.RenderReport);
			}
		}
	} else {
		rr.toggle_message('');
	}
}
rr.RenderReport = function() {
	// Grab our render location
	var el = getElement('RenderReport');
	// Initialize our report DOM
	replaceChildNodes(el,null);
	if (rr.Data.length > 1) {
		// Render the lines of data
		var i = rr.RenderSubTable(0,el);
		if (i < rr.Data.length) {
			alert('ooops, did not render all the lines?');
		}
	}
	rr.toggle_message('');
}
/*
	RenderSubTable: The sub table is a detail section in the master-detail report
	i - The index of the line of data for the first line of data for the detail (the report will go until the Total line is reached)
	el - The colgroup to append the sub-table to (or whatever element (DIV) in the case of the first row)
	Returns: i - the index value for the last row of the sub table
*/
rr.RenderSubTable = function(i,el){
	var TableID = rr.Data[i][0];
	var TD = rr.GetTD(TableID);
	var colCount = rr.Data[i].length - 5;
	var showTable = TD.rowvisible;
	if (showTable) {
		// Create a DIV to toggle between show/hide
		var toggle = createDOM('DIV',{'style':'font-size:14px', 'class':'rowdisplay'},'[show/hide]   '+TD.TableName);
		connect(toggle,'onclick',rr.ToggleTable);
		el.appendChild(toggle);
		// Create the table
		var t = createDOM('TABLE',{'border':'0','class':'tDetail'});
		var b = createDOM('TBODY',null);
		el.appendChild(t);
		t.appendChild(b);
		// Create the titles row
 		var title = createDOM('TR',{'class':'trTitle'});
		for (var j=0;j<TD.Columns.length;j++){
			//alert(TD.Columns[j].ColName);
			if (TD.Columns[j].colvisible&&((TD.Columns[j].ColType!='RowDisplay')&&(TD.Columns[j].ColType!='LoadSubTables')&&(TD.Columns[j].ColType!='RemoveTable'))) {
				var td = createDOM('TD',{'class':'tdTitle'});
				appendChildNodes(td,TD.Columns[j].ColName);
				title.appendChild(td);
			}
		}
		b.appendChild(title);
	}
	// Create the data rows
	var finished = false;
	// Loop through until we reach the "Total" row for this TableID
	while (!finished) {
		var curTableID = rr.Data[i][0];
		var RowType = rr.Data[i][2];
		// First check if the row belongs to a new sub-detail section
		if (curTableID!=TableID) {
			if (showTable) {
				var tr = createDOM('TR',null);
				var tdspan = createDOM('TD',{'colspan':colCount});
				b.appendChild(tr);
				tr.appendChild(tdspan);
				i = rr.RenderSubTable(i,tdspan);
			} else {
				i = rr.RenderSubTable(i,el);
			}
		// Second, check if the row is a data row
		} else if (RowType=='Data') {
			if (showTable) {
				b.appendChild(rr.RenderRowData(rr.Data[i],TD,false));
			}
			i++;
		// Finally, check if the row is a Total row, the last row in this detail section
		} else if (RowType=='Total') {
			if (showTable) {
				b.appendChild(rr.RenderRowTotal(rr.Data[i],TD, true));
			}
			i++;
			finished = true;
		}
	}
	return i;
}
/*
	RenderRowData: display all the columns of the row properly formatted
	row - the row of data (excluding the 3 information columns at the start and 2 at the end
	TD - The table definition (which contains the column information for formatting)
	PrePendCols - In a flat table layout, these are the columns of data to render before our data
*/
rr.RenderRowData = function(row, TD, isTotal,PrePendCols){
	var tr = createDOM('TR',{'class':'trData'});
	// Prepend any parent table columns (the clones of them)
	if (PrePendCols!=null) {
		for (var i=0;i<PrePendCols.length;i++){
			tr.appendChild(PrePendCols[i].cloneNode(true));
		}
	}
	// The first 3 columns are information about the row
	// The last two columns are related to the primary key
	for (var i=3;i<row.length-2;i++){
		var CD = rr.GetCD(TD,i);
		var coldata = row[i];
		if (CD.ColType=='Numeric') {
			coldata = rr.NumericCol(coldata,CD.NumericFormat);
		} else if (CD.ColType=='DateTime') {
			coldata = rr.DateTimeCol(coldata,CD.DateFormat);
		} else if ((CD.ColType=='ForeignKey'||CD.ColType=='Function')&&(!isNaN(coldata))) {
			coldata = rr.NumericCol(coldata,CD.NumericFormat);
		}
		var col = createDOM('TD',{'class':'tdData'},coldata)
		if (CD.Justification=='Left') {
			addElementClass(col,'leftjust');
		} else if (CD.Justification=='Right') {
			addElementClass(col,'rightjust');
		} else {
			addElementClass(col,'centrejust');
		}
		tr.appendChild(col);
	}
	return tr;
}
// format date/time data
rr.MonthNames = new Array('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
rr.DateTimeCol = function(data,fmt) {
	var d = isoTimestamp(data);
	if (fmt=='YYYY-mm-dd (ISO)') {
		return toISODate(d);
	} else if (fmt=='YYYY-mm-dd HH:MM:SS (ISO)') {
		return toISOTimestamp(d);
	} else if (fmt=='dd/mm/YYYY') {
		return d.getDate()+'/'+d.getMonth()+'/'+d.getFullYear();
	} else if (fmt=='dd-mmm-YYYY') {
		return d.getDate()+'/'+rr.MonthNames[d.getMonth()-1]+'/'+d.getFullYear();
	} else if (fmt=='YYYY-mmm') {
		return d.getFullYear()+'-'+rr.MonthNames[d.getMonth()-1];
	}
}
// format a number (too bad Mochikit doesn't do exactly what i need for all things)

rr.NumericCol = function(data,fmt) {
	if (!rr.isDefaultSet) {
		rr.NumericFmt = fmt;
		rr.isDefaultSet = true;
	}
	if (fmt=='12,34,567.12') {
		var d = numberFormatter('#.00')(parseFloat(data));
		var dec = d.slice(d.indexOf('.')+1);
		var intgr = d.slice(0,d.indexOf('.'));
		var len = intgr.length;
		var res = '';
		for (i=0;i<intgr.length;i++) {
			if ((i==3||i==5||i==7||i==9||i==11||i==13||i==15||i==17||i==19||i==21)&&(intgr[len-i-1]!='-')) {
				res = ','+res;
			}
			res = intgr[len-i-1] + res;
		}
		return res+'.'+dec;
	} else if (fmt=='12,34 lakh') {
		var d = numberFormatter('#.00')(parseFloat(data)/100000);
		var dec = d.slice(d.indexOf('.')+1);
		var intgr = d.slice(0,d.indexOf('.'));
		var len = intgr.length;
		var res = '';
		for (i=0;i<intgr.length;i++) {
			if ((i==2||i==4||i==6||i==8||i==10||i==12||i==14||i==16||i==18||i==20)&&(intgr[len-i-1]!='-')) {
				res = ','+res;
			}
			res = intgr[len-i-1] + res;
		}
		return res+' lakh';
	} else if (fmt=='12,34,567.') {
		var d = numberFormatter('#.00')(parseFloat(data));
		var intgr = d.slice(0,d.indexOf('.'));
		var len = intgr.length;
		var res = '';
		for (i=0;i<intgr.length;i++) {
			if ((i==3||i==5||i==7||i==9||i==11||i==13||i==15||i==17||i==19||i==21)&&(intgr[len-i-1]!='-')) {
				res = ','+res;
			}
			res = intgr[len-i-1] + res;
		}
		return res;
	} else if (fmt=='12,345,678.12') {
		return numberFormatter('###,###.00')(parseFloat(data));
	} else if (fmt=='12,345,678.') {
		return numberFormatter('###,###.')(parseFloat(data));
	} else if (fmt=='123.46%') {
		return percentFormat(parseFloat(data));
	} else if (fmt=='123%') {
		return numberFormatter('###,###%')(parseFloat(data));
	} else if (fmt=='123456.') {
		return numberFormatter('#.')(parseFloat(data));
	} else if (fmt=='123456.123456') {
		return numberFormatter('#.#')(parseFloat(data));
	}
}
// Render one row of data
rr.RenderRowTotal = function(row,TD){
	var tr = createDOM('TR',{'class':'trTotal'});
	// The first 3 columns are information about the row
	// The last two columns are related to the primary key
	for (var i=3;i<row.length-1;i++){
		var CD = rr.GetCD(TD,i);
		var coldata = row[i];
		if (CD.ColType=='Numeric') {
			coldata = rr.NumericCol(coldata,CD.NumericFormat);
		} else if (!isNaN(coldata)) {
			coldata = rr.NumericCol(coldata,rr.NumericFmt);
		}
		var col = createDOM('TD',{'class':'tdTotal'},coldata)
		if (CD.Justification=='Left') {
			addElementClass(col,'leftjust');
		} else if (CD.Justification=='Right') {
			addElementClass(col,'rightjust');
		} else {
			addElementClass(col,'centrejust');
		}
		tr.appendChild(col);
	}
	return tr;
}
// Find the Table Definition for a specified TableID
rr.GetTD = function(TableID) {
	for (var i=0;i<rr.Dfn.Tables.length;i++) {
		if (rr.Dfn.Tables[i].TableID == TableID) {
			return rr.Dfn.Tables[i];
		}
	}
}
/*
	GetCD: return the column definition object
	TD: The table definition that contains the column
	colnum: The column number with respect to the data
*/
rr.GetCD = function(TD,colnum){
	colnum = colnum - 3; //Adjust the colnum to match the columns definition
	var i = 0;
	for (var j=0;j<TD.Columns.length;j++) {
		if (TD.Columns[j].colvisible&&(TD.Columns[j].ColType!='RowDisplay')&&
			(TD.Columns[j].ColType!='LoadSubTables')&&(TD.Columns[j].ColType!='RemoveTable')&&(colnum==i)) {
			return TD.Columns[j];
		} else if (TD.Columns[j].colvisible&&(TD.Columns[j].ColType!='RowDisplay')&&
			(TD.Columns[j].ColType!='LoadSubTables')&&(TD.Columns[j].ColType!='RemoveTable')) {
			i++;
		}
	}
	return null;
}
/*
	ToggleTable: Used to show/hide a table in the report
	s - the signal event object
*/
rr.ToggleTable = function(s){
	var el = s.src();
	var tbl = el.nextSibling;
	while (!hasElementClass(tbl,'tDetail')){
		tbl = tbl.nextSibling;
	}
	if (hasElementClass(tbl,'invisible')) {
		removeElementClass(tbl,'invisible');
	} else {
		addElementClass(tbl,'invisible');
	}
}
/*
	PrintPreview: Open just the report tables in a separate window
	- Remove the "show/hide" text
*/

rr.Template = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">';
rr.Template = rr.Template + '<html xmlns="http://www.w3.org/1999/xhtml">';
rr.Template = rr.Template + '<head>';
rr.Template = rr.Template + '<meta content="text/html; charset=UTF-8" http-equiv="content-type" />';
rr.Template = rr.Template + '    <title>Print Preview</title>';
rr.Template = rr.Template + '   <link rel="stylesheet" href="/static/css/custom.css" type="text/css" />';
rr.Template = rr.Template + '<LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>';
rr.Template = rr.Template + '    <LINK HREF="/static/javascript/calendar_custom/calendar-green.css" TYPE="text/css" REL="stylesheet"/>';
rr.Template = rr.Template + '    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>';
rr.Template = rr.Template + '</head>';
rr.Template = rr.Template + '<body>';
rr.Template2 = '</body>';
rr.Template2 = rr.Template2 + '</html>';

rr.PrintPreview = function() {
	// Create the new window
	var w = window.open();
	//var report = getElement('RenderReport').cloneNode(true);
	var report_string = getElement('RenderReport').innerHTML;
	//el.write(report.replace('[show/hide] ',''));
	var el = w.document;
	el.open();
	el.write(rr.Template + report_string.replace('[show/hide] ','','g') + rr.Template2);
	el.close();
	rr.toggle_message('');
}

/*
	RenderFlatTable:
*/
rr.RenderFlatReport = function() {
	// Grab our render location
	var el = getElement('RenderReport');
	// Initialize our report DOM
	replaceChildNodes(el,null);
	if (rr.Data.length > 1) {
		// Render the lines of data
		var i = rr.RenderFlatSubTable(0,el,null,null);
		if (i < rr.Data.length) {
			alert('ooops, did not render all the lines?');
		}
	}
	rr.toggle_message('');
}
/*
	RenderFlatSubTable: In a flat table, a sub-table's columns get placed to the right of the parent row, which is repeated
	i - The index of the line of data for the first line of data for the detail (the report will go until the Total line is reached)
	el - The colgroup to append the sub-table to (or whatever element (DIV) in the case of the first row)
	ColHeaders - The parent row's column headers - an array of TD
	RowData - The parent row's column data - an array of TD
	Returns: i - the index value for the last row of the sub table
*/
rr.RenderFlatSubTable = function(i,el,ColHeaders, RowData){
	var TableID = rr.Data[i][0];
	var TD = rr.GetTD(TableID);
	var colCount = rr.Data[i].length - 5;
	var showTable = TD.rowvisible;
	if (showTable) {
		// Attempt to append our data to an existing table with the same ID, otherwise, create a new table
		if (getElement(TableID+'Report')==null) {
			// Create a DIV to toggle between show/hide
			var toggle = createDOM('DIV',{'style':'font-size:14px', 'class':'rowdisplay'},'[show/hide]   '+TD.TableName);
			connect(toggle,'onclick',rr.ToggleTable);
			el.appendChild(toggle);
			// Create the table
			var t = createDOM('TABLE',{'id':TableID+'Report', 'border':'0','class':'tDetail'});
			var b = createDOM('TBODY',null);
			el.appendChild(t);
			t.appendChild(b);
			// Create the titles row
			var title = createDOM('TR',{'class':'trTitle'});
			// Append clones of the parent column headers first
			if (ColHeaders!=null) {
				for (var j=0;j<ColHeaders.length;j++){
					title.appendChild(ColHeaders[j].cloneNode(true));
				}
			}
			// Append our column headers
			for (var j=0;j<TD.Columns.length;j++){
				//alert(TD.Columns[j].ColName);
				if (TD.Columns[j].colvisible&&((TD.Columns[j].ColType!='RowDisplay')&&(TD.Columns[j].ColType!='LoadSubTables')&&(TD.Columns[j].ColType!='RemoveTable'))) {
					var td = createDOM('TD',{'class':'tdTitle'});
					appendChildNodes(td,TD.Columns[j].ColName);
					title.appendChild(td);
				}
			}
			b.appendChild(title);
			// Get an array of column headers for any sub-tables that we have
			var MyColHeaders = getElementsByTagAndClassName('TD',null,title);
		} else {
			//alert(TableID);
			var t = getElement(TableID+'Report');
			var b = getElementsByTagAndClassName('TBODY', null, t)[0];
			// Get an array of my column headers to pass on to any sub-table
			var TitleRow = getElementsByTagAndClassName('TR','trTitle', t)[0];
			var MyColHeaders = getElementsByTagAndClassName('TD',null,TitleRow);
		}
	} else {
		var MyColHeaders = ColHeaders;
	}
	// Create the data rows
	var finished = false;
	// Create an null row of data, we'll fill it later
	var MyRowData = null;
	// Loop through until we reach the "Total" row for this TableID
	while (!finished) {
		var curTableID = rr.Data[i][0];
		var RowType = rr.Data[i][2];
		// First check if the row belongs to a new sub-detail section
		if (curTableID!=TableID) {
			//if (showTable) {
				// var tr = createDOM('TR',null);
				// var tdspan = createDOM('TD',{'colspan':colCount});
				// b.appendChild(tr);
				// tr.appendChild(tdspan);
				i = rr.RenderFlatSubTable(i,el,MyColHeaders,MyRowData);
			//} else {
			//	i = rr.RenderSubTable(i,el);
			//}
		// Second, check if the row is a data row
		} else if (RowType=='Data') {
			if (showTable) {
				var NewRow = rr.RenderRowData(rr.Data[i],TD,false,RowData);
				b.appendChild(NewRow);
				// Get our current row data in case we have any sub-tables coming after this
				var MyRowData = getElementsByTagAndClassName('TD','tdData',NewRow);
			} else {
				var MyRowData = RowData;
			}
			i++;
		// Finally, check if the row is a Total row, the last row in this detail section
		// NOTE: We don't render total rows in a flat table layout... it would be too confusing!
		} else if (RowType=='Total') {
			//if (showTable) {
			//	b.appendChild(rr.RenderRowTotal(rr.Data[i],TD, true));
			//}
			i++;
			finished = true;
		}
	}
	return i;
}