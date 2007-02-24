import logging
import sys
import simplejson
import pprint
import cherrypy
import datetime
from sqlobject import *
from sqlobject.sqlbuilder import Alias
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears import exception_handler
from turbogears.toolbox.catwalk import CatWalk 
import model
from model import DATE_FORMAT
import model_inventory
import inventory_catalogitem
from printer_inventory import *

log = logging.getLogger("turbocare.controllers")

class Dispensing(controllers.RootController):
	
	LocationID = '' # The particular dispensing counter where the person is located
	LocationName = ''
	
	def __init__(self, LocationID):
		'''	Initialize the dispensing counter to a location id which acts as a filter
		'''
		self.LocationID = LocationID
		self.LocationName = model.InvLocation.get(LocationID).Name
	
	@expose(html='turbocare.templates.dispensing')
	@identity.require(identity.has_permission("dispensing_view"))
	def index(self, CustomerID='', **kw):
		return dict(title='%s dispensing' % self.LocationName, customer_id=CustomerID)
	
	@expose(html='turbocare.templates.programmingerror')
	def idFail(error):
		error= "Not Permited to do operation"
		log.debug(error)
		next_link = "/billing/"
		return dict(error_message = error, next_link=next_link)

	@expose(html='turbocare.templates.programmingerror')
	def ProgrammingError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		return dict(error_message = error, next_link=next_link)

	@expose(html='turbocare.templates.dataentryerror')
	def DataEntryError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		return dict(error_message = error, next_link=next_link)
	
	#Loads receipt data
	def LoadReceiptData(self, barcode='', ReceiptID=None):
		'''	Loads the receipt data for a paid receipt (out-patient) or an un-paid receipt for in-patient
		'''
		# We have two options for loading data, a receipt id or a barcode for the customer id.  Receipt id will take precedence.
		# In the end, our goal is to load the customer information
		log.debug('CustomerID: %s' % barcode)
		try:
			CustomerID = None
			if not (ReceiptID in [None, 'None', 'null', '']):
				log.debug('LOADING... using ReceiptID %s' % ReceiptID)
				record = model.InvReceipt.get(ReceiptID).Customer
				CustomerID = record.id
			else:
				try:
					CustomerID = int(barcode)
					record = model.InvCustomer.get(CustomerID)
				except (ValueError, SQLObjectNotFound): #Normally happens with an empty barcode
					#Return an empty record with a 'NAME NOT FOUND' title
					log.debug("Customer doesn't exist... returning mostly empty results.")
					return dict(customerid=None, paid_items=[], unpaid_items=[], \
						customer_name='CUSTOMER DOES NOT EXIST!',encounter={})
			CustomerName = record.Name
		except:
			raise
			log.debug('Barcode: %s (%d), ReceiptID: %s' % (barcode, CustomerID, str(ReceiptID)))
			for line in sys.exc_info():
				log.debug('Message: %s' % str(line))
			return dict(customerid=None, paid_items=[], unpaid_items=[], customer_name='CUSTOMER DOES NOT EXIST!',\
				encounter={})
		#Load the Patient data and retreive the latest financial information and patient status
		try:
			record_encounter = model.Encounter.get(model.Person.get(record.ExternalID).GetLatestEncounter())
			EncounterDate = record_encounter.EncounterDate 
			InsuranceType = record_encounter.InsuranceClassNr.ClassId #class_id.  e.g. self_pay, private, charity, hospital, common (state run for everyone in the state)
			InsuranceName = record_encounter.InsuranceClassNr.Name #name
			if InsuranceType != 'self_pay':
				try:
					record_firm = model.InsuranceFirm.get(record_encounter.InsuranceFirmId)
					InsuranceFirm = 'Firm: %s' % record_firm.Name #People who provide insurance, not valid with self pay
					InsuranceNumber = 'Number: %s' % record_encounter.InsuranceNr #Policy Number
				except (SQLObjectNotFound, AssertionError):
					record_firm = None
					InsuranceFirm = 'Unknown insurance firm: Probably a registration ERROR'
					InsuranceNumber = 'Unknown insurance number: Check registration!!'
			else:
				InsuranceFirm = 'Firm: None (self pay)'
				InsuranceNumber = 'Number: None (self pay)'
			# In/out patient information
			EncounterClass = record_encounter.EncounterClassNr.Name
			EncounterClassID = record_encounter.EncounterClassNr.ClassId
			# If in-patient, then check the is-discharged
			if EncounterClassID == 'inpatient':
				IsDischarged = record_encounter.IsDischarged
				if IsDischarged:
					DischargeDateTime = record_encounter.DischargeDate.strftime(DATE_FORMAT) + ' ' + \
						record_encounter.DischargeTime
				else:
					DischargeDateTime = ''
			else:
				IsDischarged = False
				DischargeDateTime = ''
			Encounter = dict(type=InsuranceType, name=InsuranceName, firm=InsuranceFirm, number=InsuranceNumber,\
				encounter_class=EncounterClass, encounter_class_id = EncounterClassID, is_discharged=IsDischarged, \
				discharge_datetime=DischargeDateTime)
		except:
			log.debug("Could not get encounter information.")
			raise
			Encounter = {}
		#
		#	We need to go through all the receipt items for the customer and pick the ones which are:
		#		Paid for and not dispensed
		#	If the patient is an in-patient, then we'll also show items which are not paid for (and not dispensed)
		#
		ReceiptItemsPaid = [] # for all patients
		ReceiptItemsUnpaid = [] # for inpatients, they get this as well as the above list
		for receipt in record.Receipts: # Go through all the receipts
			if (not receipt.IsDispensed()) and receipt.IsPaidFor():
				for item in receipt.CatalogItems:
					#log.debug('Item %s is from location ids %s' % (item.ShortName(), reduce(lambda x,y: x+','+y, item.FromLocationIDList())))
					if (not item.IsDispensed()) and (item.IsPaid()) and (self.LocationID in item.FromLocationIDList()):
						# Get the quantity from the transfer record
						Quantity = 0
						StockItemID = None
						for stocklocation in item.StockItems:
							for transfer in stocklocation.TransfersToHere:
								if transfer.FromStockLocation.LocationID == self.LocationID:
									#record the last stock item id... normally there is only one from one location
									StockItemID = stocklocation.StockItemID
									BatchNumber = stocklocation.StockItem.BatchNumber
									if BatchNumber == None:
										BatchNumber = ''
									Quantity+=transfer.Qty
						ReceiptItemsPaid.append(dict(receiptitem_id=item.id,name=item.ShortName(), quantity=Quantity, \
							stockitem_id=StockItemID, batch_number=BatchNumber))
			elif (EncounterClassID == 'inpatient') and (not receipt.IsDispensed()):
				for item in receipt.CatalogItems:
					if (not item.IsDispensed()) and (self.LocationID in item.FromLocationIDList()):
						# Get the quantity from the transfer record
						Quantity = 0
						for stocklocation in item.StockItems:
							for transfer in stocklocation.TransfersToHere:
								if transfer.FromStockLocation.LocationID == self.LocationID:
									#record the last stock item id... normally there is only one from one location
									StockItemID = stocklocation.StockItemID
									BatchNumber = stocklocation.StockItem.BatchNumber
									if BatchNumber == None:
										BatchNumber = ''
									Quantity+=transfer.Qty
						ReceiptItemsUnpaid.append(dict(receiptitem_id=item.id,name=item.ShortName(), quantity=Quantity,\
							stockitem_id=StockItemID, batch_number=BatchNumber))
		#log.debug("Returing the customer information.")
		return dict(customerid=CustomerID, paid_items=ReceiptItemsPaid, unpaid_items=ReceiptItemsUnpaid, \
			customer_name=CustomerName, encounter=Encounter)
			
	@expose(format='json')
	@validate(validators={'barcode':validators.String(),'ReceiptID':validators.Int()})	
	@identity.require(identity.has_permission("dispensing_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def LoadPatient(self, barcode='', **kw):
		log.debug('Loading Patinet data...')
		return self.LoadReceiptData(barcode=barcode)
				
	#
	#	Update a single receipt item line's transfer information
	#
	
	def UpdateReceiptItemTransfer(self, ReceiptItemId):
		"""	Save/Update a receipt item's transfer information and mark item as transferred
		"""
		log.debug('...Updating transfer record for receipt item %d' % int(ReceiptItemId))
		receipt_item = model.InvReceiptItems.get(ReceiptItemId)
		for stocklocation in receipt_item.StockItems:
			for transfer in stocklocation.TransfersToHere:
				if not transfer.IsComplete:
					transfer.DateTransferred = datetime.datetime.now()
					transfer.IsComplete = True
					transfer.FromStockLocation.Quantity -= transfer.Qty
					transfer.ToStockLocation.Quantity += transfer.Qty

	@expose(format='json')
	@identity.require(identity.has_permission("dispensing_dispense"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def SaveReceiptItems(self, ReceiptItemId=[], Counter=[], CustomerID='', **kw):
		'''	Update receipt items, setting their transfer to complete.
		'''
		if len(Counter) > 1:
			log.debug("SAVING... more than one entry: %d entries" % len(Counter))
			for receiptitem_id in ReceiptItemId:
				self.UpdateReceiptItemTransfer(receiptitem_id)
		elif len(Counter) == 1:
			log.debug("SAVING... only one entry")
			self.UpdateReceiptItemTransfer(ReceiptItemId)
		return self.LoadReceiptData(barcode=CustomerID)
		
	#	AJSON action to retreive the List of customers coming to this location
	@expose(format='json')
	@identity.require(identity.has_permission("dispensing_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")

	def GetListOfCustomers(self, **kw):
		'''	Find all un-completed transfers which will come from this location and list
			Customer information and billing information related to it.
		'''
		# CustomerItems dictionary
		log.debug('Get pending items list for location %s (%d)...' % (self.LocationName, self.LocationID))
		CustomerItems = {}
		# Get the ReceiptItems
		alias = Alias(model.InvStockLocation, "inv_stock_location_alias")
		transfers = model.InvStockTransfer.select(AND (model.InvStockTransfer.q.IsComplete == False,
			model.InvStockTransfer.q.FromStockLocationID == model.InvStockLocation.q.id, model.InvStockLocation.q.LocationID ==
			self.LocationID, model.InvStockTransfer.q.ToStockLocationID == alias.q.id, alias.q.ReceiptID != None))
		for transfer in transfers:
			ReceiptItemID = transfer.ToStockLocation.ReceiptID # it really is the receipt item id
			receiptitem = model.InvReceiptItems.get(ReceiptItemID)
			CustomerID = receiptitem.Receipt.CustomerID
			if CustomerItems.has_key(CustomerID):
				CustomerItems[CustomerID].append(dict(name=receiptitem.ShortName(), paid=receiptitem.IsPaid(),\
					datetime=receiptitem.CreateTime))
			else:
				CustomerItems[CustomerID] = [dict(name=receiptitem.ShortName(), paid=receiptitem.IsPaid(), \
					datetime=receiptitem.CreateTime)]
		# Get some customer information
		CustomerInfo = {}
		for customerid in CustomerItems.keys():
			customer = model.InvCustomer.get(customerid)
			encounter = model.Encounter.get(model.Person.get(customer.ExternalID).GetLatestEncounter())
			EncounterDate = encounter.EncounterDate 
			# In/out patient information
			EncounterClass = encounter.EncounterClassNr.Name
			EncounterClassID = encounter.EncounterClassNr.ClassId
			# If in-patient, then check the is-discharged
			if EncounterClassID == 'inpatient':
				IsDischarged = encounter.IsDischarged
				if IsDischarged:
					DischargeDateTime = encounter.DischargeDate.strftime(DATE_FORMAT) + ' ' + \
						encounter.DischargeTime
				else:
					DischargeDateTime = ''
			else:
				IsDischarged = False
				DischargeDateTime = ''
			PatientInfo = dict(name=customer.Name, encounter_class=EncounterClass, encounter_classid = \
				EncounterClassID, is_discharged=IsDischarged, discharge_datetime=DischargeDateTime)
			CustomerInfo[customerid] = PatientInfo
		# Sort the Customer Keys
		keys = [(CustomerItems[x][0]['datetime'],x) for x in CustomerItems.keys()]
		keys.sort()
		CustomerKeys = [x[1] for x in keys]
		#log.debug('There are %d pending items' % len(CustomerItems.keys()))
		return dict(customer_ids=CustomerKeys, customer_items=CustomerItems, customer_info=CustomerInfo)
