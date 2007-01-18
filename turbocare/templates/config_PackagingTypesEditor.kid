<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Packaging Types Editor')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/javascript/calendar/calendar-green.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/calendar/calendar.js" TYPE="text/javascript">
  </SCRIPT>
    <SCRIPT SRC="/static/javascript/config_PackagingTypesEditor.js" TYPE="text/javascript"></SCRIPT>
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
				<form name='PackagingTypesEditorForm' action="PackagingTypesEditorSave" method="post">
					<div style="font-size:18px" class="row-blank">${DisplayName}</div>
					<div id="part1"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div class="row">
							<div style="width:200px" class="label">Name</div>
							<div><INPUT id="Name" name="Name" type="text" value="${Name}" size="40"></INPUT>
							</div>
						</div>
						<div class="row">
							<div class="label">Description</div>
							<div><TEXTAREA name="Description" rows="3" cols="40">${Description}</TEXTAREA>
							</div>
						</div>
						<div class="row">
							<div style="width:200px" class="label"><input id="btnEditGroups" type="button" value="Groups" ></input></div>
							<div id="Groups">
								<li py:for="group in Groups">${group['name']}</li>
								<INPUT py:for="group in Groups" name="Groups" type="hidden" value="${group['id']}"></INPUT>
							</div>
						</div>
					</div>
					<div id="buttons" style="display:table" class="topbuttons">
						<input id="PackagingID" type="hidden" name="PackagingID" value="${PackagingID}" />
						<input name="Operation" id="btnSave" type="submit" value="Save" ></input>
						<input name="Operation" id="btnCancel" type="submit" value="Cancel" ></input>
						<input name="Operation" id="btnAddNew" type="submit" value="New" ></input>
						<input name="Operation" id="btnDelete" type="submit" value="Delete" ></input>
						<input py:if="IsDeleted" name="Operation" id="btnUnDelete" type="submit" value="Un-Delete" ></input>
					</div>
					<div py:if="PackagingID not in ['',None]" id="LinkedItems"  style="position:relative; width:600px; left:0px; font-size:12px; display:table" class="divtable_input">
						<div style="display:table-row">
							<div style="display:table-cell;text-align:center;width:400px">Item Master entries (catalog items)</div>
						</div>
						<div py:for="item in Items" style="display:table-row">
							<div style="display:table-cell;border-top:1px solid gray;text-align:left">${item['Name']}</div>
						</div>
					</div>
				</form>
			</div>
		</div>
	</DIV>
</body>
</html>
