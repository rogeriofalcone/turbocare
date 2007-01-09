<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Stock Items Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/stores_StockItemsEditor.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
    <style type="text/css">
	Transfer {color: red}
    </style>
     <SCRIPT SRC="/static/javascript/stores_QuickMenu.js" TYPE="text/javascript"></SCRIPT>
   </head>

<body>
	<DIV style="position:relative; width:100%; left:0px; font-size:12px" class="divtable">
		<div class="row">
			<div style="vertical-align:top; width:200px">
				<br/>Quick Search:
				<br/><INPUT id="QuickSearch" name="QuickSearchText" type="text" value="Enter Search Text" size="20"></INPUT>
				<div id="QuickSearchResults">
					<li>No Search Results</li>
				</div>
				<br/><br/>Transfers To here (pending):
				<li py:for="stt in pendingSTTs"><a href="StockTransfersEditor?StockTransferID=${stt['id']}">${stt['name']}</a></li>
				<br/>Transfers From here (pending):
				<li py:for="stf in pendingSTFs"><a href="StockTransfersEditor?StockTransferID=${stf['id']}">${stf['name']}</a></li>
				<br/>Transfer Requests (pending):
				<li py:for="tr in pendingSTRs"><a href="StockTransferRequestsEditor?StockTransferRequestID=${tr['id']}">${tr['name']}</a></li>
				<br/>Purchase Orders (pending):
				<li py:for="po in pendingPOs"><a href="PurchaseOrdersEditor?PurchaseOrderID=${po['id']}">${po['name']}</a></li>
			</div>
			<div>
				<form name='StockItemForm' action="StockItemsSave" method="post">
					<div style="font-size:18px" class="row-blank">${DisplayName} (ID#: ${StockItemID})</div>
					<div id="store1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Name</div>
							<div >
								<INPUT id="Name" name="Name" type="text" value="${Name}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnPickCatalogItemID" type="button" value="Item Master" ></input></div>
							<div id="CatalogItemID">
								<a href="CatalogItemsEditor?CatalogItemID=${CatalogItemID}">${CatalogItemName}</a>
								<INPUT name="CatalogItemID" type="hidden" value="${CatalogItemID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Purchase Order</div>
							<div><A href="PurchaseOrdersEditor?PurchaseOrderID=${PurchaseOrderID}">${PurchaseOrderName}</A>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">MRP (Rs.)</div>
							<div >
								<INPUT id="MRP" name="MRP" type="text" value="${MRP}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Sale Price (Rs.)</div>
							<div >
								<INPUT id="SalePrice" name="SalePrice" type="text" value="${SalePrice}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Purchase Price (Rs.)</div>
							<div >
								<INPUT id="PurchasePrice" name="PurchasePrice" type="text" value="${PurchasePrice}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Purchased Quantity</div>
							<div >
								<INPUT id="Quantity" name="Quantity" type="text" value="${Quantity}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Batch Number</div>
							<div >
								<INPUT id="BatchNumber" name="BatchNumber" type="text" value="${BatchNumber}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Expire Date</div>
							<div >
								<INPUT id="ExpireDate" name="ExpireDate" type="text" value="${ExpireDate}" size="30" class="dateEntry"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Compound Date Produced (DISABLED)</div>
							<div >
								<INPUT id="CompoundDateProduced" name="CompoundDateProduced" type="text" value="${CompoundDateProduced}" size="30" class="dateEntry"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Compound Composition (DISABLED)</div>
							<div >
								<LI py:for="compoundqty in compoundqtys">${compoundqty}</LI>
							</div>
						</div>
					</div>
					<div id="Items"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="display:table-row">
							<div style="display:table-cell;text-align:center;width:150px">Location</div>
							<div style="display:table-cell;text-align:center">Qty Available</div>
							<div style="display:table-cell;text-align:center">Description</div>
							<div style="display:table-cell;text-align:center">Options</div>
						</div>
						<div py:for="item in items" style="display:table-row">
							<div style="display:table-cell;border-top:1px solid gray">
								${item['ItemLocation']}
								<INPUT name="ItemID" type="hidden" value="${item['ItemID']}" />
								<INPUT name="ItemCounter" type="hidden" value="1" />
							</div>
							<div style="display:table-cell;border-top:1px solid gray">${item['ItemQuantity']}</div>
							<div style="display:table-cell;border-top:1px solid gray">${item['ItemDescription']}</div>
							<div style="display:table-cell;border-top:1px solid gray">
								<INPUT type="button" class="delItem" name="Delete" value="Delete" />
								<INPUT py:if="not item['ItemIsConsumed'] and item['ItemCanTransfer']" type="button" name="Transfer" value="Transfer" class="Transfer" />
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table; width=600px" class="topbuttons">
						<input id="StockItemID" type="hidden" name="StockItemID" value="${StockItemID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="button" value="Cancel" ></input>
						<input py:if="not StockItemID in ['',None]" name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input py:if="not StockItemID in ['',None]" name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="Status == 'deleted'" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
