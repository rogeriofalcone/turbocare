<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Stock Transfer Requests Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar_custom/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar_custom/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/stores_StockTransferRequestsEditor.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
    <style type="text/css">
	FillRequest {color: red}
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
				<br/><br/>Requests for items we have:
				<li py:for="item in pendingSTRs"><a href="StockTransferRequestsEditor?StockTransferRequestID=${item['id']}">${item['name']}</a></li>
				<br/>Pending Transfers for our requests:
				<li py:for="item in pendingSTRForUs"><a href="StockTransfersEditor?StockTransferID=${item['id']}">${item['name']}</a></li>
				<br/>Pending Transfers for items we sent:
				<li py:for="item in pendingSTRFromUs"><a href="StockTransfersEditor?StockTransferID=${item['id']}">${item['name']}</a></li>
				<br/>Purchase Orders for items we requested:
				<li py:for="po in pendingPOs"><a href="PurchaseOrdersEditor?PurchaseOrderID=${po['id']}">${po['name']}</a></li>
				<br/>Latest Stock transfer requests by the current user:
				<li py:for="item in latestSTRs"><a href="StockTransferRequestsEditor?StockTransferRequestID=${item['id']}">${item['name']}</a></li>
			</div>
			<div>
				<form name='StockTransferRequestForm' action="StockTransferRequestsSave" method="post">
					<div style="font-size:18px" class="row-blank">${Name} (ID#: ${StockTransferRequestID})</div>
					<div id="store1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Requested By (person)</div>
							<div >
								<INPUT id="RequestedBy" name="RequestedBy" type="text" value="${RequestedBy}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Requested On (read-only)</div>
							<div >
								${RequestedOn}
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Required By (date)</div>
							<div >
								<INPUT id="RequiredBy" name="RequiredBy" type="text" value="${RequiredBy}" size="30" class="dateEntry"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">For Location</div>
							<div>${ForLocation}
							</div>
						</div>
						<div class="row">
							<div class="label">Notes</div>
							<div><TEXTAREA name="Notes" rows="4" cols="40">${Notes}</TEXTAREA>
							</div>
						</div>
					</div>
					<div id="Items"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="display:table-row">
							<div style="display:table-cell;text-align:center;width:150px">Name</div>
							<div style="display:table-cell;text-align:center">Qty</div>
							<div style="display:table-cell;text-align:center">PO Id</div>
							<div style="display:table-cell;text-align:center">Notes</div>
							<div style="display:table-cell;text-align:center">On Order</div>
							<div style="display:table-cell;text-align:center">Completed</div>
							<div style="display:table-cell;text-align:center">Options</div>
						</div>
						<div py:for="item in items" style="display:table-row">
							<div style="display:table-cell;border-top:1px solid gray">
								${item['ItemName']}
								<INPUT name="ItemID" type="hidden" value="${item['ItemID']}" />
								<INPUT name="ItemCounter" type="hidden" value="1" />
							</div>
							<div style="display:table-cell;border-top:1px solid gray">
								<INPUT name="ItemQty" type="text" size="6" value="${item['ItemQty']}" />
							</div>
							<div style="display:table-cell;border-top:1px solid gray">
								<INPUT name="ItemPurchaseOrderID" type="text" size="5" value="${item['ItemPurchaseOrderID']}" />
							</div>
							<div style="display:table-cell;border-top:1px solid gray">
								<INPUT name="ItemNotes" type="text" value="${item['ItemNotes']}" />
							</div>
							<div style="display:table-cell;border-top:1px solid gray">
								<SELECT name="ItemIsOnOrder">
									<OPTION py:if="item['ItemIsOnOrder']" value="True" selected="selected">True</OPTION>
									<OPTION py:if="not item['ItemIsOnOrder']" value="False" selected="selected">False</OPTION>
									<OPTION py:if="not item['ItemIsOnOrder']" value="True">True</OPTION>
									<OPTION py:if="item['ItemIsOnOrder']" value="False">False</OPTION>
								</SELECT>
							</div>
							<div style="display:table-cell;border-top:1px solid gray">
								<SELECT name="ItemIsTransferred">
									<OPTION py:if="item['ItemIsTransferred']" value="True" selected="selected">True</OPTION>
									<OPTION py:if="not item['ItemIsTransferred']" value="False" selected="selected">False</OPTION>
									<OPTION py:if="not item['ItemIsTransferred']" value="True">True</OPTION>
									<OPTION py:if="item['ItemIsTransferred']" value="False">False</OPTION>
								</SELECT>
							</div>
							<div style="display:table-cell;border-top:1px solid gray">
								<INPUT type="button" class="delItem" name="Delete" value="Delete" />
								<INPUT py:if="item['ItemCanFillRequest']" type="button" class="FillRequest" name="Fill" value="Fill" />
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table; width=600px" class="topbuttons">
						<input id="StockTransferRequestID" type="hidden" name="StockTransferRequestID" value="${StockTransferRequestID}" />
						<input py:if="not StockTransferRequestID in ['',None]" name="Operation" id="btnAddItems" type="button" value="Add Items" ></input>
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="button" value="Cancel" ></input>
						<input py:if="not StockTransferRequestID in ['',None]" name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input py:if="not StockTransferRequestID in ['',None]" name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="Status == 'deleted'" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
