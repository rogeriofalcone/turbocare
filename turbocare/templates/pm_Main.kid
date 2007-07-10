<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Person Manager')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/pm_Main.js" TYPE="text/javascript"></SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
  </head>

<body>
  ${tabber.display()}
  <table>
   <tr>
    <td valign="top">
      <div>${person_search.display()}
      <div id="search_results">&nbsp;</div>
      </div>
    </td>
    <td valign="top">
      <div class="tabber"> 
             <div class="tabbertab"><h2>Person</h2>
                <div py:content="person_form.display(value=personvalues,submit_text='Add Person')">Person Entry</div>
             </div> 
             <div class="tabbertab"><h2>Patient</h2></div> 
             <div class="tabbertab"><h2>Employee</h2></div> 
      </div>
    </td>
   </tr>
  </table>
  
</body>
</html>
