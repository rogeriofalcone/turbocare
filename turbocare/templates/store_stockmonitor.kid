<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Purchase Orders Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript"></SCRIPT>
   <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
   <SCRIPT SRC="/static/javascript/stores_StockMonitor.js" TYPE="text/javascript"></SCRIPT>
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
			<div style="display:table;width:600px">
				<div style="display:table-row;">
					<div style="display:table-cell;">
						<form name="StockItemSearchForm" id="StockItemSearchForm">
							<div style="border:1px solid black; padding:2px;" class="divtable_input">
								<div class="row">
									<div style="vertical-align:top;" >Item Name</div>
									<div><INPUT type="text" id="CatalogItemName" name="CatalogItemName" size="25" value="" /></div>
								</div>
								<div class="row">
									<div style="vertical-align:top;" >Item Groups</div>
									<div>
										<SELECT id="CatalogItemGroups" name="CatalogItemGroups" multiple="multiple" size="4">
											<OPTION py:for="item in cataloggroups" value="${item['id']}">${item['name']}</OPTION>
										</SELECT>
									</div>
								</div>
								<div class="row">
									<div></div>
									<div style="text-align:right">
										<INPUT type="reset"  />
										<INPUT id="btnCatalogItemSearch" type="button" value="Search" name="btnCatalogItemSearch" />
									</div>
								</div>
							</div> 
						</form>
					</div>
					<div style="display:table-cell; padding:2px;">
						<form action="PurchaseOrderCreate" name="PurchaseOrderCreate" id="PurchaseOrderCreate">
						<div style="display:inline-table">
							<div id="PurchaseOrderItemList" style="display:block; background-color:pink; width:350px;height:125px;overflow:auto">
							</div>
						</div>
						<div id="buttons" style="display:table;text-align:right; width:350px" class="topbuttons">
							<input name="Operation" id="btnPurchaseOrderCreate" type="submit" value="Create" ></input>
						</div>
						</form>
					</div>
				</div>
			</div>
			<br />
			<div style="font-size:12px; border:1px solid black" id="CatalogItemsList" class="divtable_input">
				<div py:for="item in catalogitems" class="row">
					<INPUT type="hidden" name="CatalogItemID" value="${item['id']}" />
					<INPUT type="hidden" name="Counter" value="1" />
					<div style="text-align:left; padding: 0px 1px 0px 1px">
						<INPUT type="checkbox" name="CatalogItemCheck" />
					</div>
					<div style="text-align:left; padding-left: 5px; border-left:1px solid gray;">
						<a href="CatalogItemsEditor?CatalogItemID=${item['id']}">${item['name']}</a>
					</div>
					<div style="text-align:left; padding-left: 5px; border-left:1px solid gray;">${item['stock']}</div>
					<div style="text-align:left; padding-left: 5px; border-left:1px solid gray;">${item['reorder']}</div>
					<div style="text-align:left; padding-left: 5px; border-left:1px solid gray;">${item['lastpo']}</div>
				</div>
			</div>
		</div>
	</DIV>
</body>
</html>
