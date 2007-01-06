function postJSON(url, postVars) {
	um.toggle_message("Sending request...");
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
}

function hasParent(id,parent_id) {
	var node = getElement(id);
	var ret_val = false;
	while (node.parentNode != null) {
		if (node.parentNode.id == parent_id){
			ret_val = true;
		}
		node = node.parentNode;
	}
	return ret_val;
}

var um = {};
var um.NextJoinList = '';// String representation of the function to execute

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
	if (hasElementClass("UserColumn","Column-lite")) {
		var el = e.src().parentNode;
		// Remove hi-lite from hi-lited items
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','UserColumn');
		for (var i=0; i<elems.length; i++) {
			removeElementClass(elems[i],'ListBoxItem-Lite');
			addElementClass(elems[i],'ListBoxItem');
		}
		// Add hi-lite to current item
		removeElementClass(el,'ListBoxItem');
		addElementClass(el,'ListBoxItem-Lite');
		// Move the item values to the form below
		getElement("UserEdit_Password").value = '';
		getElement("UserEdit_PasswordVerify").value = '';
		var inputs = getElementsByTagAndClassName('INPUT',null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id") {
				getElement("UserEdit_id").value = inputs[i].value;
			} else if (inputs[i].name == "UserName") {
				getElement("UserEdit_UserName").value = inputs[i].value;
			} else if (inputs[i].name == "DisplayName") {
				getElement("UserEdit_DisplayName").value = inputs[i].value;
			} else if (inputs[i].name == "EmailAddress") {
				getElement("UserEdit_EmailAddress").value = inputs[i].value;
			}
		}
		
	}
}
/*
	SelectGroup: When an entry is selected, copy the elements to the form below for editing
	This is only done when the column is in edit mode
*/
um.SelectGroup = function(e) {
	if (hasElementClass("GroupColumn","Column-lite")) {
		var el = e.src().parentNode;
		// Remove hi-lite from hi-lited items
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','GroupColumn');
		for (var i=0; i<elems.length; i++) {
			removeElementClass(elems[i],'ListBoxItem-Lite');
			addElementClass(elems[i],'ListBoxItem');
		}
		// Add hi-lite to current item
		removeElementClass(el,'ListBoxItem');
		addElementClass(el,'ListBoxItem-Lite');
		// Move the item values to the form below
		var inputs = getElementsByTagAndClassName('INPUT',null,el);
		for (var i=0; i<inputs.length; i++) {
			if (inputs[i].name == "id") {
				getElement("GroupEdit_id").value = inputs[i].value;
			} else if (inputs[i].name == "GroupName") {
				getElement("GroupEdit_GroupName").value = inputs[i].value;
			} else if (inputs[i].name == "DisplayName") {
				getElement("GroupEdit_DisplayName").value = inputs[i].value;
			}
		}
		
	}
}
/*
	SelectPermission: When an entry is selected, copy the elements to the form below for editing
	This is only done when the column is in edit mode
*/
um.SelectPermission = function(e) {
	if (hasElementClass("PermissionColumn","Column-lite")) {
		var el = e.src().parentNode;
		// Remove hi-lite from hi-lited items
		var elems = getElementsByTagAndClassName('DIV','ListBoxItem-Lite','PermissionColumn');
		for (var i=0; i<elems.length; i++) {
			removeElementClass(elems[i],'ListBoxItem-Lite');
			addElementClass(elems[i],'ListBoxItem');
		}
		// Add hi-lite to current item
		removeElementClass(el,'ListBoxItem');
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
	if (GroupID==null&&PermissionID==null) {
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
	if (UserID==null&&PermissionID==null) {
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
	if (UserID!=null) {
		var postVars = 'UserID='+UserID;
	} else {
		var postVars = 'GroupID='+GroupID;
	}
	var d = postJSON("FindPermissions",postVars);
	d.addCallbacks(um.RenderJoinedPermissions,um.error_report);
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
				getElement("UserEdit_id").value = inputs[i].value;
			} else if (inputs[i].name == "UserName") {
				getElement("UserEdit_UserName").value = inputs[i].value;
			} else if (inputs[i].name == "DisplayName") {
				getElement("UserEdit_DisplayName").value = inputs[i].value;
			} else if (inputs[i].name == "EmailAddress") {
				getElement("UserEdit_EmailAddress").value = inputs[i].value;
			}
		}
	} else { // we created a new user, now we're resetting
		getElement("UserEdit_Password").value = '';
		getElement("UserEdit_PasswordVerify").value = '';
		getElement("UserEdit_id").value = '';
		getElement("UserEdit_UserName").value = '';
		getElement("UserEdit_DisplayName").value = '';
		getElement("UserEdit_EmailAddress").value = '';
	}
}
/*
	NewUser: make a blank entry
*/
um.NewUser = function(e){
	if (confirm('Are you sure you want a new entry?')){
		getElement("UserEdit_Password").value = '';
		getElement("UserEdit_PasswordVerify").value = '';
		getElement("UserEdit_id").value = '';
		getElement("UserEdit_UserName").value = '';
		getElement("UserEdit_DisplayName").value = '';
		getElement("UserEdit_EmailAddress").value = '';
	}
}
/*
	DeleteUser: delete the entry
*/
um.DeleteUser = function(e){
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
			// Remove the DOM object because the delete will most likely succeed
			var postVars  = "UserID="+ID+"&Operation=Delete";
			var d = postJSON("SaveUser",postVars);
			d.addCallbacks(um.updated,um.error_report);
		} else {
			alert('Error: Inconsistency match with deleting IDs - Did you hack the DOM?');
		}
	} else {
		alert('Error: No user selected for deletion! (User must be slected in the top listing)');
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
		var postVars  = "GroupID="+ID+"&GroupName="+GroupName+"&DisplayName="+DisplayName;
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
				getElement("GroupEdit_id").value = inputs[i].value;
			} else if (inputs[i].name == "GroupName") {
				getElement("GroupEdit_GroupName").value = inputs[i].value;
			} else if (inputs[i].name == "DisplayName") {
				getElement("GroupEdit_DisplayName").value = inputs[i].value;
			}
		}
	} else { // we created a new user, now we're resetting
		getElement("GroupEdit_id").value = '';
		getElement("GroupEdit_GroupName").value = '';
		getElement("GroupEdit_DisplayName").value = '';
	}
}
/*
	NewGroup: Make a blank entry
*/
um.NewUser = function(e){
	if (confirm('Are you sure you want a new entry?'))
		getElement("GroupEdit_id").value = '';
		getElement("GroupEdit_GroupName").value = '';
		getElement("GroupEdit_DisplayName").value = '';
	}
}
/*
	DeleteUser: Save the entry
*/
um.DeleteUser = function(e){
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
			// Remove the DOM object because the delete will most likely succeed
			var postVars  = "UserID="+ID+"&Operation=Delete";
			var d = postJSON("SaveUser",postVars);
			d.addCallbacks(um.updated,um.error_report);
		} else {
			alert('Error: Inconsistency match with deleting IDs - Did you hack the DOM?');
		}
	} else {
		alert('Error: No user selected for deletion! (User must be slected in the top listing)');
	}	
}
um.showPOVendor = function(id){
	var purchaseorders = getElement("PurchaseOrders");
	//first, hide all other Purchase order vendor lines
	var elems = getElementsByTagAndClassName(null,"listingrowcontain_show",purchaseorders);
	if (elems.length > 0) {
		for (var i=0;i<elems.length;i++){
			swapElementClass(elems[i],"listingrowcontain_show","listingrowcontain");
			//removeEmptyTextNodes(elems[i]);
			//var sub_elems = getElementsByTagAndClassName(null, "listingrow", elems[i]);
			var sub_elems = getElementsByTagAndClassName('DIV',null, elems[i]);
			for (var j=0;j<sub_elems.length;j++){
				//alert(sub_elems[j].id);
				//swapElementClass(sub_elems[j],"listingrow","listingrow_hidden");
				setNodeAttribute(sub_elems[j],'style','display:none');
			}
		}
	}
	//Now show our selected line
	var elem = getElement(id);
	if (getNodeAttribute(elem,"class") == null){
		alert('help me, i am stuck in the computer, let me out.');
	} else {
		swapElementClass(elem,"listingrowcontain","listingrowcontain_show");
		//var elems = getElementsByTagAndClassName(null, "listingrow_hidden", elem);
		var elems = getElementsByTagAndClassName('DIV',null, elem);
		for (var i=0;i<elems.length;i++){
			//	alert(elems[j].id);
			//swapElementClass(elems[i],"listingrow_hidden", "listingrow");
			setNodeAttribute(elems[i],'style','display:block');
		}
	}
}

