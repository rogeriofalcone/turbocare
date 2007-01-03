<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Welcome to CIHSR TurboCare</title>
</head>
<body>
<div id="header">&nbsp;</div>
<div id="main_content">

  <div py:if="tg.identity.anonymous" id="status_block">Welcome to CIHSR</div>
  <div py:if="not tg.identity.anonymous" id="status_block">Welcome to CIHSR, ${tg.identity.user.display_name}!</div>
  <!--h1>Take steps to dive right in:</h1-->
  <div id="sidebar">
    <h2>Things to do:</h2>
    <ul class="links">
	<li py:if="tg.identity.anonymous"><a href="/login">login</a></li>
	<DIV py:for="item in menuitems">
		<a py:if="item['link']!=''" href="${item['link']}">${item['name']}</a>
		<DIV py:if="item['link']==''">${item['name']}</DIV>
		<DIV py:for="sub1item in item['sub_menu']" style="position:relative; left:20px">
			<a py:if="sub1item['link']!=''" href="${sub1item['link']}">${sub1item['name']}</a>
			<DIV py:if="sub1item['link']==''">${sub1item['name']}</DIV>
			<DIV py:for="sub2item in sub1item['sub_menu']" style="position:relative; left:20px">
				<a py:if="sub2item['link']!=''" href="${sub2item['link']}">${sub2item['name']}</a>
				<DIV py:if="sub2item['link']==''">${sub2item['name']}</DIV>
			</DIV>
		</DIV>
	</DIV>
	<DIV py:if="not tg.identity.anonymous"><a href="/logout">logout</a></DIV>
    </ul>
  </div>

</div>
</body>
</html>
