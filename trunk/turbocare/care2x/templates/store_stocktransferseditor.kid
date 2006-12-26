<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Stock Transfers Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/stores_StockTransfersEditor.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
    <style type="text/css">
	FillRequest {color: red}
    </style>
  </head>

<body>
	<DIV style="position:relative; width:100%; left:0px; font-size:12px" class="divtable">
		<div class="row">
			<div style="vertical-align:top; width:200px">
				<br/>Quick Search (for stock or item master name):
				<br/><INPUT id="QuickSearch" name="QuickSearchText" type="text" value="Enter Search Text" size="20"></INPUT>
				<div id="QuickSearchResults">
					<li>No Search Results</li>
				</div>
				<br/>Pending Transfers To Here:
				<li py:for="item in pendingSTToHere"><a href="StockTransfersEditor?StockTransferID=${item['id']}">${item['name']}</a></li>
				<br/>Pending Transfers From Here:
				<li py:for="item in pendingSTFromHere"><a href="StockTransfersEditor?StockTransferID=${item['id']}">${item['name']}</a></li>
			</div>
			<div>
				<form name='StockTransferForm' action="StockTransfersSave" method="post">
					<div style="font-size:18px" class="row-blank">${Name} (ID#: ${StockTransferID})</div>
					<div id="store1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div py:if="not FromStockLocationID in ['',None]" class="row">
							<div style="width:200px" class="label">From Stock Location</div>
							<div id="FromStockLocationID">
								${FromStockLocationName}
								<INPUT name="FromStockLocationID" type="hidden" value="${FromStockLocationID}"></INPUT>
							</div>
						</div>
						<div py:if="FromStockLocationID in ['',None]" class="row">
							<div style="width:200px" class="label"><input id="btnPickStockItemID" type="button" value="Stock Item" ></input></div>
							<div id="StockItemID">
								${StockItemName}
								<INPUT name="StockItemID" type="hidden" value="${StockItemID}"></INPUT>
							</div>
						</div>
						<div py:if="not ToStockLocationID in ['',None]" class="row">
							<div style="width:200px" class="label">To Stock Location</div>
							<div id="ToStockLocationID">
								${ToStockLocationName}
								<INPUT name="ToStockLocationID" type="hidden" value="${ToStockLocationID}"></INPUT>
							</div>
						</div>
						<div py:if="ToStockLocationID in ['',None]" class="row">
							<div style="width:200px" class="label"><input id="btnPickToLocationID" type="button" value="To Location" ></input></div>
							<div id="ToLocationID">
								${ToLocationName}
								<INPUT name="ToLocationID" type="hidden" value="${ToLocationID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Stock Transfer Request</div>
							<div >
								<A href="StockTransferRequestsEditor?StockTransferRequestID=${StockTransferRequestID}">${StockTransferRequestName}</A>
								<INPUT type="hidden" name="StockTransferRequestItemID" id="StockTransferRequestItemID" value="${StockTransferRequestItemID}" />
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Quantity</div>
							<div >
								<INPUT id="Qty" name="Qty" type="text" value="${Qty}" size="30" />
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Date Transferred</div>
							<div >
								<INPUT id="DateTransferred" name="DateTransferred" type="text" value="${DateTransferred}" size="30" class="dateEntry"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Completed</div>
							<div>${CompletedStatus}
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table; width=600px" class="topbuttons">
						<input id="StockTransferID" type="hidden" name="StockTransferID" value="${StockTransferID}" />
						<input id="FromLocationID" type="hidden" name="FromLocationID" value="${FromLocationID}" />
						<input py:if="CanComplete" name="Operation" id="btnComplete" type="submit" value="Complete" ></input>
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="button" value="Cancel" ></input>
						<input py:if="not StockTransferID in ['',None]" name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input py:if="not StockTransferID in ['',None]" name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="Status == 'deleted'" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
