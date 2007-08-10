<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
     xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>${getattr(self,'title','Bed Manager')}</title>
    <LINK HREF="/tg_static/css/widget.css" TYPE="text/css" REL="stylesheet"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <SCRIPT SRC="/static/javascript/bm_Main.js" TYPE="text/javascript"></SCRIPT>
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
    <td>Ward</td>
    <td>Rooms</td>
    <td>Beds</td>
   </tr>  
   <tr>
    <td><div id="ward_list" py:content="ward_list.display()">Wards</div></td>
    <td><div id="room_list" py:content="room_list.display()">Rooms</div></td>
    <td><div id="bed_list" py:content="bed_list.display()">Beds</div></td>    
   </tr>
  </table>
  <div id="update_data"></div>
</body>
</html>
