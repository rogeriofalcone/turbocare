<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','User Defined Report Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
	<SCRIPT SRC="/static/javascript/QueryBoxes.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/RenderReport.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/UDReportEditQuery.js" TYPE="text/javascript"></SCRIPT>
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
	<DIV> Go to: <A HREF="Builder">Report Builder</A>, <A href="index">Report Viewer</A> </DIV>
	<DIV >Step 1: Select the report
		<DIV style="display:table">
			<DIV style="display:table-row">
				<DIV style="display:table-cell">
					<SELECT name="Group" id="Group" size="5">
						<OPTION py:for="group in groups" value="${group}">${group}</OPTION>
					</SELECT>
				</DIV>
				<DIV style="display:table-cell; padding-left: 5px">
					<SELECT name="ReportFile" id="ReportFile" size="5">
						<OPTION value=""></OPTION>
					</SELECT>
				</DIV>
			</DIV>
		</DIV>
	</DIV>
	<DIV >Step 2: Edit the query definition 
		(<a href="javascript:qry.CallRedisplayTables()">re-display</a>) 
		(<a href="javascript:qry.ToggleQueryDefinition()">Show/Hide Query Definition</a>)
	</DIV>
	<br />
	<div id="QueryDefinition" class="QryMkrTbl">
	</div>
	 <DIV >Step 3: <A href="javascript:qry.SerializeQuery()">Run the query</A>
		[<A href="javascript:rr.HideDetails()">Hide all details</A> ||
		<A href="javascript:rr.ShowDetails()">Show all details</A>]
	</DIV>
	<DIV id='RenderReport' style="font-size:10px">
	</DIV>
	<DIV >Step 4: (Optional) <A href="javascript:rr.PrintPreview()">Print the results</A></DIV>
	<DIV >
		Step 5: (Optional) <A href="javascript:qry.SaveReport()">Save the revised query</A>
		<DIV style="position:relative; left:3em">Report Name: <INPUT type="text" size="30" name="ReportName" id="ReportName" value="" /></DIV>
	</DIV>
</body>
</html>
