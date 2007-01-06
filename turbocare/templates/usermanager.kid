<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
 
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <LINK HREF="/static/css/table.css" TYPE="text/css" REL="stylesheet"/>
    <title>User Manager</title>
	<style type="text/css">
		.ColumnTitle { position: relative;
			text-align: center;
			vertical-align: top;
			font-size: 14px;}
		.Column { position: relative;
			display: table-cell;
			padding: 5px 5px 5px 5px;
			width: 250px;
			border: 1px solid gray;
			font-size: 10px;}
		.Column-lite { position: relative;
			display: table-cell;
			padding: 5px 5px 5px 5px;
			margin: 5px 5px 5px 5px;
			width: 250px;
			border: 1px solid gray;
			background-color: yellow;
			font-size: 10px;}
		.ListingBox { position: relative;
			padding: 1px 1px 1px 1px;
			margin: 1px 1px 1px 1px;
			width: 200px;
			height: 150px;
			left: 8%;
			border: 1px solid gray;
			background-color: lightgray;
			font-size: 10px;
			overflow: auto;}
	</style></head>
<body>
	<DIV style="text-align:center; width:100%; left:10%; position:relative">
		<DIV class="Column-lite">
			<div class="ColumnTitle">Users</div>
			<Table>
				<TBODY>
					<TR>
						<TD>Search</TD>
						<TD><INPUT type="text" name="SearchUser" value="" /></TD>
					</TR>
					<TR>
						<TD colspan="2" style="text-align:right"><BUTTON type="button" id="btnSearchUser" name="btnSearchUser" value="Search">Search</BUTTON></TD>
					</TR>
				</TBODY>
			</Table>
			<div id="UserList" style="text-align:center">
				<DIV id="UserListSelect" class="ListingBox">
				</DIV>
			</div>
			<div id="JoinedUsers" style="text-align:center">
				<div>Linked Users</div>
				<DIV id="JoinedUsersSelect" class="ListingBox">
				</DIV>
			</div>
			<DIV id="UserEditor">
				<Table>
					<TBODY>
						<TR>
							<TD>Login ID</TD>
							<TD><INPUT type="text" name="UserName" value="" /></TD>
						</TR>
						<TR>
							<TD>Display name</TD>
							<TD><INPUT type="text" name="DisplayName" value="" /></TD>
						</TR>
						<TR>
							<TD>Email address</TD>
							<TD><INPUT type="text" name="EmailAddress" value="" /></TD>
						</TR>
						<TR>
							<TD>Password</TD>
							<TD><INPUT type="text" name="Password" value="" /></TD>
						</TR>
						<TR>
							<TD>Password verify</TD>
							<TD><INPUT type="text" name="PasswordVerify" value="" /></TD>
						</TR>
					</TBODY>
				</Table>
				<DIV style="text-align:center">
					<BUTTON type="button" name="btnNew" value="New">New</BUTTON>
					<BUTTON type="button" name="btnSave" value="Save">Save</BUTTON>
					<BUTTON type="button" name="btnCancel" value="Cancel">Cancel</BUTTON>
					<BUTTON type="button" name="btnDelete" value="Delete">Delete</BUTTON>
				</DIV>
			</DIV>
		</DIV>
		<DIV class="Column">
			<div class="ColumnTitle">Groups</div>
			<Table>
				<TBODY>
					<TR>
						<TD>Search</TD>
						<TD><INPUT type="text" id="SearchGroup" name="SearchGroup" value="" /></TD>
					</TR>
					<TR>
						<TD colspan="2" style="text-align:right"><BUTTON type="button" id="btnSearchGroup" name="btnSearchGroup" value="Search">Search</BUTTON></TD>
					</TR>
				</TBODY>
			</Table>
			<div id="GroupList" style="text-align:center">
				<DIV id="GroupListSelect" class="ListingBox">
				</DIV>
			</div>
			<div id="JoinedGroups" style="text-align:center">
				<div>Linked Groups</div>
				<DIV id="JoinedGroupsSelect" class="ListingBox">
				</DIV>
			</div>
			<DIV id="GroupEditor">
				<Table>
					<TBODY>
						<TR>
							<TD>Group Name</TD>
							<TD><INPUT type="text" name="GroupName" value="" /></TD>
						</TR>
						<TR>
							<TD>Display Name</TD>
							<TD><INPUT type="text" name="DisplayName" value="" /></TD>
						</TR>
					</TBODY>
				</Table>
				<DIV style="text-align:center">
					<BUTTON type="button" name="btnNew" value="New">New</BUTTON>
					<BUTTON type="button" name="btnSave" value="Save">Save</BUTTON>
					<BUTTON type="button" name="btnCancel" value="Cancel">Cancel</BUTTON>
					<BUTTON type="button" name="btnDelete" value="Delete">Delete</BUTTON>
				</DIV>
			</DIV>
		</DIV>
		<DIV class="Column">
			<div class="ColumnTitle">Permissions</div>
			<Table>
				<TBODY>
					<TR>
						<TD>Search</TD>
						<TD><INPUT type="text" id="SearchPermissions" name="SearchPermissions" value="" /></TD>
					</TR>
					<TR>
						<TD colspan="2" style="text-align:right"><BUTTON type="button" id="btnSearchPermissions" name="btnSearchPermissions" value="Search">Search</BUTTON></TD>
					</TR>
				</TBODY>
			</Table>
			<div id="PermissionsList" style="text-align:center">
				<DIV id="PermissionsListSelect" class="ListingBox">
				</DIV>
			</div>
			<div id="JoinedPermissions" style="text-align:center">
				<div>Linked Permission</div>
				<DIV id="JoinedPermissionsSelect" class="ListingBox">
				</DIV>
			</div>
			<DIV id="PermissionEditor">
				<Table>
					<TBODY>
						<TR>
							<TD>Permission Name</TD>
							<TD><INPUT type="text" name="PermissionName" value="" /></TD>
						</TR>
						<TR>
							<TD>Permission Description</TD>
							<TD><INPUT type="text" name="PermissionDescription" value="" /></TD>
						</TR>
					</TBODY>
				</Table>
				<DIV style="text-align:center">
					<BUTTON type="button" name="btnNew" value="New">New</BUTTON>
					<BUTTON type="button" name="btnSave" value="Save">Save</BUTTON>
					<BUTTON type="button" name="btnCancel" value="Cancel">Cancel</BUTTON>
					<BUTTON type="button" name="btnDelete" value="Delete">Delete</BUTTON>
				</DIV>
			</DIV>
		</DIV>
	</DIV>
</body>
</html>
