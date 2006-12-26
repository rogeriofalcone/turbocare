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
				<form name='registrationform' action="RegistrationPage2Save" method="post">
					<div style="position:relative; left:25px;">
						<div id="registration1" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
							<div class="row">
								<div style="width:200px" class="label">Relative Name</div>
								<div ><INPUT id="ContactPerson" name="ContactPerson" type="text" value="${ContactPerson}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div class="label">Relative Relationship</div>
								${ContactRelationLookup.display()}
							</div>
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
						</div>
						<div id="registration2" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row">
								<div style="width:200px;" class="label">Occupation</div>
								${OccupationLookup.display()}
							</div>
							<div class="row">
								<div style="width:200px" class="label">Home Phone</div>
								<div ><INPUT name="Phone1Nr" type="text" value="${Phone1Nr}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div class="label">Cell Phone</div>
								<div ><INPUT name="Cellphone1Nr" type="text" value="${Cellphone1Nr}" size="40"></INPUT></div>
							</div>
							<div class="row">
								<div class="label">E-mail</div>
								<div ><INPUT name="Email" type="text" value="${Email}" size="40"></INPUT></div>
							</div>
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
						</div>
						<div id="registration4" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
							<div class="row">
								<div style="width:200px" class="label">Financial classification</div>
								<div><SELECT name="FinancialClassNr">
										<OPTION py:for="financialclassnr in financialclassnrs" value="${financialclassnr['id']}" selected="${financialclassnr['selected']}">${financialclassnr['name']}</OPTION>
									</SELECT>
								</div>
							</div>
						</div>
						<div id="registration5" style="position:static; width:600px; font-size:12px" class="divtable_input">
							<div class="row-blank">&nbsp;&nbsp;&nbsp;&nbsp;</div>
							<div class="row">
								<div style="width:200px" class="label">Type of visit</div>
								<div>
									<INPUT py:for="encountertype in encountertypes" type="radio" name="EncounterType" value="${encountertype['id']}" checked="${encountertype['selected']}">${encountertype['name']}</INPUT>
								</div>
							</div>
						</div>
						<div id="buttons" class="topbuttons">
							<input type="hidden" name="PatientID" value="${PatientID}" />
							<input type="hidden" name="CustomerID" value="${CustomerID}" />
							<input type="hidden" name="EncounterID" value="${EncounterID}" />
							<input type="hidden" name="ReceiptID" value="${ReceiptID}" />
							<input id="btnOutpatient" type="submit" name="btnNext" value="Outpatient" ></input>
							<input id="btnInpatient" type="submit" name="btnNext" value="Inpatient" ></input>
						</div>
					</div>
				</form>
				<div id="history" style="top:75px; left:650px" class="infoboxright">Patient information
					<li py:for="line in history">${line}</li>
				</div>
</body>
</html>
