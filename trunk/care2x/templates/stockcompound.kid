<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Stock Compounding')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/tg_widgets/turbogears.widgets/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/tabber.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/static/javascript/stockcompound.js" TYPE="text/javascript">
    </SCRIPT>
</head>

<body>
	<table class="minimal" width="100%">
		<tr>
			<td class="threecol">
				<table class="minimal">
					<tr><td colspan="2"><a href="/inventory">Close (and Cancel)</a></td></tr>
					<tr><td>Quantity</td><td><INPUT type="text" id="TotalQty" name="TotalQty" value="1"></INPUT></td></tr>
					<tr>
						<td>Location</td>
						<td>
							<SELECT name="LocationName" id="LocationName">
								<OPTION py:for="location in Locations" value="${location['id']}">${location['Name']}</OPTION>
							</SELECT>
						</td>
					</tr>
				</table>
				<div class="listing" id="RequestedCatalogItems">
					<div class="listingrow" py:for="item in CatalogItems" id="listing_row_${item['id']}" ondblclick="inv.loadLocations('${item['id']}')">
					<table class="minimal">
						<tr>
							<td colspan="2">
								<INPUT type="hidden" name="CatalogItemID" value="${item['CatalogItemID']}"></INPUT>
								<INPUT type="hidden" name="id" value="${item['id']}"></INPUT>
								<INPUT type="hidden" name="CompoundID" value="${item['CompoundID']}"></INPUT>
								<p style="font-size:18px; font-weight:bold; margin: 0 0 0 0;">${item['Name']}</p><p style="font-size:15px; font-weight:bold;  margin: 0 0 0 0;">${item['Description']}</p>
							</td>
						</tr>
						<tr>
							<td>Quantity:</td><td><INPUT type="text" name="Qty" value="${item['Qty']}" readonly="1"></INPUT></td>
						</tr>
					</table>
					</div>
				</div>
			</td>
			<td class="threecol">
				<BUTTON name="btnPick" value="Pick" type="submit" onclick="inv.makeItem()">Use Selected Stock</BUTTON>
				<div id="Locations" style="overflow:auto;">&nbsp;</div>
			</td>
			<td class="threecol">
				<FORM action="StockItemCompoundSave" name="StockItemForm" id="StockItemForm" method="post">
					<BUTTON name="btnSave" value="Save" type="submit">Save and Close</BUTTON>
					<div id="StockItemCompound" class="listing">&nbsp;</div>
				</FORM>
			</td>
		</tr>
	</table>
</body>
</html>
