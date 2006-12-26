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
    <SCRIPT SRC="/static/javascript/stores_PurchaseOrdersEditor.js" TYPE="text/javascript"></SCRIPT>
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
				<A href="PurchaseOrdersEditor">New POs</A> (un-sent):
				<li py:for="po in newPOs"><a href="PurchaseOrdersEditor?PurchaseOrderID=${po['id']}">${po['name']}</a></li>
				<br/>Pending POs (sent):
				<li py:for="po in sentPOs"><a href="PurchaseOrdersEditor?PurchaseOrderID=${po['id']}">${po['name']}</a></li>
				<br/>Un-finished POs (some items received):
				<li py:for="po in unfinishedPOs"><a href="PurchaseOrdersEditor?PurchaseOrderID=${po['id']}">${po['name']}</a></li>
				<br/>Old POs (8 most recent):
				<li py:for="po in oldPOs"><a href="PurchaseOrdersEditor?PurchaseOrderID=${po['id']}">${po['name']}</a></li>
				<br/>Quick Search (Search for a PO including the Catalog item):
				<br/><INPUT id="QuickSearch" name="QuickSearchText" type="text" value="Enter Search Text" size="20"></INPUT>
				<div id="QuickSearchResults">
					<li>No Search Results</li>
				</div>
			</div>
			<div>
				<form py:if="PurchaseOrderID != None" name='PurchaseOrderForm' action="PurchaseOrderSave" method="post">
					<div style="font-size:18px" class="row-blank">${Name} (ID#: ${PurchaseOrderID})</div>
					<div id="store1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Vendor</div>
							<div id="VendorID">
								${VendorName}
								<INPUT name="VendorID" type="hidden" value="${VendorID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Notes</div>
							<div><TEXTAREA name="Notes" rows="4" cols="40">${Notes}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">PO Sent on date</div>			
							<div ><INPUT id="POSentOnDate" name="POSentOnDate" type="text" value="${POSentOnDate}" size="30" class="dateEntry"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Expected delivery date</div>			
							<div ><INPUT id="ExpectedDeliveryDate" name="ExpectedDeliveryDate" type="text" value="${ExpectedDeliveryDate}" size="30" class="dateEntry"></INPUT></div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Purchase order items</div>
							<div>
								<div id="Items" style="display:table">
									<div py:for="item in items" style="display:table-row">
										<div><INPUT py:if="POSentOnDate==None" type="button" name="POEdit${item['POItemID']}" value="Edit" class="hideUnHide" />
											<INPUT type="button" name="PODelete${item['POItemID']}" value="Delete" class="delItem" />
												<a href="CatalogItemsEditor?CatalogItemID=${item['POItemCatalogItemID']}">${item['POItemName']} </a>
											<div style="position:relative; width:300px; left:0px; font-size:12px; display:none" id="POEdit${item['POItemID']}">
												<INPUT type="hidden" name="POItemID" value="${item['POItemID']}" />
												<INPUT type="hidden" name="POItemCounter" value="${item['POItemCounter']}" />
												<div style="display:table-row">
													<div style="width:120px" class="label">Quantity Requested</div>
													<div ><INPUT name="POItemQuantityRequested" type="text" value="${item['POItemQuantityRequested']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Quantity Received</div>
													<div ><INPUT name="POItemQuantityReceived" type="text" value="${item['POItemQuantityReceived']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Quote Price</div>
													<div ><INPUT name="POItemQuotePrice" type="text" value="${item['POItemQuotePrice']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Actual Price</div>
													<div ><INPUT name="POItemActualPrice" type="text" value="${item['POItemActualPrice']}"></INPUT></div>
												</div>
												<div style="display:table-row">
													<div style="width:120px" class="label">Notes</div>
													<div ><INPUT name="POItemNotes" type="text" value="${item['POItemNotes']}"></INPUT></div>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Goods Received</div>
							<div id="GoodsReceived">
								<LI py:for="gritem in goodsreceived">
									<A href="GoodsReceivedEditor?GoodsReceivedID=${gritem['id']}">${gritem['name']}</A>
								</LI>
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input py:if="POSentOnDate!=None" name="Operation" id="btnMakeGoodsRecieved" type="submit" value="Make Goods Received" />
						<input py:if="POSentOnDate!=None" name="Operation" id="btnCopyIntoNew" type="submit" value="Copy to new PO" />
						<input py:if="POSentOnDate==None" name="Operation" id="btnAddItems" type="button" value="Add Items" />
						<input id="PurchaseOrderID" type="hidden" name="PurchaseOrderID" value="${PurchaseOrderID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="button" value="Cancel" ></input>
						<input name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
					</div>
				</form>
				<div py:if="PurchaseOrderID == None">
					<div style="display:table;width:600px">
						<div style="display:table-row;">
							<div style="display:table-cell;">
								<form name="CatalogItemSearchForm" id="CatalogItemSearchForm">
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
			</div>
		</div>
	</DIV>
</body>
</html>
