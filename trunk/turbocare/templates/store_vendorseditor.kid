<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Vendors Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar_custom/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar_custom/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/stores_VendorsEditor.js" TYPE="text/javascript"></SCRIPT>
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
			<div style="vertical-align:top; width:200px">
				<br/>Purchase orders (most recent):
				<li py:for="po in latestPOs"><a href="PurchaseOrdersEditor?PurchaseOrderID=${po['id']}">${po['name']}</a></li>
				<br/>Quotes (most recent):
				<li py:for="q in latestQs"><a href="QuotesEditor?QuoteID=${q['id']}">${q['name']}</a></li>
				<br/>Quote Requests (most recent):
				<li py:for="q in latestQRs"><a href="QuoteRequestsEditor?QuoteRequestID=${q['id']}">${q['name']}</a></li>
				<br/>Quick Search:
				<br/><INPUT id="QuickSearch" name="QuickSearchText" type="text" value="Enter Search Text" size="20"></INPUT>
				<div id="QuickSearchResults">
					<li>No Search Results</li>
				</div>
			</div>
			<div>
				<form name='VendorForm' action="VendorsSave" method="post">
					<div style="font-size:18px" class="row-blank">${Name} (ID#: ${VendorID})</div>
					<div id="store1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Name</div>
							<div >
								<INPUT id="Name" name="Name" type="text" value="${Name}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Description</div>
							<div><TEXTAREA name="Description" rows="3" cols="40">${Description}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">Delivery Instructions</div>
							<div><TEXTAREA name="DeliveryInstructions" rows="3" cols="40">${DeliveryInstructions}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Contact Name</div>
							<div >
								<INPUT id="ContactName" name="ContactName" type="text" value="${ContactName}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Phone 1</div>
							<div >
								<INPUT id="Phone1" name="Phone1" type="text" value="${Phone1}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Phone 2</div>
							<div >
								<INPUT id="Phone2" name="Phone2" type="text" value="${Phone2}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Fax</div>
							<div >
								<INPUT id="Fax" name="Fax" type="text" value="${Fax}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Email 1</div>
							<div >
								<INPUT id="EMail1" name="EMail1" type="text" value="${EMail1}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Email 2</div>
							<div >
								<INPUT id="EMail2" name="EMail2" type="text" value="${EMail2}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnPickCityID" type="button" value="City" ></input></div>
							<div id="CityID">
								<a href="AddressCitytownsEditor?CityID=${CityID}">${CityName}</a>
								<INPUT name="CityID" type="hidden" value="${CityID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Address Label</div>
							<div><TEXTAREA name="AddressLabel" rows="4" cols="40">${AddressLabel}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Avg. Delivery Time (in days)</div>
							<div >
								<INPUT id="OrderDays" name="OrderDays" type="text" value="${OrderDays}" size="30"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnEditGroups" type="button" value="Groups" ></input></div>
							<div id="Groups">
								<li py:for="group in groups">${group['name']}</li>
								<INPUT py:for="group in groups" name="Groups" type="hidden" value="${group['id']}"></INPUT>
								<INPUT py:for="group in groups" name="GroupsCounter" type="hidden" value="1" />
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table; width=600px" class="topbuttons">
						<input id="VendorID" type="hidden" name="VendorID" value="${VendorID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="button" value="Cancel" ></input>
						<input py:if="not VendorID in ['','None']" name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input py:if="not VendorID in ['','None']" name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="Status == 'deleted'" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
