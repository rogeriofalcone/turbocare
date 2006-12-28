<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Purchase Order')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/tg_widgets/turbogears.widgets/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/tabber.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/static/javascript/purchaseorder.js" TYPE="text/javascript">
    </SCRIPT>
</head>

<body>
	<table class="minimal" width="100%">
		<tr>
			<td class="threecol">
				<a py:if="'PreviousLink' in dir()" href="${PreviousLink}">Close (and Cancel)</a>
				<div class="listing" id="CatalogItems">
					<div class="listingrow" py:for="item in CatalogItems" id="listing_row_${item['id']}">
					<table class="minimal">
						<tr><td colspan="2"><INPUT type="hidden" name="CatalogItem" value="${item['id']}"></INPUT>
						<h3>${item['Name']}&nbsp;&nbsp;${item['Description']}</h3></td></tr>
						<tr><td><INPUT type="hidden" name="Name" value="${item['Name']}"></INPUT>
						<INPUT type="hidden" name="Description" value="${item['Description']}"></INPUT>
						<INPUT type="hidden" name="Vendor" value=""></INPUT>
						<INPUT type="hidden" name="Counter" value="1"></INPUT>
						Quantity:</td><td><INPUT type="text" name="QuantityRequested" value="${item['Quantity']}"></INPUT></td></tr>
						<tr><td>Notes:</td><td><INPUT type="text" name="Notes" value="${item['Notes']}"></INPUT></td></tr>
						<tr><td>Quote price:</td><td><INPUT type="text" name="QuotePrice" value="" readonly="1"></INPUT></td></tr>
					</table>
					</div>
				</div>
			</td>
			<td class="threecol"><div id="vendors" style="overflow:auto;">&nbsp;</div></td>
			<td class="threecol">
				<FORM action="PurchaseOrderCreateNewSave" name="PurchaseOrderForm" id="PurchaseOrderForm" method="post">
					<BUTTON id="btnSave" name="btnSave" value="Save" type="submit">Save and Close</BUTTON>
					<div id="PurchaseOrders" class="listing">&nbsp;</div>
				</FORM>
			</td>
		</tr>
	</table>
</body>
</html>
