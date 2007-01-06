function postJSON(url, postVars) {
	um.toggle_message("Sending request...");
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
}


var um = {};
um.NextJoinList = '';// String representation of the function to execute

um.collectPostVars = function(f)
{
  var postVars='';
  for(var i=0; i<f.elements.length;i++)
  {
    var t = f.elements[i].type;
    if(t.indexOf('text') > -1 )
    {
      if(postVars!='') postVars+='&';
      postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].value);
    }
    if(t.indexOf('hidden') > -1 )
    {
      if(postVars!='') postVars+='&';
      postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].value);
    }
    if(t.indexOf('select') > -1)
    {
      if(postVars!='') postVars+='&';
      if (getNodeAttribute(f.elements[i],'multiple') != null) {
      	postVars+= f.elements[i].name +'='+ um.multiselect_csv(f.elements[i].id);
      } else {
      	postVars+= f.elements[i].name +'='+ f.elements[i].options[f.elements[i].selectedIndex].value;
      }
    }
  }
  return postVars;
}

um.multiselect_csv = function(element_id){
	var nodes = getElement(element_id).childNodes;
	var csv = '';
	for (var i=0;i<nodes.length;i++){
	 	if (nodes[i].selected){
	 		csv += nodes[i].value +',';
	 	}
	}
	csv = csv.slice(0,csv.length-1);
	return csv;
}

// AJSON reactions ==================
um.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	um.toggle_message("");
	if (data.message != null) {
		var display = createDOM('DIV',{'class':'displaymsg','id':'last_result_msg'},data.message);
		if (getNodeAttribute('last_result_msg','class') == null){
			document.body.appendChild(display);
		} else {
			swapDOM(field.id,display);
		}
	}
	var d = callLater(5,remove_message);
}

um.error_report = function(data){
	um.toggle_message("");
	alert('ERROR: ' + data);
}

um.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

// AJSON actions ====================
um.saveForm = function(url){
	um.toggle_message("Saving...");
  	var postVars =um.collectPostVars(document.ObjForm);
  	var d = postJSON(url,postVars);
  	d.addCallbacks(um.updated,um.error_report);
  	return false;
}

um.saveData = function(url,vars){
	um.toggle_message("Saving...");
  	var d = postJSON(url,vars);
  	d.addCallbacks(um.updated,um.error_report);
}