um.hidePOVendor = function(id){
	elem = getElement(id);
	for (var i=1;i<elem.childNodes.length;i++){
		makeInvisible(elem.childNodes[i]);
	}
}

um.moveItem = function(){
	var purchaseorders = getElement("PurchaseOrders");
	//get the vendor
	var elems = getElementsByTagAndClassName(null,"listingrow_vendor",document);
	var vendor = elems[0];
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_vendor","listingrow");
	}
	//get the catalogitem
	var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
	if (elems.length < 1) {
		alert('There is a problem with the javascript.');
	}
	var catalogitem = elems[0];
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_item","listingrow");
	}
	if ((vendor == null) || (catalogitem == null)){
		alert("First, choose a catalog item and a vendor.");
	} else {
		//look for vendor in purchase order list
		var vendor_po = getElement("PO_"+vendor.id);
		var linkdiv = createDOM('DIV',{'id':'closelink_'+catalogitem.id, 'class':'listingrow'});
		var closelink = createDOM('A',{'href':'javascript:um.removeItem("'+catalogitem.id+'")'}, "Remove");
		linkdiv.appendChild(closelink);
		if (getNodeAttribute(vendor_po,"class") == null) {
			elems = getElementsByTagAndClassName("input",null,vendor);
			for (i=0;i<elems.length;i++){
				if (elems[i].name == "vendorname"){
					var VendorName = elems[i].value;
				}
			}
			var vendor_po = createDOM('DIV',{'id':'PO_'+vendor.id, 'class':'listingrowcontain', 'onclick':'um.showPOVendor("PO_'+vendor.id+'")'},VendorName);
			vendor_po.appendChild(linkdiv);
			vendor_po.appendChild(catalogitem.cloneNode(true));
			swapDOM(catalogitem,null);
			purchaseorders.appendChild(vendor_po);
		} else {
			vendor_po.appendChild(linkdiv);
			vendor_po.appendChild(catalogitem.cloneNode(true));
			swapDOM(catalogitem,null);
		}
		//show our current po vendor line
		um.showPOVendor('PO_'+vendor.id);
		um.clearVendors();
	}
}

