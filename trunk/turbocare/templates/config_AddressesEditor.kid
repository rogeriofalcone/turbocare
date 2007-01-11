<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Address Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/config_AddressesEditor.js" TYPE="text/javascript"></SCRIPT>
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
				Quick Search:
				<br/><INPUT id="QuickSearch" name="QuickSearchText" type="text" value="Enter Search Text" size="20"></INPUT>
				<div id="QuickSearchResults">
					<li>No Search Results</li>
				</div>
			</div>
			<div>
				<form name='AddressesEditorForm' action="AddressesEditorSave" method="post">
					<div id="part1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="font-size:18px" class="row-blank">${DisplayName}</div>
						<div class="row">
							<div style="width:200px" class="label">City Name</div>
							<div><INPUT id="Name" name="Name" type="text" value="${Name}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Block/Locality (within city/town if applicable)</div>
							<div><INPUT name="Block" type="text" value="${Block}" size="40" />
							</div>
						</div>
						<div class="row">
							<div class="label">PIN Code</div>			
							<div ><INPUT name="ZipCode" type="text" value="${ZipCode}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">District</div>			
							<div ><INPUT name="District" type="text" value="${District}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">State</div>			
							<div ><INPUT name="State" type="text" value="${State}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Country Code</div>			
							<div ><INPUT name="IsoCountryId" type="text" value="${IsoCountryId}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">UN ECE Modifier [optional]</div>			
							<div ><INPUT name="UneceModifier" type="text" value="${UneceModifier}" size="2"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">UN ECE LO Code [optional]</div>			
							<div ><INPUT name="UneceLocode" type="text" value="${UneceLocode}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">UN ECE LO Code Type</div>			
							<div ><INPUT name="UneceLocodeType" type="text" value="${UneceLocodeType}" size="10"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">UN ECE Coordinates</div>			
							<div ><INPUT name="UneceCoordinates" type="text" value="${UneceCoordinates}" size="25"></INPUT>
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input id="AddressID" type="hidden" name="AddressID" value="${AddressID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="submit" value="Cancel" ></input>
						<input name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="IsDeleted" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
