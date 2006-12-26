<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Forms Tutorial')}</title>
    <SCRIPT TYPE="text/javascript">
    function doFind(url) {
		window.open(url,"find_window","toolbar=no,location=no,menubar=no,scrollbars=yes,resizable=yes,width=350,height=350")
	};
	</SCRIPT>
	${extra_script}
</head>

<body>
	<div class="notification">${message}</div>
    <p py:content="form(action=action)">Comment form</p>
	<p py:if="defined('list_form')">${list_form.display()}
	<div id="search_result">&nbsp;</div>
	</p>
</body>
</html>
