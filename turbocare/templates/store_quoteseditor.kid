<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Quotes Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar_custom/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar_custom/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/PickList.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/stores_QuotesEditor.js" TYPE="text/javascript"></SCRIPT>
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
				<br/>Quotes (most recent):
				<li py:for="q in latestQs"><a href="QuotesEditor?QuoteID=${q['id']}">${q['name']}</a></li>
				<br/>Quick Search:
				<br/><INPUT id="QuickSearch" name="QuickSearchText" type="text" value="Enter Search Text" size="20"></INPUT>
				<div id="QuickSearchResults">
					<li>No Search Results</li>
				</div>
			</div>
			<div>
				<form name='QuoteForm' action="QuotesSave" method="post">
					<div style="font-size:18px" class="row-blank">${Name } (ID#: ${QuoteID})</div>
					<div id="store1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label"><input id="btnPickVendorID" type="button" value="Vendor" ></input></div>
							<div id="VendorID">
								<a href="VendorsEditor?VendorID=${VendorID}">${VendorName}</a>
								<INPUT name="VendorID" type="hidden" value="${VendorID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnPickQuoteRequestID" type="button" value="Quote Request" ></input></div>
							<div id="QuoteRequestID">
								<a href="QuoteRequestsEditor?QuoteRequestID=${QuoteRequestID}">${QuoteRequestName}</a>
								<INPUT name="QuoteRequestID" type="hidden" value="${QuoteRequestID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Valid On Date</div>
							<div >
								<INPUT id="ValidOn" name="ValidOn" type="text" value="${ValidOn}" size="30" class="dateEntry"></INPUT>
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
							<div style="display:table-cell;text-align:center">Item name</div>
							<div style="display:table-cell;text-align:center">Product name</div>
							<div style="display:table-cell;text-align:center">Price (Rs)</div>
							<div style="display:table-cell;text-align:center">Ranking</div>
							<div style="display:table-cell;text-align:center">Notes</div>
							<div style="display:table-cell;text-align:center">Options</div>
						</div>
						<div py:for="item in items" style="display:table-row">
							<div style="display:table-cell">
								${item['ItemName']}
								<INPUT name="ItemID" type="hidden" value="${item['ItemID']}" />
								<INPUT name="ItemCounter" type="hidden" value="1" />
							</div>
							<div style="display:table-cell">
								<INPUT name="ItemProduct" type="text" value="${item['ItemProduct']}" />
							</div>
							<div style="display:table-cell">
								<INPUT name="ItemPrice" type="text" size="12" value="${item['ItemPrice']}" />
							</div>
							<div style="display:table-cell">
								<INPUT name="ItemRanking" type="text" size="4" value="${item['ItemRanking']}" />
							</div>
							<div style="display:table-cell">
								<INPUT name="ItemNotes" type="text" value="${item['ItemNotes']}" />
							</div>
							<div style="display:table-cell">
								<INPUT type="button" class="delItem" name="Delete" value="Delete" />
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table; width=600px" class="topbuttons">
						<input id="QuoteID" type="hidden" name="QuoteID" value="${QuoteID}" />
						<input py:if="not QuoteID in ['','None']" name="Operation" id="btnAddItems" type="button" value="Add Items" ></input>
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="button" value="Cancel" ></input>
						<input py:if="not QuoteID in ['','None']" name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input py:if="not QuoteID in ['','None']" name="Operation" id="btnCopyToNew" type="submit" value="Copy to New" ></input>
						<input py:if="not QuoteID in ['','None']" name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="Status == 'deleted'" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
