<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
 
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/registration_search.js" TYPE="text/javascript"></SCRIPT>
    <title>Registration Search</title>
</head>
<body>
 	<DIV class="big_text_1">Registration
		<DIV class="big_text_2">Search</DIV>
		<DIV style="height:50px" class="quote"><DIV  style="font-size:18px">To search, either enter a customer id, name, 
		or use the barcode scanner.  Use the Address search box to limit the search.</DIV></DIV>
			<div style="width:50%; left:0px; position:relative; font-size:18px" class="divtable">
				<DIV  class="row" style="font-size:18px">
					<div style="text-align: center" class="clear"><a href="RegistrationPage1">Add a new patient</a></div>
				</DIV>
				<DIV  class="row" style="font-size:18px">
					<div style="text-align: center" class="clear">Or Search</div>
				</DIV>				
				<FORM name="SearchForm" id="SearchForm">
				<div class="row">
					<div style="text-align: right" class="clear">Name</div>
					<div style="text-align: left" class="clear">
						<INPUT id="SearchText" name="SearchText" type="text" value="" size="40"  />
						<INPUT id="btnSearch" name="Search" type="Button" value="Search" />
					</div>
				</div>
				<div class="row">
					<div style="text-align: right" class="clear">Address</div>
					<div style="text-align: left" class="clear"><INPUT id="SearchAddress" name="SearchAddress" type="text" value="" size="40"  /></div>
				</div>
				</FORM>
			</div>
			<DIV id="SearchResults" class="ListItemRow" style="text-align: left; font-size:12px; list-style-type: none"></DIV>
	</DIV>
</body>
</html>
