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

class Configuration(controllers.RootController):
#===== Inventory App Stuff ====================================================
	@expose(html='turbocare.templates.configuration_menu')
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
				result['ParentDeptNrName'] = Department.ParentDeptNr.Name
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

	@expose()
	@validate(validators={'Name':validators.String(),'Block':validators.String(),'ZipCode':validators.String(),\
		'District':validators.String(),'State':validators.String(),'IsoCountryId':validators.String(),\
		'UneceModifier':validators.String(),'UneceLocode':validators.String(),'UneceLocodeType':validators.Int(),\
		'UneceCoordinates':validators.String(),'Operation':validators.String(),'AddressID':validators.Int()})
	@identity.require(identity.has_permission("admin_controllers_configuration"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def LocationsEditorSave(self, Name='', Block='', ZipCode='', District='', State='', IsoCountryId='',
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
	def LocationsEditorQuickSearch(self, QuickSearchText='', **kw):
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
		