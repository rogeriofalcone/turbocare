/*
	Application wide shortcuts:
*/
var shortcuts = {};//keyboard short cut operations
shortcuts.keypress = function(dom_obj){
	if ((dom_obj.modifier()['ctrl'] == true) && (dom_obj.key()['string'] == 'c')) {
		usermenu.renderCustomerIdDialog();
	}
}
shortcuts.keydown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		var customerid = getElement("dialog_CustomerID");
		if ((customerid != null) && (customerid.value != null) && (customerid.value != '')){
			//Load the items available for the customer
			usermenu.customeriddialog_remove();
			var postVars = 'CustomerID='+customerid.value;
			document.location.href = 'RegistrationPage1?'+postVars;
		}
	}
}


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
	var Item = function(link, name, number) {
		var link = createDOM('A',{'id':'menu_link_'+number, 'href':link, 'style':'padding: 0px 2px 0px 2px;'},'[('+number+') '+name+']');
		return link;
	}
	//Reset the message
	usermenu.toggle_message('');
	//Remove any existing search box
	var MyMenu = getElement("UserMenu");
	replaceChildNodes(MyMenu,null);
	var results = data.results;
	for (i=0;i<results.length;i++){
		MyMenu.appendChild(Item(results[i].link,results[i].name,i));
	}
}

//Connect on onload for the document to open the document using javascript
connect(window, 'onload', usermenu.LoadMenu);
