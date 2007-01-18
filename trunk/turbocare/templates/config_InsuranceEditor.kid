<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Insurance Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/config_InsuranceEditor.js" TYPE="text/javascript"></SCRIPT>
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
			<div style="vertical-align:top; width:200px">
				Quick Search:
				<br/><INPUT id="QuickSearch" name="QuickSearchText" type="text" value="Enter Search Text" size="20"></INPUT>
				<div id="QuickSearchResults">
					<li>No Search Results</li>
				</div>
			</div>
			<div>
				<form name='InsuranceEditorForm' action="InsuranceEditorSave" method="post">
					<div style="font-size:18px" class="row-blank">${DisplayName}</div>
					<div id="part1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Name</div>
							<div><INPUT id="Name" name="Name" type="text" value="${Name}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Address</div>
							<div><TEXTAREA name="Addr" rows="3" cols="40">${Addr}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">Mailing Address (if different from above)</div>
							<div><TEXTAREA name="AddrMail" rows="3" cols="40">${AddrMail}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">Billing Address (if different from above)</div>
							<div><TEXTAREA name="AddrBilling" rows="3" cols="40">${AddrBilling}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Country Code (IND)</div>
							<div><INPUT id="IsoCountryId" name="IsoCountryId" type="text" value="${IsoCountryId}" size="3"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Sub-Area (Optional)</div>
							<div><INPUT id="SubArea" name="SubArea" type="text" value="${SubArea}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">E-mail Address</div>
							<div><INPUT id="AddrEmail" name="AddrEmail" type="text" value="${AddrEmail}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Phone (main)</div>
							<div><INPUT id="PhoneMain" name="PhoneMain" type="text" value="${PhoneMain}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Phone (other)</div>
							<div><INPUT id="PhoneAux" name="PhoneAux" type="text" value="${PhoneAux}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Fax (main)</div>
							<div><INPUT id="FaxMain" name="FaxMain" type="text" value="${FaxMain}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Fax (other)</div>
							<div><INPUT id="FaxAux" name="FaxAux" type="text" value="${FaxAux}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Contact Person</div>
							<div><INPUT id="ContactPerson" name="ContactPerson" type="text" value="${ContactPerson}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Contact Phone</div>
							<div><INPUT id="ContactPhone" name="ContactPhone" type="text" value="${ContactPhone}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Contact Fax</div>
							<div><INPUT id="ContactFax" name="ContactFax" type="text" value="${ContactFax}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Contact E-mail</div>
							<div><INPUT id="ContactEmail" name="ContactEmail" type="text" value="${ContactEmail}" size="40"></INPUT>
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input id="FirmID" type="hidden" name="FirmID" value="${FirmID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="submit" value="Cancel" ></input>
						<input name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="IsDeleted" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
					<div py:if="FirmID not in ['',None]" id="InsuranceUsers"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="display:table-row">
							<div style="display:table-cell;text-align:center;width:400px">Name</div>
							<div style="display:table-cell;text-align:center">Date of Use</div>
						</div>
						<div py:for="person in InsuranceUsers" style="display:table-row">
							<div style="display:table-cell;border-top:1px solid gray;text-align:left">${person['PersonName']}</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:left;padding-left:10px">${person['EncounterDate']}</div>
						</div>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
