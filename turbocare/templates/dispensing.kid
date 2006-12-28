<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/dispensing.js" TYPE="text/javascript"></SCRIPT>
    <title>${title}</title>
</head>
<body>
	<DIV  style="display: none" id="customer_id">${customer_id}</DIV>
	<DIV style="display: table; width: 100%">
		<DIV style="display: table-row">
		<DIV style="display: table-cell; width: 50%">
			<DIV style="text-align:left; list-style-type: none" class="ListItemRow" id="CurrentItemsTitle"> Nothing loaded
			</DIV>
			<FORM name="CustomerItems" id="CustomerItems">
				<div style="position:relative; font-size:14px" class="divtable_list" id="CustomerItemsTable">

				</div>
			</FORM>
		</DIV>
		<DIV style="display: table-cell">
			<DIV style="text-align:left" class="ListItemRow" id="PendingItemsTitle">0 Pending Items</DIV>
			<DIV style="position:relative; font-size:14px" class="listing" id="PendingItems">
			</DIV>
		</DIV>
		</DIV>
	</DIV>
</body>
</html>
