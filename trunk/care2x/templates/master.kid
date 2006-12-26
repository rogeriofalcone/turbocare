<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/> 
    <title py:replace="''">Care2x CIHSR Implementation</title> 
    <SCRIPT SRC="/static/javascript/MochiKit.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/userMenu.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/static/javascript/validate.js" TYPE="text/javascript"></SCRIPT>
   <link rel="stylesheet" href="/static/css/custom.css" type="text/css" />
    <meta py:replace="item[:]"/> 
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
    <div py:if="tg.config('identity.on',False) and not 'logging_in' in locals()"
        id="pageLogin">
        <span py:if="tg.identity.anonymous">
            <a href="/login">Login</a>
        </span>
        <span py:if="not tg.identity.anonymous">
            Welcome ${tg.identity.user.display_name}.
            <a href="/logout">Logout</a>
        </span>
    </div>
    <div id="UserMenu" style="font-family:helvetica,arial,serif;font-size:11px;text-align:center" class="userMenu">
    </div>
<div class="docheader">
CiHSR - TurboCare</div>

    <div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

    <div py:replace="[item.text]+item[:]"/>

	<p/>
	<p class="docfooter">Copyright (c) 2006 Wesley Penner, uber web-designer</p>
 	<p class="docfooter">I'm not too proud, honest</p>
</body>

</html>