um.selectVendor = function(id){
	//deselect any previous vendor and select current vendor
	var elems = getElementsByTagAndClassName(null,"listingrow_vendor",document);
	for (var i=0;i<elems.length;i++){
		swapElementClass(elems[i],"listingrow_vendor","listingrow");
	}
	vendor = getElement("vendor_"+id);
	swapElementClass(vendor,"listingrow","listingrow_vendor");
	//Find the current quote price
	for (var i=0;i<vendor.childNodes.length;i++){
		if (vendor.childNodes[i].name == 'QuotePrice'){
			var QuotePrice = vendor.childNodes[i].value;
		}
		if (vendor.childNodes[i].name == 'id'){
			var VendorId = vendor.childNodes[i].value;
		}
	}	
	//find the selected catalog item and change the quote price
	var elems = getElementsByTagAndClassName(null,"listingrow_item",document);
	var catalogitem = elems[0];
	if (getNodeAttribute(catalogitem,"class") == "listingrow_item"){
		elems = getElementsByTagAndClassName("input",null,catalogitem);
		for (var i=0;i<elems.length;i++){
			if (elems[i].name == 'QuotePrice'){
				elems[i].value = QuotePrice;
			}
			if (elems[i].name == 'Vendor'){
				elems[i].value = VendorId;
			}
		}
	}
}

um.openListing = function(url,dest){
	//This also does a search like above
	//url: Where to get the data; dest: where to place the result object, defaults to main location
	if (dest != null){
		um.list_dest = dest;
	} else {
		um.list_dest = null;
	}
	if (url != null){
		um.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(um.renderListing);
	}
}

um.openPickList = function(url){
	if (url != null){
		um.toggle_message("Loading...");
	 	var d = loadJSONDoc(url);
	  	d.addCallback(um.pickList);
	}
}

// load view/form data =========

um.clearVendors = function() {
	var vendors = createDOM('DIV',{'id':'vendors', 'style':'overflow:auto;'});
	swapDOM('vendors',vendors);
}
um.renderVendors = function(data){
	var tr = function(label, data){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',data);
		row.appendChild(label);
		row.appendChild(data);
		return row;
	}
	var vendorDiv = function(record){
		var br = createDOM('BR',null);
		var div = createDOM('DIV',{'class':'listingrow','id':'vendor_'+record.id, 'ondblclick':'um.selectVendor('+record.id+')'});
		var vendorname = createDOM('INPUT',{'type':'hidden', 'name':'vendorname', 'value':record.Name + ", " + record.Description});
		var vendorid = createDOM('INPUT',{'type':'hidden', 'name':'id', 'value':record.id});
		var quoteprice = createDOM('INPUT',{'type':'hidden', 'name':'QuotePrice', 'value':record.Price});
		var table = createDOM('TABLE',{'class':'minimal'});
		var tbody = createDOM('TBODY',null);
		appendChildNodes(tbody, tr("Name",record.Name + ", " + record.Description), tr("Ranking",record.Ranking), tr("Product",record.Product), tr("Price","Rs. " + record.Price), tr("Notes",record.Notes), tr("Valid starting",record.ValidOn));
		table.appendChild(tbody);
		div.appendChild(vendorname);
		div.appendChild(vendorid);
		div.appendChild(quoteprice);
		div.appendChild(table);
		return div;
	}
	um.toggle_message();
	var vendors = createDOM('DIV',{'id':'vendors', 'style':'overflow:auto;'});
	for (var i=0; i<data.items.length;i++){
		var record = data.items[i];
		if (record.Status != 'deleted'){
			vendors.appendChild(vendorDiv(record));
		}
	}
	swapDOM('vendors',vendors);
}

connect(document,'onload',um.OnLoad);