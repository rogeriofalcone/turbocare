<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Doctors Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar_custom/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar_custom/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/config_DoctorsEditor.js" TYPE="text/javascript"></SCRIPT>
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
				<form name='DoctorsEditorForm' action="DoctorsEditorSave" method="post">
					<div style="font-size:18px" class="row-blank">${DisplayName}</div>
					<div id="part1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div py:if="PersonID in ['',None]" class="row">
							<div style="width:200px" class="label"><input id="btnPersonID" type="button" value="Person Record" ></input></div>
							<div id="PersonID">
								If the doctor you are adding exists in the system (customer or past patient) then link them with this option instead of
								creating a new person entry for the Doctor.
								<INPUT name="PersonID" type="hidden" value="${PersonID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Is Discharged</div>
							<div><INPUT name="IsDischarged" type="checkbox" checked="${IsDischarged}" />
							</div>
						</div>
					</div>
					<div id="part2"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Title</div>
							<div><SELECT name="Title">
									<OPTION py:for="title in titles" value="${title['id']}" selected="${title['selected']}">${title['name']}</OPTION>
								</SELECT>
							</div>
						</div>
						<div class="row">
							<div class="label">First name</div>
							<div ><INPUT name="NameFirst" type="text" value="${NameFirst}" size="40"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Middle name</div>
							<div ><INPUT name="NameMiddle" type="text" value="${NameMiddle}" size="40"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Last name</div>
							<div ><INPUT name="NameLast" type="text" value="${NameLast}" size="40"></INPUT></div>
						</div>
						<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
					</div>
					<div id="part3"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" >
								<div style="width:300px" class="label">Age</div>
								<div ><INPUT id="Age" type="text" name="Age" size="3" value="${Age}"></INPUT></div>
							</div>
							<div style="width:300px">
								<div style="width:200px" class="label">Birthdate</div>
								<div ><INPUT id='DateBirth' type="text" name="DateBirth" size="15" value="${DateBirth}" class="dateEntry"></INPUT></div>
							</div>
						</div>
					</div>
					<div id="part4"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" >
								<div style="width:200px" class="label">Gender</div>
								<div ><SELECT name="Gender" size="3">
										<OPTION py:for="gender in genders" value="${gender['name']}" selected="${gender['selected']}">${gender['name']}</OPTION>
									</SELECT>
								</div>
							</div>
							<div style="width:200px">
								<div style="width:200px" class="label">Religion</div>
								<div><SELECT name="Religion" size="3">
										<OPTION py:for="religion in religions" value="${religion['id']}" selected="${religion['selected']}">${religion['name']}</OPTION>
									</SELECT>
								</div>
							</div>
							<div style="width:200px">
								<div style="width:200px" class="label">Tribe</div>
								<div><SELECT name="Tribe" size="3">
										<OPTION py:for="tribe in tribes" value="${tribe['id']}" selected="${tribe['selected']}">${tribe['name']}</OPTION>
									</SELECT>
								</div>
							</div>
						</div>
					</div>
					<div id="part5"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
						<div class="row">
							<div class="label">Street Address</div>
							<div ><INPUT id="AddressStreet" name="AddressStreet" type="text" value="${AddressStreet}" size="40"></INPUT></div>
						</div>
						<div class="row">
							<div style="width:200px" class="label">Find City</div>
							<div>
								<input id="btnCityTown" name="btnCityTown" type="button" value="Find City"></input>
								<div id="SelectedCity" style="display:inline;border:none;font-size:10px">${SelectedCity}</div>
							</div>
						</div>
						<div class="row">
							<div class="label">City/town</div>
							<div ><INPUT id="CityTownName" name="CityTownName" type="text" value="${CityTownName}" size="40"></INPUT>
								<INPUT id="AddrCitytownNrID" name="AddrCitytownNrID" type="hidden" value="${AddrCitytownNrID}"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Post office</div>
							<div ><INPUT id="PostOffice" name="PostOffice" type="text" value="${PostOffice}" size="40"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Block</div>
							<div ><INPUT id="Block" name="Block" type="text" value="${Block}" size="40"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Ditrict</div>
							<div ><INPUT id="District" name="District" type="text" value="${District}" size="40"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">State</div>
							<div ><INPUT id="State" name="State" type="text" value="${State}" size="40"></INPUT></div>
						</div>
						<div class="row">
							<div class="label">Country</div>
							<div ><INPUT id="Country" name="Country" type="text" value="${Country}" size="40"></INPUT></div>
						</div>			
					</div>
					<div id="SaveInformation"  style="background: pink; position:relative; width:600px; left:0px; font-size:12px; display:none" class="divtable_input">
						You've selected a person from previously entered data to be a Doctor.  To make this person a Doctor in the system, press 'Save'.  If, after
						pressing save you realize that it was the wrong person, you can use the "Delete" button to remove the person as a Doctor.  This does
						not remove the person from the system, it just removes them from the list of Doctors.  After saving the record, you will be able to edit
						the Doctor's details in the edit screen.
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<INPUT py:if="PersonID not in ['',None]" name="PersonID" type="hidden" value="${PersonID}"></INPUT>
						<input id="PersonellID" type="hidden" name="PersonellID" value="${PersonellID}" />
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