/*
	LoadUsers: Load the list of users.  If there is search text, then filter the list based
	on the search text.
*/
um.LoadUsers = function(e){
	var SearchText = getElement('SearchUser').value;
	um.toggle_message("Loading...");
	var d = postJSON("FindUsers","SearchText="+SearchText);
	d.addCallbacks(um.renderUsers,um.error_report);
}
/*
	LoadGroups: Load the list of groups.  If there is search text, then filter the list based
	on the search text.
*/
um.LoadGroups = function(e){
	var SearchText = getElement('SearchGroup').value;
	um.toggle_message("Loading...");
	var d = postJSON("FindGroups","SearchText="+SearchText);
	d.addCallbacks(um.renderGroups,um.error_report);
}
/*
	LoadPermissions: Load the list of permissions.  If there is search text, then filter the list based
	on the search text.
*/
um.LoadPermissions = function(e){
	var SearchText = getElement('SearchPermission').value;
	um.toggle_message("Loading...");
	var d = postJSON("FindPermissions","SearchText="+SearchText);
	d.addCallbacks(um.renderPermissions,um.error_report);
}
/*
	renderUsers: Display the results for the search
*/
um.renderUsers = function(d) {
	um.toggle_message('');
	var Listing = getElement('UserListSelect'); // The destination for our user entries
	for (var i=0; i<d.users.length; i++) {
		var div = createDOM('DIV',{'class':'ListBoxItem'});
		var chk = createDOM('INPUT',{'type':'checkbox'});
		var id = createDOM('INPUT',{'type':'hidden','name':'id', 'value':d.users[i].db.id});
		var UserName = createDOM('INPUT',{'type':'hidden','name':'UserName','value':d.users[i].db.user_name});
		var DisplayName = createDOM('INPUT',{'type':'hidden','name':'DisplayName','value':d.users[i].db.display_name});
		var EmailAddress = createDOM('INPUT',{'type':'hidden','name':'EmailAddress','value':d.users[i].db.email_address});
		appendChildNodes(div,chk,d.users[i].name,id,UserName,DisplayName,EmailAddress);
		Listing.appendChild(div);
		connect(chk,'onclick',um.MoveUser);// When a user checks the box, it moves the item down to the join list below it
		connect(div,'ondblclick',um.SelectUser); // When in edit mode, double clicking a user entry will hi-lite the entry and copy the values to the data entry form below
	}
}
/*
	renderGroups: Display the results for the search
*/
um.renderGroups = function(d) {
	um.toggle_message('');
	var Listing = getElement('GroupListSelect'); // The destination for our user entries
	for (var i=0; i<d.groups.length; i++) {
		var div = createDOM('DIV',{'class':'ListBoxItem'});
		var chk = createDOM('INPUT',{'type':'checkbox'});
		var id = createDOM('INPUT',{'type':'hidden','name':'id','value':d.groups[i].db.id});
		var GroupName = createDOM('INPUT',{'type':'hidden','name':'GroupName','value':d.groups[i].db.group_name});
		var DisplayName = createDOM('INPUT',{'type':'hidden','name':'DisplayName','value':d.groups[i].db.display_name});
		appendChildNodes(div,chk,d.groups[i].name,id,GroupName,DisplayName);
		Listing.appendChild(div);
		connect(chk,'onclick',um.MoveGroup);// Moves the item down to the join list below it
		connect(div,'ondblclick',um.SelectGroup); // When in edit mode, double clicking an entry will hi-lite the entry and copy the values to the data entry form below
	}
}
/*
	renderPermissions: Display the results for the search
*/
um.renderPermissions = function(d) {
	um.toggle_message('');
	var Listing = getElement('PermissionListSelect'); // The destination for our user entries
	for (var i=0; i<d.permissions.length; i++) {
		var div = createDOM('DIV',{'class':'ListBoxItem'});
		var chk = createDOM('INPUT',{'type':'checkbox'});
		var id = createDOM('INPUT',{'type':'hidden','name':'id','value':d.permissions[i].db.id});
		var PermissionName = createDOM('INPUT',{'type':'hidden','name':'PermissionName','value':d.permissions[i].db.permission_name});
		var Description = createDOM('INPUT',{'type':'hidden','name':'Description','value':d.permissions[i].db.description});
		appendChildNodes(div,chk,d.permissions[i].name,id,PermissionName,Description);
		Listing.appendChild(div);
		connect(chk,'onclick',um.MovePermission);// Moves the item down to the join list below it
		connect(div,'ondblclick',um.SelectPermission); // When in edit mode, double clicking an entry will hi-lite the entry and copy the values to the data entry form below
	}
}
/*
	MoveUser: Move an item from the listing to the joins listing
	Note: This is only done when editing Groups
*/
um.MoveUser = function(e) {
	if (hasElementClass("GroupColumn","Column-lite")) {
		var el = e.src().parentNode; // select the entire div
		// find the id for our node
		var inputs = getElementsByTagAndClassName("INPUT",null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name=="id") {
				var ID = inputs[i].value;
				break;
			}
			var ID = null;
			alert('ooops, cannot move the item.  Porgramming error');
		}
		var Listing = el.parentNode;
		var JoinListing = getElement('JoinedUsersSelect');
		// Check to make sure an item with the same id doesn't already exists, if it does, just delete the item
		var inputs = getElementsByTagAndClassName("INPUT",null,JoinListing);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id" && inputs[i].value == ID) {
				var Match = true;
				break;
			}
			var Match = false;
		}
		// Move the node down to the JoinListing - check to make sure the connect events stay connected
		if (Match) {
			Listing.removeChild(el);
		} else {
			JoinListing.appendChild(Listing.removeChild(el));
		}
	}
}
/*
	MoveGroup: Move an item from the listing to the joins listing
	Note: This is only done when editing Users or Permissions
*/
um.MoveGroup = function(e) {
	if (hasElementClass("UserColumn","Column-lite")||hasElementClass("PermissionColumn","Column-lite")) {
		var el = e.src().parentNode; // select the entire div
		// find the id for our node
		var inputs = getElementsByTagAndClassName("INPUT",null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name=="id") {
				var ID = inputs[i].value;
				break;
			}
			var ID = null;
			alert('ooops, cannot move the item.  Porgramming error');
		}
		var Listing = el.parentNode;
		var JoinListing = getElement('JoinedGroupsSelect');
		// Check to make sure an item with the same id doesn't already exists, if it does, just delete the item
		var inputs = getElementsByTagAndClassName("INPUT",null,JoinListing);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id" && inputs[i].value == ID) {
				var Match = true;
				break;
			}
			var Match = false;
		}
		// Move the node down to the JoinListing - check to make sure the connect events stay connected
		if (Match) {
			Listing.removeChild(el);
		} else {
			JoinListing.appendChild(Listing.removeChild(el));
		}
	}
}
/*
	MovePermission: Move an item from the listing to the joins listing
	Note: This is only done when editing Groups
*/
um.MovePermission = function(e) {
	if (hasElementClass("GroupColumn","Column-lite")) {
		var el = e.src().parentNode; // select the entire div
		// find the id for our node
		var inputs = getElementsByTagAndClassName("INPUT",null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name=="id") {
				var ID = inputs[i].value;
				break;
			}
			var ID = null;
			alert('ooops, cannot move the item.  Porgramming error');
		}
		var Listing = el.parentNode;
		var JoinListing = getElement('JoinedPermissionsSelect');
		// Check to make sure an item with the same id doesn't already exists, if it does, just delete the item
		var inputs = getElementsByTagAndClassName("INPUT",null,JoinListing);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id" && inputs[i].value == ID) {
				var Match = true;
				break;
			}
			var Match = false;
		}
		// Move the node down to the JoinListing - check to make sure the connect events stay connected
		if (Match) {
			Listing.removeChild(el);
		} else {
			JoinListing.appendChild(Listing.removeChild(el));
		}
	}
}
/*
	SelectUser: When an entry is selected, copy the elements to the form below for editing
	This is only done when the column is in edit mode
*/
um.SelectUser = function(e) {
	e.stop();
	if (hasElementClass("UserColumn","Column-lite")) {
		var el = e.target();
		// Remove hi-lite from hi-lited items
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','UserColumn');
		for (var i=0; i<elems.length; i++) {
			removeElementClass(elems[i],'ListBoxItem-Lite');
		}
		// Add hi-lite to current item
		addElementClass(el,'ListBoxItem-Lite');
		// Move the item values to the form below
		getElement("UserEdit_Password").value = '';
		getElement("UserEdit_PasswordVerify").value = '';
		var inputs = getElementsByTagAndClassName('INPUT',null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id") {
				var ID = inputs[i].value;
				getElement("UserEdit_id").value = ID;
			} else if (inputs[i].name == "UserName") {
				getElement("UserEdit_UserName").value = inputs[i].value;
			} else if (inputs[i].name == "DisplayName") {
				getElement("UserEdit_DisplayName").value = inputs[i].value;
			} else if (inputs[i].name == "EmailAddress") {
				getElement("UserEdit_EmailAddress").value = inputs[i].value;
			}
		}
		// Render the list of joined groups and permissions
		um.NextJoinList = 'um.LoadJoindPermissions('+ID+',null)';
		um.LoadJoinedGroups(ID,null);
	}
}
/*
	SelectGroup: When an entry is selected, copy the elements to the form below for editing
	This is only done when the column is in edit mode
*/
um.SelectGroup = function(e) {
	e.stop();
	if (hasElementClass("GroupColumn","Column-lite")) {
		var el = e.target();
		// Remove hi-lite from hi-lited items
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','GroupColumn');
		for (var i=0; i<elems.length; i++) {
			removeElementClass(elems[i],'ListBoxItem-Lite');
		}
		// Add hi-lite to current item
		addElementClass(el,'ListBoxItem-Lite');
		// Move the item values to the form below
		var inputs = getElementsByTagAndClassName('INPUT',null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id") {
				var ID = inputs[i].value;
				getElement("GroupEdit_id").value = ID;
			} else if (inputs[i].name == "GroupName") {
				getElement("GroupEdit_GroupName").value = inputs[i].value;
			} else if (inputs[i].name == "DisplayName") {
				getElement("GroupEdit_DisplayName").value = inputs[i].value;
			}
		}
		// Render the list of joined users and permissions
		um.NextJoinList = 'um.LoadJoindPermissions(null,'+ID+')';
		um.LoadJoinedUsers(ID,null);		
	}
}
/*
	SelectPermission: When an entry is selected, copy the elements to the form below for editing
	This is only done when the column is in edit mode
*/
um.SelectPermission = function(e) {
	e.stop();
	if (hasElementClass("PermissionColumn","Column-lite")) {
		var el = e.target();
		// Remove hi-lite from hi-lited items
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','PermissionColumn');
		for (var i=0; i<elems.length; i++) {
			removeElementClass(elems[i],'ListBoxItem-Lite');
		}
		// Add hi-lite to current item
		addElementClass(el,'ListBoxItem-Lite');
		// Move the item values to the form below
		var inputs = getElementsByTagAndClassName('INPUT',null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id") {
				getElement("PermissionEdit_id").value = inputs[i].value;
			} else if (inputs[i].name == "PermissionName") {
				getElement("PermissionEdit_PermissionName").value = inputs[i].value;
			} else if (inputs[i].name == "Description") {
				getElement("PermissionEdit_PermissionDescription").value = inputs[i].value;
			}
		}
		// Render the list of joined groups and users
		um.NextJoinList = 'um.LoadJoindUsers(null,'+ID+')';
		um.LoadJoinedGroups(null,ID);				
	}
}
/*
	GetJoinedIDs: Looks for Inputs with the name "id" and creates a postable variable list
	VarName: The name of the post variable, such that: &VarName=Val1&VarName=Val2&VarName=Val3...
	ParentNode: The node to search for the inputs with the name = "id"
	NOTE: the return value is always formatted with a starting &
*/
um.GetJoinedIDs = function(VarName, ParentNode){
	var PostVars = '';
	var inputs = getElementsByTagAndClassName('INPUT',null,ParentNode);
	for (var i=0; i<inputs.length; i++) {
		if (inputs[i].name=='id') {
			PostVars += '&' + VarName + '=' + inputs[i].value;
		}
	}
	return PostVars;
}
/*
	LoadJoinedUsers: Populate the JoinedUsers list box div with users
	GroupID - If we want to filter the user list on a GroupID
	PermissionID - We want to filter on a Permission
*/
um.LoadJoinedUsers = function(GroupID, PermissionID) {
	if (GroupID!=null||PermissionID!=null) {
		if (GroupID!=null) {
			var postVars = 'GroupID='+GroupID;
		} else {
			var postVars = 'PermissionID='+PermissionID;
		}
		var d = postJSON("FindUsers",postVars);
		d.addCallbacks(um.RenderJoinedUsers,um.error_report);
	} else { //clear the list
		replaceChildNodes('JoinedUsersSelect',null);
	}
}
/*
	RenderJoinedUsers: Display the listing of joined users
*/
um.RenderJoinedUsers = function(d) {
	um.toggle_message('');
	var Listing = getElement('JoinedUsersSelect'); // The destination for our user entries
	for (var i=0; i<d.users.length; i++) {
		var div = createDOM('DIV',{'class':'ListBoxItem'});
		var chk = createDOM('INPUT',{'type':'checkbox','checked':'checked'});
		var id = createDOM('INPUT',{'type':'hidden','name':'id', 'value':d.users[i].db.id});
		var UserName = createDOM('INPUT',{'type':'hidden','name':'UserName','value':d.users[i].db.user_name});
		var DisplayName = createDOM('INPUT',{'type':'hidden','name':'DisplayName','value':d.users[i].db.display_name});
		var EmailAddress = createDOM('INPUT',{'type':'hidden','name':'EmailAddress','value':d.users[i].db.email_address});
		appendChildNodes(div,chk,d.users[i].name,id,UserName,DisplayName,EmailAddress);
		Listing.appendChild(div);
		connect(chk,'onclick',um.MoveUser);// When a user checks the box, it moves the item down to the join list below it
		connect(div,'ondblclick',um.SelectUser); // When in edit mode, double clicking a user entry will hi-lite the entry and copy the values to the data entry form below
	}
	// For loading the joined lists, there are usually two lists to load.  Check to see if there is another list to load
	if (!(um.NextJoinList=='')) {
		var EvalString = um.NextJoinList;
		um.NextJoinList = '';
		eval(EvalString);
	}
}
/*
	LoadJoinedGroups: Populate the JoinedGroups list box div with groups
	UserID - If we want to filter the user list on a User
	PermissionID - We want to filter on a Permission
*/
um.LoadJoinedGroups = function(UserID, PermissionID) {
	if (UserID!=null||PermissionID!=null) {
		if (UserID!=null) {
			var postVars = 'UserID='+UserID;
		} else {
			var postVars = 'PermissionID='+PermissionID;
		}
		var d = postJSON("FindGroups",postVars);
		d.addCallbacks(um.RenderJoinedGroups,um.error_report);
	} else {
		replaceChildNodes('JoinedGroupsSelect',null);
	}
}

