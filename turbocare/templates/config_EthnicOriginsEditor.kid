<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Ethnic Origins Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar_custom/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar_custom/calendar.js" TYPE="text/javascript">
  </SCRIPT>
      <SCRIPT SRC="/static/javascript/config_EthnicOrigins.js" TYPE="text/javascript"></SCRIPT>
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
			<div>
				<div style="font-size:18px" class="row-blank">Ethnic Origins Classifications Editor (For Tribes Editing, select the "tribe" classification)</div>
				<div id="part1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
					<div class="row">
						<div style="width:200px" class="label">Classifications</div>
						<div>
							<SELECT id="Classification" name="Classification" size="8">
								<OPTION py:for="classif in classifications" value="${classif['id']}" selected="${classif['selected']}">${classif['name']}</OPTION>
							</SELECT>
						</div>
					</div>
					<div class="row">
						<div class="label" id="ClassEditLabel">Selected Classification (Edit Mode)</div>
						<div>
							<INPUT id="EditClassificationName" name="EditClassificationName" type="text" value="${EditClassName}" size="40" />
							<INPUT id="EditClassificationID" name="EditClassificationID" type="hidden" value="${EditClassID}" />
						</div>
					</div>
				</div>
				<div id="buttons" style="display:table" class="topbuttons">
					<input name="Operation" id="btnSaveClass" type="button" value="Save" ></input>
					<input name="Operation" id="btnCancelClass" type="button" value="Cancel" ></input>
					<input name="Operation" id="btnAddNewClass" type="button" value="New" ></input>
					<input name="Operation" id="btnDeleteClass" type="button" value="Delete" ></input>
					<input name="Operation" id="btnUnDeleteClass" type="button" value="Un-Delete" />
				</div>
				<div style="font-size:18px" class="row-blank">Ethnic Origin Types Editor (Linked to the above classification)</div>
				<div id="part2"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
					<div class="row">
						<div style="width:200px" class="label">Types</div>
						<div>
							<SELECT id="EthnicOrigType" name="EthnicOrigType" size="8">
								<OPTION py:for="type in ethnicorigtypes" value="${type['id']}" selected="${type['selected']}">${type['name']}</OPTION>
							</SELECT>
						</div>
					</div>
					<div class="row">
						<div py:if="EditTypeID==''" class="label" id="TypeEditLabel">Selected Type (New Entry)</div>
						<div py:if="EditTypeID!=''" class="label" id="TypeEditLabel">Selected Type (Edit Mode)</div>
						<div>
							<INPUT id="EditTypeName" name="EditTypeName" type="text" value="${EditTypeName}" size="40" />
							<INPUT id="EditTypeID" name="EditTypeID" type="hidden" value="${EditTypeID}" />
						</div>
					</div>
				</div>
				<div id="buttons" style="display:table" class="topbuttons">
					<input name="Operation" id="btnSaveType" type="button" value="Save" ></input>
					<input name="Operation" id="btnCancelType" type="button" value="Cancel" ></input>
					<input name="Operation" id="btnAddNewType" type="button" value="New" ></input>
					<input name="Operation" id="btnDeleteType" type="button" value="Delete" ></input>
					<input name="Operation" id="btnUnDeleteType" type="button" value="Un-Delete" />
				</div>
			</div>
		</div>
	</DIV>
</body>
</html>
