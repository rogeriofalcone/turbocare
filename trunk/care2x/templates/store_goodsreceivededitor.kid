<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Goods Received Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript"></SCRIPT>
   <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/stores_GoodsReceivedEditor.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
  </head>

<body>
	<DIV style="position:relative; width:100%; left:0px; font-size:12px" class="divtable">
		<div class="row">
			<div style="vertical-align:top; width:300px">
				<br/>Pending POs (sent):
				<li py:for="po in sentPOs"><a href="PurchaseOrdersEditor?PurchaseOrderID=${po['id']}">${po['name']}</a></li>
				<br/>Un-finished POs (some items received):
				<li py:for="po in unfinishedPOs"><a href="PurchaseOrdersEditor?PurchaseOrderID=${po['id']}">${po['name']}</a></li>
				<br/>Latest GRs:
				<li py:for="gr in latestGRs"><a href="GoodsReceivedEditor?GoodsReceivedID=${gr['id']}">${gr['name']}</a></li>
				<br/>Quick Search (Search for a GR including the Catalog item):
				<br/><INPUT id="QuickSearch" name="QuickSearchText" type="text" value="Enter Search Text" size="20"></INPUT>
				<div id="QuickSearchResults">
					<li>No Search Results</li>
				</div>
			</div>
			<div>
				<form py:if="GoodsReceivedID != None" name='PurchaseOrderForm' action="GoodsReceivedSave" method="post">
					<div style="font-size:18px" class="row-blank">${Name} (ID#: ${GoodsReceivedID})</div>
					<div id="store1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Purchase Order</div>
							<div id="PurchaseOrderID">
								<a href="PurchaseOrdersEditor?PurchaseOrderID=${PurchaseOrderID}">${PurchaseOrderName}</a>
								<INPUT name="PurchaseOrderID" type="hidden" value="${PurchaseOrderID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Notes</div>
							<div><TEXTAREA id="Notes" name="Notes" rows="4" cols="40">${Notes}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">Date received</div>			
							<div ><INPUT id="DateReceived" name="DateReceived" type="text" value="${DateReceived}" size="30" class="dateEntry"></INPUT></div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Items received</div>
							<div>
								<div id="Items" style="display:table">
									<div py:for="item in items" style="display:table-row">
										<div><INPUT py:if="1 >= item['GRStockItemLocations']" type="button" name="GREdit${item['GRItemID']}" value="Edit" class="hideUnHide" />
											<INPUT py:if="1 >= item['GRStockItemLocations']" type="button" name="GRDelete${item['GRItemID']}" value="Delete" class="delItem" />
											<A href="StockItemsEditor?StockItemID=${item['GRItemID']}">${item['GRItemName']}</A> Locations: ${item['GRStockItemLocations']}
											<div style="position:relative; width:300px; left:0px; font-size:12px; display:none" id="GREdit${item['GRItemID']}">
												<INPUT type="hidden" name="GRItemID" value="${item['GRItemID']}" />
												<INPUT type="hidden" name="GRItemCounter" value="1" />
												<div style="display:table-row">
													<div style="width:120px" class="label">Name</div>
													<div ><INPUT name="GRItemName" type="text" value="${item['GRItemName']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Item master name</div>
													<div ><INPUT name="GRItemCatalogItemName" type="text" value="${item['GRItemCatalogItemName']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Quantity</div>
													<div ><INPUT name="GRItemQuantity" type="text" value="${item['GRItemQuantity']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Purchase Price</div>
													<div ><INPUT name="GRItemPurchasePrice" type="text" value="${item['GRItemPurchasePrice']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Sale Price</div>
													<div ><INPUT name="GRItemSalePrice" type="text" value="${item['GRItemSalePrice']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">M.R.P.</div>
													<div ><INPUT name="GRItemMRP" type="text" value="${item['GRItemMRP']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Batch Number</div>
													<div ><INPUT name="GRItemBatchNumber" type="text" value="${item['GRItemBatchNumber']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Expire Date</div>
													<div ><INPUT id="GRItemExpireDate${item['GRItemID']}" name="GRItemExpireDate" type="text" value="${item['GRItemExpireDate']}" class="dateEntry"></INPUT></div>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input name="Operation" id="btnAddItems" type="button" value="Add Items" />
						<input id="GoodsReceivedID" type="hidden" name="GoodsReceivedID" value="${GoodsReceivedID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="button" value="Cancel" ></input>
						<input name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="Status == 'deleted'" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
