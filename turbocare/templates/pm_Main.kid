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
    <script src="/tg_widgets/div_dialogs.js/dimmingdiv.js" type="text/javascript"></script>
    <link media="all" href="/tg_widgets/div_dialogs.css/dimming.css" type="text/css" rel="stylesheet"></link>
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
      <div class="tabber" style="width: 800px"> 
             <div class="tabbertab" style="height:500px; overflow: auto"><h2>Person</h2>
                <div id="person_form_contents" py:content="person_form.display(value=personvalues)">Person Entry</div>
             </div> 
             <div class="tabbertab" style="height:500px; overflow: auto"><h2>Customer</h2>
                <div py:content="customer_form.display(value=customervalues)">Customer Entry</div>
                Receipts
                <div py:content="customer_receipts.display(receiptvalues)">Receipts</div>
                Payments
                <div py:content="customer_payments.display(paymentvalues)">Payments</div>
             </div> 
             <div class="tabbertab" style="height:500px; overflow: auto"><h2>Patient</h2>
                Encounters
                <div py:content="encounters.display(encountervalues)">Encounters</div>
             </div>
             <div class="tabbertab" style="height:500px; overflow: auto"><h2>Employee</h2>
                <div py:content="personell_form.display(value=personellvalues)">Customer Entry</div>
             </div>
      </div>
    </td>
   </tr>
  </table>
  <div id="update_data"></div>
</body>
</html>
