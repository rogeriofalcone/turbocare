<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:py="http://purl.org/kid/ns#">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Search Form')}</title>
    <script src="/tg_js/MochiKit.js"></script> 
    <script src="/tg_widgets/turbogears.widgets/ajax.js" type="text/javascript">
    </script>
    <script src="/tg_widgets/turbogears/js/widget.js" type="text/javascript">
    </script>
    <script src="/tg_widgets/turbogears.widgets/ajaxgrid.js" type="text/javascript">
    </script>
    <link rel="stylesheet" href="/static/css/custom.css" type="text/css" />
    <SCRIPT TYPE="text/javascript">
    function retPick(form,field,id) {
    	eval("opener.document." + form + "." + field + ".value = " + id);
    	opener.update_form_delay();
    	window.close();
	};
	</SCRIPT>
</head>

<body>

    <div>
        ${group_list}
    </div>
 
</body>
</html>
