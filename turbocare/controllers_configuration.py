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
			InvAddress = model.InvAddressCitytown.get(AddressID)
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
		
			
