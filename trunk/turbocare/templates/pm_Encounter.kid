<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Person Manager')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/lang/calendar-en.js" TYPE="text/javascript">
    </SCRIPT>
    <script src="/tg_widgets/div_dialogs.js/dimmingdiv.js" type="text/javascript"></script>
    <link media="all" href="/tg_widgets/div_dialogs.css/dimming.css" type="text/css" rel="stylesheet"></link>
    <SCRIPT SRC="/tg_widgets/turbogears.widgets/calendar/calendar-setup.js" TYPE="text/javascript">
    </SCRIPT>
    <SCRIPT SRC="/tg_static/js/widget.js" TYPE="text/javascript">
    </SCRIPT>
  </head>

<body>
  <table>
   <tr>
    <td valign="top">
      <div>${person_search.display()}
      <div id="search_results">&nbsp;</div>
      </div>
    </td>
    <td valign="top">
    <h2><a href="${PersonLink}">${Name}</a></h2>
      <div style="width: 800px;overflow: auto"> 
         <div id="encounter_form_contents" py:content="encounter_form.display(value=encountervalues)">Encounter Entry</div>
         Receipts
         <div py:content="encounter_receipts.display(receiptvalues)">Receipts</div>
      </div>
    </td>
   </tr>
  </table>
</body>
</html>
