import logging
import sys
import simplejson
from datetime import datetime
import time
# import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears import exception_handler
import model
from model import DATE_FORMAT

log = logging.getLogger("turbocare.controllers")

class TusharAdministrativeError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Configuration(controllers.RootController):
	
	@expose(html='turbocare.templates.configuration_menu')
	def index(self, **kw):
		#raise TusharAdministrativeError('Did you run this on your laptop first?')
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
		
	@expose(html='turbocare.templates.config_AddressesEditor')
	@validate(validators={'AddressID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def AddressesEditor(self, AddressID=None, **kw):
		'''	Either load an address for editing, or bring up an empty form for adding a new address 
			Addresses are stored both in inventory and care2x, so I do some synchronization between
			the two tables automatically everytime an address is loaded.  Currently, inventory information
			overides the care2x info.
		'''
		if AddressID==None: # Create a blank form
			DisplayName = 'NEW ENTRY'
			Name = ''
			Block = ''
			ZipCode = ''
			District = ''
			State = 'Nagaland'
			IsoCountryId = 'IND'
			UneceModifier = ''
			UneceLocode = ''
			UneceLocodeType = ''
			UneceCoordinates = ''
			AddressID = ''
			IsDeleted = False
		else:
			try:
				InvAddress = model.InvAddressCitytown.get(AddressID)
			except SQLObjectNotFound:
				turbogears.flash('The item with id %d does not exist (perhaps it was deleted)' % AddressID)
				raise cherrypy.HTTPRedirect('AddressesEditor')
			try:
				CareAddress = model.AddressCityTown.get(AddressID)
			except SQLObjectNotFound:
				# The care2x table didn't have the entry, so add it in
				CareAddress = model.AddressCityTown(Name=InvAddress.Name, Block=InvAddress.Block, 
					ZipCode=InvAddress.ZipCode, District=InvAddress.District, State=InvAddress.State, 
					IsoCountryId=InvAddress.IsoCountryId, UneceModifier=InvAddress.UneceModifier,
					UneceLocode=InvAddress.UneceLocode, UneceLocodeType=InvAddress.UneceLocodeType, 
					UneceCoordinates=InvAddress.UneceCoordinates,id=InvAddress.id, Status=InvAddress.Status)
			DisplayName = "%s (%d)" % (InvAddress.Name, AddressID)
			Name = InvAddress.Name
			if InvAddress.Name != CareAddress.Name:
				CareAddress.Name = InvAddress.Name
			Block = InvAddress.Block
			if InvAddress.Block != CareAddress.Block:
				CareAddress.Block = InvAddress.Block
			ZipCode = InvAddress.ZipCode
			if InvAddress.ZipCode != CareAddress.ZipCode:
				CareAddress.ZipCode = InvAddress.ZipCode
			District = InvAddress.District
			if InvAddress.District != CareAddress.District:
				CareAddress.District = InvAddress.District
			State = InvAddress.State
			if InvAddress.State != CareAddress.State:
				CareAddress.State = InvAddress.State
			IsoCountryId = InvAddress.IsoCountryId
			if InvAddress.IsoCountryId != CareAddress.IsoCountryId:
				CareAddress.IsoCountryId = InvAddress.IsoCountryId
			UneceModifier = InvAddress.UneceModifier
			if InvAddress.UneceModifier != CareAddress.UneceModifier:
				CareAddress.UneceModifier = InvAddress.UneceModifier
			UneceLocode = InvAddress.UneceLocode
			if InvAddress.UneceLocode != CareAddress.UneceLocode:
				CareAddress.UneceLocode = InvAddress.UneceLocode
			UneceLocodeType = InvAddress.UneceLocodeType
			if InvAddress.UneceLocodeType != CareAddress.UneceLocodeType:
				CareAddress.UneceLocodeType = InvAddress.UneceLocodeType
			UneceCoordinates = InvAddress.UneceCoordinates
			if InvAddress.UneceCoordinates != CareAddress.UneceCoordinates:
				CareAddress.UneceCoordinates = InvAddress.UneceCoordinates
			IsDeleted = InvAddress.Status=='deleted'
		return dict(DisplayName=DisplayName, Name=Name, Block=Block, ZipCode=ZipCode, District=District,
		State=State, IsoCountryId=IsoCountryId, UneceModifier=UneceModifier, UneceLocode=UneceLocode,
		UneceLocodeType=UneceLocodeType, UneceCoordinates=UneceCoordinates, AddressID=AddressID,
		IsDeleted=IsDeleted)

	@expose()
	@validate(validators={'Name':validators.String(),'Block':validators.String(),'ZipCode':validators.String(),\
		'District':validators.String(),'State':validators.String(),'IsoCountryId':validators.String(),\
		'UneceModifier':validators.String(),'UneceLocode':validators.String(),'UneceLocodeType':validators.Int(),\
		'UneceCoordinates':validators.String(),'Operation':validators.String(),'AddressID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def AddressesEditorSave(self, Name='', Block='', ZipCode='', District='', State='', IsoCountryId='',
		UneceModifier='', UneceLocode='', UneceLocodeType=None, UneceCoordinates='', AddressID=None,
		Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		if Operation=='Save': # Either update or create a new entry
			if AddressID in ['',None]: # Create a new entry
				# It's tricky to add a new address for two tables which should always be synced but might not be
				# So, if we create a new address with an id conflict in the Care2x table, then we'll sync the Inv table
				# with the care2x table and try creating the address again.  We'll repeat until we don't have a id
				# conflict
				AddressAdded = False
				while not AddressAdded:
					InvAddress = model.InvAddressCitytown(Name=Name, Block=Block, ZipCode=ZipCode, 
						District=District, State=State, IsoCountryId=IsoCountryId, UneceModifier=UneceModifier,
						UneceLocode=UneceLocode, UneceLocodeType=UneceLocodeType, 
						UneceCoordinates=UneceCoordinates)
					# Search to see if the Care2x table has the id taken already
					try:
						CareAddress = model.AddressCityTown.get(InvAddress.id)
						# If we don't raise an exception, this means the address exists.  Sync the Inventory address
						# with this address and then try again
						InvAddress.Name = CareAddress.Name
						InvAddress.Block = CareAddress.Block
						InvAddress.ZipCode = CareAddress.ZipCode
						InvAddress.District = CareAddress.District
						InvAddress.State = CareAddress.State
						InvAddress.IsoCountryId = CareAddress.IsoCountryId
						InvAddress.UneceModifier = CareAddress.UneceModifier
						InvAddress.UneceLocode = CareAddress.UneceLocode
						InvAddress.UneceLocodeType = CareAddress.UneceLocodeType
						InvAddress.UneceCoordinates = CareAddress.UneceCoordinates					
					except SQLObjectNotFound:
						# This is what we're hoping for, now we can add the address safely
						CareAddress = model.AddressCityTown(Name=Name, Block=Block, ZipCode=ZipCode, 
							District=District, State=State, IsoCountryId=IsoCountryId, UneceModifier=UneceModifier,
							UneceLocode=UneceLocode, UneceLocodeType=UneceLocodeType, 
							UneceCoordinates=UneceCoordinates,id=InvAddress.id)
						AddressAdded = True
						turbogears.flash('New Record Added')
				AddressID = InvAddress.id
			else: # Update an entry
				InvAddress = model.InvAddressCitytown.get(AddressID)
				InvAddress.Name = Name
				InvAddress.Block = Block
				InvAddress.ZipCode = ZipCode
				InvAddress.District = District
				InvAddress.State = State
				InvAddress.IsoCountryId = IsoCountryId
				InvAddress.UneceModifier = UneceModifier
				InvAddress.UneceLocode = UneceLocode
				InvAddress.UneceLocodeType = UneceLocodeType
				InvAddress.UneceCoordinates = UneceCoordinates					
				try:
					CareAddress = model.AddressCityTown.get(AddressID)
					CareAddress.Name = Name
					CareAddress.Block = Block
					CareAddress.ZipCode = ZipCode
					CareAddress.District = District
					CareAddress.State = State
					CareAddress.IsoCountryId = IsoCountryId
					CareAddress.UneceModifier = UneceModifier
					CareAddress.UneceLocode = UneceLocode
					CareAddress.UneceLocodeType = UneceLocodeType
					CareAddress.UneceCoordinates = UneceCoordinates					
				except SQLObjectNotFound:
					# The care2x table didn't have the entry, so add it in
					CareAddress = model.AddressCityTown(Name=InvAddress.Name, Block=InvAddress.Block, 
						ZipCode=InvAddress.ZipCode, District=InvAddress.District, State=InvAddress.State, 
						IsoCountryId=InvAddress.IsoCountryId, UneceModifier=InvAddress.UneceModifier,
						UneceLocode=InvAddress.UneceLocode, UneceLocodeType=InvAddress.UneceLocodeType, 
						UneceCoordinates=InvAddress.UneceCoordinates,id=InvAddress.id)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and AddressID!=None:
			# We need to check if any of the id's are in use before attempting to delete an address from the system
			InvAddress = model.InvAddressCitytown.get(AddressID)
			try:
				CareAddress = model.AddressCityTown.get(AddressID)
				if len(CareAddress.Persons)>0 or len(InvAddress.Vendors)>0 or len(InvAddress.Customers)>0:
					# Mark the entry as deleted
					CareAddress.Status = 'deleted'
					InvAddress.Status = 'deleted'
					turbogears.flash('Record Marked Deleted')
				else:
					CareAddress.destroySelf()
					InvAddress.destroySelf()
					turbogears.flash('Record Deleted')
			except SQLObjectNotFound: # we only need to check the Inventory table for the address
				if len(InvAddress.Vendors)>0 or len(InvAddress.Customers)>0:
					# Mark the entry as deleted
					InvAddress.Status = 'deleted'
					# CREATE the care2x entry... and mark it deleted
					CareAddress = model.AddressCityTown(Name=InvAddress.Name, Block=InvAddress.Block, 
						ZipCode=InvAddress.ZipCode, District=InvAddress.District, State=InvAddress.State, 
						IsoCountryId=InvAddress.IsoCountryId, UneceModifier=InvAddress.UneceModifier,
						UneceLocode=InvAddress.UneceLocode, UneceLocodeType=InvAddress.UneceLocodeType, 
						UneceCoordinates=InvAddress.UneceCoordinates,id=InvAddress.id,Status=InvAddress.Status)
					turbogears.flash('Record Marked Deleted')
				else:
					InvAddress.destroySelf()
					turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and AddressID!=None:
			InvAddress = model.InvAddressCitytown.get(AddressID)
			try:
				CareAddress = model.AddressCityTown.get(AddressID)
				# Mark the entry as ok
				CareAddress.Status = ''
				InvAddress.Status = ''
				turbogears.flash('Record Un-Deleted')
			except SQLObjectNotFound: # we only need to check the Inventory table for the address
				InvAddress.Status = ''
				# CREATE the care2x entry
				CareAddress = model.AddressCityTown(Name=InvAddress.Name, Block=InvAddress.Block, 
					ZipCode=InvAddress.ZipCode, District=InvAddress.District, State=InvAddress.State, 
					IsoCountryId=InvAddress.IsoCountryId, UneceModifier=InvAddress.UneceModifier,
					UneceLocode=InvAddress.UneceLocode, UneceLocodeType=InvAddress.UneceLocodeType, 
					UneceCoordinates=InvAddress.UneceCoordinates,id=InvAddress.id,Status=InvAddress.Status)
				turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			pass
		elif Operation=='New':
			AddressID=''
		else:
			turbogears.flash('Error in processing request')
		if AddressID in ['', None]:
			raise cherrypy.HTTPRedirect('AddressesEditor')
		else:
			raise cherrypy.HTTPRedirect('AddressesEditor?AddressID=%d' % AddressID)
		
		
	@expose(format='json')
	def AddressesEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing address entry '''
		if QuickSearchText=='*':
			addresses = model.InvAddressCitytown.select(orderBy=[model.InvAddressCitytown.q.Name])
		else:
			addresses = model.InvAddressCitytown.select(OR (model.InvAddressCitytown.q.Name.contains(str(QuickSearchText)),
				model.InvAddressCitytown.q.Block.contains(str(QuickSearchText)),
				model.InvAddressCitytown.q.District.contains(str(QuickSearchText)),
				model.InvAddressCitytown.q.State.contains(str(QuickSearchText))),
				orderBy=[model.InvAddressCitytown.q.Name])
		results = []
		for item in addresses:
			results.append(dict(id=item.id, text=item.DisplayNameAlt()))
		return dict(results=results)
		
	@expose(html='turbocare.templates.config_EthnicOriginsEditor')
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def EthnicOriginsEditor(self, **kw):
		'''	Load the Ethnic Origins editing screen
			Ethnic origins includes the Tribes options
		items= model.TypeEthnicOrig.select(AND (model.TypeEthnicOrig.q.ClassNrID==model.ClassEthnicOrig.q.id,
		model.ClassEthnicOrig.q.Name == 'Tribe'),orderBy=[model.TypeEthnicOrig.q.Name])
		'''
		# Load the classifications
		classifications = [dict(id=x.id, name=(x.Name+' '+x.Status).strip(), selected=None) for x in model.ClassEthnicOrig.select(orderBy=[model.ClassEthnicOrig.q.Name])]
		if len(classifications)==0:
			model.ClassEthnicOrig(Name='tribe',LdVar='')
			classifications = [dict(id=x.id, name=(x.Name+' '+x.Status).strip(), selected=None) for x in model.ClassEthnicOrig.select(orderBy=[model.ClassEthnicOrig.q.Name])]
		EditClassName = classifications[0]['name']
		EditClassID = classifications[0]['id']
		classifications[0]['selected'] = 'selected'
		ClassDeleted = model.ClassEthnicOrig.get(EditClassID).Status == 'deleted'
		# Load the types
		ethnicorigtypes = [dict(id=x.id, name=(x.Name+' '+x.Status).strip(), selected=None) for x in model.TypeEthnicOrig.select(AND (
			model.TypeEthnicOrig.q.ClassNrID==model.ClassEthnicOrig.q.id,model.ClassEthnicOrig.q.id==EditClassID),
			orderBy=[model.ClassEthnicOrig.q.Name])]
		if len(ethnicorigtypes) == 0:
			EditTypeName = ''
			EditTypeID = ''
			TypeDeleted = False
		else:
			EditTypeName = ethnicorigtypes[0]['name']
			EditTypeID = ethnicorigtypes[0]['id']
			ethnicorigtypes[0]['selected'] = 'selected'
			TypeDeleted = model.TypeEthnicOrig.get(EditTypeID).Status == 'deleted'
		return dict(classifications=classifications, EditClassName=EditClassName, EditClassID=EditClassID,
		ClassDeleted=ClassDeleted, ethnicorigtypes=ethnicorigtypes, EditTypeName=EditTypeName, 
		EditTypeID=EditTypeID, TypeDeleted=TypeDeleted)
	
	@expose(format='json')
	@validate(validators={'ClassID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def EthnicOriginsEditorSelectClass(self, ClassID=None, **kw):
		'''	Select a classification, return a list of types for editing'''
		# Load the classifications
		if ClassID==None:
			return dict(message = "No classification selected, Error")
		else:
			Classif = model.ClassEthnicOrig.get(ClassID)
			EditClassName = Classif.Name
			EditClassID = ClassID
			ClassDeleted =  Classif.Status == 'deleted'
			# Load the types
			ethnicorigtypes = [dict(id=x.id, name=(x.Name+' '+x.Status).strip(), selected=None) for x in model.TypeEthnicOrig.select(AND (
				model.TypeEthnicOrig.q.ClassNrID==model.ClassEthnicOrig.q.id,model.ClassEthnicOrig.q.id==EditClassID),
				orderBy=[model.ClassEthnicOrig.q.Name])]
			if len(ethnicorigtypes) == 0:
				message = '0 linked records'
				EditTypeName = ''
				EditTypeID = ''
				TypeDeleted = False
			else:
				EditTypeName = ethnicorigtypes[0]['name']
				EditTypeID = ethnicorigtypes[0]['id']
				ethnicorigtypes[0]['selected'] = 'selected'
				TypeDeleted = model.TypeEthnicOrig.get(EditTypeID).Status == 'deleted'
				message = ''
			return dict(EditClassName=EditClassName, EditClassID=EditClassID, message=message,
			ClassDeleted=ClassDeleted, ethnicorigtypes=ethnicorigtypes, EditTypeName=EditTypeName, 
			EditTypeID=EditTypeID, TypeDeleted=TypeDeleted)
	
	@expose(format='json')
	@validate(validators={'ClassID':validators.Int(),'ClassName':validators.String(),'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def EthnicOriginsEditorSaveClass(self, ClassID=None, ClassName='', Operation='', **kw):
		'''	Save a Ethnic Origin classification.  Either Update/Create New/Delete or Un-delete an entry '''
		Classif = None
		if Operation=='Save':
			if ClassID==None: # create a new entry
				if ClassName != '':
					Classif = model.ClassEthnicOrig(Name=ClassName)
					message = "New Classification Record Added"
				else:
					message = "ERROR: Cannot save without a name"
			elif ClassName!='': # Update a record
				try:
					Classif = model.ClassEthnicOrig.get(ClassID)
					Classif.Name = ClassName
					message = "Record updated"
				except SQLObjectNotFound:
					message = "ERROR: Failed to locate the record to update (deleted while you were sleeping perhaps)"
			else:
				message = "ERROR: Cannot save without a name"
		elif Operation=='Cancel' and ClassID!=None:
			Classif = model.ClassEthnicOrig.get(ClassID)
		elif Operation=='Delete' and ClassID!=None:
			try:
				Classif = model.ClassEthnicOrig.get(ClassID)
				if len(Classif.Types) > 0:
					Classif.Status = 'deleted'
					message = "Record Marked Deleted"
				else:
					Classif.destroySelf()
					Classif = None
					message = "Record Deleted!"
			except SQLObjectNotFound:
				message = "ERROR: Failed to locate the record to delete (perhaps someone deleted it before you)"
		elif Operation=='Un-Delete' and ClassID!=None:
			try:
				Classif = model.ClassEthnicOrig.get(ClassID)
				Classif.Status = ''
				message = "Record Un-Deleted"
			except SQLObjectNotFound:
				message = "ERROR: Failed to locate the record to un-delete (perhaps someone excamunicated the record)"
		# Load the data for the Forms
		# Load the classifications
		classifications = [dict(id=x.id, name=(x.Name+' '+x.Status).strip(), selected=None) for x in model.ClassEthnicOrig.select(orderBy=[model.ClassEthnicOrig.q.Name])]
		if Classif==None:
			EditClassName = classifications[0]['name']
			EditClassID = classifications[0]['id']
			ClassDeleted = False
			classifications[0]['selected'] = 'selected'
		else:
			EditClassName = Classif.Name
			EditClassID = Classif.id
			ClassDeleted = Classif.Status == 'deleted'
			for classif in classifications:
				if classif['id'] == Classif.id:
					classif['selected'] = True
					break
		# Load the types
		ethnicorigtypes = [dict(id=x.id, name=(x.Name+' '+x.Status).strip(), selected=None) for x in model.TypeEthnicOrig.select(AND (
			model.TypeEthnicOrig.q.ClassNrID==model.ClassEthnicOrig.q.id,model.ClassEthnicOrig.q.id==EditClassID),
			orderBy=[model.ClassEthnicOrig.q.Name])]
		if len(ethnicorigtypes) == 0:
			EditTypeName = ''
			EditTypeID = ''
			TypeDeleted = False
		else:
			EditTypeName = ethnicorigtypes[0]['name']
			EditTypeID = ethnicorigtypes[0]['id']
			ethnicorigtypes[0]['selected'] = 'selected'
			TypeDeleted = model.TypeEthnicOrig.get(EditTypeID).Status == 'deleted'
		return dict(classifications=classifications, EditClassName=EditClassName, EditClassID=EditClassID,
		ClassDeleted=ClassDeleted, ethnicorigtypes=ethnicorigtypes, EditTypeName=EditTypeName, 
		EditTypeID=EditTypeID, TypeDeleted=TypeDeleted, message=message)

	@expose(format='json')
	@validate(validators={'ClassID':validators.Int(),'TypeID':validators.Int(),'TypeName':validators.String(),'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def EthnicOriginsEditorSaveType(self, ClassID=None, TypeID=None, TypeName='', Operation='', **kw):
		'''	Save a Ethnic Origin classification.  Either Update/Create New/Delete or Un-delete an entry '''
		Type = None
		if Operation=='Save':
			if TypeID==None and ClassID!=None: # create a new entry
				if TypeName != '':
					Type = model.TypeEthnicOrig(Name=TypeName,ClassNrID=ClassID)
					message = "New Type Record Added"
				else:
					message = "ERROR: Cannot save without a name"
			elif TypeName!='': # Update a record
				try:
					Type = model.TypeEthnicOrig.get(TypeID)
					Type.Name = TypeName
					message = "Record updated"
				except SQLObjectNotFound:
					message = "ERROR: Failed to locate the record to update (deleted while you were sleeping perhaps)"
			else:
				message = "ERROR: Cannot save without a name or classification"
		elif Operation=='Cancel' and TypeID!=None:
			Type = model.TypeEthnicOrig.get(TypeID)
		elif Operation=='Delete' and TypeID!=None:
			try:
				Type = model.TypeEthnicOrig.get(TypeID)
				if len(Type.Persons) > 0:
					Type.Status = 'deleted'
					message = "Record Marked Deleted"
				else:
					Type.destroySelf()
					Type = None
					message = "Record Deleted!"
			except SQLObjectNotFound:
				message = "ERROR: Failed to locate the record to delete (perhaps someone deleted it before you)"
		elif Operation=='Un-Delete' and TypeID!=None:
			try:
				Type = model.TypeEthnicOrig.get(TypeID)
				Type.Status = ''
				message = "Record Un-Deleted"
			except SQLObjectNotFound:
				message = "ERROR: Failed to locate the record to un-delete (perhaps someone excamunicated the record)"
		# Load the data for the Form
		# Load the ethnic origin types
		if Type==None and ClassID!=None:
			ethnicorigtypes = [dict(id=x.id, name=(x.Name+' '+x.Status).strip(), selected=None) for x in model.TypeEthnicOrig.select(AND (
				model.TypeEthnicOrig.q.ClassNrID==model.ClassEthnicOrig.q.id,model.ClassEthnicOrig.q.id==ClassID),
				orderBy=[model.ClassEthnicOrig.q.Name])]
		elif Type==None and ClassID==None:
			ethnicorigtypes = []
		else:
			ClassID = Type.ClassNrID
			ethnicorigtypes = [dict(id=x.id, name=(x.Name+' '+x.Status).strip(), selected=None) for x in model.TypeEthnicOrig.select(AND (
				model.TypeEthnicOrig.q.ClassNrID==model.ClassEthnicOrig.q.id,model.ClassEthnicOrig.q.id==ClassID),
				orderBy=[model.ClassEthnicOrig.q.Name])]
		# Load the types
		if len(ethnicorigtypes) == 0:
			EditTypeName = ''
			EditTypeID = ''
			TypeDeleted = False
		elif Type!=None:
			EditTypeName = Type.Name
			EditTypeID = Type.id
			for type in ethnicorigtypes:
				if type['id'] == Type.id:
					type['selected'] = 'selected'
					break
			TypeDeleted = Type.Status == 'deleted'
		else:
			EditTypeName = ethnicorigtypes[0]['name']
			EditTypeID = ethnicorigtypes[0]['id']
			ethnicorigtypes[0]['selected'] = 'selected'
			TypeDeleted = model.TypeEthnicOrig.get(EditTypeID).Status == 'deleted'			
		return dict(ethnicorigtypes=ethnicorigtypes, EditTypeName=EditTypeName, 
		EditTypeID=EditTypeID, TypeDeleted=TypeDeleted, message=message)
		
	@expose(html='turbocare.templates.config_LocationsEditor')
	@validate(validators={'LocationID':validators.Int(),'DepartmentID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def LocationsEditor(self, LocationID=None, DepartmentID=None, **kw):
		'''	Either load an address for editing, or bring up an empty form for adding a new location/department 
			Locations are stored both in inventory and care2x (as departments).
			LocationID is used when available.
		'''
		def Checked(value):
			if value:
				return "checked"
			else:
				return None
				
		def AddDepartment(Loc):
			'''	Add a department entry for the location 
				Return the new department
			'''
			# First, search for a matching department
			departments = model.Department.select(model.Department.q.NameFormal==Loc.Name)
			if departments.count() == 0: # Create a new department
				Dept = model.Department(NameFormal=Loc.Name, Id=Loc.Name.replace(' ','_').lower(), 
					NameShort=Loc.Name, NameAlternate=Loc.Name, Description=Loc.Description)
				Loc.DepartmentID = Dept.id
			else: # Join the first entry (Normally, the formal name should be unique)
				Loc.DepartmentID = Dept.id
			return Dept
			
		def AddLocation(Dept):
			'''	Find or create a Location for the selected department '''
			# First search for a matching location
			locations = model.InvLocation.select(AND (model.InvLocation.q.Name==Dept.NameFormal,
				model.InvLocation.q.DepartmentID==None))
			if locations.count()==0: # Create a location
				Loc = model.InvLocation(Name=Dept.NameFormal, Description=Dept.Description,
					DepartmentID=Dept.id)
			else: # join the first matching
				Loc = locations[0]
				Loc.DepartmentID = Dept.id
			return Loc
			
		# Attempt to load our Location and Department objects
		# During this step, we'll attempt to synchronize the entries if possible
		if LocationID!=None: # attempt to load a location id
			try:
				Location = model.InvLocation.get(LocationID)
				if Location.DepartmentID!=None: # attempt to find the related department
					DepartmentID=Location.DepartmentID
					try:
						Department = model.Department.get(DepartmentID)
					except SQLObjectNotFound: # The department that was linked was deleted
						Department = AddDepartment(Location)
						DepartmentID = Department.id
				else:
					Department = AddDepartment(Location)
					DepartmentID = Department.id
			except SQLObjectNotFound:
				turbogears.flash("The LocationID %d could not be found (deleted?)" % LocationID)
				Location=None
				LocationID=None
		else:
			Location=None
		if Location==None and DepartmentID!=None: # Attempt to load a Department id
			try:
				Department = model.Department.get(DepartmentID)
				if len(Department.Locations) > 0: # Just pick the first one, this is how it should be.
					Location = Department.Locations[0]
				else:
					Location = AddLocation(Department)
				LocationID = Location.id
			except SQLObjectNotFound:
				turbogears.flash("The DepartmentID %d could not be found (deleted?)" % DepartmentID)
				Department=None
				DepartmentID=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if LocationID==None: # Create a blank form
			result['PermDisp'] = None
			result['PermStore'] = None
			result['DispPermissionExists'] = True
			result['StorePermissionExists'] = True
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['Description'] = ''
			result['IsStore'] = None
			result['CanReceive'] = None
			result['CanSell'] = None
			result['IsConsumed'] = None
			result['AdmitInpatient'] = None
			result['AdmitOutpatient'] = None
			result['HasOncallDoc'] = None
			result['HasOncallNurse'] = None
			result['DoesSurgery'] = None
			result['ThisInstitution'] = None
			result['IsSubDept'] = None
			result['IsInactive'] = None
			result['WorkHours'] = ''
			result['ConsultHours'] = ''
			result['Address'] = ''
			result['ParentDeptNrID'] = ''
			result['ParentDeptNrName'] = ''
			result['types'] = [] # Type field: id, name
			DepartmentTypes = model.TypeDepartment.select(orderBy=[model.TypeDepartment.q.Name])
			for depTyp in DepartmentTypes:
				result['types'].append(dict(id=depTyp.id, name=depTyp.Name, selected=None))
			result['locationgroups'] = [] # Groups field: id, name
			result['LocationID'] = ''
			result['DepartmentID'] = ''
			result['IsDeleted'] = False
		else:
			PermDisp = Location.Name.lower().replace(' ','_') + '_disp_view'
			PermStore = Location.Name.lower().replace(' ','_') + '_store_view'
			result['PermDisp'] = PermDisp
			result['PermStore'] = PermStore
			result['DispPermissionExists'] = model.Permission.select(model.Permission.q.permission_name==PermDisp).count()>0
			result['StorePermissionExists'] = model.Permission.select(model.Permission.q.permission_name==PermStore).count()>0
			result['DisplayName'] = "%s (%d/%d)" % (Location.Name, LocationID, DepartmentID)
			result['Name'] = Location.Name
			result['Description'] = Location.Description
			result['IsStore'] = Checked(Location.IsStore)
			result['CanReceive'] = Checked(Location.CanReceive)
			result['CanSell'] = Checked(Location.CanSell)
			result['IsConsumed'] = Checked(Location.IsConsumed)
			result['AdmitInpatient'] = Checked(Department.AdmitInpatient)
			result['AdmitOutpatient'] = Checked(Department.AdmitOutpatient)
			result['HasOncallDoc'] = Checked(Department.HasOncallDoc)
			result['HasOncallNurse'] = Checked(Department.HasOncallNurse)
			result['DoesSurgery'] = Checked(Department.DoesSurgery)
			result['ThisInstitution'] = Checked(Department.ThisInstitution)
			result['IsSubDept'] = Checked(Department.IsSubDept)
			result['IsInactive'] = Checked(Department.IsInactive)
			result['WorkHours'] = Department.WorkHours
			result['ConsultHours'] = Department.ConsultHours
			result['Address'] = Department.Address
			result['ParentDeptNrID'] = Department.ParentDeptNrID
			if Department.ParentDeptNrID == 0:
				Department.ParentDeptNrID = None
				result['ParentDeptNrID'] = Department.ParentDeptNrID
				result['ParentDeptNrName'] = ''
			if Department.ParentDeptNrID != None:
				result['ParentDeptNrName'] = Department.ParentDeptNr.NameFormal
			else:
				result['ParentDeptNrName'] = ''
			result['types'] = [] # Type field: id, name
			DepartmentTypes = model.TypeDepartment.select(orderBy=[model.TypeDepartment.q.Name])
			for depTyp in DepartmentTypes:
				if depTyp.id == Department.TypeID:
					result['types'].append(dict(id=depTyp.id, name=depTyp.Name, selected="selected"))
				else:
					result['types'].append(dict(id=depTyp.id, name=depTyp.Name, selected=None))
			result['locationgroups'] = [] # Groups field: id, name
			for group in Location.Groups:
				result['locationgroups'].append(dict(id=group.id, name=group.Name))
			result['LocationID'] = LocationID
			result['DepartmentID'] = DepartmentID
			result['IsDeleted'] = False
		return result

	@expose(format='json')
	@validate(validators={'LocationID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def LocationsEditorGroupSelect(self, LocationID=None, **kw):
		'''	Load the Location Group Options
			Mark items which are already selected as selected
		'''
		cur_groups = []
		if LocationID!=None:
			Location = model.InvLocation.get(LocationID)
			for group in Location.Groups:
				cur_groups.append(group.id)
		groups = model.InvGrpLocation.select(orderBy=[model.InvGrpLocation.q.Name])
		results = []
		for group in groups:
			results.append(dict(id=group.id, text=group.Name, selected=(group.id in cur_groups)))
		return dict(results=results)
	
	@expose(format='json')
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def LocationEditorParentDepartmentSelect(self, SearchText='', **kw):
		'''	Load the Parent item options
		'''
		SearchText = str(SearchText)
		items = model.Department.select(model.Department.q.NameFormal.contains(SearchText),
			orderBy=[model.Department.q.NameFormal])
		results = []
		for item in items:
			results.append(dict(id=item.id, text='%s (%d)' % (item.NameFormal,item.id)))
		return dict(results=results, function_name='LocationEditorParentDepartmentSelect')
	
	@expose()
	@validate(validators={'Name':validators.String(),'Description':validators.String(),'IsStore':validators.Bool(),\
		'CanReceive':validators.Bool(),'CanSell':validators.Bool(),'IsConsumed':validators.Bool(),\
		'AdmitInpatient':validators.Bool(),'AdmitOutpatient':validators.Bool(),'HasOncallDoc':validators.Bool(),\
		'HasOncallNurse':validators.Bool(),'DoesSurgery':validators.Bool(),'ThisInstitution':validators.Bool(),
		'IsSubDept':validators.Bool(),'IsInactive':validators.Bool(),'WorkHours':validators.String(),\
		'ConsultHours':validators.String(),'Address':validators.String(),'ParentDeptNrID':validators.Int(),\
		'Type':validators.Int(),'LocationID':validators.Int(),'DepartmentID':validators.Int(),'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def LocationsEditorSave(self, Name='', Description='', IsStore=None, CanReceive=None, CanSell=None, IsConsumed=None,
		AdmitInpatient=None, AdmitOutpatient=None, HasOncallDoc=None, HasOncallNurse=None, DoesSurgery=None,
		ThisInstitution=None, IsSubDept=None, IsInactive=None, WorkHours='', ConsultHours='', Address='', 
		ParentDeptNrID=None, Type=None, LocationGroups=[], LocationID=None, DepartmentID=None, Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		# If we're given a LocationID or DepartmentID, then we'll try to load both items.  If we get a problem, then we'll
		# skip the operation and attempt to reload the screen in edit mode (because I'm too lazy to fix it here).  NOTE:
		# If we have one ID we should have the other.  Both should be created when the item is initially loaded
		log.debug('LocationsEditorSave')
		if LocationID!=None or DepartmentID!=None:
			try:
				Location = model.InvLocation.get(LocationID)
				if Location.DepartmentID != DepartmentID:
					turbogears.flash("It seems that the data has been hacked in a way I don't want to handle.  Changes are lost and we're going to start over")
					raise cherrypy.HTTPRedirect('LocationsEditor?LocationID=%d' % LocationID)
				Department = model.Department.get(DepartmentID)
			except SQLObjectNotFound, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				errorArr = errorstr[0].split(' ')
				table = errorArr[2]
				id = errorArr[6]
				if table == 'Department':
					Location.DepartmentID = None
					raise cherrypy.HTTPRedirect('LocationsEditor?LocationID=%d' % LocationID)
				else:
					raise cherrypy.HTTPRedirect('LocationsEditor?DepartmentID=%d' % DepartmentID)
		if Operation=='Save': # Either update or create a new entry
			log.debug('...Save')
			Name = str(Name)
			Description = str(Description)
			WorkHours = str(WorkHours)
			ConsultHours = str(ConsultHours)
			Address = str(Address)
			if LocationID==None: # Create a new entry
				log.debug('...New Entry')
				Department = model.Department(NameFormal=Name, Id=Name.replace(' ','_').lower(), Type=Type,
					NameShort=Name, NameAlternate=Name, Description=Description,AdmitInpatient=AdmitInpatient,
					AdmitOutpatient=AdmitOutpatient,HasOncallDoc=HasOncallDoc,HasOncallNurse=HasOncallNurse,
					DoesSurgery=DoesSurgery,ThisInstitution=ThisInstitution,IsSubDept=IsSubDept,IsInactive=IsInactive,
					WorkHours=WorkHours,ConsultHours=ConsultHours,Address=Address,ParentDeptNrID=ParentDeptNrID)
				Location = model.InvLocation(Name=Name, Description=Description,DepartmentID=Department.id,
					IsStore=IsStore,CanReceive=CanReceive,CanSell=CanSell,IsConsumed=IsConsumed)
				DepartmentID = Department.id
				LocationID = Location.id
				turbogears.flash('New Entry Created (id: %d/%d)' % (LocationID,DepartmentID))
			else: # Update an entry
				# Update the InvLocation entry
				Location.Name = Name
				Location.Description = Description
				Location.IsStore = IsStore
				Location.CanReceive = CanReceive
				Location.CanSell = CanSell
				Location.IsConsumed = IsConsumed
				#Location Groups
				if isinstance(LocationGroups, basestring): # only one entry
					LocationGroups = [int(LocationGroups)]
				else:
					LocationGroups = [int(x) for x in LocationGroups]
				# Make a current listing of group ids
				CurrGroups = [x.id for x in Location.Groups]
				# Add new groups
				for groupid in LocationGroups:
					if not groupid in CurrGroups:
						Location.addInvGrpLocation(groupid)
				# Remove groups
				for groupid in CurrGroups:
					if not groupid in LocationGroups:
						Location.removeInvGrpLocation(groupid)
				# Update the department entry
				Department.NameFormal = Name
				Department.Id = Name.replace(' ','_').lower()
				Department.Type = Type
				Department.NameShort = Name
				Department.NameAlternate = Name
				Department.Description = Description
				Department.AdmitInpatient = AdmitInpatient
				Department.AdmitOutpatient = AdmitOutpatient
				Department.HasOncallDoc = HasOncallDoc
				Department.HasOncallNurse = HasOncallNurse
				Department.DoesSurgery = DoesSurgery
				Department.ThisInstitution = ThisInstitution
				Department.IsSubDept = IsSubDept
				Department.IsInactive = IsInactive
				Department.WorkHours = WorkHours
				Department.ConsultHours = ConsultHours
				Department.Address = Address
				Department.ParentDeptNrID = ParentDeptNrID
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and LocationID!=None:
			# We need to check if any of the id's are in use before attempting to delete an address from the system
			if len(Location.StockItems)>0 or len(Department.DutyPlans)>0 or len(Department.DrgQuicklists)>0 \
				or len(Department.TechRepairs)>0 or len(Department.OpMedDocs)>0 or \
				len(Department.Appointments)>0 or len(Department.BloodTestRequests)>0 or len(Department.Wards)>0\
				or len(Department.MedOrdercatalogs)>0 or len(Department.MedOrderlists)>0 or len(Department.MedReports)>0\
				or len(Department.EncounterOps)>0 or len(Department.PersonellAssignments)>0 or len(Department.Phones)>0\
				or len(Department.PharmaOrderlists)>0 or len(Department.RadioTestFindings)>0 or len(Department.RadioTestRequests)>0\
				or len(Department.Encounters)>0 or len(Department.EncounterDiagnosticsReports)>0 or len(Department.BaclaborTestFindings)>0:
				# Marke the items deleted
				Location.Status = 'deleted'
				Department.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				for group in Location.Groups:
					Location.removeInvGrpLocation(group)
				Location.destroySelf()
				Department.destroySelf()
				LocationID = None
				DepartmentID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and LocationID!=None:
			Location.Status = ''
			Department.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			LocationID=''
			DepartmentID=''
		else:
			turbogears.flash('Error in processing request')
		if LocationID in ['',None]:
			raise cherrypy.HTTPRedirect('LocationsEditor')
		else:
			raise cherrypy.HTTPRedirect('LocationsEditor?LocationID=%d' % LocationID)
		
	@expose(format='json')
	def LocationsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing location entry '''
		if QuickSearchText=='*':
			locations = model.InvLocation.select(model.InvLocation.q.DepartmentID==None,orderBy=[model.InvLocation.q.Name])
			departments = model.Department.select(orderBy=[model.Department.q.NameFormal])
		else:
			locations = model.InvLocation.select(AND (model.InvLocation.q.Name.contains(str(QuickSearchText)), 
				model.InvLocation.q.DepartmentID==None),	orderBy=[model.InvLocation.q.Name])
			departments = model.Department.select(model.Department.q.NameFormal.contains(str(QuickSearchText)),
				orderBy=[model.Department.q.NameFormal])
		results = []
		for item in locations:
			results.append(dict(id=item.id, text=item.Name, type='location'))
		for item in departments:
			results.append(dict(id=item.id, text=item.NameFormal, type='department'))
		return dict(results=results)
		
	@expose(format='json')
	@validate(validators={'TypeID':validators.Int(),'TypeName':validators.String(),'Operation':validators.String()})
	def LocationsEditorDepartmentTypeSave(self, TypeID=None, TypeName='', Operation='', **kw):
		'''	edit a department type entry
			returns an updated list of department types, including the currently selected entry
		'''
		message = ''
		if Operation == 'Save':
			if TypeID == None: # create a new entry
				Type = model.TypeDepartment(Type=TypeName.lower().replace(' ','_'), Name=TypeName,
					Description=TypeName)
				message = 'New Department Type Created'
			else: # Update the entry
				try:
					Type = model.TypeDepartment.get(TypeID)
					Type.Type = TypeName.lower().replace(' ','_')
					Type.Name = TypeName
					Type.Description = TypeName
					message = 'Department Type Updated'
				except SQLObjectNotFound:
					message = 'The Department Type you wanted to edit could not be found, possibly deleted by someone else'
					TypeID = None
		elif Operation == 'Cancel':
			message = 'Changes cancelled'
		elif Operation == 'Delete' and TypeID!=None:
			try:
				Type = model.TypeDepartment.get(TypeID)
				if len(Type.Departments) > 0:
					Type.Status = 'deleted'
					Type.Name += ' **DELETED**'
					message = 'Department Type Marked Deleted'
				else:
					Type.destroySelf()
					TypeID = None
					message = 'Department Type Deleted'					
			except SQLObjectNotFound:
				message = 'The Department Type you wanted to delete could not be found (looks like someone else did the work faster)'
				TypeID = None
		elif Operation == 'Un-Delete' and TypeID!=None:
			try:
				Type = model.TypeDepartment.get(TypeID)
				Type.Status = ''
				Type.Name = Type.Name.replace('**DELETED**','').strip()
				message = 'Department Type Updated'
			except SQLObjectNotFound:
				message = 'The Department Type you wanted to Un-Delete could not be found, possibly deleted by someone else'
				TypeID = None
		else:
			TypeID = None
			message = 'The Operation you tried to perform could not be executed properly'
		# Produce an updated list of department types
		types = model.TypeDepartment.select(orderBy=[model.TypeDepartment.q.Name])
		if TypeID == None and types.count()>0:
			TypeID = types[0].id
		results = []
		for type in types:
			results.append(dict(id=type.id, name=type.Name, selected=type.id==TypeID))
		return dict(results=results, message=message)
		
	@expose(html='turbocare.templates.config_WardsEditor')
	@validate(validators={'WardID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def WardsEditor(self, WardID=None, **kw):
		'''	Either load a ward for editing, or bring up an empty form for adding a new ward 
		'''
		def Checked(value):
			if value:
				return "checked"
			else:
				return None
		# Attempt to load our Ward
		if WardID!=None: # attempt to load a location id
			try:
				Ward = model.Ward.get(WardID)
			except SQLObjectNotFound:
				turbogears.flash("The WardID %d could not be found (deleted?)" % WardID)
				Ward=None
				WardID=None
		else:
			Ward=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if WardID==None: # Create a blank form
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['DateCreate'] = datetime.now().strftime(DATE_FORMAT)
			result['DateClose'] = ''
			result['IsTempClosed'] = None
			result['Description'] = ''
			result['Info'] = ''
			result['RoomNrStart'] = 1
			result['RoomNrEnd'] = 1
			result['Roomprefix'] = ''
			result['DeptNrID'] = ''
			result['DeptNrName'] = ''
			result['WardID'] = None
			result['IsDeleted'] = False
		else:
			result['DisplayName'] = "%s (%d)" % (Ward.Name, WardID)
			result['Name'] = Ward.Name
			result['DateCreate'] = Ward.DateCreate
			result['DateClose'] = Ward.DateClose
			result['IsTempClosed'] = Checked(Ward.IsTempClosed)
			result['Description'] = Ward.Description
			result['Info'] = Ward.Info
			result['RoomNrStart'] = Ward.RoomNrStart
			result['RoomNrEnd'] = Ward.RoomNrEnd
			result['Roomprefix'] = Ward.Roomprefix
			if Ward.DeptNrID in [0, None]:
				if Ward.DeptNrID==0:
					Ward.DeptNrID=None
				result['DeptNrID'] = None
				result['DeptNrName'] = ''
			else:
				result['DeptNrID'] = Ward.DeptNrID
				result['DeptNrName'] = Ward.DeptNr.NameFormal
			result['WardID'] = WardID
			result['IsDeleted'] = Ward.Status=='deleted'
			# Load the rooms linked to the ward as a list
			rooms = []
			for room in Ward.Rooms:
				rooms.append(dict(RoomID=room.id, RoomNr=room.RoomNr, NrOfBeds=room.NrOfBeds, Status=room.Description()))
			result['rooms'] = rooms
		return result
	
	@expose()
	@validate(validators={'Name':validators.String(),'Description':validators.String(),'DateCreate':validators.String(),\
		'DateClose':validators.String(),'IsTempClosed':validators.Bool(),'Info':validators.String(),\
		'RoomNrStart':validators.Int(),'RoomNrEnd':validators.Int(),'Roomprefix':validators.String(),\
		'DeptNrID':validators.Int(),'WardID':validators.Int(),'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def WardsEditorSave(self, Name='', Description='', DateCreate='', DateClose='', IsTempClosed=None,
		Info='', RoomNrStart=None, RoomNrEnd=None, Roomprefix='', DeptNrID=None,
		WardID=None, Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		log.debug('WardsEditorSave')
		if WardID!=None:
			try:
				Ward = model.Ward.get(WardID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('WardsEditor')
		if Operation in ['Save (No Room Updates)','Save']: # Either update or create a new entry
			log.debug('...Save')
			Name = str(Name)
			Description = str(Description)
			Info = str(Info)
			Roomprefix = str(Roomprefix)
			# Silly but necessary date manipulations (I really wish the validators for dates worked!!!)
			if not DateCreate in ['',None]:
				DateCreate = datetime.fromtimestamp(time.mktime(time.strptime(DateCreate[0:10],DATE_FORMAT)))
			else:
				DateCreate = None
			if not DateClose in ['',None]:
				DateClose = datetime.fromtimestamp(time.mktime(time.strptime(DateClose[0:10],DATE_FORMAT)))
			else:
				DateClose = None
			if WardID==None: # Create a new entry
				log.debug('...New Entry')
				Ward = model.Ward(WardId=Name.lower().replace(' ','_'), Name=Name, DateCreate=DateCreate,
				DateClose=DateClose, IsTempClosed=IsTempClosed,Description=Description,Info=Info,DeptNrID=DeptNrID,
				RoomNrStart=RoomNrStart, RoomNrEnd=RoomNrEnd, Roomprefix=Roomprefix)
				RoomMessage = ''
				if Operation=='Save': # Only save rooms if the user wants to update this information
					# Type room configuration
					RoomTypes = model.TypeRoom.select(model.TypeRoom.q.Type=='ward')
					if RoomTypes.count() == 0:
						RoomType = model.TypeRoom(Type='ward', Name='Ward room')
						RoomTypeID = RoomType.id
					else:
						RoomTypeID = RoomTypes[0].id
					# Create the related rooms
					RoomCount = 0
					if RoomNrStart >=0 and RoomNrEnd >= RoomNrStart:
						for RoomNr in range(RoomNrStart, RoomNrEnd+1):
							RoomCount += 1
							Room = model.Room(TypeNrID=RoomTypeID,RoomNr=RoomNr,WardNrID=Ward.id,DeptNrID=Ward.DeptNrID)
						RoomMessage = 'and %d rooms created' % RoomCount
					else:
						RoomMessage = 'but there seems be a problem with the room numbers (no rooms created)'
					WardID = Ward.id
				turbogears.flash('New Entry Created (id: %d) %s' % (WardID, RoomMessage))
			else: # Update an entry
				Ward.WardId = Name.lower().replace(' ','_')
				Ward.Name = Name
				Ward.DateCreate = DateCreate
				Ward.DateClose = DateClose
				Ward.IsTempClosed = IsTempClosed
				Ward.Description = Description
				Ward.Info = Info
				Ward.DeptNrID = DeptNrID
				Ward.RoomNrStart = RoomNrStart
				Ward.RoomNrEnd = RoomNrEnd
				Ward.Roomprefix = Roomprefix
				CurrRooms = [x.RoomNr for x in Ward.Rooms]
				# Manage the rooms
				# Type room configuration
				RoomTypes = model.TypeRoom.select(model.TypeRoom.q.Type=='ward')
				if RoomTypes.count() == 0:
					RoomType = model.TypeRoom(Type='ward', Name='Ward room')
					RoomTypeID = RoomType.id
				else:
					RoomTypeID = RoomTypes[0].id
				DuplicateRooms = 0
				DelRoomCount = 0
				NewRoomCount = 0
				UnDelRoomCount = 0
				if Operation=='Save': # Only save rooms if the user wants to update this information
					if RoomNrStart >=0 and RoomNrEnd >= RoomNrStart:
						NewRooms = [x for x in range(RoomNrStart,RoomNrEnd+1)]
						for RoomNr in NewRooms:
							if RoomNr not in CurrRooms:
								NewRoomCount += 1
								Room = model.Room(TypeNrID=RoomTypeID,RoomNr=RoomNr,WardNrID=Ward.id,DeptNrID=Ward.DeptNrID)
						for Room in Ward.Rooms:
							if Room.RoomNr not in NewRooms:
								DelRoomCount += 1
								Room.Status = 'deleted'
								# Room.destroySelf() -- Maybe have it really delete the record
							elif Room.RoomNr in NewRooms and Room.Status=='deleted': # un-delete the entry
								UnDelRoomCount += 1
								Room.Status = ''
					for RoomNr in CurrRooms:
						if CurrRooms.count(RoomNr) > 1:
							DuplicateRooms += 1
				turbogears.flash('Recorded Updated with %d rooms created, %d rooms marked deleted, %d duplicate room entries and %d rooms un-deleted' \
				% (NewRoomCount,DelRoomCount,DuplicateRooms/2, UnDelRoomCount))
		elif Operation=='Delete' and WardID!=None:
			# We need to check if any of the id's are in use before attempting to delete an address from the system
			if len(Ward.Rooms)>0:
				# Mark the items deleted
				Ward.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				Ward.destroySelf()
				WardID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and WardID!=None:
			Ward.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			WardID=''
		else:
			turbogears.flash('Error in processing request')
		if WardID in ['',None]:
			raise cherrypy.HTTPRedirect('WardsEditor')
		else:
			raise cherrypy.HTTPRedirect('WardsEditor?WardID=%d' % WardID)
		
	@expose(format='json')
	def WardsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing location entry '''
		if QuickSearchText=='*':
			wards = model.Ward.select(orderBy=[model.Ward.q.Name])
		else:
			wards = model.Ward.select(model.Ward.q.Name.contains(str(QuickSearchText)),orderBy=[model.Ward.q.Name])
		results = []
		for item in wards:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)
		
	@expose(format='json')
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def WardsEditorDepartmentSelect(self, SearchText='', **kw):
		'''	Load the department item options
		'''
		SearchText = str(SearchText)
		items = model.Department.select(model.Department.q.NameFormal.contains(SearchText),
			orderBy=[model.Department.q.NameFormal])
		results = []
		for item in items:
			results.append(dict(id=item.id, text='%s (%d)' % (item.NameFormal,item.id)))
		return dict(results=results, function_name='WardsEditorDepartmentSelect')

	@expose(html='turbocare.templates.config_RoomsEditor')
	@validate(validators={'RoomID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def RoomsEditor(self, RoomID=None, **kw):
		'''	Either load a ward for editing, or bring up an empty form for adding a new ward 
		'''
		def Checked(value):
			if value:
				return "checked"
			else:
				return None
		# Attempt to load our Room
		if RoomID!=None: # attempt to load the record
			try:
				Room = model.Room.get(RoomID)
			except SQLObjectNotFound:
				turbogears.flash("The RoomID %d could not be found (deleted?)" % RoomID)
				Room=None
				RoomID=None
		else:
			Room=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if RoomID==None: # Create a blank form
			result['RoomID'] = ''
			result['DisplayName'] = 'New Entry'
			result['RoomNr'] = ''
			result['DateCreate'] = datetime.now().strftime(DATE_FORMAT)
			result['DateClose'] = ''
			result['IsTempClosed'] = None
			result['Info'] = ''
			result['NrOfBeds'] = 0
			result['DeptNrID'] = ''
			result['DeptNrName'] = ''
			result['WardNrID'] = ''
			result['WardNrName'] = ''
			result['IsDeleted'] = False
			result['ClosedBeds'] = []
		else:
			result['RoomID'] = RoomID
			result['DisplayName'] = 'Room Nr. %d (%d) %s' % (Room.RoomNr, Room.id, Room.Description())
			result['RoomNr'] = Room.RoomNr
			result['DateCreate'] = Room.DateCreate
			result['DateClose'] = Room.DateClose
			result['IsTempClosed'] = Checked(Room.IsTempClosed)
			result['Info'] = Room.Info
			result['NrOfBeds'] = Room.NrOfBeds
			result['DeptNrID'] = Room.DeptNrID
			if Room.DeptNrID in [0,None]:
				if Room.WardNrID not in [0,None]:
					if Room.WardNr.DeptNrID not in [0,None]:
						result['DeptNrName'] = Room.WardNr.DeptNr.NameFormal
				else:
					result['DeptNrName'] = ''
				if Room.DeptNrID == 0:
					Room.DeptNrID = 0
			else:
				result['DeptNrName'] = Room.DeptNr.NameFormal
			result['WardNrID'] = Room.WardNrID
			if Room.WardNrID in [0,None]:
				if Room.WardNrID == 0:
					Room.WardNrID = 0
				result['WardNrName'] = ''
			else:
				result['WardNrName'] = Room.WardNr.Name
			result['IsDeleted'] = Room.Status == 'deleted'
			ClosedBedArr = Room.ClosedBeds.split('/')
			NewClosedBedArr = []
			if len(ClosedBedArr[0]) == 0:
				ClosedBedArr = []
			else:
				for x in ClosedBedArr:
					if len(x)>0:
						NewClosedBedArr.append(int(x))
			ClosedBedArr = NewClosedBedArr
			ClosedBeds = []
			for bed in range(1,Room.NrOfBeds+1):
				if bed not in ClosedBedArr:
					ClosedBeds.append(dict(BedNr=bed, checked='checked'))
				else:
					ClosedBeds.append(dict(BedNr=bed, checked=None))
			result['ClosedBeds'] = ClosedBeds
			# Listing of Beds currently in use
			beds = Room.BedsInUse()
			result['beds'] = beds
		return result
	
	@expose()
	@validate(validators={'RoomNr':validators.Int(),'Info':validators.String(),'DateCreate':validators.String(),\
		'DateClose':validators.String(),'IsTempClosed':validators.Bool(),'DeptNrID':validators.Int(),\
		'NrOfBeds':validators.Int(),'WardNrID':validators.Int(),'RoomID':validators.Int(),'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def RoomsEditorSave(self, RoomNr=None, Info='', DateCreate='', DateClose='', IsTempClosed=None,
		 NrOfBeds=None,  DeptNrID=None, WardNrID=None, RoomID=None, Operation='', ClosedBeds=[], **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		log.debug('RoomsEditorSave')
		if RoomID!=None:
			try:
				Room = model.Room.get(RoomID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('RoomsEditor')
		if Operation=='Save': # Either update or create a new entry
			log.debug('...Save')
			# Type room configuration
			RoomTypes = model.TypeRoom.select(model.TypeRoom.q.Type=='ward')
			if RoomTypes.count() == 0:
				RoomType = model.TypeRoom(Type='ward', Name='Ward room')
				RoomTypeID = RoomType.id
			else:
				RoomTypeID = RoomTypes[0].id
			Info = str(Info)
			# Silly but necessary date manipulations (I really wish the validators for dates worked!!!)
			if not DateCreate in ['',None]:
				DateCreate = datetime.fromtimestamp(time.mktime(time.strptime(DateCreate[0:10],DATE_FORMAT)))
			else:
				DateCreate = None
			if not DateClose in ['',None]:
				DateClose = datetime.fromtimestamp(time.mktime(time.strptime(DateClose[0:10],DATE_FORMAT)))
			else:
				DateClose = None
			# Update the Closed Beds variable - NOTE, the variable actually returns back the beds which are NOT closed
			log.debug(ClosedBeds)
			if len(ClosedBeds) == 0:
				ClosedBeds = []
			elif isinstance(ClosedBeds,basestring):
				ClosedBeds = [int(ClosedBeds)]
			else:
				ClosedBeds = [int(x) for x in ClosedBeds]
			ClosedBedsString = '' # This will hold the true closed beds (not open beds)
			for bed in range(1,NrOfBeds+1):
				if bed not in ClosedBeds:
					ClosedBedsString += '%d/' % bed
			if RoomID==None: # Create a new entry
				log.debug('...New Entry')
				Room = model.Room(TypeNrID=RoomTypeID,DateCreate=DateCreate,DateClose=DateClose,IsTempClosed=IsTempClosed,
				RoomNr=RoomNr,WardNrID=WardNrID,DeptNrID=DeptNrID,NrOfBeds=NrOfBeds,Info=Info,ClosedBeds=ClosedBedsString)
				RoomID = Room.id
				turbogears.flash('New Entry Created (id: %d)' % RoomID)
			else: # Update an entry
				Room.TypeNrID = RoomTypeID
				Room.DateCreate = DateCreate
				Room.DateClose = DateClose
				Room.IsTempClosed = IsTempClosed
				Room.RoomNr = RoomNr
				Room.WardNrID = WardNrID
				if WardNrID == None: # Don't allow editing of the department unless the ward is blank
					Room.DeptNrID = DeptNrID
				else:
					Room.DeptNrID = None
				Room.NrOfBeds = NrOfBeds
				Room.Info = Info
				Room.ClosedBeds = ClosedBedsString
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and RoomID!=None:
			# Just check to make sure no one is using the room at the time
			if len(model.GetBedActivityInformation(RoomID=RoomID)) > 0:
				# Mark the item deleted
				Room.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				Room.destroySelf()
				RoomID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and WardID!=None:
			Room.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			RoomID=''
		else:
			turbogears.flash('Error in processing request')
		if RoomID in ['',None]:
			raise cherrypy.HTTPRedirect('RoomsEditor')
		else:
			raise cherrypy.HTTPRedirect('RoomsEditor?RoomID=%d' % RoomID)
		
	@expose(format='json')
	def RoomsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing location entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			rooms = model.Room.select(orderBy=[model.Room.q.RoomNr])
		else:
			rooms = model.Room.select(OR (AND (model.Ward.q.id==model.Room.q.WardNrID, model.Ward.q.Name.contains(str(QuickSearchText))),
			AND(model.Department.q.id==model.Room.q.DeptNrID,model.Department.q.NameFormal.contains(QuickSearchText))),
			orderBy=[model.Ward.q.Name, model.Department.q.NameFormal, model.Room.q.RoomNr],distinct=True)
		results = []
		for item in rooms:
			if item.WardNrID not in [0, None]:
				results.append(dict(id=item.id, text='%s - %d' % (item.WardNr.Name, item.RoomNr)))
			elif item.DeptNrID not in [0, None]:
				results.append(dict(id=item.id, text='%s - %d' % (item.DeptNr.NameFormal, item.RoomNr)))
			else:
				results.append(dict(id=item.id, text='Un-linked room #%d' % item.RoomNr))
		return dict(results=results)
		
	@expose(format='json')
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def RoomsEditorWardSelect(self, SearchText='', **kw):
		'''	Load the department item options
		'''
		SearchText = str(SearchText)
		items = model.Ward.select(model.Ward.q.Name.contains(str(SearchText)),orderBy=[model.Ward.q.Name])
		results = []
		for item in items:
			results.append(dict(id=item.id, text='%s (%d)' % (item.Name,item.id)))
		return dict(results=results, function_name='RoomsEditorWardSelect')
		
	def GetDefaultCustomerLocationID(self):
		'''	When moving inventory to a location where it's sold, we need to mark the new location as the customer
			location.  Most customers should have a location already defined, but we need
			a default just in case
		'''
		items = model.InvLocation.select(model.InvLocation.q.Name.contains('Customer'))
		if items.count() > 0:
			return items[0].id
		else:
			return None
	
	@expose(html='turbocare.templates.config_DoctorsEditor')
	@validate(validators={'PersonellID':validators.Int(),'PersonID':validators.Int(),'CustomerID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def DoctorsEditor(self, PersonellID=None, PersonID=None, CustomerID=None, **kw):
		'''	Either load a Doctor for editing, or bring up an empty form for adding a Doctor ward
			A Doctor, just like anyone else in the system, should have a Person and Customer Record
		'''
		def Checked(value):
			if value:
				return "checked"
			else:
				return None
		def CreateCustomer(Person):
			"""	Create a customer record based on the Person record """
			citytown = model.AddressCityTown.get(Person.AddrCitytownNrID)
			AddressLabel = '%s\n%s\n%s, %s\n%s\n%s' % (Person.AddrStr, citytown.Name, citytown.Block, citytown.District, citytown.State, citytown.ZipCode)			
			PersonName = ('%s %s,%s,%s' % (Person.Title, Person.NameFirst, Person.NameMiddle, Person.NameLast)).replace(',,',',').replace(',', ' ').strip()
			customer = model.InvCustomer(Name=PersonName ,CityID=Person.AddrCitytownNrID , AddressLabel=AddressLabel, CreditAmount=0.0, \
				InventoryLocation=self.GetDefaultCustomerLocationID(), ExternalID=Person.id)
			return customer
		def GetCustomer(Person):
			"""	Look for a customer based on the person record.  If none is found, then create it """
			customers = model.InvCustomer.select(model.InvCustomer.q.ExternalID==Person.id)
			if customers.count() == 0:
				return CreateCustomer(Person)
			else:
				return customers[0]
		result = {} # The dictionary for our template variables
		# Attempt to load person information, PersonellID will take precedence
		# log.debug('DoctorsEditor, PersonellID: %r, PersonID: %r, CustomerID: %r' % (PersonellID, PersonID, CustomerID))
		if PersonellID != None or PersonID != None or CustomerID != None: # Attempt to load the doctor
			try:
				if PersonellID != None:
					Personell = model.Personell.get(PersonellID)
					Person = Personell.Person
					PersonID = Person.id
					if len(Person.Customer) == 0:
						turbogears.flash("Note: A customer record was added for the Doctor (a required record by the program)")
						Customer = GetCustomer(Person)
						CustomerID = Customer.id
					else:
						Customer = Person.Customer[0]
						CustomerID = Customer.id
				elif PersonID != None:
					Person = model.Person.get(PersonID)
					if len(Person.Personell) == 0:
						turbogears.flash("The person you loaded is not a Doctor.  If you want to make them a Doctor, then search for the person in the 'Person Record' link option")
						raise cherrypy.HTTPRedirect('DoctorsEditor')
					else:
						Personell = Person.Personell[0]
						PersonellID = Personell.id
					Customer = GetCustomer(Person)
					CustomerID = Customer.id
				elif CustomerID != None:
					Customer = model.InvCustomer.get(CustomerID)
					if Customer.ExternalID == None:
						turbogears.flash("There was an error in trying to load the Doctor.  The customer you choose is not a Doctor.")
						raise cherrypy.HTTPRedirect('DoctorsEditor')
					else:
						PersonID = Customer.ExternalID
					Person = model.Person.get(PersonID)
					if len(Person.Personell) == 0:
						turbogears.flash("There was an error in trying to load the Doctor.  The customer you choose is not a Doctor.")
						raise cherrypy.HTTPRedirect('DoctorsEditor')
					else:
						Personell = Person.Personell[0]
					PersonellID = Personell.id
			except SQLObjectNotFound, errorstr:
				turbogears.flash("There was an error in trying to load the Doctor.")
				errorArr = errorstr[0].split(' ')
				table = errorArr[2]
				id = errorArr[6]
				if table == 'InvCustomer':
					turbogears.flash("There was an error in trying to load the Doctor.  The Customer record (id: %s) could not be found" % id)
					raise cherrypy.HTTPRedirect('DoctorsEditor')
				elif table == 'Person':
					turbogears.flash("There was an error in trying to load the Doctor.  The Person record (Person id: %s) could not be found" % id)
					raise cherrypy.HTTPRedirect('DoctorsEditor')
				elif table == 'Personell':
					turbogears.flash("There was an error in trying to load the Doctor.  The Personell record (Personell id: %s) could not be found" % id)
					raise cherrypy.HTTPRedirect('DoctorsEditor')
				else:
					turbogears.flash("There was an error in trying to load the Doctor.  The object %s record (%s id: %d) could not be found" % (table,table,id))
		else: # Prepare for a blank form
			Personell = None
			PersonellID = None
			Person = None
			PersonID = None
			Customer = None
			CustomerID = None
		if Personell == None: # No personell selected, load an empty form for a new entry
			result['DisplayName'] = 'Create a New Entry'
			result['IsDischarged'] = None
			result['titles'] = [dict(id=x, name=x, selected=None) for x in model.dbTitles]
			result['NameFirst'] = ''
			result['NameMiddle'] = ''
			result['NameLast'] = ''
			result['genders'] = [dict(name=x, selected=None) for x in model.dbGender]
			result['religions'] = [dict(id=x, name=x, selected=None) for x in model.dbReligion]
			result['tribes'] =  [dict(id=x.id, name=x.Name, selected=None) for x in model.TypeEthnicOrig.select(AND (model.TypeEthnicOrig.q.ClassNrID==model.ClassEthnicOrig.q.id,
				model.ClassEthnicOrig.q.Name == 'Tribe'),orderBy=[model.TypeEthnicOrig.q.Name])]
			result['AddressStreet'] = ''
			result['SelectedCity'] = 'No City Selected'
			result['AddrCitytownNrID'] = ''
			result['CityTownName'] = ''
			result['PostOffice'] = ''
			result['Block'] = ''
			result['District'] = ''
			result['State'] = ''
			result['Country'] = ''
			result['PersonID']=''
			result['PersonellID']=''
			result['Age']=''
			result['DateBirth']=''
			result['IsDeleted'] = False
		else:
			def Selected(value):
				""" Returns 'selected' if the value is true, otherwise false """
				if value:
					return 'selected'
				else:
					return None
			if Personell.JobFunctionTitle != 'Doctor':
				turbogears.flash("The person you loaded is not a Doctor.  If you want to make them a Doctor, then search for the person in the 'Person Record' link option, and then save it")
				raise cherrypy.HTTPRedirect('DoctorsEditor')				
			result['DisplayName'] = '%s (%d/%d)' % (Person.DisplayName(), PersonellID, PersonID)
			result['IsDischarged'] = Checked(Personell.IsDischarged)
			result['titles'] = [dict(id=x, name=x, selected=Selected(Person.Title==x)) for x in model.dbTitles]
			result['NameFirst'] = Person.NameFirst
			result['NameMiddle'] = Person.NameMiddle
			result['NameLast'] = Person.NameLast
			result['genders'] = [dict(name=x, selected=Selected(Person.Sex==x)) for x in model.dbGender]
			result['religions'] = [dict(id=x, name=x, selected=Selected(Person.Religion==x)) for x in model.dbReligion]
			result['tribes'] =  [dict(id=x.id, name=x.Name, selected=Selected(Person.EthnicOrigID==x.id)) for x in model.TypeEthnicOrig.select(AND (model.TypeEthnicOrig.q.ClassNrID==model.ClassEthnicOrig.q.id,
				model.ClassEthnicOrig.q.Name == 'Tribe'),orderBy=[model.TypeEthnicOrig.q.Name])]
			result['AddressStreet'] = Person.AddrStr
			if Person.AddrCitytownNrID == 0:
				Person.AddrCitytownNrID = None
			result['AddrCitytownNrID'] = Person.AddrCitytownNrID
			if Person.AddrCitytownNrID == None:
				result['CityTownName'] = ''
				result['PostOffice'] = ''
				result['Block'] = ''
				result['District'] = ''
				result['State'] = ''
				result['Country'] = ''
				result['SelectedCity'] = 'No City Selected'
			else:
				result['CityTownName'] = Person.AddrCitytownNr.Name
				result['PostOffice'] = Person.AddrCitytownNr.ZipCode
				result['Block'] = Person.AddrCitytownNr.Block
				result['District'] = Person.AddrCitytownNr.District
				result['State'] = Person.AddrCitytownNr.State
				result['Country'] = Person.AddrCitytownNr.IsoCountryId
				result['SelectedCity'] = '(id:%d) %s in %s, %s (%s)' % (result['AddrCitytownNrID'], result['Block'], result['CityTownName'],
					result['District'], result['PostOffice'])
			result['PersonID']=PersonID
			result['PersonellID']=PersonellID
			result['DateBirth']=Person.DateBirth.strftime(DATE_FORMAT)
			if Person.DateBirth != '':
				result['Age'] = int(((datetime.now().date() - Person.DateBirth).days+0.5)/365.25)
			else:
				result['Age'] = ''
			result['DateBirth']=Person.DateBirth.strftime(DATE_FORMAT)
			result['IsDeleted'] = Personell.Status=='deleted'
		return result
	
	@expose()
	@validate(validators={'Tribe':validators.String(),'Title':validators.String(), 'Gender':validators.String(), \
	'Religion':validators.String(),'NameFirst':validators.String(), 'NameMiddle':validators.String(), \
	'NameLast':validators.String(),'AddressStreet':validators.String(), 'AddrCitytownNrID':validators.Int(), \
	'PersonID':validators.Int(),'PersonellID':validators.Int(), 'Operation':validators.String(), \
	'DateBirth':validators.String(),'IsDischarged':validators.Bool()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def DoctorsEditorSave(self, Tribe='', Title='', Gender='', Religion='', NameFirst='', NameMiddle='', NameLast='', AddressStreet='',\
			AddrCitytownNrID=None, PersonID=None, DateBirth='', Age='', \
			PersonellID=None, Operation='', IsDischarged=None, **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		def CreateCustomer(Person):
			"""	Create a customer record based on the Person record """
			citytown = model.AddressCityTown.get(Person.AddrCitytownNrID)
			AddressLabel = '%s\n%s\n%s, %s\n%s\n%s' % (Person.AddrStr, citytown.Name, citytown.Block, citytown.District, citytown.State, citytown.ZipCode)			
			PersonName = ('%s %s,%s,%s' % (Person.Title, Person.NameFirst, Person.NameMiddle, Person.NameLast)).replace(',,',',').replace(',', ' ').strip()
			customer = model.InvCustomer(Name=PersonName ,CityID=Person.AddrCitytownNrID , AddressLabel=AddressLabel, CreditAmount=0.0, \
				InventoryLocation=self.GetDefaultCustomerLocationID(), ExternalID=Person.id)
			return customer
		def GetCustomer(Person):
			"""	Look for a customer based on the person record.  If none is found, then create it """
			customers = model.InvCustomer.select(model.InvCustomer.q.ExternalID==Person.id)
			if customers.count() == 0:
				return CreateCustomer(Person)
			else:
				return customers[0]
		log.debug('DoctorsEditorSave')
		if PersonellID!=None: # Load the record for editing
			try:
				Personell = model.Personell.get(PersonellID)
				Person = Personell.Person
				PersonID = Person.id
				Customer = GetCustomer(Person)
				CustomerID = Customer.id
			except SQLObjectNotFound, errorstr:
				table = errorArr[2]
				id = errorArr[6]
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost. The %s with id %s doesn't exist. Try again." % (table, id))
				raise cherrypy.HTTPRedirect('DoctorsEditor')
		if PersonID != None and PersonellID==None: # Do a quick check to make sure a personell record doesn't already exist for the person as a Doctor
			doctors=model.Personell.select(AND (model.Personell.q.JobFunctionTitle == 'Doctor', model.Personell.q.PersonID==PersonID))
			if doctors.count() > 0:
				turbogears.flash("There are %d records that match what you were trying to create.  Edit the record displayed" % doctors.count())
				raise cherrypy.HTTPRedirect('DoctorsEditor?PersonellID=%d' % doctors[0].id)			
		if Operation=='Save': # Either update or create a new entry
			log.debug('...Save')
			# Silly but necessary date manipulations (I really wish the validators for dates worked!!!)
			if not DateBirth in ['',None]:
				DateBirth = datetime.fromtimestamp(time.mktime(time.strptime(DateBirth[0:10],DATE_FORMAT)))
			else:
				DateBirth = None
			# Update the Closed Beds variable - NOTE, the variable actually returns back the beds which are NOT closed
			if PersonellID==None: # Create a new entry
				if PersonID==None: # Create a new person and customer entry
					Person = model.Person(NameFirst=NameFirst,NameLast=NameLast,NameMiddle=NameMiddle,\
						AddrStr=AddressStreet,AddrCitytownNrID=AddrCitytownNrID,Sex=Gender,Religion=Religion,\
						DateBirth=DateBirth, EthnicOrig=int(Tribe))
					PersonID = Person.id
					citytown = model.AddressCityTown.get(AddrCitytownNrID)
					AddressLabel = '%s\n%s\n%s, %s\n%s\n%s' % (AddressStreet, citytown.Name, citytown.Block, citytown.District, citytown.State, citytown.ZipCode)			
					DoctorName = ('%s %s,%s,%s' % (Title, NameFirst, NameMiddle, NameLast)).replace(',,',',').replace(',', ' ').strip()
					Customer = model.InvCustomer(Name=DoctorName ,CityID=Person.AddrCitytownNrID , AddressLabel=AddressLabel, CreditAmount=0.0, \
						InventoryLocation=self.GetDefaultCustomerLocationID(), ExternalID=Person.id)
					CustomerID = Customer.id
					PersonText = 'New Person entry (id: %d) created, New Customer entry (id: %d) created.' % (PersonID, CustomerID)
				else: # Linking to an existing Person entry
					try:
						Person = model.Person.get(PersonID)
						Customer = GetCustomer(Person)
						CustomerID = Customer.id
						PersonText = 'Entry is linked to existing Person entry (id: %d)' % PersonID
					except SQLObjectNotFound, errorstr:
						table = errorArr[2]
						id = errorArr[6]
						turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost. The %s with id %s doesn't exist. You're attempt to link this person in as a Doctor failed." % (table, id))
						raise cherrypy.HTTPRedirect('DoctorsEditor')
				Personell = model.Personell(PersonID=PersonID, JobFunctionTitle='Doctor')
				PersonellID = Personell.id
				turbogears.flash('New Entry Created (id: %d) %s' % (PersonellID,PersonText))
			else: # Update an entry
				Personell.IsDischarged = IsDischarged
				Person.Title = Title
				Person.NameFirst = NameFirst
				Person.NameMiddle = NameMiddle
				Person.NameLast = NameLast
				Customer.Name = ('%s %s,%s,%s' % (Title, NameFirst, NameMiddle, NameLast)).replace(',,',',').replace(',', ' ').strip()
				#Update address
				if Person.AddrStr != AddressStreet or Person.AddrCitytownNrID != AddrCitytownNrID:
					Person.AddrStr = AddressStreet
					Person.AddrCitytownNrID = AddrCitytownNrID
					citytown = model.AddressCityTown.get(AddrCitytownNrID)
					Customer.CityID = citytown.id
					AddressLabel = '%s\n%s\n%s, %s\n%s\n%s' % (AddressStreet, citytown.Name, citytown.Block, citytown.District, citytown.State, citytown.ZipCode)
					Customer.AddressLabel = AddressLabel
				# Other info
				Person.Sex = Gender
				Person.Religion = Religion
				Person.DateBirth = DateBirth
				if Tribe in ['',None]:
					Person.EthnicOrig = None
				else:
					Person.EthnicOrig = int(Tribe)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and Personell!=None:
			# Just check to make sure no one is using the room at the time
			if len(Personell.Encounters) > 0:
				# Mark the item deleted
				Personell.Status = 'deleted'
				turbogears.flash('Personell Record Marked Deleted')
			else:
				Personell.destroySelf()
				PersonellID = None
				turbogears.flash('Personell Record Deleted')
		elif Operation=='Un-Delete' and Personell!=None:
			Personell.Status = ''
			turbogears.flash('Personell Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			PersonellID=''
		else:
			turbogears.flash('Error in processing request')
		if PersonellID in ['',None]:
			raise cherrypy.HTTPRedirect('DoctorsEditor')
		else:
			raise cherrypy.HTTPRedirect('DoctorsEditor?PersonellID=%d' % PersonellID)
	
	@expose(format='json')
	def DoctorsEditorSearchDoctor(self, QuickSearchText):
		'''	search for Doctors
		'''
		QuickSearchText = QuickSearchText.lower()
		items=model.Personell.select(AND (model.Personell.q.JobFunctionTitle == 'Doctor', model.Personell.q.Status != 'deleted', \
		model.Personell.q.IsDischarged == False,model.Personell.q.PersonID==model.Person.q.id),
		orderBy=[model.Person.q.NameFirst,model.Person.q.NameLast])
		doctors = [dict(id=x.id, text=x.DisplayName()) for x in items]
		if len(doctors) > 0:
			if QuickSearchText == '*':
				return dict(results=doctors)
			else:
				return dict(results=filter(lambda doctor: QuickSearchText in doctor['text'].lower(), doctors))
		else:
			return dict(results=[])
			
	@expose(format='json')
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def DoctorsEditorPersonSelect(self, SearchText='', **kw):
		'''	Load the person options
		'''
		SearchText = str(SearchText)
		TextWords = SearchText.replace(',','').split()
		qArgs = ""
		qAddr = ''
		if not (SearchText in [None, '']):
			# Look for First, middle last name
			if len(TextWords) == 3: #Try a first, middle, last name search
				qArgs+="AND ("
				qArgs+="model.Person.q.NameFirst.contains('"+ TextWords[0] + "'),"
				qArgs+="model.Person.q.NameMiddle.contains('"+ TextWords[1] + "'),"
				qArgs+="model.Person.q.NameLast.contains('"+ TextWords[2] + "')"
				qArgs+="),"
			if len(TextWords) == 2: #Try a first, last name search and vice versa
				qArgs+="OR (AND ("
				qArgs+="model.Person.q.NameFirst.contains('"+ TextWords[0] + "'),"
				qArgs+="model.Person.q.NameLast.contains('"+ TextWords[1] + "')"
				qArgs+="), AND ("
				qArgs+="model.Person.q.NameFirst.contains('"+ TextWords[1] + "'),"
				qArgs+="model.Person.q.NameLast.contains('"+ TextWords[0] + "')"
				qArgs+=")),"
			if len(TextWords) == 1: #Try a first or last name search
				qArgs+="OR ("
				qArgs+="model.Person.q.NameFirst.contains('"+ TextWords[0] + "'),"
				qArgs+="model.Person.q.NameLast.contains('"+ TextWords[0] + "')"
				qArgs+="),"
		OrderBy = 'orderBy=[model.Person.q.NameFirst,model.Person.q.NameLast]'
		if len(qArgs) > 0:
			items = eval('model.Person.select(%s,%s)' % (qArgs[:-1],OrderBy))
		else:
			items = model.Person.select(orderBy=[model.Person.q.NameFirst,model.Person.q.NameLast])[0:100]
		results = []
		for item in items:
			results.append(dict(id=item.id, text='%s (%d)' % (item.DisplayName(),item.id)))
		return dict(results=results, function_name='DoctorsEditorPersonSelect')
	
	@expose(format='json')
	def DoctorsEditorCityTownSearch(self, CityTownName='', PostOffice='', Block='', District='', State='', Country='',  **kw):
		'''	Search for Addresses (by Block, City/Town, District, State)
		'''
		qArgs = ''
		if CityTownName != '':
			qArgs+="model.AddressCityTown.q.Name.contains('"+ CityTownName + "'),"
		if PostOffice != '':
			qArgs+="model.AddressCityTown.q.ZipCode.contains('"+ PostOffice + "'),"
		if District != '':
			qArgs+="model.AddressCityTown.q.District.contains('"+ District + "'),"
		if State != '':
			qArgs+="model.AddressCityTown.q.State.contains('"+ State + "'),"
		if Country != '':
			qArgs+="model.AddressCityTown.q.IsoCountryId.contains('"+ Country + "'),"
		if Block != '':
			qArgs+="model.AddressCityTown.q.Block.contains('"+ Block + "'),"
		if len(qArgs) > 0:
			log.debug('Query String [Args]: model.AddressCityTown.select(AND (%s))' % qArgs[:-1])
			items = eval('model.AddressCityTown.select(AND (%s))' % qArgs[:-1])
		else:
			items = []
		Results = []
		for item in items:
			Text = '(id:%d) %s' % (item.id, item.DisplayName())
			Results.append(dict(id=item.id,text=Text,city_town_name=item.Name, post_office=item.ZipCode, \
				district=item.District, state=item.State, country=item.IsoCountryId, block=item.Block))
		return dict(result_count=len(Results), results=Results, city_town_name=CityTownName, post_office=PostOffice,\
			block=Block, district=District, state=State, country=Country)
			
	@expose(html='turbocare.templates.config_InsuranceEditor')
	@validate(validators={'FirmID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def InsuranceEditor(self, FirmID=None, **kw):
		'''	Either load an insurance firm for editing, or bring up an empty form for adding a new ward 
		'''
		# Attempt to load our Room
		if FirmID!=None: # attempt to load the record
			try:
				Firm = model.InsuranceFirm.get(FirmID)
			except SQLObjectNotFound:
				turbogears.flash("The FirmID %d could not be found (deleted?)" % FirmID)
				Firm=None
				FirmID=None
		else:
			Firm=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if FirmID==None: # Create a blank form
			result['FirmID'] = ''
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['IsoCountryId'] = 'IND'
			result['SubArea'] = ''
			result['Addr'] = ''
			result['AddrMail'] = ''
			result['AddrBilling'] = ''
			result['AddrEmail'] = ''
			result['PhoneMain'] = ''
			result['PhoneAux'] = ''
			result['FaxMain'] = ''
			result['FaxAux'] = ''
			result['ContactPerson'] = ''
			result['ContactPhone'] = ''
			result['ContactFax'] = ''
			result['ContactEmail'] = ''
			result['InsuranceUsers'] = []
			result['IsDeleted'] = False
		else:
			result['FirmID'] = FirmID
			result['DisplayName'] = '%s (%d)' % (Firm.Name, FirmID)
			result['Name'] = Firm.Name
			result['IsoCountryId'] = Firm.IsoCountryId
			result['SubArea'] = Firm.SubArea
			result['Addr'] = Firm.Addr
			result['AddrMail'] = Firm.AddrMail
			result['AddrBilling'] = Firm.AddrBilling
			result['AddrEmail'] = Firm.AddrEmail
			result['PhoneMain'] = Firm.PhoneMain
			result['PhoneAux'] = Firm.PhoneAux
			result['FaxMain'] = Firm.FaxMain
			result['FaxAux'] = Firm.FaxAux
			result['ContactPerson'] = Firm.ContactPerson
			result['ContactPhone'] = Firm.ContactPhone
			result['ContactFax'] = Firm.ContactFax
			result['ContactEmail'] = Firm.ContactEmail
			result['IsDeleted'] = Firm.Status == 'deleted'
			result['InsuranceUsers'] = Firm.Persons()
		return result
	
	@expose()
	@validate(validators={'FirmID':validators.Int(),'Name':validators.String(),'IsoCountryId':validators.String(),\
	'SubArea':validators.String(),'Addr':validators.String(),'AddrMail':validators.String(),'AddrBilling':validators.String(),\
	'AddrEmail':validators.String(),'PhoneMain':validators.String(),'PhoneAux':validators.String(),'FaxMain':validators.String(),\
	'FaxAux':validators.String(),'ContactPerson':validators.String(),'ContactPhone':validators.String(),\
	'ContactFax':validators.String(),'ContactEmail':validators.String(),'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def InsuranceEditorSave(self, FirmID=None,Name='',IsoCountryId='',SubArea='',Addr='',AddrMail='',
		AddrBilling='',AddrEmail='',PhoneMain='',PhoneAux='',FaxMain='',FaxAux='',
		ContactPerson='',ContactPhone='',ContactFax='',ContactEmail='',Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		log.debug('InsuranceEditorSave')
		if FirmID!=None:
			try:
				Firm = model.InsuranceFirm.get(FirmID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('InsuranceEditor')
		if Operation=='Save': # Either update or create a new entry
			log.debug('...Save')
			# Type room configuration
			InsuranceTypes = model.TypeInsurance.select(model.TypeInsurance.q.Type=='private')
			if InsuranceTypes.count() == 0:
				InsuranceType = model.TypeInsurance(Type='private', Name='Private Insurance')
				InsuranceTypeID = InsuranceType.id
			else:
				InsuranceTypeID = InsuranceTypes[0].id
			if FirmID==None: # Create a new entry
				log.debug('...New Entry')
				if AddrMail=='':
					AddrMail = Addr
				if AddrBilling=='':
					AddrBilling = Addr
				Firm = model.InsuranceFirm(Name=Name,IsoCountryId=IsoCountryId,SubArea=SubArea,FirmId='',
					TypeNrID=InsuranceTypeID,FaxMain=FaxMain,FaxAux=FaxAux,ContactPerson=ContactPerson,
					Addr=Addr,AddrMail=AddrMail,AddrBilling=AddrBilling,AddrEmail=AddrEmail,PhoneMain=PhoneMain,
					PhoneAux=PhoneAux,ContactPhone=ContactPhone,ContactFax=ContactFax,ContactEmail=ContactEmail)
				Firm.FirmId = str(Firm.id)
				FirmID = Firm.id
				turbogears.flash('New Entry Created (id: %d)' % FirmID)
			else: # Update an entry
				Firm.Name = str(Name)
				Firm.IsoCountryId = str(IsoCountryId)
				Firm.SubArea = str(SubArea)
				if Firm.Addr!=Addr:
					if AddrMail=='':
						AddrMail = Addr
					if AddrBilling=='':
						AddrBilling = Addr
				Firm.Addr = str(Addr)
				Firm.AddrMail = str(AddrMail)
				Firm.AddrBilling = str(AddrBilling)
				Firm.AddrEmail = str(AddrEmail)
				Firm.PhoneMain = str(PhoneMain)
				Firm.PhoneAux = str(PhoneAux)
				Firm.FaxMain = str(FaxMain)
				Firm.FaxAux = str(FaxAux)
				Firm.ContactPerson = str(ContactPerson)
				Firm.ContactPhone = str(ContactPhone)
				Firm.ContactFax = str(ContactFax)
				Firm.ContactEmail = str(ContactEmail)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and FirmID!=None:
			# Just check to make sure no one is using the room at the time
			if len(Firm.Persons()) > 0:
				# Mark the item deleted
				Firm.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				Firm.destroySelf()
				FirmID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and FirmID!=None:
			Firm.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			FirmID=''
		else:
			turbogears.flash('Error in processing request')
		if FirmID in ['',None]:
			raise cherrypy.HTTPRedirect('InsuranceEditor')
		else:
			raise cherrypy.HTTPRedirect('InsuranceEditor?FirmID=%d' % FirmID)
		
	@expose(format='json')
	def InsuranceEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing location entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			firms = model.InsuranceFirm.select(orderBy=[model.InsuranceFirm.q.Name])
		else:
			firms = model.InsuranceFirm.select(model.InsuranceFirm.q.Name.contains(QuickSearchText),
			orderBy=[model.InsuranceFirm.q.Name])
		results = []
		for item in firms:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)
		
	@expose(html='turbocare.templates.config_PackagingTypesEditor')
	@validate(validators={'PackagingID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def PackagingTypesEditor(self, PackagingID=None, **kw):
		'''	Either load an packaging types for editing, or bring up an empty form for adding a new entry 
		'''
		if PackagingID!=None: # attempt to load the record
			try:
				Packaging = model.InvPackaging.get(PackagingID)
			except SQLObjectNotFound:
				turbogears.flash("The PackagingID %d could not be found (deleted?)" % PackagingID)
				Packaging=None
				PackagingID=None
		else:
			Packaging=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if PackagingID==None: # Create a blank form
			result['PackagingID'] = ''
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['Description'] = ''
			result['Groups'] = []
			result['Items'] = []
			result['IsDeleted'] = False
		else:
			result['PackagingID'] = PackagingID
			result['DisplayName'] = '%s (%d)' % (Packaging.Name, PackagingID)
			result['Name'] = Packaging.Name
			result['Description'] = Packaging.Description
			try:
				result['Groups'] = [dict(id=x.id, name=x.Name) for x in Packaging.Groups]
			except SQLObjectNotFound, errorstr:
				turbogears.flash('There was a problem loading this record.  Some linked data has been removed from the system, which is causing the problem.  Try reloading this record (sometimes repeatedly) until the error is corrected.  Have a nice day.')
				errorArr = errorstr[0].split(' ')
				table = errorArr[2]
				id = errorArr[6]
				# Remove the offending record
				if table == 'InvGrpPackaging':
					Packaging.removeInvGrpPackaging(int(id))
			result['Items'] = [dict(Name=x.DisplayName()) for x in Packaging.CatalogItems]
			result['IsDeleted'] = Packaging.Status=='deleted'
		return result
		
	@expose()
	@validate(validators={'PackagingID':validators.Int(),'Name':validators.String(),'Description':validators.String(),\
	'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PackagingTypesEditorSave(self, PackagingID=None,Name='',Description='',Operation='', Groups=[], **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		if PackagingID!=None:
			try:
				Packaging = model.InvPackaging.get(PackagingID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('PackagingTypesEditor')
		if Operation=='Save': # Either update or create a new entry
			# Format the Groups as a list of integers
			if isinstance(Groups, basestring): # a single entry
				Groups = [int(Groups)]
			else:
				Groups = [int(x) for x in Groups]
			if PackagingID==None: # Create a new entry
				Packaging = model.InvPackaging(Name=Name,Description=Description)
				# Add Groups
				for group in Groups:
					Packaging.addInvGrpPackaging(group)
				PackagingID = Packaging.id
				turbogears.flash('New Entry Created (id: %d)' % PackagingID)
			else: # Update an entry
				Packaging.Name = str(Name)
				Packaging.Description = str(Description)
				# Get a list of current groups
				CurGroups = [x.id for x in Packaging.Groups]
				# Add new groups
				for group in Groups:
					if group not in CurGroups:
						Packaging.addInvGrpPackaging(group)
				# Remove groups
				for group in CurGroups:
					if group not in Groups:
						Packaging.removeInvGrpPackaging(group)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and PackagingID!=None:
			# Just check to make sure no one is using the room at the time
			if len(Packaging.CatalogItems) > 0:
				# Mark the item deleted
				Packaging.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				# Remove all groups before deleting
				for group in Packaging.Groups:
					Packaging.removeInvGrpPackaging(group)
				Packaging.destroySelf()
				PackagingID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and PackagingID!=None:
			Packaging.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			PackagingID=''
		else:
			turbogears.flash('Error in processing request')
		if PackagingID in ['',None]:
			raise cherrypy.HTTPRedirect('PackagingTypesEditor')
		else:
			raise cherrypy.HTTPRedirect('PackagingTypesEditor?PackagingID=%d' % PackagingID)
		
	@expose(format='json')
	def PackagingTypesEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			packages = model.InvPackaging.select(orderBy=[model.InvPackaging.q.Name])
		else:
			packages = model.InvPackaging.select(model.InvPackaging.q.Name.contains(QuickSearchText),
				orderBy=[model.InvPackaging.q.Name])
		results = []
		for item in packages:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)
	
	@expose(format='json')
	@validate(validators={'PackagingID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def PackagingTypesEditorGroupSelect(self, PackagingID=None, **kw):
		'''	Load the Group Options
			Mark items which are already selected as selected
		'''
		cur_groups = []
		if PackagingID!=None:
			Packaging = model.InvPackaging.get(PackagingID)
			for group in Packaging.Groups:
				cur_groups.append(group.id)
		groups = model.InvGrpPackaging.select(orderBy=[model.InvGrpPackaging.q.Name])
		results = []
		for group in groups:
			results.append(dict(id=group.id, text=group.Name, selected=(group.id in cur_groups)))
		return dict(results=results)
		
	@expose(html='turbocare.templates.config_CatalogItemGroupsEditor')
	@validate(validators={'GroupID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CatalogItemGroupsEditor(self, GroupID=None, **kw):
		'''	Either load an Catalog Item Groups for editing, or bring up an empty form for adding a new entry 
		'''
		if GroupID!=None: # attempt to load the record
			try:
				Group = model.InvGrpStock.get(GroupID)
			except SQLObjectNotFound:
				turbogears.flash("The GroupID %d could not be found (deleted?)" % GroupID)
				Group=None
				GroupID=None
		else:
			Group=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if GroupID==None: # Create a blank form
			result['GroupID'] = ''
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['Description'] = ''
			result['IsDeleted'] = False
		else:
			result['GroupID'] = GroupID
			result['DisplayName'] = '%s (%d) linked to %d items' % (Group.Name, GroupID, len(Group.CatalogItems))
			result['Name'] = Group.Name
			result['Description'] = Group.Description
			result['IsDeleted'] = Group.Status=='deleted'
		return result
		
	@expose()
	@validate(validators={'GroupID':validators.Int(),'Name':validators.String(),'Description':validators.String(),\
	'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def CatalogItemGroupsEditorSave(self, GroupID=None,Name='',Description='',Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		if GroupID!=None:
			try:
				Group = model.InvGrpStock.get(GroupID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('CatalogItemGroupsEditor')
		if Operation=='Save': # Either update or create a new entry
			if GroupID==None: # Create a new entry
				Group = model.InvGrpStock(Name=Name,Description=Description)
				GroupID = Group.id
				turbogears.flash('New Entry Created (id: %d)' % GroupID)
			else: # Update an entry
				Group.Name = str(Name)
				Group.Description = str(Description)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and GroupID!=None:
			# Just check to make sure no one is using the room at the time
			if len(Group.CatalogItems) > 0:
				# Mark the item deleted
				Group.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				Group.destroySelf()
				GroupID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and GroupID!=None:
			Group.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			GroupID=''
		else:
			turbogears.flash('Error in processing request')
		if GroupID in ['',None]:
			raise cherrypy.HTTPRedirect('CatalogItemGroupsEditor')
		else:
			raise cherrypy.HTTPRedirect('CatalogItemGroupsEditor?GroupID=%d' % GroupID)
		
	@expose(format='json')
	def CatalogItemGroupsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			groups = model.InvGrpStock.select(orderBy=[model.InvGrpStock.q.Name])
		else:
			groups = model.InvGrpStock.select(model.InvGrpStock.q.Name.contains(QuickSearchText),
				orderBy=[model.InvGrpStock.q.Name])
		results = []
		for item in groups:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)
		
	@expose(html='turbocare.templates.config_LocationGroupsEditor')
	@validate(validators={'GroupID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def LocationGroupsEditor(self, GroupID=None, **kw):
		'''	Either load an Location Groups for editing, or bring up an empty form for adding a new entry 
		'''
		if GroupID!=None: # attempt to load the record
			try:
				Group = model.InvGrpLocation.get(GroupID)
			except SQLObjectNotFound:
				turbogears.flash("The GroupID %d could not be found (deleted?)" % GroupID)
				Group=None
				GroupID=None
		else:
			Group=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if GroupID==None: # Create a blank form
			result['GroupID'] = ''
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['Description'] = ''
			result['IsDeleted'] = False
		else:
			result['GroupID'] = GroupID
			result['DisplayName'] = '%s (%d) linked to %d items' % (Group.Name, GroupID, len(Group.Locations))
			result['Name'] = Group.Name
			result['Description'] = Group.Description
			result['IsDeleted'] = Group.Status=='deleted'
		return result
		
	@expose()
	@validate(validators={'GroupID':validators.Int(),'Name':validators.String(),'Description':validators.String(),\
	'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def LocationGroupsEditorSave(self, GroupID=None,Name='',Description='',Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		if GroupID!=None:
			try:
				Group = model.InvGrpLocation.get(GroupID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('LocationGroupsEditor')
		if Operation=='Save': # Either update or create a new entry
			if GroupID==None: # Create a new entry
				Group = model.InvGrpLocation(Name=Name,Description=Description)
				GroupID = Group.id
				turbogears.flash('New Entry Created (id: %d)' % GroupID)
			else: # Update an entry
				Group.Name = str(Name)
				Group.Description = str(Description)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and GroupID!=None:
			# Just check to make sure no one is using the room at the time
			if len(Group.Locations) > 0:
				# Mark the item deleted
				Group.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				Group.destroySelf()
				GroupID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and GroupID!=None:
			Group.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			GroupID=''
		else:
			turbogears.flash('Error in processing request')
		if GroupID in ['',None]:
			raise cherrypy.HTTPRedirect('LocationGroupsEditor')
		else:
			raise cherrypy.HTTPRedirect('LocationGroupsEditor?GroupID=%d' % GroupID)
		
	@expose(format='json')
	def LocationGroupsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			groups = model.InvGrpLocation.select(orderBy=[model.InvGrpLocation.q.Name])
		else:
			groups = model.InvGrpLocation.select(model.InvGrpLocation.q.Name.contains(QuickSearchText),
				orderBy=[model.InvGrpLocation.q.Name])
		results = []
		for item in groups:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)
		
	@expose(html='turbocare.templates.config_CustomerGroupsEditor')
	@validate(validators={'GroupID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CustomerGroupsEditor(self, GroupID=None, **kw):
		'''	Either load an Customer Groups for editing, or bring up an empty form for adding a new entry 
		'''
		if GroupID!=None: # attempt to load the record
			try:
				Group = model.InvGrpCustomer.get(GroupID)
			except SQLObjectNotFound:
				turbogears.flash("The GroupID %d could not be found (deleted?)" % GroupID)
				Group=None
				GroupID=None
		else:
			Group=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if GroupID==None: # Create a blank form
			result['GroupID'] = ''
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['Description'] = ''
			result['IsDeleted'] = False
		else:
			result['GroupID'] = GroupID
			result['DisplayName'] = '%s (%d) linked to %d items' % (Group.Name, GroupID, len(Group.Customers))
			result['Name'] = Group.Name
			result['Description'] = Group.Description
			result['IsDeleted'] = Group.Status=='deleted'
		return result
		
	@expose()
	@validate(validators={'GroupID':validators.Int(),'Name':validators.String(),'Description':validators.String(),\
	'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def CustomerGroupsEditorSave(self, GroupID=None,Name='',Description='',Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		if GroupID!=None:
			try:
				Group = model.InvGrpCustomer.get(GroupID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('CustomerGroupsEditor')
		if Operation=='Save': # Either update or create a new entry
			if GroupID==None: # Create a new entry
				Group = model.InvGrpCustomer(Name=Name,Description=Description)
				GroupID = Group.id
				turbogears.flash('New Entry Created (id: %d)' % GroupID)
			else: # Update an entry
				Group.Name = str(Name)
				Group.Description = str(Description)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and GroupID!=None:
			# Just check to make sure no one is using the room at the time
			if len(Group.Customers) > 0:
				# Mark the item deleted
				Group.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				Group.destroySelf()
				GroupID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and GroupID!=None:
			Group.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			GroupID=''
		else:
			turbogears.flash('Error in processing request')
		if GroupID in ['',None]:
			raise cherrypy.HTTPRedirect('CustomerGroupsEditor')
		else:
			raise cherrypy.HTTPRedirect('CustomerGroupsEditor?GroupID=%d' % GroupID)
		
	@expose(format='json')
	def CustomerGroupsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			groups = model.InvGrpCustomer.select(orderBy=[model.InvGrpCustomer.q.Name])
		else:
			groups = model.InvGrpCustomer.select(model.InvGrpCustomer.q.Name.contains(QuickSearchText),
				orderBy=[model.InvGrpCustomer.q.Name])
		results = []
		for item in groups:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)

	@expose(html='turbocare.templates.config_VendorGroupsEditor')
	@validate(validators={'GroupID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def VendorGroupsEditor(self, GroupID=None, **kw):
		'''	Either load an Vendor Groups for editing, or bring up an empty form for adding a new entry 
		'''
		if GroupID!=None: # attempt to load the record
			try:
				Group = model.InvGrpVendor.get(GroupID)
			except SQLObjectNotFound:
				turbogears.flash("The GroupID %d could not be found (deleted?)" % GroupID)
				Group=None
				GroupID=None
		else:
			Group=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if GroupID==None: # Create a blank form
			result['GroupID'] = ''
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['Description'] = ''
			result['IsDeleted'] = False
		else:
			result['GroupID'] = GroupID
			result['DisplayName'] = '%s (%d) linked to %d items' % (Group.Name, GroupID, len(Group.Vendors))
			result['Name'] = Group.Name
			result['Description'] = Group.Description
			result['IsDeleted'] = Group.Status=='deleted'
		return result
		
	@expose()
	@validate(validators={'GroupID':validators.Int(),'Name':validators.String(),'Description':validators.String(),\
	'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def VendorGroupsEditorSave(self, GroupID=None,Name='',Description='',Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		if GroupID!=None:
			try:
				Group = model.InvGrpVendor.get(GroupID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('VendorGroupsEditor')
		if Operation=='Save': # Either update or create a new entry
			if GroupID==None: # Create a new entry
				Group = model.InvGrpVendor(Name=Name,Description=Description)
				GroupID = Group.id
				turbogears.flash('New Entry Created (id: %d)' % GroupID)
			else: # Update an entry
				Group.Name = str(Name)
				Group.Description = str(Description)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and GroupID!=None:
			# Just check to make sure no one is using the room at the time
			if len(Group.Vendors) > 0:
				# Mark the item deleted
				Group.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				Group.destroySelf()
				GroupID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and GroupID!=None:
			Group.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			GroupID=''
		else:
			turbogears.flash('Error in processing request')
		if GroupID in ['',None]:
			raise cherrypy.HTTPRedirect('VendorGroupsEditor')
		else:
			raise cherrypy.HTTPRedirect('VendorGroupsEditor?GroupID=%d' % GroupID)
		
	@expose(format='json')
	def VendorGroupsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			groups = model.InvGrpVendor.select(orderBy=[model.InvGrpVendor.q.Name])
		else:
			groups = model.InvGrpVendor.select(model.InvGrpVendor.q.Name.contains(QuickSearchText),
				orderBy=[model.InvGrpVendor.q.Name])
		results = []
		for item in groups:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)
		
	@expose(html='turbocare.templates.config_PackagingGroupsEditor')
	@validate(validators={'GroupID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def PackagingGroupsEditor(self, GroupID=None, **kw):
		'''	Either load an Packaging Groups for editing, or bring up an empty form for adding a new entry 
		'''
		if GroupID!=None: # attempt to load the record
			try:
				Group = model.InvGrpPackaging.get(GroupID)
			except SQLObjectNotFound:
				turbogears.flash("The GroupID %d could not be found (deleted?)" % GroupID)
				Group=None
				GroupID=None
		else:
			Group=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if GroupID==None: # Create a blank form
			result['GroupID'] = ''
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['Description'] = ''
			result['IsDeleted'] = False
		else:
			result['GroupID'] = GroupID
			result['DisplayName'] = '%s (%d) linked to %d items' % (Group.Name, GroupID, len(Group.Packagings))
			result['Name'] = Group.Name
			result['Description'] = Group.Description
			result['IsDeleted'] = Group.Status=='deleted'
		return result
		
	@expose()
	@validate(validators={'GroupID':validators.Int(),'Name':validators.String(),'Description':validators.String(),\
	'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PackagingGroupsEditorSave(self, GroupID=None,Name='',Description='',Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		if GroupID!=None:
			try:
				Group = model.InvGrpPackaging.get(GroupID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('PackagingGroupsEditor')
		if Operation=='Save': # Either update or create a new entry
			if GroupID==None: # Create a new entry
				Group = model.InvGrpPackaging(Name=Name,Description=Description)
				GroupID = Group.id
				turbogears.flash('New Entry Created (id: %d)' % GroupID)
			else: # Update an entry
				Group.Name = str(Name)
				Group.Description = str(Description)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and GroupID!=None:
			# Just check to make sure no one is using the room at the time
			if len(Group.Packagings) > 0:
				# Mark the item deleted
				Group.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				Group.destroySelf()
				GroupID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and GroupID!=None:
			Group.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			GroupID=''
		else:
			turbogears.flash('Error in processing request')
		if GroupID in ['',None]:
			raise cherrypy.HTTPRedirect('PackagingGroupsEditor')
		else:
			raise cherrypy.HTTPRedirect('PackagingGroupsEditor?GroupID=%d' % GroupID)
		
	@expose(format='json')
	def PackagingGroupsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			groups = model.InvGrpPackaging.select(orderBy=[model.InvGrpPackaging.q.Name])
		else:
			groups = model.InvGrpPackaging.select(model.InvGrpPackaging.q.Name.contains(QuickSearchText),
				orderBy=[model.InvGrpPackaging.q.Name])
		results = []
		for item in groups:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)
		
	@expose(html='turbocare.templates.config_CompoundGroupsEditor')
	@validate(validators={'GroupID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CompoundGroupsEditor(self, GroupID=None, **kw):
		'''	Either load an Compound Groups for editing, or bring up an empty form for adding a new entry 
		'''
		if GroupID!=None: # attempt to load the record
			try:
				Group = model.InvGrpCompound.get(GroupID)
			except SQLObjectNotFound:
				turbogears.flash("The GroupID %d could not be found (deleted?)" % GroupID)
				Group=None
				GroupID=None
		else:
			Group=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if GroupID==None: # Create a blank form
			result['GroupID'] = ''
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['Description'] = ''
			result['IsDeleted'] = False
		else:
			result['GroupID'] = GroupID
			result['DisplayName'] = '%s (%d) linked to %d items' % (Group.Name, GroupID, len(Group.Compounds))
			result['Name'] = Group.Name
			result['Description'] = Group.Description
			result['IsDeleted'] = Group.Status=='deleted'
		return result
		
	@expose()
	@validate(validators={'GroupID':validators.Int(),'Name':validators.String(),'Description':validators.String(),\
	'Operation':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def CompoundGroupsEditorSave(self, GroupID=None,Name='',Description='',Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		if GroupID!=None:
			try:
				Group = model.InvGrpCompound.get(GroupID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('CompoundGroupsEditor')
		if Operation=='Save': # Either update or create a new entry
			if GroupID==None: # Create a new entry
				Group = model.InvGrpCompound(Name=Name,Description=Description)
				GroupID = Group.id
				turbogears.flash('New Entry Created (id: %d)' % GroupID)
			else: # Update an entry
				Group.Name = str(Name)
				Group.Description = str(Description)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and GroupID!=None:
			# Just check to make sure no one is using the room at the time
			if len(Group.Compounds) > 0:
				# Mark the item deleted
				Group.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				Group.destroySelf()
				GroupID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and GroupID!=None:
			Group.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			GroupID=''
		else:
			turbogears.flash('Error in processing request')
		if GroupID in ['',None]:
			raise cherrypy.HTTPRedirect('CompoundGroupsEditor')
		else:
			raise cherrypy.HTTPRedirect('CompoundGroupsEditor?GroupID=%d' % GroupID)
		
	@expose(format='json')
	def CompoundGroupsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			groups = model.InvGrpCompound.select(orderBy=[model.InvGrpCompound.q.Name])
		else:
			groups = model.InvGrpCompound.select(model.InvGrpCompound.q.Name.contains(QuickSearchText),
				orderBy=[model.InvGrpCompound.q.Name])
		results = []
		for item in groups:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)
		
	@expose(html='turbocare.templates.config_PatientTypeEditor')
	@validate(validators={'PatientTypeID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def PatientTypeEditor(self, PatientTypeID=None, **kw):
		'''	Either load an patient type for editing, or bring up an empty form for adding a new entry 
		'''
		# Attempt to load our entry
		if PatientTypeID!=None: # attempt to load the record
			try:
				PatientType = model.ClassInsurance.get(PatientTypeID)
			except SQLObjectNotFound:
				turbogears.flash("The PatientTypeID %d could not be found (deleted?)" % PatientTypeID)
				PatientType=None
				PatientTypeID=None
		else:
			PatientType=None
		# Prepare our form
		result = {} # The dictionary we are sending to the web page
		if PatientTypeID==None: # Create a blank form
			result['PatientTypeID'] = ''
			result['DisplayName'] = 'New Entry'
			result['Name'] = ''
			result['ClassId'] = ''
			result['Description'] = ''
			result['IsDeleted'] = False
		else:
			result['PatientTypeID'] = PatientTypeID
			result['DisplayName'] = '%s (%d)' % (PatientType.Name, PatientTypeID)
			result['Name'] = PatientType.Name
			result['ClassId'] = PatientType.ClassId
			result['Description'] = PatientType.Description
			result['IsDeleted'] = PatientType.Status == 'deleted'
		return result
	
	@expose()
	@validate(validators={'PatientTypeID':validators.Int(),'Name':validators.String(),'ClassId':validators.String(),\
	'Description':validators.String()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PatientTypeEditorSave(self, PatientTypeID=None,Name='',ClassId='',Description='',Operation='', **kw):
		'''	Save changes.  Either create a new entry, update an existing entry or attempt to delete an entry 
			Save/Cancel/New/Delete are the various operations we have
		'''
		log.debug('PatientTypeEditorSave')
		if PatientTypeID!=None:
			try:
				PatientType = model.ClassInsurance.get(PatientTypeID)
			except SQLObjectNotFound: #, errorstr:
				turbogears.flash("There is an error on a database entry I thought should exist, but doesn't, so all the changes are lost.  Try again.")
				raise cherrypy.HTTPRedirect('PatientTypeEditor')
		if Operation=='Save': # Either update or create a new entry
			log.debug('...Save')
			if PatientTypeID==None: # Create a new entry
				log.debug('...New Entry')
				ClassId = ClassId.lower().replace(' ','_')
				PatientType = model.ClassInsurance(Name=Name,ClassId=ClassId,Description=Description, LdVar='')
				PatientTypeID = PatientType.id
				turbogears.flash('New Entry Created (id: %d)' % PatientTypeID)
			else: # Update an entry
				PatientType.Name = str(Name)
				PatientType.ClassId = str(ClassId.lower().replace(' ','_'))
				PatientType.Description = str(Description)
				turbogears.flash('Recorded Updated')
		elif Operation=='Delete' and PatientTypeID!=None:
			# Just check to make sure no one is using the room at the time
			if len(PatientType.Encounters) > 0:
				# Mark the item deleted
				PatientType.Status = 'deleted'
				turbogears.flash('Record Marked Deleted')
			else:
				PatientType.destroySelf()
				PatientTypeID = None
				turbogears.flash('Record Deleted')
		elif Operation=='Un-Delete' and PatientTypeID!=None:
			PatientType.Status = ''
			turbogears.flash('Record Un-Deleted')
		elif Operation=='Cancel':
			turbogears.flash('Updates Cancelled')
		elif Operation=='New':
			PatientTypeID=''
		else:
			turbogears.flash('Error in processing request')
		if PatientTypeID in ['',None]:
			raise cherrypy.HTTPRedirect('PatientTypeEditor')
		else:
			raise cherrypy.HTTPRedirect('PatientTypeEditor?PatientTypeID=%d' % PatientTypeID)
		
	@expose(format='json')
	def PatientTypeEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Search for an existing location entry '''
		QuickSearchText = str(QuickSearchText)
		if QuickSearchText=='*':
			PatientTypes = model.ClassInsurance.select(orderBy=[model.ClassInsurance.q.Name])
		else:
			PatientTypes = model.ClassInsurance.select(model.ClassInsurance.q.Name.contains(QuickSearchText),
			orderBy=[model.ClassInsurance.q.Name])
		results = []
		for item in PatientTypes:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)