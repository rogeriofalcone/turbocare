<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Add Receipt Items')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/tg_widgets/turbogears.widgets/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/tabber.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/static/javascript/billing_receiptitemsadd.js" TYPE="text/javascript">
    </SCRIPT>
</head>

<body>
	<table class="minimal" width="100%">
		<tr>
			<td class="threecol">
				<a href="">Close (and Cancel)</a>
				<div class="listing" id="Items">
					<div class="listingrow" py:for="item in Items" id="listing_row_${item['id']}" ondblclick="inv.loadItemOptions('${item['id']}')">
					<table class="minimal">
						<tr><td colspan="2">
						<INPUT type="hidden" name="ItemID" value="${item['id']}"></INPUT>
						<INPUT type="hidden" name="Counter" value="1"></INPUT>
						<INPUT type="hidden" name="ReceiptID" value="${item['ReceiptID']}"></INPUT>
						<h3>${item['Name']}</h3></td></tr>
						<tr><td><INPUT type="hidden" name="Name" value="${item['Name']}"></INPUT>
						<INPUT type="hidden" name="ItemOptionID" value=""></INPUT>
						Quantity:</td><td><INPUT type="text" name="Quantity" value="${item['Quantity']}"></INPUT></td></tr>
					</table>
					</div>
				</div>
			</td>
			<td class="threecol">
				<BUTTON name="btnPick" value="Pick" type="submit" onclick="inv.moveItem()">${BtnPickText}</BUTTON>
				<div id="ItemOptions" style="overflow:auto;">&nbsp;</div></td>
			<td class="threecol">
				<FORM action="FinalItemsCreateNewSave" name="FinalItemsForm" id="FinalItemsForm" method="post">
				<BUTTON name="btnSave" value="Save" type="submit">Save and Close</BUTTON>
				<div id="FinalItems" class="listing">&nbsp;</div></FORM></td>
		</tr>
	</table>
</body>
</html>
