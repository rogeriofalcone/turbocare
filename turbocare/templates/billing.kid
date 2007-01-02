<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Billing')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/billing.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
  </head>

<body>
	<div id="customer_id" style="display:none" py:content="customer_id">This is replaced.</div>
	<div id="receipt_id" style="display:none" py:content="receipt_id">This is replaced.</div>
	<form name='receiptform'>
		<div id="buttons" class="topbuttons">
			<input id="btnSave" type="button" value="Save" class="invisible"></input>
			<input id="btnNew" type="button" value="New Bill"></input>
			<input id="btnAppend" type="button" value="Append"></input>
			<input id="btnEdit" type="button" value="Edit"></input>
			<input id="btnCancel" type="button" value="Cancel" class="invisible"></input>
			<input id="btnPrint" type="button" value="Print"></input>
		</div>
		<div id="receipt" class="main">
			<div class="title">Receipt information: No Customer Selected</div>
			<div class="billtable">
				<div class="rowtitle">
					<div class="w40">Item</div>
					<div class="w10">Qty</div>
					<div>Rs/Item</div>
					<div class="w15">Total</div>
					<div class="w20">Assigned Stock</div>
					<div class="last"></div>
					<div class="last"></div>
					<div class="last"></div>
					
				</div>
				<div class="rowtotal">
					<div class="w40" style="text-align:right">Total</div>
					<div class="w10"> </div>
					<div> </div>
					<div class="w15" style="text-align:right">0</div>
					<div class="w20"></div>
					<div></div>
					<div></div>
					<div class="last"></div>
				</div>
			</div>
		</div>
	</form>
	<div id="buttons" class="topbuttons">
		<input id="btnPay" type="button" value="Confirm Payment"></input>
		<input id="btnRefund" style="display:none" type="button" value="Refund Cash"></input>
	</div>
	<div id="RightBox" style="top:60px" class="infoboxright"> Information
		<div id="customer_info">Billing information
			<li>Type:</li>
			<li>Firm: </li>
			<li>Number: </li>
		</div>
		<div id="history">History information
		</div>
	</div>
</body>
</html>
