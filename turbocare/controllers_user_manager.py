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
			
