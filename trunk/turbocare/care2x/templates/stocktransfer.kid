<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Stock Transfers')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/tg_widgets/turbogears.widgets/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/tabber.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/static/javascript/stocktransfer.js" TYPE="text/javascript">
    </SCRIPT>
</head>

<body>
	<table class="minimal" width="100%">
		<tr>
			<td class="threecol">&nbsp;&nbsp;
				<a href="/inventory">Close (and Cancel)</a>
				<div class="listing" id="RequestedCatalogItems">
					<div class="listingrow" py:for="item in RequestedCatalogItems" id="listing_row_${item['id']}" ondblclick="inv.loadLocations('${item['id']}')">
					<table class="minimal">
						<tr>
							<td colspan="2">
								<INPUT type="hidden" name="ForLocation" value="${item['ForLocationName']}"></INPUT>
								<INPUT type="hidden" name="StockTransferRequestItemID" value="${item['id']}"></INPUT>
								<INPUT type="hidden" name="CatalogItemID" value="${item['CatalogItemID']}"></INPUT>
								<INPUT type="hidden" name="ForLocationID" value="${item['ForLocationID']}"></INPUT>
								<INPUT type="hidden" name="QtyRequested" value="${item['Qty']}"></INPUT>
								<h3>${item['Name']} requested on ${item['RequestedOn']}</h3>
							</td>
						</tr>
						<tr>
							<td>Quantity requested:</td><td><INPUT type="text" name="QuantityRequested" value="${item['Qty']}" readonly="1"></INPUT></td>
						</tr>
						<tr><td>Notes:</td><td><INPUT type="text" name="Notes" value="${item['Notes']}" readonly="1"></INPUT></td></tr>
					</table>
					</div>
				</div>
			</td>
			<td class="threecol">
				<BUTTON name="btnPick" value="Pick" type="submit" onclick="inv.makeItem()">Transfer from selected location</BUTTON>
				<div id="Locations" style="overflow:auto;">&nbsp;</div>
			</td>
			<td class="threecol">
				<FORM action="StockTransferCreateNewSave" name="StockTransferForm" id="StockTransferForm" method="post">
					<BUTTON name="btnSave" value="Save" type="submit">Save and Close</BUTTON>
					<div id="StockTransfers" class="listing">&nbsp;</div>
				</FORM>
			</td>
		</tr>
	</table>
</body>
</html>
