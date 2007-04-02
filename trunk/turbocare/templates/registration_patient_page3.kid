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
		<DIV py:if="PatientClass == 'Inpatient'" style="position:relative; left:0px">
				<form name='registrationform' action="RegistrationPage3Save" method="post">
					<div style="position:relative; left:25px;">
						<div id="registration3" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
							<div style="width:200px" class="row">
								<div style="width:200px" class="label">Ward</div>
								<div ><SELECT id="Ward" name="Ward" size="5">
										<OPTION py:for="ward in wards" value="${ward['id']}" selected="${ward['selected']}">${ward['name']}</OPTION>
									</SELECT>
								</div>
							</div>
							<div style="width:200px" class="row">
								<div style="width:200px" class="label">Room</div>
								<div><SELECT id="Room" name="Room"  size="5">
										<OPTION py:for="room in rooms" value="${room['id']}" selected="${room['selected']}">${room['name']}</OPTION>
									</SELECT>
								</div>
							</div>
							<div style="width:200px" class="row">
								<div style="width:200px" class="label">Bed</div>
								<div><SELECT id="Bed" name="Bed"  size="5">
										<OPTION py:for="bed in beds" value="${bed['id']}" selected="${bed['selected']}">${bed['name']}</OPTION>
									</SELECT>
								</div>
							</div>
						</div>
						<div py:if="Referrer == True" id="registration1" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
							<div class="row">
								<div style="width:200px" class="label">Referring Institution</div>
								<div ><INPUT name="ReferrerInstitution" type="text" value="${ReferrerInstitution}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referring Doctor</div>
								<div ><INPUT name="ReferrerDr" type="text" value="${ReferrerDr}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referring Department</div>
								<div ><INPUT name="ReferrerDept" type="text" value="${ReferrerDept}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referrer Diagnosis</div>
								<div ><INPUT name="ReferrerDiagnosis" type="text" value="${ReferrerDiagnosis}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referrer Recomended Therapy</div>
								<div ><INPUT name="ReferrerRecomTherapy" type="text" value="${ReferrerRecomTherapy}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referrer Notes</div>
								<div ><INPUT name="ReferrerNotes" type="text" value="${ReferrerNotes}" size="40"></INPUT></div>
							</div>
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
						</div>

						<div id="registration5" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
							<div class="row">
								<div style="width:200px" class="label">Booklet label printing</div>
								<div ><INPUT name="BookletPrinting" type="checkbox" checked="${BookletPrinting}" size="40"></INPUT></div>
							</div>
						</div>
						<div id="buttons" style="position:static" class="topbuttons">
							<input type="hidden" name="PatientID" id="PatientID" value="${PatientID}" />
							<input type="hidden" name="PatientClass" value="${PatientClass}" />
							<input type="hidden" name="CustomerID" id="CustomerID" value="${CustomerID}" />
							<input type="hidden" name="EncounterID" id="EncounterID" value="${EncounterID}" />
							<input type="hidden" name="ReceiptID" id="ReceiptID" value="${ReceiptID}" />
							<input id="btnOutpatient" type="submit" name="btnNext" value="Billing" ></input>
						</div>
					</div>
				</form>
		</DIV>
		<DIV py:if="PatientClass == 'Outpatient'">
				<form name='registrationform' action="RegistrationPage3Save" method="post">
					<div style="position:relative; left:25px;">
						<div py:if="Referrer == True" id="registration1" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
							<div class="row">
								<div style="width:200px" class="label">Referring Institution</div>
								<div ><INPUT name="ReferrerInstitution" type="text" value="${ReferrerInstitution}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referring Doctor</div>
								<div ><INPUT name="ReferrerDr" type="text" value="${ReferrerDr}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referring Department</div>
								<div ><INPUT name="ReferrerDept" type="text" value="${ReferrerDept}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referrer Diagnosis</div>
								<div ><INPUT name="ReferrerDiagnosis" type="text" value="${ReferrerDiagnosis}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referrer Recomended Therapy</div>
								<div ><INPUT name="ReferrerRecomTherapy" type="text" value="${ReferrerRecomTherapy}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Referrer Notes</div>
								<div ><INPUT name="ReferrerNotes" type="text" value="${ReferrerNotes}" size="40"></INPUT></div>
							</div>
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
						</div>
						<div id="registration4" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
							<div class="row">
								<div style="width:200px" class="label">Consultation Queue</div>
								<div><SELECT id="Queue" name="Queue">
										<OPTION py:for="queue in queues" value="${queue['id']}" selected="${queue['selected']}">${queue['name']}</OPTION>
									</SELECT>
								</div>
							</div>
							<div class="row">
								<div style="width:200px" class="label">Assign Doctor</div>
								${DoctorLookup.display()}
							</div>
						</div>
						<div id="registration5" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
							<div class="row">
								<div style="width:200px" class="label">Booklet label printing</div>
								<div ><INPUT name="BookletPrinting" type="checkbox" checked="${BookletPrinting}" size="40"></INPUT></div>
							</div>
						</div>
						<div id="buttons" style="position:static; width:600px" class="topbuttons">
							<input type="hidden" name="PatientID" id="PatientID" value="${PatientID}" />
							<input type="hidden" name="PatientClass" value="${PatientClass}" />
							<input type="hidden" name="CustomerID" id="CustomerID" value="${CustomerID}" />
							<input type="hidden" name="EncounterID" id="EncounterID" value="${EncounterID}" />
							<input type="hidden" name="ReceiptID" id="ReceiptID" value="${ReceiptID}" />
							<input id="btnOutpatient" type="submit" name="btnNext" value="Billing" ></input>
						</div>
					</div>
				</form>
		</DIV>
				<div id="history" style="top:75px; left:650px" class="infoboxright">Patient information
					<li py:for="line in history">${line}</li>
				</div>
</body>
</html>
