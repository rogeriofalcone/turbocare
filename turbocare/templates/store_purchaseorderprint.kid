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
			<div>
				<form name='PurchaseOrderPrintForm' action="PurchaseOrdersEditorPrint" method="post">
					<div style="font-size:18px" class="row-blank">Purchase Order (ID#: ${PurchaseOrderID})</div>
					<INPUT name="PurchaseOrderID" type="hidden" value="${PurchaseOrderID}"></INPUT>
					<div id="store1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div class="label">Prepared by</div>			
							<div ><INPUT name="PreparedBy" type="text" value="${PreparedBy}" size="30"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Checked by</div>			
							<div ><INPUT name="CheckedBy" type="text" value="${CheckedBy}" size="30"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Approved by</div>			
							<div ><INPUT name="ApprovedBy" type="text" value="${ApprovedBy}" size="30"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">To Address</div>
							<div><TEXTAREA name="ToAddress" rows="4" cols="40">${ToAddress}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">From Address</div>
							<div><TEXTAREA name="FromAddress" rows="4" cols="40">${FromAddress}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">Delivery Instructions</div>
							<div><TEXTAREA name="DeliveryInstructions" rows="4" cols="40">${DeliveryInstructions}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">Packing and Forwarding</div>
							<div><TEXTAREA name="PackingAndForwarding" rows="4" cols="40">${PackingAndForwarding}</TEXTAREA>
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input name="Operation" id="btnPrint" type="submit" value="Print" ></input>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
