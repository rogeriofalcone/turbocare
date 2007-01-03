//AJAX Post function

//Funky redraw function
function redraw(){
	resizeBy(-1,0);
	resizeBy(1,0);
}

var usermenu = {};

usermenu.postJSON = function(url, postVars) {
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
}

// variables ===================
usermenu.g_nTimeoutId;
// utility functions ===========
/*
	Load the menu - ajax style.
*/
usermenu.LoadMenu = function(dom_obj){
	usermenu.toggle_message("Loading the usermenu...");
	var d = usermenu.postJSON('/LoadMenu','');
	d.addCallbacks(usermenu.RenderUserMenu,usermenu.error_report);
}

// AJSON reactions ==================
usermenu.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	usermenu.toggle_message("");
	if (data.result_msg != null) {
		var display = createDOM('DIV',{'class':'displaymsg','id':'last_result_msg'},data.result_msg);
		if (getNodeAttribute('last_result_msg','class') == null){
			document.body.appendChild(display);
		} else {
			swapDOM(field.id,display);
		}
	}
	var d = callLater(5,remove_message);
}
usermenu.error_report = function(data){
	usermenu.toggle_message("ERROR");
	var d = callLater(5,usermenu.toggle_message);
}

usermenu.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

/*
	AJSON Reactions to the above actions
*/

/* 	
	Render the Menu
*/
usermenu.RenderUserMenu = function(data){
	var SubMenu = function(results,parentid,myid,MenuDiv) {
		var Menu = createDOM('DIV',{'id':myid,'style':'display:none'});
		// Create link to parent menu
		Menu.appendChild(createDOM('A',{'href':"javascript:usermenu.ShowMenu('"+parentid+"')", 
			'style':'padding: 0px 2px 0px 2px;'},'[<<Previous Menu]'));
		for (var i=0;i<results.length;i++){
			var subid = '';
			if (results[i].sub_menu.length > 0) {
				subid = myid+'SubMenu' + i;
				// Menu and Sub menu DIVs are not nested, but I attach them to the top level DIV
				SubMenu(results[i].sub_menu,myid,subid,MenuDiv);
				Menu.appendChild(createDOM('A',{'href':"javascript:usermenu.ShowMenu('"+subid+"')", 
					'style':'padding: 0px 2px 0px 2px;'},'['+results[i].name+'>>]'));
			} else {
				Menu.appendChild(createDOM('A',{'href':results[i].link,	'style':'padding: 0px 2px 0px 2px;'},
					'['+results[i].name+']'));
			}
		}
		MenuDiv.appendChild(Menu);
	}
	//Reset the message
	usermenu.toggle_message('');
	//Remove any existing search box
	var MyMenu = getElement("UserMenu");
	replaceChildNodes(MyMenu,null);
	// Create Menu Bar
	var Menu = createDOM('DIV',{'id':'MainMenu'});
	var results = data.results;
	for (var i=0;i<results.length;i++){
		var subid = '';
		if (results[i].sub_menu.length > 0) {
			subid = 'MainMenuSubMenu' + i;
			// Menu and Sub menu DIVs are not nested, but I attach them to the top level DIV
			SubMenu(results[i].sub_menu,'MainMenu',subid,MyMenu);
			Menu.appendChild(createDOM('A',{'href':"javascript:usermenu.ShowMenu('"+subid+"')", 
				'style':'padding: 0px 2px 0px 2px;'},'['+results[i].name+'>>]'));
		} else {
			Menu.appendChild(createDOM('A',{'href':results[i].link,	'style':'padding: 0px 2px 0px 2px;'},
				'['+results[i].name+']'));
		}
	}
	MyMenu.appendChild(Menu);
}
/*
	ShowMenu: Hide the current menu and display the Child or Parent menu
	currid: The id for the current menu DIV (which we want to hide)
	nextid: The id for the Child or Parent menu DIV we want to display
*/
usermenu.ShowMenu = function(showid) {
	var divs = getElementsByTagAndClassName('DIV',null,'UserMenu');
	for (var i=0;i<divs.length;i++) {
		if (divs[i].id==showid) {
			divs[i].style.display = '';
		} else {
			divs[i].style.display = 'none';
		}
	}
}


//Connect on onload for the document to open the document using javascript
connect(window, 'onload', usermenu.LoadMenu);
