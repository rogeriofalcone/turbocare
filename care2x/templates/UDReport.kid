<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','User Defined Report')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
	<SCRIPT SRC="/static/javascript/QueryBoxes.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/RenderReport.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/UDReport.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
    <style type="text/css">
	Transfer {color: red}
    </style>
  </head>

<body>
	Step 1:  Select the starting table
	<div>
		<SELECT id="TableName" style="font-size:11px">
			<OPTION py:for="table in tablenames" value="${table}">${table}:  ${tablenames[table]}</OPTION>
		</SELECT>
	</div>
	Step 2: Choose the columns, filters, groupings etc (<a href="javascript:qry.RedisplayTables()">re-display</a>)
	<div id="QueryDefinition" class="QryMkrTbl">
	</div>
	Step 3: <A href="javascript:qry.SerializeQuery()">Run the query</A>
	<DIV id='RenderReport' style="font-size:10px">
	</DIV>
	Step 4: (Optional) Print the results
	Step 5: (Optional) Save the query
</body>
</html>
