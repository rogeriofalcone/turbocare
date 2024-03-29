<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'master.kid'">
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>CatWalk</title>
    <link type="text/css" rel="stylesheet" href="${tg.tg_static}/css/widget.css" />
    <link type="text/css" rel="stylesheet" href="${tg.tg_static}/css/toolbox.css" />
    <link type="text/css" rel="stylesheet" href="${tg.tg_toolbox}/catwalk/css/catwalk.css" />
    <link type="text/css" rel="stylesheet" href="${tg.widgets}/turbogears.widgets/calendar/calendar-green.css" />
    <script type="text/javascript" src="${tg.tg_toolbox}/catwalk/javascript/greybox/AmiJS.js"></script>
    <script type="text/javascript" src="${tg.tg_js}/MochiKit.js"></script>
    <script type="text/javascript" src="${tg.tg_static}/js/widget.js"></script>
    <script type="text/javascript" src="${tg.tg_static}/js/tool-man/core.js"></script>
    <script type="text/javascript" src="${tg.tg_static}/js/tool-man/events.js"></script>
    <script type="text/javascript" src="${tg.tg_static}/js/tool-man/css.js"></script>
    <script type="text/javascript" src="${tg.tg_static}/js/tool-man/coordinates.js"></script>
    <script type="text/javascript" src="${tg.tg_static}/js/tool-man/drag.js"></script>
    <script type="text/javascript" src="${tg.tg_static}/js/tool-man/dragsort.js"></script>
    <script type="text/javascript" src="${tg.widgets}/turbogears.widgets/calendar/calendar.js"></script>
    <script type="text/javascript" src="${tg.widgets}/turbogears.widgets/calendar/lang/calendar-en.js"></script>
    <script type="text/javascript" src="${tg.widgets}/turbogears.widgets/calendar/calendar-setup.js"></script>
    <script type="text/javascript" src="${tg.tg_toolbox}/catwalk/javascript/catwalk.js"></script>
    <script type="text/javascript" src="${tg.tg_toolbox}/catwalk/javascript/browse.js"></script>
    <script type="text/javascript" src="${tg.tg_toolbox}/catwalk/javascript/greybox/greybox.js"></script>
    <script type="text/javascript">
    <![CDATA[
        var tg_static_directory = '${tg.tg_static}';
        var GB_ANIMATION = false;
        var GB_IMG_DIR = '${tg.tg_toolbox}/catwalk/javascript/greybox/';
        var GB_overlay_click_close = true;
    ]]>
    </script>
    <style type="text/css">
        @import url(${tg.tg_toolbox}/catwalk/javascript/greybox/greybox.css); 
        @import url(${tg.tg_static}/css/widget.css);
        .page_arrow { border-width:2px;border-style:outset;margin-bottom:2px;border-color:#999;}
        .page_select {font-size:10px;width:50px}
        .grid th { cursor:default;font-weight:100;text-align:left;padding:4px;background-color:#f0f0f0;color:#333;}
        .grid_icon_cell {background-color:#e3e3e3; } 
        .grid_icon { visibility:hidden}
        .odd, .even { cursor:pointer}
        * html #GB_overlay {
          background-image: url(${tg.tg_toolbox}/catwalk/javascript/greybox/blank.gif);
          filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="${tg.tg_toolbox}/catwalk/javascript/greybox/overlay.png", sizingMethod="scale");
        }
    </style>
</head>

<body >
    <table class="menu_form">
        <tr>
            <td id="left_col" valign="top">
                <div id="models">
                    <ul id="object_list">
                        <li py:for="model in models" 
                            id="${model}"
                            itemID="${model}"
    onmouseover="if(document.getElementById('handle_${model}')) document.getElementById('handle_${model}').style.visibility='visible'"
    onmouseOut="if(document.getElementById('handle_${model}')) document.getElementById('handle_${model}').style.visibility='hidden'"
                         >
                            <table border="0" cellspacing="2">
                                <tr>
                                    <td id="handle_${model}" class="handle">&#x2195;</td>
                                    <td><a id="list_${model}" href="javascript:catwalk.displayObject('${model}')">${model}</a></td>
                                </tr>
                            </table>
                         </li>
                    </ul>
                </div>
            </td>
            <td id="main_area" valign="top">
                <form name="myform" action="" onsubmit="return catwalk.submiting()">
                <div id="content"></div>
                </form>
            </td>
        </tr>
    </table>
    <br /><br /><br />
    <script type="text/javascript">
        dragsort.makeListSortable(document.getElementById('object_list'),setHandle,catwalk.endModelDrag);
    </script>
</body>
</html>
