<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Stock Monitor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript"></SCRIPT>
   <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
     <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
       <SCRIPT SRC="/static/javascript/stores_QuickMenu.js" TYPE="text/javascript"></SCRIPT>
 </head>

<body>
	<DIV style="position:relative; width:100%; left:0px; font-size:12px" class="divtable">
		<div class="row">
			<form name="StockItemSearchForm" id="StockItemSearchForm" action="StockMonitor" method="post">
				<div style="border:1px solid black; padding:2px;" class="divtable_input">
					<div class="row">
						<div style="vertical-align:top;" >Item Name</div>
						<div><INPUT type="text" id="SearchText" name="SearchText" size="25" value="${SearchText}" /></div>
					</div>
					<div class="row">
						<div style="vertical-align:top;" >Item Groups</div>
						<div>
							<SELECT id="Groups" name="Groups" multiple="multiple" size="4">
								<OPTION py:for="item in CatalogItemGroups" value="${item['id']}" selected="${item['selected']}">${item['name']}</OPTION>
							</SELECT>
						</div>
					</div>
					<div class="row">
						<div></div>
						<div style="text-align:right">
							<INPUT type="reset"  />
							<INPUT id="btnStockItemSearch" type="submit" value="Search" name="btnStockItemSearch" />
						</div>
					</div>
				</div> 
			</form>
		</div>
		<br />
		<div class="row">
			Displaying ${len(results)} of ${ResultCount} Stock Items from ${LocationName}
		</div>
		<br />
		<div class="row">
			<div style="font-size:12px; border:1px solid black" id="StockItemsList" class="divtable_input">
				<div class="row">
					<div py:for="item in ColumnTitles" style="text-align:center; padding-left: 5px; border-left:1px solid gray; border-bottom:1px solid black">
						${item}
					</div>
				</div>
				<div py:for="item in results" class="row" style="">
					<div style="text-align:left; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">
						<a href="StockItemsEditor?StockItemID=${item['StockItemID']}">${item['StockItemName']}</a>
					</div>
					<div style="text-align:left; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">
						<a href="CatalogItemsEditor?CatalogItemID=${item['CatalogItemID']}">${item['CatalogItemName']}</a>
					</div>
					<div style="text-align:right; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white">${item['QtyAvailable']}</div>
					<div style="text-align:right; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">${item['RateOfConsumption']}</div>
					<div style="text-align:right; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">${item['QtyAvailableLocation']}</div>
					<div style="text-align:right; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">${item['QtyConsumedLocation']}</div>
					<div style="text-align:right; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">${item['QtyTransferredToLocation']}</div>
					<div style="text-align:right; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">${item['QtyTransferredFromLocation']}</div>
					<div style="text-align:right; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">${item['QtyTransferringToLocation']}</div>
					<div style="text-align:right; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">${item['QtyTransferringFromLocation']}</div>
					<div style="text-align:right; padding-left: 5px; border-left:1px solid gray; border-bottom:3px solid white;">${item['QtyCreatedAtLocation']}</div>
				</div>
			</div>
		</div>
	</DIV>
</body>
</html>
