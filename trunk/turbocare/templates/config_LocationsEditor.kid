<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Department/Locations Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/config_LocationsEditor.js" TYPE="text/javascript"></SCRIPT>
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
				<form name='LocationsEditorForm' action="LocationsEditorSave" method="post">
					<div id="part1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="font-size:18px" class="row-blank">${DisplayName}</div>
						<div class="row">
							<div style="width:200px" class="label">Name</div>
							<div><INPUT id="Name" name="Name" type="text" value="${Name}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Description</div>
							<div><TEXTAREA name="Description" rows="4" cols="40">${Description}</TEXTAREA>
							</div>
						</div>
					</div>
					
					<div id="part2" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px; padding-left:0px" >
								<div style="width:200px" class="label">Is Store</div>
								<div ><INPUT name="IsStore" type="checkbox" checked="${IsStore}"></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">Can Receive</div>
								<div ><INPUT name="CanReceive" type="checkbox" checked="${CanReceive}" ></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">Can Sell</div>
								<div ><INPUT name="CanSell" type="checkbox" checked="${CanSell}"></INPUT></div>
							</div>
						</div>
					</div>
					<div id="part3" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px; padding-left:0px" >
								<div style="width:200px" class="label">Is Consumed</div>
								<div ><INPUT name="IsConsumed" type="checkbox" checked="${IsConsumed}"></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">Admit Inpatient</div>
								<div ><INPUT name="AdmitInpatient" type="checkbox" checked="${AdmitInpatient}" ></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">Admit Outpatient</div>
								<div ><INPUT name="AdmitOutpatient" type="checkbox" checked="${AdmitOutpatient}"></INPUT></div>
							</div>
						</div>
					</div>
					<div id="part4" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px; padding-left:0px" >
								<div style="width:200px" class="label">Has On call Doc</div>
								<div ><INPUT name="HasOncallDoc" type="checkbox" checked="${HasOncallDoc}"></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">Has On call Nurse</div>
								<div ><INPUT name="HasOncallNurse" type="checkbox" checked="${HasOncallNurse}" ></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">Does Surgery</div>
								<div ><INPUT name="DoesSurgery" type="checkbox" checked="${DoesSurgery}"></INPUT></div>
							</div>
						</div>
					</div>
					<div id="part5" style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px; padding-left:0px" >
								<div style="width:200px" class="label">This Institution</div>
								<div ><INPUT name="ThisInstitution" type="checkbox" checked="${ThisInstitution}"></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">Is Sub Dept</div>
								<div ><INPUT name="IsSubDept" type="checkbox" checked="${IsSubDept}" ></INPUT></div>
							</div>
							<div style="width:200px" >
								<div style="width:200px" class="label">Is Inactive</div>
								<div ><INPUT name="IsInactive" type="checkbox" checked="${IsInactive}"></INPUT></div>
							</div>
						</div>
					</div>
						
						
					<div id="part6"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">						
						<div class="row">
							<div class="label">Department Type</div>			
							<div >
								<SELECT name="Type" id="Type">
									<OPTION py:for="type in types" value="${type['id']}" selected="${type['selected']}">${type['name']}</OPTION>
								</SELECT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnEditLocationGroups" type="button" value="Location Groups" ></input></div>
							<div id="LocationGroups">
								<li py:for="locationgroup in locationgroups">${locationgroup['name']}</li>
								<INPUT py:for="locationgroup in locationgroups" name="LocationGroups" type="hidden" value="${locationgroup['id']}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Work Hours</div>			
							<div ><INPUT name="WorkHours" type="text" value="${WorkHours}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Consult Hours</div>			
							<div ><INPUT name="ConsultHours" type="text" value="${ConsultHours}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Address</div>
							<div><TEXTAREA name="Address" rows="4" cols="40">${Address}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnParentDeptNrID" type="button" value="Parent Department" ></input></div>
							<div id="ParentDeptNrID">
								${ParentDeptNrName}
								<INPUT name="ParentDeptNrID" type="hidden" value="${ParentDeptNrID}"></INPUT>
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input id="LocationID" type="hidden" name="LocationID" value="${LocationID}" />
						<input id="DepartmentID" type="hidden" name="DepartmentID" value="${DepartmentID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="submit" value="Cancel" ></input>
						<input name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="IsDeleted" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
					<div py:if="(not DispPermissionExists) or (not StorePermissionExists)" id="buttons" style="display:table;background-color:pink">
						<div py:if="not DispPermissionExists" style="display:table-row;">
							<br/>The permission "${PermDisp}" does not exist yet.  If you want to access this location for Inventory Dispensing (such as a 
							pharmacy dispensing counter), then you'll need to create this permission and assign groups to it.
						</div>
						<div py:if="not StorePermissionExists" style="display:table-row;" >
							<br/>The permission "${PermStore}" does not exist yet.  If you want to access this location for Inventory Management (such as
							stock transfers, or possibly Purchase Orders), then you'll need to create this permission and assign groups to it.
						</div>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
