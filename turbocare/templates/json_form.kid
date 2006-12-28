<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
py:extends="'master.kid'">
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Forms Tutorial')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/tabber.css" TYPE="text/css" REL="stylesheet"/>
	<link rel="stylesheet" type="text/css" href="/static/css/yui/fonts.css" />
	<link rel="stylesheet" type="text/css" href="/static/css/yui/menu.css" /> 
	<link rel="stylesheet" type="text/css" href="/static/css/yui/tree.css" /> 
	<link rel="stylesheet" type="text/css" href="/static/css/yui/grids.css" /> 
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
  	<script type="text/javascript">
		var tabberOptions = {manualStartup:true};
	</script>
	<script type="text/javascript" src="/static/javascript/tabber.js">
	</script>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
     <SCRIPT SRC="/static/javascript/prototype.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/scriptaculous.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/dragdrop.js" TYPE="text/javascript"></SCRIPT>
	<script type="text/javascript" src="/static/javascript/yui/build/yahoo/yahoo.js"></script>
	<script type="text/javascript" src="/static/javascript/yui/build/dom/dom.js"></script>
	<script type="text/javascript" src="/static/javascript/yui/build/event/event.js"></script>
	<script type="text/javascript" src="/static/javascript/yui/build/container/container_core.js"></script>
	<script type="text/javascript" src="/static/javascript/yui/build/menu/menu.js"></script>
	<script type="text/javascript" src="/static/javascript/yui/build/treeview/treeview.js"></script>
    <SCRIPT SRC="/static/javascript/inv.js" TYPE="text/javascript"></SCRIPT>
 </head>

<body>
	<div py:content="data">This is replaced.</div>
	<table class="menupage">
		<tr>
			<td><div id="app_menu"></div></td>
			<td id="app_treeview_td" width="0%"><div id="app_treeview" style="overflow:auto;">&nbsp;</div></td>
			<td width="100%"><div id="dom_obj" style="overflow:auto;">&nbsp;</div></td>
		</tr>
	</table>
</body>
</html>
