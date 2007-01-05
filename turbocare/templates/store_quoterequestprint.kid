<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Quote Request Print')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
  <SCRIPT SRC="/static/javascript/stores_QuoteRequestsPrint.js" TYPE="text/javascript">
    </SCRIPT>
</head>

<body>
	<DIV style="position:relative; width:100%; left:0px; font-size:12px" class="divtable">
		<div class="row">
			<div>
				<form name='QuoteRequestPrintForm' action="QuoteRequestsEditorPrint" method="post">
					<div style="font-size:18px" class="row-blank">Quote Request (ID#: ${QuoteRequestID})</div>
					<INPUT name="QuoteRequestID" type="hidden" value="${QuoteRequestID}"></INPUT>
					<div id="store1"  style="position:relative; width:800px; left:0px; font-size:12px; display:table" class="divtable_input">
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
							<div class="label">From Address</div>
							<div><TEXTAREA name="FromAddress" rows="4" cols="40">${FromAddress}</TEXTAREA>
							</div>
						</div>
					</div>
					<div id="VendorDetails" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:100px">Vendor</div>
							<div style="width:250px">To Address</div>
							<div style="width:250px">Notes</div>
						</div>
						<div py:for="vendorid, vendorname, vendoraddress, vendornotes in zip(VendorIDs, VendorNames, VendorAddresses, VendorNotes)" class="row">
							<div style="width:100px;background-color:lightgray;vertical-align:top" >
								<BUTTON id="RemoveVendor${vendorid}" type="button" name="RemoveVendor" value="Remove ${vendorname}">Remove ${vendorname}</BUTTON>
								<INPUT type="hidden" name="VendorIDs" value="${vendorid}" />
							</div>
							<div style="width:250px" >
								<TEXTAREA name="VendorAddresses" rows="4" cols="35">${vendoraddress}</TEXTAREA>
							</div>
							<div style="width:250px" >
								<TEXTAREA name="VendorNotes" rows="4" cols="35">${vendornotes}</TEXTAREA>
							</div>
						</div>
					</div>

					<div id="buttons" style="display:table" class="topbuttons">
						<input name="Operation" id="btnPrint" type="submit" value="Print" ></input>
					</div>
				</form>
			</div>
		</div>
		<div py:for="report in reports" class="row">
			Quote Request for: <A href="${report['link']}">${report['name']}</A>
		</div>
	</DIV>
</body>
</html>
