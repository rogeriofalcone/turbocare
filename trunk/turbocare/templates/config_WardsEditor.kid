<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Wards Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar_custom/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar_custom/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/config_WardsEditor.js" TYPE="text/javascript"></SCRIPT>
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
				<form name='WardsEditorForm' action="WardsEditorSave" method="post">
					<div style="font-size:18px" class="row-blank">${DisplayName}</div>
					<div id="part1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Name</div>
							<div><INPUT id="Name" name="Name" type="text" value="${Name}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnDeptNrID" type="button" value="Department" ></input></div>
							<div id="DeptNrID">
								<a href="LocationsEditor?DepartmentID=${DeptNrID}">${DeptNrName}</a>
								<INPUT id="DeptNrIDval" name="DeptNrID" type="hidden" value="${DeptNrID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Description</div>
							<div><TEXTAREA name="Description" rows="3" cols="40">${Description}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div class="label">Info</div>
							<div><TEXTAREA name="Info" rows="3" cols="40">${Info}</TEXTAREA>
							</div>
						</div>
					</div>
					<div id="part2" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:150px; padding-left:0px" >
								<div style="width:150px" class="label">Is Temp. Closed</div>
								<div ><INPUT name="IsTempClosed" type="checkbox" checked="${IsTempClosed}"></INPUT></div>
							</div>
							<div style="width:150px" >
								<div style="width:150px" class="label">Room Nr. Start</div>
								<div ><INPUT name="RoomNrStart" type="text" value="${RoomNrStart}" size="5"></INPUT></div>
							</div>
							<div style="width:150px" >
								<div style="width:150px" class="label">Room Nr. End</div>
								<div ><INPUT name="RoomNrEnd" type="text" value="${RoomNrEnd}" size="5"></INPUT></div>
							</div>
							<div style="width:150px" >
								<div style="width:150px" class="label">Room prefix</div>
								<div ><INPUT name="Roomprefix" type="text" value="${Roomprefix}" size="4"></INPUT></div>
							</div>
						</div>
					</div>
					<div id="part3" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="width:200px" class="row">
							<div class="label">Date Created</div>			
							<div ><INPUT id="DateCreate" name="DateCreate" type="text" value="${DateCreate}" size="30" class="dateEntry"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Date Closed</div>			
							<div ><INPUT id="DateClose" name="DateClose" type="text" value="${DateClose}" size="30" class="dateEntry"></INPUT></div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input id="WardID" type="hidden" name="WardID" value="${WardID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnSaveNoRoom" type="submit" value="Save (No Room Updates)" ></input>
						<input name="Operation" id="btnCancel" type="submit" value="Cancel" ></input>
						<input name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="IsDeleted" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
					<div py:if="not WardID in ['',None]" id="Rooms"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="display:table-row">
							<div style="display:table-cell;text-align:center;width:50px">Room Nr.</div>
							<div style="display:table-cell;text-align:center;width:70px">Nr. of beds</div>
							<div style="display:table-cell;text-align:center">Status</div>
						</div>
						<div py:for="room in rooms" style="display:table-row">
							<div style="display:table-cell;border-top:1px solid gray">
								<A py:if="not room['RoomID'] in ['',None]" href="RoomsEditor?RoomID=${room['RoomID']}">${room['RoomNr']}</A>
								<SPAN py:if="room['RoomID'] in ['',None]">${room['RoomNr']}</SPAN>
							</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:right">${room['NrOfBeds']}</div>
							<div style="display:table-cell;border-top:1px solid gray;text-align:left;padding-left:10px">${room['Status']}</div>
						</div>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
