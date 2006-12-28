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
from turbogears.toolbox.catwalk import CatWalk 
import model
from model import DATE_FORMAT
import model_inventory
import inventory_catalogitem
from printer_inventory import *

log = logging.getLogger("turbocare.controllers")

class Billing(controllers.RootController):
#===== Inventory App Stuff ====================================================
	@expose(html='turbocare.templates.billing')
	def index(self, customer_id='', receipt_id='', **kw):
		return dict(customer_id=customer_id,receipt_id=receipt_id, title="Billing")

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
		if next_link == '':
			next_link = "/billing/"
		return dict(error_message = error, next_link=next_link)

	@expose(html='turbocare.templates.dataentryerror')
	def DataEntryError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		if next_link == '':
			next_link = "/billing/"
		return dict(error_message = error, next_link=next_link)
	
	#Loads a patient.  We use this a number of places
	def LoadPatientData(self, barcode='', ReceiptID=None):
		#We have two options for loading data, a receipt id or a barcode for the customer id.  Receipt id will take precedence.
		log.debug('CustomerID: %s, ReceiptID: %s' % (barcode, ReceiptID))
		try:
			CustomerID = 0
			if not (ReceiptID in [None, 'None', 'null', '']):
				log.debug('LOADING... using ReceiptID %s' % ReceiptID)
				record_rcpt = model.InvReceipt.get(ReceiptID)
				record = record_rcpt.Customer
				CustomerID = record.id
			else:
				try:
					CustomerID = int(barcode)
					record = model.InvCustomer.get(CustomerID)
				except (ValueError, SQLObjectNotFound): #Normally happens with an empty barcode
					#Return an empty record with a 'NAME NOT FOUND' title
					return dict(customerid=None, receiptid=None, receipt_status='(no data found)', \
						receipt_items=[], receipt_history=[], customer_name='CUSTOMER DOES NOT EXIST!', \
						financial={}, encounterid=None)
				PurchaseDate, ReceiptID = record.MostRecentReceipt()
				if ReceiptID != None:
					record_rcpt = model.InvReceipt.get(ReceiptID)
			CustomerName = record.Name
			if ReceiptID == None:
				Financial = dict(type='unknown', name='Unknown', firm=None, number=None)
				return dict(customerid=CustomerID, receiptid=None, receipt_status='No Receipts', \
					receipt_items=[], receipt_history=[], customer_name=CustomerName, \
					financial=Financial, encounterid=None)
			#Current receipt status
			ReceiptStatus = record_rcpt.StatusText()
		except:
			raise
			log.debug('Barcode: %s (%d), ReceiptID: %s' % (barcode, CustomerID, str(ReceiptID)))
			for line in sys.exc_info():
				log.debug('Message: %s' % str(line))
			raise cherrypy.HTTPRedirect('ProgrammingError?next_link=billing&error="%s %s"' %
				("Bad barcode: ",sys.exc_info()[0]))
		#Load Receipt History
		ReceiptHistory = []
		receipt_history = [(x.CreateTime,x.TotalPaidCalc(),x.TotalPaymentCalc(),len(x.CatalogItems),x.Name(),x.id) \
			for x in record.Receipts]
		receipt_history.sort()
		receipt_history.reverse()
		for item in receipt_history:
			try:
				description = "%d items purchased on %s.  Rs. %d of Rs. %d paid" % (item[3],
					item[0].strftime(DATE_FORMAT), item[1], item[2])
			except AttributeError:
				description = item[4]		
			ReceiptHistory.append(dict(description=description, receiptid=item[5]))
		#Load the Patient data and retreive the latest financial information
		try:
			#some initial records had receipt not tied to Encounters, so we'll fix that here if we need to.
			if record_rcpt.ExternalId == None:
				record_encounter = model.Encounter.get(model.Person.get(record.ExternalID).GetLatestEncounter(record_rcpt.CreateTime))
				record_rcpt.ExternalId = record_encounter.id
			else:
				record_encounter = model.Encounter.get(record_rcpt.ExternalId)
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
			# Calculate the balance owing (for all receipts)
			BalanceOwing = record.CalcBalance()
			if BalanceOwing > 0:
				Balance = 'Customer owes: Rs. %d' % BalanceOwing
			else:
				Balance = 'Customer credit: Rs. %d' % -BalanceOwing
			# Set a flag indicating if the current Balance includes the current receipt
			IsCurrReceiptInBalance = not (record.CalcBalance() == record.CalcBalance(record_rcpt.id))
			# Calculate the balance paid on the current receipt
			CurrReceiptPaid = record_rcpt.TotalPaidCalc()
			# Calculate the total billed (all receipts)
			AllReceipts = 'Total billed: Rs. %d' % record.CalcPayment()
			# Calculate the total paid
			AllPayments = 'Total payments: Rs. %d' % record.CalcPaymentsMade()
			Financial = dict(type=InsuranceType, name=InsuranceName, firm=InsuranceFirm, number=InsuranceNumber,\
				balance=Balance, balance_amt=BalanceOwing, curr_receipt_paid=CurrReceiptPaid, all_receipts=\
				AllReceipts, all_payments=AllPayments, is_curr_receipt_in_balance=IsCurrReceiptInBalance)
		except:
			raise
			raise cherrypy.HTTPRedirect('ProgrammingError?next_link=billing&error="Could not retrieve \
				patient financial information: "+%s' % sys.exc_info()[0])
		#If the receipt is un-assigned, ie. none of the items are have a stock location, then we have to choose
		#potential candidates.  Where assignments are obvious, make the assignment, but mark the stocklocation
		#as not being paid.
		ReceiptItems = [] #We return this to the javascript program
		StockLocationsList = [] #Array of stock locations
		#Figure out the most popular stock location for non-services
		for item in record_rcpt.CatalogItems:
			if (not item.CatalogItem.IsService) and (len(item.StockItems)==0):
				StockItemID = item.CatalogItem.NextStockItemID()
				if not (StockItemID in [None, '', 'None']):
					record_stockitem = model.InvStockItem.get(StockItemID)
					StockLocationsList += [x.id for x in record_stockitem.Locations]					
		StockLocations = dict([(x, StockLocationsList.count(x)) for x in StockLocationsList])
		#Create our dictionary for the javascript program
		for item in record_rcpt.CatalogItems:
			LocationOptions = {}
			UnitPrice = 0
			LocationName = 'Item Not Available!' #Assign this just in case
			LocationID = None
			Total = 0
			#Stock location options for the particular catalog item
			StockItemID = item.CatalogItem.NextStockItemID()
			if StockItemID != None:
				record_stock = model.InvStockItem.get(StockItemID)
				LocationOptions = dict([(x.id, x.Name()) for x in record_stock.AvailableStockLocations()])
				UnitPrice = record_stock.SalePrice
			if len(item.StockItems) == 0: #This means the item is not assigned and we should do that now
				if (StockItemID != None) and (len(LocationOptions)>0):
					description = record_stock.Name
					if item.CatalogItem.IsService: #For services, assign the first location, options for others
						LocationName = LocationOptions[LocationOptions.keys()[0]]
					else: #Find the first location which matches the maximum count (i.e., the preferred location)
						tmpStockLocations = dict([(x, StockLocations[x]) for x in LocationOptions])
						LocationName = LocationOptions[tmpStockLocations.keys()[tmpStockLocations.values().index(max([tmpStockLocations[x] for x in set(LocationOptions)]))]]
				else:
					description = item.CatalogItem.Name + ' (NOT IN STOCK)'
				if item.Status == '':
					ReceiptItems.append(dict(receiptitemid=item.id, description=description, qty=item.Quantity,\
						locationname=LocationName, locationoptions=LocationOptions, unitprice=UnitPrice,
						catalogitemid=item.CatalogItemID, stocklocationid='', ismodified='true'))
			else: #The item is assigned so we don't need to set a default
				description = item.CatalogItem.Name
				if item.Status == '':
					for stocklocation in item.StockItems:
						#Get the location where it's from based on the stock transfer (can be multiple locations)
						LocationName = stocklocation.FromName()
						ReceiptItems.append(dict(receiptitemid=item.id, description=description, qty=item.Quantity,\
							locationname=LocationName, locationoptions=LocationOptions, unitprice=UnitPrice,
							catalogitemid=item.CatalogItemID, stocklocationid=stocklocation.id, ismodified='false'))
		return dict(customerid=CustomerID, receiptid=ReceiptID, receipt_status=ReceiptStatus, \
			receipt_items=ReceiptItems, receipt_history=ReceiptHistory, customer_name=CustomerName, \
			financial=Financial, encounterid=record_encounter.id)	
			
	@expose(format='json')
	@validate(validators={'barcode':validators.String(),'ReceiptID':validators.Int()})	
	def LoadPatient(self, barcode='', ReceiptID=None, **kw):
		return self.LoadPatientData(barcode=barcode, ReceiptID=ReceiptID)
	
	def GetDefaultCustomerLocationID(self):
		'''	When moving inventory to a location where it's sold, we need to mark the new location as the customer
			location.  Most customers should have a location already defined, but we need
			a default just in case
		'''
		items = model.InvLocation.select(model.InvLocation.Name.contains('Customer'))
		if len(items) > 0:
			return items[0].id
		else:
			return None
	
	def UndoStockTransfers(self, StockLocationID):
		'''	Remove all stock transfers from a stock location
			Update all locations where we got stock from and cancel
			the transfers.
			
			Completed transfers will not be removed!!!!!
		'''
		del_list = []
		record = model.InvStockLocation.get(StockLocationID)
		for transfer in record.TransfersToHere:
			if not transfer.IsComplete:
				log.debug('UNDO STOCK TRANSFER: returning stock to original location')
				transfer.Status = 'deleted'
				del_list.append(transfer.id)
		for id in del_list:
			log.debug('UNDO STOCK TRANSFER: deleting stock transfer record')
			transfer = model.InvStockTransfer.get(id)
			transfer.destroySelf()
	#
	#	Auto transfer check
	#
	
	def AutoTransferReceiptItems(self, ReceiptID):
		'''	Go through the receipt items and check to see if the item is
			an automatic transfer item, that is, the item is marked as a non-
			dispensable item (ie. it cannot be dispensed) so we need to
			transfer it automatically.  Registration and bed assignment are
			examples of such items.  NOTE: dispensing for automatic items
			should only happen AFTER payment.  If the item is not paid for
			then make sure it is not marked dispensed
		'''
		log.debug('AutoTransferReceiptItems');
		receipt = model.InvReceipt.get(ReceiptID)
		for item in receipt.CatalogItems:
			if item.IsPaid() and (not item.CatalogItem.IsDispensable):
				#find all transfers (normally just one) and mark them complete
				for stocklocation in item.StockItems:
					for transfer in stocklocation.TransfersToHere:
						if not transfer.IsComplete:
							transfer.IsComplete = True
							transfer.DateTransferred = model.cur_date_time()
							transfer.FromStockLocation.Quantity -= transfer.Qty
							transfer.ToStockLocation.Quantity += transfer.Qty
							log.debug('....Auto dispensing item %d' % item.id)
			elif (not item.IsPaid()) and (not item.CatalogItem.IsDispensable):
				#find all transfers (normally just one) and mark them not complete
				for stocklocation in item.StockItems:
					for transfer in stocklocation.TransfersToHere:
						if transfer.IsComplete:
							transfer.FromStockLocation.Quantity += transfer.Qty
							transfer.ToStockLocation.Quantity -= transfer.Qty
							transfer.IsComplete = False
						log.debug('....Marking not dispensed item %d' % item.id)
				
	#
	#	Save a single receipt item line
	#
	
	def SaveReceiptItem(self, CusomterId, ReceiptId=None, ReceiptItemId=None, CatalogItemId=None,\
		Qty=0, StockLocationId=None, StockLocationIDset=None, EncounterId=None):
		"""	Save/Update a receipt item
		"""
		log.debug('...Saving receipt item...')
		log.debug('...CustomerID: %s, ReceiptId=%s, ReceiptItemId=%s, CatalogItemId=%s,\
			Qty=%s, StockLocationId=%s, StockLocationIDset=%s, EncounterId=%s' % (CusomterId, \
			ReceiptId, ReceiptItemId, CatalogItemId, Qty, 	StockLocationId, StockLocationIDset, EncounterId)) 
		if ReceiptId == None:
			#Make a new receipt entry
			record_rcpt = model.InvReceipt(CustomerID=CustomerId, ExternalId=EncounterId)
			ReceiptId = record_rcpt.id
		else: #load the receipt
			record_rcpt = model.InvReceipt.get(ReceiptId)
		if ReceiptItemId in [None, 'None', 'null', 'Null', '']:
			#The receipt item isn't created yet
			log.debug('....the receipt item does not exist')
			#Check if the catalog item is in the current receipt so we can attempt to merge this line
			ReceiptItemId = record_rcpt.ContainsCatalogItemID(CatalogItemId)
			# If the ReceiptItem uses a different stock item, then we'll create a separate receipt item anyway
			if (ReceiptItemId != None) and (StockLocationId != None):
				record_rcpt_item = model.InvReceiptItems.get(ReceiptItemId)
				if not (StockLocationId in record_rcpt_item.StockLocationIDs()):
					log.debug('....attempted to find a matching catalog item but failed')
					ReceiptItemId = None
			if ReceiptItemId == None:
				#This is a new catalog item, so we Add it to the receipt
				log.debug('....creating a new Receipt Item')
				record_rcpt_item = model.InvReceiptItems(ReceiptID=ReceiptId, CatalogItemID=CatalogItemId, Quantity=Qty)
				ReceiptItemId = record_rcpt_item.id
				#Add the stock item
				if StockLocationId != None:
					#First check that we have enough stock before transferring
					record_stck_location = model.InvStockLocation.get(StockLocationId)
					if record_stck_location.QtyAvailable() > Qty:
						if record_rcpt.Customer.InventoryLocationID == None:
							LocationID = self.GetDefaultCustomerLocationID()
						else:
							LocationID = record_rcpt.Customer.InventoryLocationID 
						#Create a new entry for the stock location NOTE: The destination location isn't updated with the quantity until the transfer completes
						record_new_stocklocation = model.InvStockLocation(StockItem=record_stck_location.StockItemID, \
							LocationID=LocationID, ReceiptID=ReceipItemtId, Quantity=0.0, IsConsumed=True, IsSold=True)
						#Create the stock transfer
						record_stck_transfer = model.InvStockTransfer(FromStockLocationID=StockLocationId, \
							ToStockLocation=record_new_stocklocation.id, Qty=Qty)
						# Do not deduct quantity until transfer completed
						# ** record_stck_location.Quantity -= Qty
						#Update the unit price
						record_rcpt_item.UnitCost = record_stck_location.StockItem.SalePrice
						#Check if the catalog item is dispensable, if it isn't, then mark it transferred already
						# CHANGE NOTE: this transfer happens using the "AutoTransferReceiptItems" function
						# and only after payment is made
						#if not record_stck_location.StockItem.CatalogItem.IsDispensable:
						#	record_stck_transfer.IsComplete = True
						#	record_stck_transfer.DateTransferred = model.cur_date_time()
						#	log.debug('....Completing transfer')
						log.debug('....created stock transfer for new receipt')
					else:
						log.debug('....NOT ENOUGH STOCK FOR TRANSFER for new receipt!!')
				ReceiptItemId = record_rcpt_item.id
			else:
				#merge this new entry with the existing item assuming that more is wanted
				log.debug('....merging new receipt item with previous item')
				record_rcpt_item = model.InvReceiptItems.get(ReceiptItemId)
				record_rcpt_item.Qutantity += Qty
				#Add the stock item
				#First check that we have enough stock before transferring
				record_stck_location = model.InvStockLocation.get(StockLocationId)
				if record_stck_location.QtyAvailable() > Qty:
					if record_rcpt.Customer.InventoryLocationID == None:
						LocationID = self.GetDefaultCustomerLocationID()
					else:
						LocationID = record_rcpt.Customer.InventoryLocationID 
					#check for an existing stock location to move the stock to
					if len(record_rcpt_item.StockItems) > 0:
						log.debug('....moving stock to an existing location')
						record_new_stocklocation = record_rcpt_item.StockItems[0]
						# Stock isn't updated until the transfer is complete
						# ** record_new_stocklocation.Quantity += Qty
					else:
						#Create a new entry for the stock location NOTE: Stock quantity is updated after the transfer is complete
						log.debug('....moving stock to a new location')
						record_new_stocklocation = model.InvStockLocation(StockItem=record_stck_location.StockItemID, \
							LocationID=LocationID, ReceiptID=ReceipItemtId, Quantity=0.0, IsConsumed=True, IsSold=True)
					#Create the stock transfer
					record_stck_transfer = model.InvStockTransfer(FromStockLocationID=StockLocationId, \
						ToStockLocation=record_new_stocklocation.id, Qty=Qty)
					# Removed the next line because stock quantities are updated after the transfer completes
					# ** record_stck_location.Quantity -= Qty
					#Update unit price (shouldn't have to do this, but I'll do it anyway) 
					record_rcpt_item.UnitCost = record_stck_location.StockItem.SalePrice
					#Check if the catalog item is dispensable, if it isn't, then mark it transferred already
					# CHANGE NOTE: this transfer happens using the "AutoTransferReceiptItems" function
					# and only after payment is made
					#if not record_stck_location.StockItem.CatalogItem.IsDispensable:
					#	record_stck_transfer.IsComplete = True
					#	record_stck_transfer.DateTransferred = model.cur_date_time()
					#	log.debug('....Completing transfer')
					log.debug('....transfer of additional stock for merged record completed')
				else:
					log.debug('....NOT ENOUGH STOCK FOR TRANSFER for merging receipt!!')
		else:
			log.debug('....Check/Update the receipt item')
			#Check/Update the receipt item
			record_rcpt_item = model.InvReceiptItems.get(ReceiptItemId)
			#If the receipt Item is finished (i.e. already transferred) then no editing allowed!!
			if not record_rcpt_item.IsFinished():
				#Update/verify stock location
				if not (StockLocationIDset in [None,'None','null','Null', '']): #We already had a transfer configured, so we need to check it
					log.debug('....modifying a pre-defined StockLocationID')
					record_stck_location = model.InvStockLocation.get(StockLocationIDset)
					if not record_stck_location.NoPendingTransfers(): #only allow changing of stock location if the transfer is not complete
						log.debug('....Updating the quantity on the receipt item, from %d to %d' % (record_rcpt_item.Quantity, Qty))
						record_rcpt_item.Quantity = Qty
						if not (StockLocationId in record_stck_location.FromLocationID()):
							#We are attempting to change the location from where we're getting the stock
							#Undo all previous transfers to the StockLocation
							log.debug('....un-doing stock transfer')
							self.UndoStockTransfers(record_stck_location.id)
							#Create the stock transfer
							log.debug('....creating the replacement stock transfer')
							record_stck_transfer = model.InvStockTransfer(FromStockLocationID=StockLocationId, \
								ToStockLocation=record_stck_location.id, Qty=Qty)
							record_from_stck_location = model.InvStockLocation.get(StockLocationId)
							#Update the unit price
							record_rcpt_item.UnitCost = record_from_stck_location.StockItem.SalePrice
							#Check if the catalog item is dispensable, if it isn't, then mark it transferred already
							# CHANGE NOTE: this transfer happens using the "AutoTransferReceiptItems" function
							# and only after payment is made
							#if not record_from_stck_location.StockItem.CatalogItem.IsDispensable:
							#	record_stck_transfer.IsComplete = True
							#	record_stck_transfer.DateTransferred = model.cur_date_time()
							#	log.debug('....Completing transfer')
							log.debug('....replacement transfer complete')
						else: #We are only changing the quantity from where we got the original stock
							#One of the stock transfers (usually just one) is updated
							log.debug('....changing the quantity which we originally transferred')
							for stocktransfer in record_stck_location.TransfersToHere:
								if stocktransfer.FromStockLocationID == StockLocationId:
									log.debug('....modifying the stock transfer to the new amount')
									stocktransfer.Qty = Qty
					else:
						log.debug('....the stock is already transferred.  I can\'t update')
				elif StockLocationId != None: #we didn't have assigned stock before, but now it's assigned
					log.debug('....Updating the quantity on the receipt item, from %d to %d' % (record_rcpt_item.Quantity, Qty))
					record_rcpt_item.Quantity = Qty
					#First check that we have enough stock before transferring
					record_stck_location = model.InvStockLocation.get(StockLocationId)
					log.debug('....no pre-defined stock location')
					log.debug('....adding a new StockLocationID. Name: %s, Amount: %s' % \
						(record_stck_location.Name(), Qty))
					if record_stck_location.QtyAvailable() > float(Qty):
						if record_rcpt.Customer.InventoryLocationID == None:
							LocationID = self.GetDefaultCustomerLocationID()
						else:
							LocationID = record_rcpt.Customer.InventoryLocationID 
						#check for an existing stock location to move the stock to
						if len(record_rcpt_item.StockItems) > 0:
							log.debug('......there is an existing destination stock location')
							record_new_stocklocation = record_rcpt_item.StockItems[0]
						else:
							log.debug('......creating a new dest. stock location.')
							#Create a new entry for the stock location
							record_new_stocklocation = model.InvStockLocation(StockItemID=record_stck_location.StockItemID, \
								LocationID=LocationID, ReceiptID=ReceiptItemId, Quantity=0.0, IsConsumed=True, IsSold=True)
						#Create the stock transfer
						log.debug('......creating a new stock transfer')
						record_stck_transfer = model.InvStockTransfer(FromStockLocationID=StockLocationId, \
							ToStockLocation=record_new_stocklocation.id, Qty=Qty)
						#Update the unit price
						record_rcpt_item.UnitCost = record_stck_location.StockItem.SalePrice
						# CHANGE NOTE: this transfer happens using the "AutoTransferReceiptItems" function
						# and only after payment is made
						#if not record_stck_location.StockItem.CatalogItem.IsDispensable:
						#	record_stck_transfer.IsComplete = True
						#	record_stck_transfer.DateTransferred = model.cur_date_time()
						#	log.debug('....Completing transfer')
						log.debug('....updating receipt item by adding a stock transfer complete (no previously assigned stock transfer)')
					else:
						log.debug('....NOT ENOUGH STOCK FOR TRANSFER for updating receipt with no assigned stock location!!')
			else:
				log.debug('....Cannot update item (%d) since it is finished' % record_rcpt_item.id)

	
	@expose(format='json')
	@identity.require(identity.has_permission("bill_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def SaveReceipt(self, CustomerId=[], ReceiptId=[], ReceiptItemId=[], CatalogItemId=[], Qty=[], StockLocationId=[],\
		Counter=[], EncounterId=[], StockLocationIDset=[], IsModified=[], **kw):
		'''	Save the Receipt form to the database, adding and updating as needed.
			The only operation we don't perform is deleting receipt items
			Returns: a reloaded version of the receipt
		'''
		if len(Counter) > 1:
			log.debug("SAVING... more than one entry: %d, %d, %d,%d, %d, %d,%d, %d, %d,%d" % \
				(len(CustomerId), len(ReceiptId), len(ReceiptItemId), len(CatalogItemId), len(Qty), \
				len(StockLocationId), len(Counter), len(EncounterId), len(StockLocationIDset), len(IsModified)))
			ReceiptID = ReceiptId[0]
			for cusomter_id, receipt_id, receipt_item_id, catalog_item_id, qty, stock_location_id, encounter_id, \
				stock_location_id_set, is_modified in zip(CustomerId, ReceiptId, ReceiptItemId, CatalogItemId, \
				Qty, StockLocationId, EncounterId, StockLocationIDset, IsModified):
				log.debug('... IsModfied: %s' % is_modified)
				if is_modified == 'true':
					try:
						stock_location_id_set = int(stock_location_id_set)
					except ValueError:
						stock_location_id_set = None
					self.SaveReceiptItem(int(cusomter_id), int(receipt_id), int(receipt_item_id), int(catalog_item_id),\
						float(qty), int(stock_location_id), stock_location_id_set, int(encounter_id))
			#Update the receipt total
			log.debug('SAVE RECEIPT: Update the receipt total payment')
			record = model.InvReceipt.get(ReceiptID)
			record.TotalPayment = record.TotalPaymentCalc()
		elif len(Counter) == 1:
			log.debug("SAVING... only one entry")
			ReceiptID = ReceiptId
			try:
				StockLocationIDset = int(StockLocationIDset)
			except ValueError:
				StockLocationIDset = None
			self.SaveReceiptItem(int(CustomerId), int(ReceiptId), int(ReceiptItemId), int(CatalogItemId), \
				float(Qty), int(StockLocationId), StockLocationIDset, int(EncounterId))
			#Update the receipt total
			log.debug('SAVE RECEIPT: Update the receipt total payment')
			record = model.InvReceipt.get(ReceiptID)
			record.TotalPayment = record.TotalPaymentCalc()
		else:
			ReceiptID = None
		# if the receipt has been paid (at least in part) mark items for Auto transfer
		if ReceiptID != None and record.TotalPaidCalc() > 0:
			self.AutoTransferReceiptItems(record.id)
		return self.LoadPatientData(ReceiptID=ReceiptID)
	
	@identity.require(identity.has_permission( "bill_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def IsSelfPay(self, ReceiptID):
		'''	Return true if the customer is self-pay '''
		receipt = model.InvReceipt.get(ReceiptID)
		if receipt.ExternalId == None:
			encounter = model.Encounter.get(model.Person.get(receipt.Customer.ExternalID).GetLatestEncounter(receipt.CreateTime))
			receipt.ExternalId = encounter.id
		else:
			encounter = model.Encounter.get(receipt.ExternalId)
		InsuranceType = encounter.InsuranceClassNr.ClassId #class_id.  e.g. self_pay, private, charity, hospital, common (state run for everyone in the state)
		if InsuranceType == 'self_pay':
			return True
		else:
			return False
		
	@expose(format='json')
	@identity.require(identity.has_permission("bill_pay"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	@validate(validators={'CashNotes':validators.String(),'InsrNotes':validators.String(),'CashAmt':validators.Number(),\
	'InsrAmt':validators.Number(), 'TotalCashAmt':validators.Number(),'ReceiptID':validators.Int()})	
	def MakeReceiptPayment(self, ReceiptID, TotalCashAmt=0, CashAmt=0, CashNotes='', InsrAmt=0, InsrNotes='', **kw):
		'''	Go through all the receipt items in the receipt and mark the items
			as paid for.  Create a new payment record (marking the date and 
			amount when money was exchanged).
		'''
		log.debug('MakeReceiptPayment')
		try:
			record = model.InvReceipt.get(ReceiptID)
		except (ValueError, SQLObjectNotFound): #happens when the conversion fails or the record is not found
			return dict(flash='No record to make payment for')
		# Make our payment record
		if TotalCashAmt !=0:
			payment = model.InvCustomerPayment(CustomerID=record.CustomerID, DatePaid=model.cur_date_time(),\
				Amount=TotalCashAmt,Notes=CashNotes)
		# Figure out how much money the customer has for spending - without including the current receipt amount
		CurrCredit = -record.Customer.CalcBalance(DoNotIncludReceiptID=ReceiptID)
		log.debug('....Current credit: %d' % CurrCredit)
		# Make sure no one is trying to cheat the program by forcing an Insurance payment
		if self.IsSelfPay(ReceiptID) and InsrAmt > 0:
			CashAmt += InsrAmt
			InsrAmt = 0
		# Go through and confirm the unit cost again
		for item in record.CatalogItems:
			item.UnitCost = item.StockItems[0].StockItem.SalePrice
		# Apply the payment to our Receipt and linked items
		record.TotalPayment = record.TotalPaymentCalc()
		NewAmt = CurrCredit + InsrAmt # This is what we have to spend
		record.TotalPaid += NewAmt
		# Cap the total paid to the payment required
		if record.TotalPaid > record.TotalPayment:
			record.TotalPaid = record.TotalPayment
		log.debug('....Money to spend: %d' % record.TotalPaid)
		# The TotalAmt is what we have for making payments on our stock location items
		TotalAmt = record.TotalPaid
		record.TotalSelfPay = CashAmt # Shows how much of the bill is Cash amount
		record.SelfPayNotes = CashNotes
		record.TotalInsurance = InsrAmt # How much of this bill is paid by insurance
		record.InsuranceNotes = InsrNotes
		# Update payments on the stock items for accounting and dispensing
		for item in record.CatalogItems:
			if (not item.IsPaid()) and (not item.IsDispensed()):#Don't change items which are paid for or dispensed
				log.debug('....Updating payments on stock location')
				PartPay = round(item.Quantity * item.UnitCost) - item.TotalPaid()
				if PartPay > 0: #We need to apply new payments to our stock (as much as we have money for)
					if PartPay > TotalAmt:
						PartPay = TotalAmt
						TotalAmt = 0
						log.debug('....Too little money')
					else:
						TotalAmt -= PartPay
					for stocklocation in item.StockItems:
						stockpaid = round(stocklocation.QtyAfterTransfers() * stocklocation.StockItem.SalePrice) - stocklocation.TotalPaid
						log.debug('....StockLocation %d with Rs. %d' % (stocklocation.id,stockpaid))
						if stockpaid > 0: # We still have more to pay
							if stockpaid > PartPay:
								stockpaid = PartPay
								PartPay = 0
								log.debug('....Too little rupees')
							else:
								PartPay -= stockpaid
							stocklocation.TotalPaid += round(stockpaid)
						elif stockpaid < 0: # we have reduced stock from this transfer
							PartPay -= stockpaid
							stocklocation.TotalPaid = round(stocklocation.QtyAfterTransfers() * stocklocation.StockItem.SalePrice)
				else: #We've reduced amounts and are actually refunding money at this point.  Fix our payment records
					TotalAmt -= PartPay
					# Go through all the stock items and adjust the TotalPaid.  Don't worry about keeping track
					# since we've reduced cost
					for stocklocation in item.StockItems:
						stocklocation.TotalPaid = round(stocklocation.QtyAfterTransfers() * stocklocation.StockItem.SalePrice)
			else:
				TotalAmt -= item.TotalPaid()
		# For auto-transfer items, transfer them after payment
		self.AutoTransferReceiptItems(ReceiptID)
		return self.LoadPatientData(ReceiptID=ReceiptID)

	@expose(format='json')
	@identity.require(identity.has_permission("bill_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def DeleteReceiptItem(self, ReceiptItemID, **kw):
		'''	Delete a specific receipt item from a receipt
			It won't delete any completed items or items for which a payment has been made
		'''
		record = model.InvReceiptItems.get(ReceiptItemID)
		ReceiptID = record.ReceiptID
		if not record.IsFinished():
			#Undo the stock transfer
			for stocklocation in record.StockItems:
				self.UndoStockTransfers(stocklocation.id)
			# Delete stock locations (normally just one stock location per receipt item)
			stock_location_ids = [x.id for x in record.StockItems]
			for item in stock_location_ids:
				record_stck_location = model.InvStockLocation.get(item)
				record_stck_location.destroySelf()
			record.destroySelf()
		receipt = model.InvReceipt.get(ReceiptID)
		receipt.TotalPayment = receipt.TotalPaymentCalc()
		return self.LoadPatientData(ReceiptID=ReceiptID)

	#
	#	Functions for adding a New Receipt
	#
	
	#	Step 1: Generate the Javascript data for choosing our catalog items
	#		Id or id is the CustomerID
	#		If ReceiptID is left blank, then a new Bill will be made
	@expose(format='json')
	@identity.require(identity.has_permission("bill_create"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CustomerAddReceipt(self, Id='', id='', ReceiptID='', data='', **kw):
		result_msg = ""
		if Id !='':
			id=Id
		Quantity = dict(id="c_Quantity", name="Quantity", label="Quantity", type="Numeric", attr=dict(length=10), data='0')
		Discount = dict(id="c_Discount", name="Discount", label="Discount", type="Numeric", attr=dict(length=10), data='')
		UnitCost = dict(id="c_UnitCost", name="UnitCost", label="Unit cost", type="StringRO", attr=dict(length=10), data='')
		#Search variables
		Name = dict(id="c_Name", name="Name", label="Name", type="String",attr=dict(length=25), data='')
		IsSelectable = dict(id="c_IsSelectable", name="IsSelectable", label="IsSelectable", type="Hidden", attr=dict(length=10), data='true')
		IsForSale = dict(id="c_IsForSale", name="IsForSale", label="IsForSale", type="Hidden", attr=dict(length=10), data='true')
		InvGrpStockNames = []
		for item in model.InvGrpStock.select():
			InvGrpStockNames.append(item.Name)
		SrchCatalogGroups = dict(id="c_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect",\
			attr=dict(Groups=InvGrpStockNames), data='')
		return dict(id=id, Name='CustomerAddReceipt', Label='Create a receipt', \
			FieldsSrch=[Name, SrchCatalogGroups,IsSelectable,IsForSale], Inputs=[Quantity], SrchUrl='CatalogItemSearch', \
			DataUrl='', Url='CustomerSaveReceipt', \
			UrlVars='id=%s&ReceiptID=%s' % (id, ReceiptID), result_msg=result_msg, SrchNow=False, NoAjax=True)
	
	#	Step 2: Save the items.  If no receipt is given, then create a new receipt.
	@expose()
	@identity.require(identity.has_permission( "bill_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CustomerSaveReceipt(self, Id='', id='', ReceiptID='', data='', **kw):
		result_msg = ''
		if Id !='':
			id = Id
		if data!='' and id!='':
			log.debug('CustomerID: %s' % id)
			log.debug('ReceiptID: %s' % ReceiptID)
			try:
				if id in [None, '', 'None', 'null']:
					raise ValueError
				CustomerID = int(id)
			except ValueError: #In most cases, this should come up because a customer id was not selected
				raise cherrypy.HTTPRedirect('ProgrammingError?error=%s&next_link=%s' % \
				("You'll need to select a customer first (bad customer id - couldn't convert)", '/billing'))
			data = simplejson.loads(data)
			if ReceiptID  in [None, '', 'None', 'null']:
				#Create a new receipt entry
				receipt = model.InvReceipt(CustomerID = CustomerID, TotalPayment = 0.0, TotalPaid = 0.0, TotalSelfPay = 0.0,\
					TotalInsurance = 0.0)
				totalcost = 0.0
				ReceiptID = receipt.id
			else:
				#Load the existing receipt
				receipt = model.InvReceipt.get(ReceiptID)
				totalcost = receipt.TotalPayment
				ReceiptID = receipt.id
			for item in data:
				try:
					Quantity = float(item['Quantity'])
				except ValueError:
					Quantity = 0
				try:
					CatalogItemID = int(item['id'])
				except:
					raise
				new_item = model.InvReceiptItems(ReceiptID=ReceiptID, CatalogItemID=CatalogItemID, Quantity=Quantity)
				totalcost += new_item.UnitCost*Quantity
			receipt.TotalPayment = totalcost
		raise cherrypy.HTTPRedirect('ReceiptItemsLoad?ReceiptID=%s' % ReceiptID)
		
	#	Step 3: Load the data so that the receipt items can be assigned to a particular stock location
	@identity.require(identity.has_permission( "bill_edit"))
	@expose(html='turbocare.templates.billing_receiptitemsadd')
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def ReceiptItemsLoad(self, ReceiptID, **kw):
		ReceiptItems = []
		try:
			receipt = model.InvReceipt.get(ReceiptID)
		except ValueError: #In most cases, this should come up because a customer id was not selected
			raise cherrypy.HTTPRedirect('ProgrammingError?error=%s&next_link=%s' % \
			("You'll need to select a customer first (bad receipt id - couldn't convert)", 'billing'))		
		for item in receipt.CatalogItems:
			if len(item.StockItems) == 0:
				ReceiptItems.append(dict(id=item.id, ReceiptID=ReceiptID, Name=item.Name(), Quantity=item.Quantity))
		return dict(Name='ReceiptItemsLoad', Label='Receipt items add', Items=ReceiptItems, BtnPickText='Select Location')
	
	#	Step 4: Save the Receipt items with their updated stock locations, then redirect back to the billing screen.
	#	This page just saves data and then redirects the user to the next appropriate page.
	@expose()
	@identity.require(identity.has_permission( "bill_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def FinalItemsCreateNewSave(self, ItemID=[], ReceiptID=[], Counter=[], ItemOptionID=[], Quantity=[], **kw):
		if len(Counter) > 1:
			#Get Location info
			receipt = model.InvReceipt.get(ReceiptID[0])
			LocationID = receipt.Customer.InventoryLocationID
			if LocationID == None:
				LocationID = self.GetDefaultCustomerLocationID()
			for receiptitem_id, receipt_id, stocklocation_id, quantity in zip(ItemID, ReceiptID,\
				ItemOptionID, Quantity):
				#Try converting our values
				try:
					receiptitem_id = int(receiptitem_id)
					receipt_id = int(receipt_id)
					stocklocation_id = int(stocklocation_id)
					quantity = float(quantity)
				except:
					raise
				# Get the stock location we want to transfer from
				stocklocation = model.InvStockLocation.get(stocklocation_id)
				# Create a new stock location for the customer
				new_stocklocation = model.InvStockLocation(StockItemID=stocklocation.StockItemID, LocationID=LocationID,\
					ReceiptID=receiptitem_id, Quantity=0.0, IsConsumed=True, IsSold=True)
				# Create a transfer record
				record_stck_transfer = model.InvStockTransfer(FromStockLocationID=stocklocation.id, \
					ToStockLocation=new_stocklocation.id, Qty=quantity)
				#Update the unit price
				receipt_item = model.InvReceiptItems.get(receiptitem_id)
				receipt_item.UnitCost = stocklocation.StockItem.SalePrice
			ReceiptID = receipt_id
		elif len(Counter) == 1:
			#Try converting our values
			try:
				ItemID = int(ItemID) # Receipt item id
				ReceiptID = int(ReceiptID) # Receipt id
				ItemOptionID = int(ItemOptionID) # Stock location id
				Quantity = float(Quantity) #... quantity, well duh!
			except:
				raise
			#Get Location info
			receipt = model.InvReceipt.get(ReceiptID)
			LocationID = receipt.Customer.InventoryLocationID
			if LocationID == None:
				LocationID = self.GetDefaultCustomerLocationID()
			# Get the stock location we want to transfer from
			stocklocation = model.InvStockLocation.get(ItemOptionID)
			# Create a new stock location for the customer
			new_stocklocation = model.InvStockLocation(StockItemID=stocklocation.StockItemID, LocationID=LocationID,\
				ReceiptID=ItemID, Quantity=0.0, IsConsumed=True, IsSold=True)
			# Create a transfer record
			record_stck_transfer = model.InvStockTransfer(FromStockLocationID=stocklocation.id, \
				ToStockLocation=new_stocklocation.id, Qty=Quantity)
			#Update the unit price
			receipt_item = model.InvReceiptItems.get(ItemID)
			receipt_item.UnitCost = stocklocation.StockItem.SalePrice
			#Update total payment on the receipt
			receipt.TotalPayment = receipt.TotalPaymentCalc()
		raise cherrypy.HTTPRedirect('index?receipt_id=%d' % ReceiptID)
		return False
		
	#	AJSON action to retreive the ItemOptions, also known as the Stock locations
	@expose(format='json')
	@identity.require(identity.has_permission( "bill_edit"))	
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")

	def GetItemOptions(self, ItemId, **kw):
		#Get the ReceiptItem
		receiptitem = model.InvReceiptItems.get(ItemId)
		#Get the stock item
		StockItemID = receiptitem.CatalogItem.NextStockItemID()
		stockitem = model.InvStockItem.get(StockItemID)
		#Return our list of stock locations
		ItemOptions = []
		for location in stockitem.Locations:
			if location.Location.CanSell:
				try:
					ExpireDate = location.StockItem.ExpireDate.strftime(DATE_FORMAT)
				except:
					ExpireDate = 'No Expire Date'
				ItemOptions.append(dict(id=location.id, Name=location.Name(), UnitPrice=location.StockItem.SalePrice, \
					ExpireDate=ExpireDate, Status=location.Status))
		return dict(items=ItemOptions)
		
	@expose(format='json')
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def BillingPrintReceipt(self, ReceiptID, **kw):
		'''	Calls the PrintReceipt function in "printer_inventory.py" and passes it the receipt id to print
		'''
		return dict(result_msg=PrintReceipt(ReceiptID,cherrypy.request.remoteAddr))

	#Map billing back to the index
	billing = index
	#
	#	External stuff
	#
	CatalogItemSearch = inventory_catalogitem.CatalogItemSearch
	
	#
	#	COMMENTS
	#
	# TESTED:
	#	1. When I have a receipt with un-assigned stock locations, it will add new stock locations
	#	2. When I have a receipt whose transfer is not complete, It will update quantity changes
	#
	# TO TEST:
	#	1. Reject modifications to a completed receipt
	#	2. Adding A new bill
	#	3. Appending new items to a bill
	#	4. Changing the location of an assigned receipt item