/*
	RenderJoinedGroups: Display the listing of joined groups
*/
um.RenderJoinedGroups = function(d) {
	um.toggle_message('');
	var Listing = getElement('JoinedGroupsSelect'); // The destination for our group entries
	for (var i=0; i<d.groups.length; i++) {
		var div = createDOM('DIV',{'class':'ListBoxItem'});
		var chk = createDOM('INPUT',{'type':'checkbox','checked':'checked'});
		var id = createDOM('INPUT',{'type':'hidden','name':'id','value':d.groups[i].db.id});
		var GroupName = createDOM('INPUT',{'type':'hidden','name':'GroupName','value':d.groups[i].db.group_name});
		var DisplayName = createDOM('INPUT',{'type':'hidden','name':'DisplayName','value':d.groups[i].db.display_name});
		appendChildNodes(div,chk,d.groups[i].name,id,GroupName,DisplayName);
		Listing.appendChild(div);
		connect(chk,'onclick',um.MoveGroup);// Moves the item down to the join list below it
		connect(div,'ondblclick',um.SelectGroup); // When in edit mode, double clicking an entry will hi-lite the entry and copy the values to the data entry form below
	}
	// For loading the joined lists, there are usually two lists to load.  Check to see if there is another list to load
	if (!(um.NextJoinList=='')) {
		var EvalString = um.NextJoinList;
		um.NextJoinList = '';
		eval(EvalString);
	}
}
/*
	LoadJoinedPermissions: Populate the JoinedPermissions list box div with permissions
	UserID - If we want to filter the user list on a User
	GroupID - We want to filter on a Group
*/
um.LoadJoinedPermissions = function(UserID, GroupID) {
	if (UserID!=null||GroupID!=null) {
		if (UserID!=null) {
			var postVars = 'UserID='+UserID;
		} else {
			var postVars = 'GroupID='+GroupID;
		}
		var d = postJSON("FindPermissions",postVars);
		d.addCallbacks(um.RenderJoinedPermissions,um.error_report);
	} else {
		replaceChildNodes('JoinedPermissionsSelect',null);
	}
}
/*
	RenderJoinedPermissions: Display the listing of joined permissions
*/
um.RenderJoinedPermissions = function(d) {
	um.toggle_message('');
	var Listing = getElement('JoinedPermissionsSelect'); // The destination for our user entries
	for (var i=0; i<d.permissions.length; i++) {
		var div = createDOM('DIV',{'class':'ListBoxItem'});
		var chk = createDOM('INPUT',{'type':'checkbox'});
		var id = createDOM('INPUT',{'type':'hidden','name':'id','value':d.permissions[i].db.id});
		var PermissionName = createDOM('INPUT',{'type':'hidden','name':'PermissionName','value':d.permissions[i].db.permission_name});
		var Description = createDOM('INPUT',{'type':'hidden','name':'Description','value':d.permissions[i].db.description});
		appendChildNodes(div,chk,d.permissions[i].name,id,PermissionName,Description);
		Listing.appendChild(div);
		connect(chk,'onclick',um.MovePermission);// Moves the item down to the join list below it
		connect(div,'ondblclick',um.SelectPermission); // When in edit mode, double clicking an entry will hi-lite the entry and copy the values to the data entry form below
	}
	// For loading the joined lists, there are usually two lists to load.  Check to see if there is another list to load
	if (!(um.NextJoinList=='')) {
		var EvalString = um.NextJoinList;
		um.NextJoinList = '';
		eval(EvalString);
	}
}
/*
	SaveUser: Save the entry
*/
um.SaveUser = function(e){
	var ID = getElement("UserEdit_id").value;
	var UserName = getElement("UserEdit_UserName").value;
	var DisplayName = getElement("UserEdit_DisplayName").value;
	var EmailAddress = getElement("UserEdit_EmailAddress").value;
	var Password = getElement("UserEdit_Password").value;
	var PasswordVerify = getElement("UserEdit_PasswordVerify").value;
	if ((Password != '' && PasswordVerify != '' && Password == PasswordVerify)||(Password == '' && PasswordVerify == '' && ID != '')) {
		um.toggle_message("Saving...");
		if (ID!='') { // Update a user
			var postVars  = "UserID="+ID+"&UserName="+UserName+"&DisplayName="+DisplayName;
			postVars += "&EmailAddress="+EmailAddress+"&Operation=Save&Password="+Password;
			postVars += um.GetJoinedIDs('Groups','JoinedGroupsSelect');
			var d = postJSON("SaveUser",postVars);
			d.addCallbacks(um.updated,um.error_report);
		} else { // Create a new user
			var postVars  = "UserName="+UserName+"&DisplayName="+DisplayName;
			postVars += "&EmailAddress="+EmailAddress+"&Operation=New&Password="+Password;
			postVars += um.GetJoinedIDs('Groups','JoinedGroupsSelect');
			var d = postJSON("SaveUser",postVars);
			d.addCallbacks(um.updated,um.error_report);
		}
	} else {
		alert('Error: Either the passwords do not match OR you are creating a new user without a password!');
	}
}
/*
	CancelUser: Cancel the entry, reload from the original entry
*/
um.CancelUser = function(e){
	var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','UserColumn');
	if (elems.length > 0) { // Updating a user, and we're resetting
		var el = elems[0];
		// Move the item values to the form below
		getElement("UserEdit_Password").value = '';
		getElement("UserEdit_PasswordVerify").value = '';
		var inputs = getElementsByTagAndClassName('INPUT',null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id") {
				var ID = inputs[i].value
				getElement("UserEdit_id").value = ID;
			} else if (inputs[i].name == "UserName") {
				getElement("UserEdit_UserName").value = inputs[i].value;
			} else if (inputs[i].name == "DisplayName") {
				getElement("UserEdit_DisplayName").value = inputs[i].value;
			} else if (inputs[i].name == "EmailAddress") {
				getElement("UserEdit_EmailAddress").value = inputs[i].value;
			}
		}
		// Render the list of joined groups and permissions
		um.NextJoinList = 'um.LoadJoindPermissions('+ID+',null)';
		um.LoadJoinedGroups(ID,null);
	} else { // we created a new user, now we're resetting
		getElement("UserEdit_Password").value = '';
		getElement("UserEdit_PasswordVerify").value = '';
		getElement("UserEdit_id").value = '';
		getElement("UserEdit_UserName").value = '';
		getElement("UserEdit_DisplayName").value = '';
		getElement("UserEdit_EmailAddress").value = '';
		um.LoadJoinedGroups(null,null);
		um.LoadJoindPermissions(null,null);
	}
}
/*
	NewUser: make a blank entry
*/
um.NewUser = function(e){
	if (confirm('Are you sure you want a new entry?')){
		// Remove hi-lite from hi-lited items
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','UserColumn');
		for (var i=0; i<elems.length; i++) {
			removeElementClass(elems[i],'ListBoxItem-Lite');
		}
		getElement("UserEdit_Password").value = '';
		getElement("UserEdit_PasswordVerify").value = '';
		getElement("UserEdit_id").value = '';
		getElement("UserEdit_UserName").value = '';
		getElement("UserEdit_DisplayName").value = '';
		getElement("UserEdit_EmailAddress").value = '';
		um.LoadJoinedGroups(null,null);
		um.LoadJoindPermissions(null,null);
	}
}
/*
	DeleteUser: delete the entry
*/
um.DeleteUser = function(e){
	if (confirm('Are you sure you want to delete?')) {
		var ID = getElement("UserEdit_id").value;
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','UserColumn');
		if (elems.length > 0) {
			var el = elems[0];
			var inputs = getElementsByTagAndClassName('INPUT',null,el);
			var CheckID = null;
			for (var i=0; i<inputs.length; i++) {
				if (inputs[i].name == "id") {
					CheckID = inputs[i].value;
					break;
				}
			}
			if (CheckID == ID && ID!=null) {
				um.toggle_message("Deleting...");
				var postVars  = "UserID="+ID+"&Operation=Delete";
				var d = postJSON("SaveUser",postVars);
				d.addCallbacks(um.DeleteUserClean,um.error_report);
			} else {
				alert('Error: Inconsistency match with deleting IDs - Did you hack the DOM?');
			}
		} else {
			alert('Error: No user selected for deletion! (User must be selected in the top listing)');
		}
	}
}
/*
	DeleteUserClean: remove the object from DOM and clean up the joined lists
*/
um.DeleteUserClean = function(d) {
	um.toggle_message('');
	um.LoadJoinedGroups(null,null);
	um.LoadJoindPermissions(null,null);
	getElement("UserEdit_Password").value = '';
	getElement("UserEdit_PasswordVerify").value = '';
	getElement("UserEdit_id").value = '';
	getElement("UserEdit_UserName").value = '';
	getElement("UserEdit_DisplayName").value = '';
	getElement("UserEdit_EmailAddress").value = '';
	var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','UserColumn');
	if (elems.length > 0) {
		var el = elems[0];
		swapDOM(el,null);
	}
}
/*
	SaveGroup: Save the entry
*/
um.SaveGroup = function(e){
	var ID = getElement("GroupEdit_id").value;
	var GroupName = getElement("GroupEdit_GroupName").value;
	var DisplayName = getElement("GroupEdit_DisplayName").value;
	um.toggle_message("Saving...");
	if (ID!='') { // Update a group
		var postVars  = "GroupID="+ID+"&GroupName="+GroupName+"&DisplayName="+DisplayName;
		postVars += "&Operation=Save";
		postVars += um.GetJoinedIDs('Users','JoinedUsersSelect');
		postVars += um.GetJoinedIDs('Permissions','JoinedPermissionsSelect');
		var d = postJSON("SaveGroup",postVars);
		d.addCallbacks(um.updated,um.error_report);
	} else { // Create a new group
		var postVars  = "GroupName="+GroupName+"&DisplayName="+DisplayName;
		postVars += "&Operation=New";
		postVars += um.GetJoinedIDs('Users','JoinedUsersSelect');
		postVars += um.GetJoinedIDs('Permissions','JoinedPermissionsSelect');
		var d = postJSON("SaveGroup",postVars);
		d.addCallbacks(um.updated,um.error_report);
	}
}
/*
	CancelGroup: Cancel the entry, reload from the original entry
*/
um.CancelGroup = function(e){
	var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','GroupColumn');
	if (elems.length > 0) { // Updating a user, and we're resetting
		var el = elems[0];
		// Move the item values to the form below
		var inputs = getElementsByTagAndClassName('INPUT',null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id") {
				var ID = inputs[i].value;
				getElement("GroupEdit_id").value = ID;
			} else if (inputs[i].name == "GroupName") {
				getElement("GroupEdit_GroupName").value = inputs[i].value;
			} else if (inputs[i].name == "DisplayName") {
				getElement("GroupEdit_DisplayName").value = inputs[i].value;
			}
		}
		um.NextJoinList = 'um.LoadJoindPermissions(null,'+ID+')';
		um.LoadJoinedUsers(ID,null);		
	} else { // we created a new user, now we're resetting
		getElement("GroupEdit_id").value = '';
		getElement("GroupEdit_GroupName").value = '';
		getElement("GroupEdit_DisplayName").value = '';
		um.LoadJoinedUsers(null,null);		
		um.LoadJoindPermissions(null,null);		
	}
}
/*
	NewGroup: Make a blank entry
*/
um.NewGroup = function(e){
	if (confirm('Are you sure you want a new entry?')){
		// Remove hi-lite from hi-lited items
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','GroupColumn');
		for (var i=0; i<elems.length; i++) {
			removeElementClass(elems[i],'ListBoxItem-Lite');
		}
		getElement("GroupEdit_id").value = '';
		getElement("GroupEdit_GroupName").value = '';
		getElement("GroupEdit_DisplayName").value = '';
		um.LoadJoinedUsers(null,null);		
		um.LoadJoindPermissions(null,null);		
	}
}
/*
	DeleteGroup: Delete the entry
*/
um.DeleteGroup = function(e){
	if (confirm('Are you sure you want to delete?')) {
		var ID = getElement("GroupEdit_id").value;
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','GroupColumn');
		if (elems.length > 0) {
			var el = elems[0];
			var inputs = getElementsByTagAndClassName('INPUT',null,el);
			var CheckID = null;
			for (var i=0; i<inputs.length; i++) {
				if (inputs[i].name == "id") {
					CheckID = inputs[i].value;
					break;
				}
			}
			if (CheckID == ID && ID!=null) {
				um.toggle_message("Deleting...");
				var postVars  = "GroupID="+ID+"&Operation=Delete";
				var d = postJSON("SaveGroup",postVars);
				d.addCallbacks(um.DeleteGroupClean,um.error_report);
			} else {
				alert('Error: Inconsistency match with deleting IDs - Did you hack the DOM?');
			}
		} else {
			alert('Error: No group selected for deletion! (Group must be selected in the top listing)');
		}
	}
}
/*
	DeleteGroupClean: remove the object from DOM and clean up the joined lists
*/
um.DeleteGroupClean = function(d) {
	um.toggle_message('');
	getElement("GroupEdit_id").value = '';
	getElement("GroupEdit_GroupName").value = '';
	getElement("GroupEdit_DisplayName").value = '';
	um.LoadJoinedUsers(null,null);		
	um.LoadJoindPermissions(null,null);		
	var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','GroupColumn');
	if (elems.length > 0) {
		var el = elems[0];
		swapDOM(el,null);
	}
}
/*
	SavePermission: Save the entry
*/
um.SavePermission = function(e){
	var ID = getElement("PermissionEdit_id").value;
	var PermissionName = getElement("PermissionEdit_PermissionName").value;
	var Description = getElement("PermissionEdit_PermissionDescription").value;
	um.toggle_message("Saving...");
	if (ID!='') { // Update a group
		var postVars  = "PermissionID="+ID+"&PermissionName="+PermissionName+"&Description="+Description;
		postVars += "&Operation=Save";
		postVars += um.GetJoinedIDs('Groups','JoinedGroupsSelect');
		var d = postJSON("SavePermission",postVars);
		d.addCallbacks(um.updated,um.error_report);
	} else { // Create a new group
		var postVars  = "PermissionName="+PermissionName+"&Description="+Description;
		postVars += "&Operation=New";
		postVars += um.GetJoinedIDs('Groups','JoinedGroupsSelect');
		var d = postJSON("SavePermission",postVars);
		d.addCallbacks(um.updated,um.error_report);
	}
}
/*
	CancelPermission: Cancel the entry, reload from the original entry
*/
um.CancelPermission = function(e){
	var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','PermissionColumn');
	if (elems.length > 0) { // Updating a user, and we're resetting
		var el = elems[0];
		// reload values
		var inputs = getElementsByTagAndClassName('INPUT',null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id") {
				var ID = inputs[i].value;
				getElement("PermissionEdit_id").value = ID;
			} else if (inputs[i].name == "PermissionName") {
				getElement("PermissionEdit_PermissionName").value = inputs[i].value;
			} else if (inputs[i].name == "Description") {
				getElement("PermissionEdit_PermissionDescription").value = inputs[i].value;
			}
		}
		um.NextJoinList = 'um.LoadJoindUsers(null,'+ID+')';
		um.LoadJoinedGroups(null,ID);				
	} else { // we created a new user, now we're resetting
		getElement("PermissionEdit_id").value = '';
		getElement("PermissionEdit_PermissionName").value = '';
		getElement("PermissionEdit_PermissionDescription").value = '';
		um.LoadJoinedUsers(null,null);		
		um.LoadJoinedGroups(null,null);		
	}
}
/*
	NewPermission: Make a blank entry
*/
um.NewPermission = function(e){
	if (confirm('Are you sure you want a new entry?')){
		// Remove hi-lite from hi-lited items
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','PermissionColumn');
		for (var i=0; i<elems.length; i++) {
			removeElementClass(elems[i],'ListBoxItem-Lite');
		}		
		getElement("PermissionEdit_id").value = '';
		getElement("PermissionEdit_PermissionName").value = '';
		getElement("PermissionEdit_PermissionDescription").value = '';
		um.LoadJoinedUsers(null,null);		
		um.LoadJoinedGroups(null,null);		
	}
}
/*
	DeletePermission: Delete the entry
*/
um.DeletePermission = function(e){
	if (confirm('Are you sure you want to delete?')) {
		var ID = getElement("PermissionEdit_id").value;
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','PermissionColumn');
		if (elems.length > 0) {
			var el = elems[0];
			var inputs = getElementsByTagAndClassName('INPUT',null,el);
			var CheckID = null;
			for (var i=0; i<inputs.length; i++) {
				if (inputs[i].name == "id") {
					CheckID = inputs[i].value;
					break;
				}
			}
			if (CheckID == ID && ID!=null) {
				um.toggle_message("Deleting...");
				var postVars  = "PermissionID="+ID+"&Operation=Delete";
				var d = postJSON("SavePermission",postVars);
				d.addCallbacks(um.DeletePermissionClean,um.error_report);
			} else {
				alert('Error: Inconsistency match with deleting IDs - Did you hack the DOM?');
			}
		} else {
			alert('Error: No permission selected for deletion! (Permission must be selected in the top listing)');
		}
	}
}
/*
	DeleteGroupClean: remove the object from DOM and clean up the joined lists
*/
um.DeletePermissionClean = function(d) {
	um.toggle_message('');
	getElement("PermissionEdit_id").value = '';
	getElement("PermissionEdit_PermissionName").value = '';
	getElement("PermissionEdit_PermissionDescription").value = '';
	um.LoadJoinedUsers(null,null);		
	um.LoadJoinedGroups(null,null);		
	var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','PermissionColumn');
	if (elems.length > 0) {
		var el = elems[0];
		swapDOM(el,null);
	}
}
/*
	SelectColumn: Select either the User, Group or Permission column
	show and hide various sections depending on choice.
*/
um.SelectColumn = function(e){
	var el = e.src();//or is it src();
	// Remove the Column-Lite class
	var cols = getElementsByTagAndClassName('DIV','Column-lite',document);
	for (var i=0; i<cols.length; i++) {
		removeElementClass(cols[i],'Column-lite');
	}
	// Remove the ListBoxItem-Lite class
	var cols = getElementsByTagAndClassName('DIV','ListBoxItem-Lite',document);
	for (var i=0; i<cols.length; i++) {
		removeElementClass(cols[i],'ListBoxItem-Lite');
	}
	addElementClass(el,'Column-lite');
	// Modify the columns
	if (el.id=='UserColumn') {
		getElement('JoinedUsers').style.display = 'none';
		getElement('UserEditor').style.display = '';
		getElement('JoinedGroups').style.display = '';
		getElement('GroupEditor').style.display = 'none';
		getElement('JoinedPermissions').style.display = '';
		getElement('PermissionEditor').style.display = 'none';
	} else if (el.id=='GroupColumn') {
		getElement('JoinedUsers').style.display = '';
		getElement('UserEditor').style.display = 'none';
		getElement('JoinedGroups').style.display = 'none';
		getElement('GroupEditor').style.display = '';
		getElement('JoinedPermissions').style.display = '';
		getElement('PermissionEditor').style.display = 'none';
	} else if (el.id=='PermissionColumn') {
		getElement('JoinedUsers').style.display = '';
		getElement('UserEditor').style.display = 'none';
		getElement('JoinedGroups').style.display = '';
		getElement('GroupEditor').style.display = 'none';
		getElement('JoinedPermissions').style.display = 'none';
		getElement('PermissionEditor').style.display = '';
	}
}
/*
	SearchBoxKeydown: Detects a key down event for all the search boxes
*/
um.SearchBoxKeydown = function(e) {
	if (e.key()['string']=='KEY_ENTER') {
		e.stop();
		var el = e.src();
		if (el.id == 'SearchUser') {
			um.LoadUsers();
		} else if (el.id == 'SearchGroup') {
			um.LoadGroups();
		} else if (el.id == 'SearchPermission') {
			um.LoadPermissions();
		}
	}
}
/*
	OnLoad: Attache events when the document is loaded
*/
um.OnLoad = function(e) {
	connect('btnSearchUser','onclick',um.LoadUsers);
	connect('btnSearchGroup','onclick',um.LoadGroups);
	connect('btnSearchPermission','onclick',um.LoadPermissions);
	connect('UserEdit_btnNew','onclick',um.NewUser);
	connect('UserEdit_btnSave','onclick',um.SaveUser);
	connect('UserEdit_btnCancel','onclick',um.CancelUser);
	connect('UserEdit_btnDelete','onclick',um.DeleteUser);
	connect('GroupEdit_btnNew','onclick',um.NewGroup);
	connect('GroupEdit_btnSave','onclick',um.SaveGroup);
	connect('GroupEdit_btnCancel','onclick',um.CancelGroup);
	connect('GroupEdit_btnDelete','onclick',um.DeleteGroup);
	connect('PermissionEdit_btnNew','onclick',um.NewPermission);
	connect('PermissionEdit_btnSave','onclick',um.SavePermission);
	connect('PermissionEdit_btnCancel','onclick',um.CancelPermission);
	connect('PermissionEdit_btnDelete','onclick',um.DeletePermission);
	connect('SearchUser','onkeydown',um.SearchBoxKeydown);
	connect('SearchGroup','onkeydown',um.SearchBoxKeydown);
	connect('SearchPermission','onkeydown',um.SearchBoxKeydown);
	connect('UserColumn','ondblclick',um.SelectColumn);
	connect('GroupColumn','ondblclick',um.SelectColumn);
	connect('PermissionColumn','ondblclick',um.SelectColumn);
	// Initialize our screen for users
	getElement('JoinedUsers').style.display = 'none';
	getElement('UserEditor').style.display = '';
	getElement('JoinedGroups').style.display = '';
	getElement('GroupEditor').style.display = 'none';
	getElement('JoinedPermissions').style.display = '';
	getElement('PermissionEditor').style.display = 'none';
	um.LoadUsers();
}
connect(window,'onload',um.OnLoad);