<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Rooms Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar_custom/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar_custom/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/config_RoomsEditor.js" TYPE="text/javascript"></SCRIPT>
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
				<form name='RoomsEditorForm' action="RoomsEditorSave" method="post">
					<div style="font-size:18px" class="row-blank">${DisplayName}</div>
					<div id="part1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Room Number</div>
							<div><INPUT id="RoomNr" name="RoomNr" type="text" value="${RoomNr}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnDeptNrID" type="button" value="Department" ></input></div>
							<div id="DeptNrID">
								<a py:if="DeptNrID not in [0,'',None]" href="LocationsEditor?DepartmentID=${DeptNrID}">${DeptNrName}</a>
								<span py:if="DeptNrID in [0,'',None]">${DeptNrName}</span>
								<INPUT name="DeptNrID" type="hidden" value="${DeptNrID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnWardNrID" type="button" value="Ward" ></input></div>
							<div id="WardNrID">
								<a href="WardsEditor?WardID=${WardNrID}">${WardNrName}</a>
								<INPUT name="WardNrID" type="hidden" value="${WardNrID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Information</div>
							<div><TEXTAREA name="Info" rows="3" cols="40">${Info}</TEXTAREA>
							</div>
						</div>
					</div>
					<div id="part2" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:300px; padding-left:0px" >
								<div style="width:200px" class="label">Is Temp. Closed</div>
								<div ><INPUT name="IsTempClosed" type="checkbox" checked="${IsTempClosed}"></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:300px" class="label">Number Of Beds</div>
								<div ><INPUT name="NrOfBeds" type="text" value="${NrOfBeds}" size="5"></INPUT></div>
							</div>
						</div>
					</div>
					<div id="part3" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Open/Closed Beds (checked is open)</div>			
							<div >
								<INPUT py:for="bed in ClosedBeds" name="ClosedBeds" type="checkbox" checked="${bed['checked']}" value="${bed['BedNr']}">${bed['BedNr']}</INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Date Created</div>			
							<div ><INPUT id="DateCreate" name="DateCreate" type="text" value="${DateCreate}" size="30" class="dateEntry"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Date Closed</div>			
							<div ><INPUT id="DateClose" name="DateClose" type="text" value="${DateClose}" size="30" class="dateEntry"></INPUT></div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input id="RoomID" type="hidden" name="RoomID" value="${RoomID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="submit" value="Cancel" ></input>
						<input name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="IsDeleted" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
					<div py:if="not RoomID in ['',None]" id="Beds"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="display:table-row">
							<div style="display:table-cell;text-align:center;width:50px">Bed Nr.</div>
							<div style="display:table-cell;text-align:center">Patient name</div>
							<div style="display:table-cell;text-align:center;">Start</div>
							<div style="display:table-cell;text-align:center;">Days in use</div>							
						</div>
						<div py:for="bed in beds" style="display:table-row">
							<div style="display:table-cell;border-top:1px solid gray">
								${bed['BedNr']}
							</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:left">${bed['PatientName']}</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:left;padding-left:10px">${bed['Start']}</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:left;padding-left:10px">${bed['Days']}</div>
						</div>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
