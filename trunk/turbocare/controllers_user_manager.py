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

# Lists of users, groups and permissions which the program will refuse to delete
mandatory_users = ['admin']
mandatory_groups = ['admin', 'superuser']
mandatory_permissions =  ['admin_users']
mandatory_user_group = [('admin','admin'),('admin','superuser')]
mandatory_group_permission = [('admin','admin_users'),('superuser','admin_users')]

class UserManager(controllers.RootController):
	
	def __init__(self):
		'''	Make sure the mandatory users, groups and permissions exist '''
		# Check the users
		for user in mandatory_users:
			users = model.User.select(model.User.q.user_name==user)
			if users.count() == 0:
				User = model.User(user_name=user, display_name=user, password=user)
		# Check groups
		for group in mandatory_groups:
			groups = model.Group.select(model.Group.q.group_name==group)
			if groups.count() == 0:
				Group = model.Group(group_name=group, display_name=group)
		# Check permissions
		for permission in mandatory_permissions:
			permissions = model.Permission.select(model.Permission.q.permission_name==permission)
			if permissions.count() == 0:
				Permission = model.Permission(permission_name=permission, description=permission)		
		# Check the user groups
		for ug in mandatory_user_group:
			try:
				user = model.User.select(model.User.q.user_name==ug[0])[0]
				group = model.Group.select(model.Group.q.group_name==ug[1])[0].id
				CurrGroups = [x.id for x in user.groups]
				if not group in CurrGroups:
					user.addGroup(group)
			except:
				log.debug('The user/group combo %r generated an error' % ug)
		# Check the group permissions
		for gp in mandatory_group_permission:
			try:
				group = model.Group.select(model.Group.q.group_name==gp[0])[0]
				permission = model.Permission.select(model.Permission.q.permission_name==gp[1])[0].id
				CurrPermissions = [x.id for x in group.permissions]
				if not permission in CurrPermissions:
					group.addPermission(permission)
			except:
				log.debug('The group/permission combo %r generated an error' % gp)
				
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
			users = [] 
			userids = []
			for group in Permission.groups:
				for user in group.users:
					if not user.id in userids:
						users.append(dict(id=user.id, name="%s [%s]" % (user.user_name, user.display_name), db=user))
						userids.append(user.id)
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
			permissions = [] 
			permissionids = []
			for group in User.groups:
				for permission in group.permissions:
					if not permission.id in permissionids:
						permissionids.append(permission.id)
						permissions.append(dict(id=permission.id,
							name="%s [%s]" % (permission.permission_name, permission.description), db=permission) )
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
			# First, check to see that no other user with the login id exists
			checkusers = model.User.select(model.User.q.user_name==str(UserName))
			if checkusers.count() == 0:
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
				UserID = User.id
			else:
				message = "Failed! User with that id already exists"
				UserID = checkusers[0].id
		elif Operation == 'Save' and UserID != None:
			message = ''
			User = model.User.get(UserID)
			if User.user_name in mandatory_users and UserName!=User.user_name:
				message = 'Cannot change the user name for this user.'
			else:
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
			if message == '':
				message = "User Updated Successfully"
			UserID = User.id
		elif Operation == 'Delete' and UserID != None:
			User = model.User.get(UserID)
			UserID = None
			if User.user_name in mandatory_users:
				message = "ERROR: Cannot delete this user, operation failed"
			else:
				# Remove groups
				for group in User.groups:
					User.removeGroup(group)
				# Delete the User
				User.destroySelf()
				message="User Deleted"
		else:
			message = "Operation Failed"
		return dict(message=message,UserID=UserID)

	@expose(format='json')
	@validate(validators={'GroupID':validators.Int(),'GroupName':validators.String(),'DisplayName':validators.String(),
	'Operation':validators.String()})
	def SaveGroup(self, GroupID=None, Users=[], Permissions=[], GroupName='', DisplayName='', Operation='', **kw):
		'''	Add/Update/Delete a group  '''
		if Operation == 'New':
			# Create a new group
			# Make sure we're not adding a duplicate group
			checkgroups = model.Group.select(model.Group.q.group_name==str(GroupName))
			if checkgroups.count() == 0:
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
				GroupID = Group.id
			else:
				message = "Failed! At least one group with that name already exists"
				GroupID = checkgrups[0].id
		elif Operation == 'Save' and GroupID != None:
			message = ''
			Group = model.Group.get(GroupID)
			if Group.group_name in mandatory_groups and Group.group_name!=GroupName:
				message = "Cannot change the group name for this group"
			else:
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
			if message == '':
				message = "Group Updated Successfully"
		elif Operation == 'Delete' and GroupID != None:
			Group = model.Group.get(GroupID)
			GroupID = None
			if Group.group_name in mandatory_groups:
				message = "ERROR: Cannot delete this group, operation failed"
			else:
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
		return dict(message=message, GroupID=GroupID)

	@expose(format='json')
	@validate(validators={'PermissionID':validators.Int(),'PermissionName':validators.String(),
	'Description':validators.String(),'Operation':validators.String()})
	def SavePermission(self, PermissionID=None, Groups=[], PermissionName='', Description='', Operation='', **kw):
		'''	Add/Update/Delete a permission  '''
		if Operation == 'New':
			# Create a new permission linked to the groups.
			# Make sure we're not adding a duplicate permission
			checkpermissions = model.Permission.select(model.Permission.q.permission_name==str(PermissionName))
			if checkpermissions.count() == 0:
				Permission = model.Permission(permission_name=PermissionName, description=Description)
				# Add the permission to the groups (by id)
				if isinstance(Groups, basestring): # only one group was added
					Permission.addGroup(int(Groups))
				else:
					for group in Groups:
						Permission.addGroup(int(group))
				message = "New Permission Added Successfully"
				PermissionID = Permission.id
			else:
				message = "Failed! At least one permission with that name already exists."
				PermissionID = checkpermissions[0].id
		elif Operation == 'Save' and PermissionID != None:
			message = ''
			Permission = model.Permission.get(PermissionID)
			if Permission.permission_name in mandatory_permissions and Permission.permission_name!=PermissionName:
				message = 'Cannot change the name of this permission'
			else:
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
			if message == '':
				message = "Permission Updated Successfully"
		elif Operation == 'Delete' and PermissionID != None:
			Permission = model.Permission.get(PermissionID)
			PermissionID=None
			if Permission.permission_name in mandatory_permissions:
				message = "ERROR: Cannot delete this permission, operation failed."
			else:
				# Remove groups
				for group in Permission.groups:
					Permission.removeGroup(group)
				# Delete the Permission
				Permission.destroySelf()
				message="Permission Deleted"
		else:
			message = "Operation Failed"
		return dict(message=message,PermissionID=PermissionID)