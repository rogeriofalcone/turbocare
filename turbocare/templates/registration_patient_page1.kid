<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Patient Registration')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/registration.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
  </head>

<body>
				<form name='registrationform' action="RegistrationPage1Save" method="post">
					<div id="registration1" style="position:relative; width:600px; left:25px; font-size:12px" class="divtable_input">
						<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
						<div class="row">
							<div style="width:200px" class="label">Patient type</div>
							<div><SELECT name="PatientType" id="PatientType">
									<OPTION py:for="patienttype in patienttypes" value="${patienttype['id']}" selected="${patienttype['selected']}">${patienttype['name']}</OPTION>
								</SELECT>
							</div>
						</div>
						<div class="row">
							<div class="label">Insurance provider</div>
							<div><SELECT name="Firm">
									<OPTION py:for="firm in firms" value="${firm['id']}" selected="${firm['selected']}">${firm['name']}</OPTION>
								</SELECT>
							</div>
						</div>
						<div class="row">
							<div class="label">Insurance number</div>			
							<div ><INPUT name="InsuranceNumber" type="text" value="${InsuranceNumber}" size="40"></INPUT></div>
						</div>
						<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
						<div class="row">
							<div class="label">Title</div>
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
					<div id="registration2" style="position:relative; width:600px; left:25px; font-size:12px" class="divtable_input">
						<div class="row">
							<div style="width:200px" >
								<div style="width:300px" class="label">Age</div>
								<div ><INPUT id="Age" type="text" name="Age" size="3" value="${Age}"></INPUT></div>
							</div>
							<div style="width:300px">
								<div style="width:200px" class="label">Birthdate</div>
								<div ><INPUT id='DateBirth' type="text" name="DateBirth" size="15" readonly="1" value="${DateBirth}"></INPUT></div>
							</div>
						</div>
					</div>
					<div id="registration3" style="position:relative; width:600px; left:25px; font-size:12px" class="divtable_input">
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
					<div id="registration4" style="position:relative; width:600px; left:25px; font-size:12px" class="divtable_input">
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
					<div id="buttons" class="topbuttons">
						<input type="hidden" name="PatientID" value="${PatientID}" />
						<input type="hidden" name="CustomerID" value="${CustomerID}" />
						<input id="btnSave" type="submit" value="Save/Next" ></input>
						<input id="btnCancel" type="button" value="Cancel" ></input>
					</div>
					</form>
				<div id="history" style="top:130px; left:650px" class="infoboxright">Patient information
					<li py:for="line in history">${line}</li>
				</div>
</body>
</html>
