import logging
import sys
import simplejson
import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears import exception_handler
import model
from model import DATE_FORMAT

log = logging.getLogger("turbocare.controllers")

class UserManager(controllers.RootController):
#===== Inventory App Stuff ====================================================
	@expose(html='turbocare.templates.usermanager')
	def index(self, **kw):
		return dict()

	@expose(html='turbocare.templates.programmingerror')
	def idFail(error):
		error= "Not Permited to do operation"
		log.debug(error)
		next_link = "/configuration/"
		return dict(error_message = error, next_link=next_link)
		
	@expose(html='turbocare.templates.programmingerror')
	def ProgrammingError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		if next_link == '':
			next_link = "/configuration/"
		return dict(error_message = error, next_link=next_link)

	@expose(html='turbocare.templates.dataentryerror')
	def DataEntryError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		if next_link == '':
			next_link = "/configuration/"
		return dict(error_message = error, next_link=next_link)
	
	@expose(format='json')
	@validate(validators={'SearchText':validators.String(),'GroupID':validators.Int(),'UserID':validators.Int(),
	'PermissionID':validators.Int()})
	def FindUsers(self, SearchText='', UserID=None, GroupID=None, PermissionID=None, **kw):
		'''	Return a list of users  '''
		if SearchText != '':
			# Search for the users
			SearchText = str(SearchText)
			Users = model.User.select(OR (model.User.q.user_name.contains(SearchText),
				model.User.q.email_address.contains(SearchText), model.User.q.display_name.contains(SearchText)),
				orderBy=[model.User.q.user_name])
			users = [dict(id=x.id, name="%s [%s]" % (x.user_name, x.display_name), db=x) for x in Users]
		elif GroupID != None:
			Group = model.Group.get(GroupID)
			users =  [dict(id=x.id, name="%s [%s]" % (x.user_name, x.display_name), db=x) for x in Group.users]
		elif PermissionID != None:
			Permission = model.Permission.get(PermissionID)
			for group in Permission.groups:
				users =  [dict(id=x.id, name="%s [%s]" % (x.user_name, x.display_name), db=x) for x in group.users]
		elif UserID != None:
			User = model.User.get(UserID)
			users = [dict(id=User.id,name="%s [%s]" % (User.user_name, User.display_name), db=User)]
		else:
			# Search for all users
			Users = model.User.select(orderBy=[model.User.q.user_name])
			users = [dict(id=x.id, name="%s [%s]" % (x.user_name, x.display_name), db=x) for x in Users]			
		return dict(users=users)

	@expose(format='json')
	@validate(validators={'SearchText':validators.String(),'GroupID':validators.Int(),'UserID':validators.Int(),
	'PermissionID':validators.Int()})
	def FindGroups(self, SearchText='', UserID=None, GroupID=None, PermissionID=None, **kw):
		'''	Return a list of groups  '''
		if SearchText != '':
			# Search for the groups
			SearchText = str(SearchText)
			Groups = model.Group.select(OR (model.Group.q.group_name.contains(SearchText),
				model.Group.q.display_name.contains(SearchText)),
				orderBy=[model.Group.q.group_name])
			groups = [dict(id=x.id, name="%s [%s]" % (x.group_name, x.display_name), db=x) for x in Groups]
		elif UserID != None:
			User = model.User.get(UserID)
			groups =  [dict(id=x.id, name="%s [%s]" % (x.group_name, x.display_name), db=x) for x in User.groups]
		elif PermissionID != None:
			Permission = model.Permission.get(PermissionID)
			groups =  [dict(id=x.id, name="%s [%s]" % (x.group_name, x.display_name), db=x) for x in Permission.groups]
		elif GroupID != None:
			Group = model.Group.get(GroupID)
			groups = [dict(id=Group.id,name="%s [%s]" % (Group.group_name, Group.display_name), db=Group)]
		else:
			# Search for all groups
			Groups = model.Group.select(orderBy=[model.Group.q.group_name])
			groups = [dict(id=x.id, name="%s [%s]" % (x.group_name, x.display_name), db=x) for x in Groups]
		return dict(groups=groups)

	@expose(format='json')
	@validate(validators={'SearchText':validators.String(),'GroupID':validators.Int(),'UserID':validators.Int(),
	'PermissionID':validators.Int()})
	def FindPermissions(self, SearchText='', UserID=None, GroupID=None, PermissionID=None, **kw):
		'''	Return a list of permissions  '''
		if SearchText != '':
			# Search for the permissions
			SearchText = str(SearchText)
			Permissions = model.Permission.select(OR (model.Permission.q.permission_name.contains(SearchText),
				model.Permission.q.description.contains(SearchText)),
				orderBy=[model.Permission.q.permission_name])
			permissions = [dict(id=x.id, name="%s [%s]" % (x.permission_name, x.description), db=x) for x in Permissions]
		elif GroupID != None:
			Group = model.Group.get(GroupID)
			permissions =  [dict(id=x.id, name="%s [%s]" % (x.permission_name, x.description), db=x) for x in Group.permissions]
		elif UserID != None:
			User = model.User.get(UserID)
			for group in User.groups:
				permissions =  [dict(id=x.id, name="%s [%s]" % (x.permission_name, x.description), db=x) for x in group.permissions]
		elif PermissionID != None:
			Permission = model.Permission.get(PermissionID)
			permissions = [dict(id=Permission.id,name="%s [%s]" % (Permission.permission_name, Permission.description), db=Permission)]
		else:
			# Search for all permissions
			Permissions = model.Permission.select(orderBy=[model.Permission.q.permission_name])
			permissions = [dict(id=x.id, name="%s [%s]" % (x.permission_name, x.description), db=x) for x in Permissions]
		return dict(permissions=permissions)
		
	@expose(format='json')
	@validate(validators={'Password':validators.String(),'UserID':validators.Int(),'UserName':validators.String(),
	'DisplayName':validators.String(),'EmailAddress':validators.String(),'Operation':validators.String()})
	def SaveUser(self, UserID=None, Groups=[], Password='', UserName='', DisplayName='', 
		EmailAddress='', Operation='', **kw):
		'''	Add/Update/Delete a user  '''
		if Operation == 'New':
			# Create a new user linked to the groups.
			# Note: The password is autmatically hashed when the record is saved.  This is done on the SQLObject object.
			User = model.User(user_name=UserName, display_name=DisplayName, password=Password, 
				email_address=EmailAddress)
			# Add the user to the groups (by id)
			if isinstance(Groups, basestring): # only one group was added
				User.addGroup(int(Groups))
			else:
				for group in Groups:
					User.addGroup(int(group))
			message = "New User Added Successfully"
		elif Operation == 'Save' and UserID != None:
			User = model.User.get(UserID)
			User.user_name = UserName
			User.display_name = DisplayName
			User.email_address = EmailAddress
			if Password != '':
				User.password = Password
			# Make a listing of the new groups
			if isinstance(Groups, basestring):
				NewGroups = [int(Groups)]
			else:
				NewGroups = [int(x) for x in Groups]
			# Make a listing of our current groups
			CurrGroups = [x.id for x in User.groups]
			# Add new groups
			for group in NewGroups:
				if not group in CurrGroups:
					User.addGroup(group)
			# Remove deleted groups
			for group in CurrGroups:
				if not group in NewGroups:
					User.removeGroup(group)
			message = "User Updated Successfully"
		elif Operation == 'Delete' and UserID != None:
			User = model.User.get(UserID)
			# Remove groups
			for group in User.groups:
				User.removeGroup(group)
			# Delete the User
			User.destroySelf()
			message="User Deleted"
		else:
			message = "Operation Failed"
		return dict(message=message)

	@expose(format='json')
	@validate(validators={'GroupID':validators.Int(),'GroupName':validators.String(),'DisplayName':validators.String(),
	'Operation':validators.String()})
	def SaveGroup(self, GroupID=None, Users=[], Permissions=[], GroupName='', DisplayName='', Operation='', **kw):
		'''	Add/Update/Delete a group  '''
		if Operation == 'New':
			# Create a new group
			Group = model.Group(group_name=GroupName, display_name=DisplayName)
			# Add the user to the groups (by id)
			if isinstance(Users, basestring): # only one user was added
				Group.addUser(int(Users))
			else:
				for user in Users:
					Group.addUser(int(user))
			if isinstance(Permissions, basestring): # only one user was added
				Group.addPermission(int(Permissions))
			else:
				for permission in Permissions:
					Group.addPermission(int(permission))
			message = "New Group Added Successfully"
		elif Operation == 'Save' and GroupID != None:
			Group = model.Group.get(GroupID)
			Group.group_name = GroupName
			Group.display_name = DisplayName
			# Get our New users list
			if isinstance(Users, basestring):
				NewUsers = [int(Users)]
			else:
				NewUsers = [int(x) for x in Users]
			# Get our current user list
			CurrUsers = [x.id for x in Group.users]
			# Add new users
			for user in NewUsers:
				if not user in CurrUsers:
					Group.addUser(user)
			# Remove deleted users
			for user in CurrUsers:
				if not user in NewUsers:
					Group.removeUser(user)
			# Get our New Permissions list
			if isinstance(Permissions, basestring):
				NewPermissions = [int(Permissions)]
			else:
				NewPermissions = [int(x) for x in Permissions]
			# Get our current permissions
			CurrPermissions = [x.id for x in Group.permissions]
			# Add new permissions
			for permission in NewPermissions:
				if not permission in CurrPermissions:
					Group.addPermission(permission)
			# Remove deleted users
			for permission in CurrPermissions:
				if not permission in NewPermissions:
					Group.removePermission(permission)
			message = "Group Updated Successfully"
		elif Operation == 'Delete' and GroupID != None:
			Group = model.Group.get(GroupID)
			# Remove users
			for user in Group.users:
				Group.removeUser(user)
			# Remove permission
			for permission in Group.permissions:
				Group.removePermission(permission)
			# Delete the Group
			Group.destroySelf()
			message="Group Deleted"
		else:
			message = "Operation Failed"
		return dict(message=message)

	@expose(format='json')
	@validate(validators={'PermissionID':validators.Int(),'PermissionName':validators.String(),
	'Description':validators.String(),'Operation':validators.String()})
	def SavePermission(self, PermissionID=None, Groups=[], PermissionName='', Description='', Operation='', **kw):
		'''	Add/Update/Delete a permission  '''
		if Operation == 'New':
			# Create a new permission linked to the groups.
			Permission = model.Permission(permission_name=PermissionName, description=Description)
			# Add the permission to the groups (by id)
			if isinstance(Groups, basestring): # only one group was added
				Permission.addGroup(int(Groups))
			else:
				for group in Groups:
					Permission.addGroup(int(group))
			message = "New Permission Added Successfully"
		elif Operation == 'Save' and PermissionID != None:
			Permission = model.Permission.get(PermissionID)
			Permission.permission_name = PermissionName
			Permission.description = Description
			# Make a listing of the new groups
			if isinstance(Groups, basestring):
				NewGroups = [int(Groups)]
			else:
				NewGroups = [int(x) for x in Groups]
			# Make a listing of our current groups
			CurrGroups = [x.id for x in Permission.groups]
			# Add new groups
			for group in NewGroups:
				if not group in CurrGroups:
					Permission.addGroup(group)
			# Remove deleted groups
			for group in CurrGroups:
				if not group in NewGroups:
					Permission.removeGroup(group)
			message = "Permission Updated Successfully"
		elif Operation == 'Delete' and PermissionID != None:
			Permission = model.Permission.get(PermissionID)
			# Remove groups
			for group in Permission.groups:
				Permission.removeGroup(group)
			# Delete the Permission
			Permission.destroySelf()
			message="Permission Deleted"
		else:
			message = "Operation Failed"
		return dict(message=message)