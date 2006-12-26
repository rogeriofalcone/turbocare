import logging
import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model

@expose(format='json')
def Receipt(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvReceipt.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		TotalPayment_data = str(record.TotalPayment)
		TotalPaid_data = str(record.TotalPaid)
		TotalSelfPay_data = str(record.TotalSelfPay)
		SelfPayNotes_data = record.SelfPayNotes
		TotalInsurance_data = '%d' % record.TotalInsurance
		InsuranceNotes_data = record.InsuranceNotes
		#ForeignKeys
		try:
			Customer_data = record.Customer.id
			Customer_display = record.Customer.Name + ' ('+str(record.Customer.id)+')'
		except AttributeError: 
			Customer_data = ''
			Customer_display = 'None'
		#MultiJoin and RelatedJoin
		CatalogItems_data = 'There are ' + str(len(record.CatalogItems)) + ' records'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data=''
		TotalPayment_data = ''
		TotalPaid_data = ''
		TotalSelfPay_data = ''
		SelfPayNotes_data = ''
		TotalInsurance_data = ''
		InsuranceNotes_data = ''
		#ForeignKeys
		Customer_data = ''
		Customer_display = 'None'
		#MultiJoin and RelatedJoin
		CatalogItems_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		Name_data=''
		#ForeignKeys
		Customer_data = ''
		Customer_display = 'None'
		#MultiJoin and RelatedJoin
		CatalogItems_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	#MultiJoin and RelatedJoin
	Id = dict(id="re_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="re_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	TotalPayment = dict(id="re_TotalPayment", name="TotalPayment", label="Total payment", type="Currency",attr=dict(), data=TotalPayment_data)
	TotalPaid = dict(id="re_TotalPaid", name="TotalPaid", label="Total paid", type="Currency",attr=dict(), data=TotalPaid_data)
	TotalSelfPay = dict(id="re_TotalSelfPay", name="TotalSelfPay", label="Total self pay", type="Currency",attr=dict(), data=TotalSelfPay_data)
	SelfPayNotes = dict(id="re_SelfPayNotes", name="SelfPayNotes", label="Self pay notes", type="String",attr=dict(length=50), data=SelfPayNotes_data)
	TotalInsurance = dict(id="re_TotalInsurance", name="TotalInsurance", label="TotalInsurance", type="Currency",attr=dict(), data=TotalInsurance_data)
	InsuranceNotes = dict(id="re_InsuranceNotes", name="InsuranceNotes", label="Insurance notes", type="String",attr=dict(length=50), data=InsuranceNotes_data)
	#Accounting = dict(id="re_Accounting", name="Accounting", label="Accounting", type="String",attr=dict(length=50), data=Accounting_data)
	#ForeignKeys
	SrchName = dict(id="re_SrchName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Customer = dict(id="re_Customer", name="Customer", label="Customer", type="ForeignKey",attr=dict(srchUrl="CustomerSearch",lookupUrl="CustomerGet", edit_url='Customer', srchFields=[SrchName]), data=Customer_data, init_display=Customer_display)
	#MultiJoin
	CatalogItems = dict(id="re_CatalogItems", name="CatalogItems", label="Requested items", type="MultiJoin",attr=dict(displayUrl="ReceiptMultiJoinList",listUrl="ReceiptMultiJoinList",linkUrl="ReceiptItems"), data=CatalogItems_data)
	#Fields
	fields = [Id,Name, Customer, CatalogItems, TotalPayment, TotalPaid, TotalSelfPay, SelfPayNotes, TotalInsurance, \
		InsuranceNotes]
	#Configure any of the links that might need configuring
	if id == '':
		ReceiptMenu = 'ReceiptMenu'
	else:
		ReceiptMenu = 'ReceiptMenu?id=' + id
	#Just for searching
	#RETURN VALUES HERE
	return dict(id=id, Name='Receipt', Label='Receipt entry', Fields=fields, FieldsSrch=[Name], \
	Read='Receipt', Add='ReceiptSave', Del='ReceiptDel', UnDel='ReceiptUnDel', Edit='Receipt', \
	Save='ReceiptSave', SrchUrl='ReceiptSearch', MenuBar=ReceiptMenu)

@expose(format='json')
def ReceiptMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("Receipt")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("Receipt")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("Receipt")', menu=[\
			dict(label='Copy into new', url='javascript:inv.openObjForm("Receipt?id='+id+'&Op=CopyIntoNew")'),\
			dict(label='Add purchased items', url='ReceiptAddItems?id='+id)])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def ReceiptGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvReceipt.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		if record.Status == 'deleted':
			display = record.Customer.Name + ' ***MARKED DELETED*** paid Rs. ' + str(record.TotalPaid) + ' on ' + record.CreateTime.strftime('%Y-%m-%d')
		else:
			display = record.Customer.Name + ' paid Rs. ' + str(record.TotalPaid) + ' on ' + record.CreateTime.strftime('%Y-%m-%d')
		return dict(display=display, record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'TotalPayment':validators.Number(), 'TotalPaid':validators.Number(), 'TotalSelfPay':validators.Number(), 'SelfPayNotes':validators.String(), 'TotalInsurance':validators.Number(), 'InsuranceNotes':validators.String(),'Customer':validators.Int()})
def ReceiptSave(self, Customer, Id='', id='', Name='', TotalPayment=0, TotalPaid=0, TotalSelfPay=0, \
	SelfPayNotes='', TotalInsurance=0, InsuranceNotes='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvReceipt.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				if TotalPayment in [None, 'None', '']:
					TotalPayment = 0.0
				if TotalPaid in [None, 'None', '']:
					TotalPaid = 0.0
				if TotalSelfPay in [None, 'None', '']:
					TotalSelfPay = 0.0
				if TotalInsurance in [None, 'None', '']:
					TotalInsurance = 0.0
				#Updating the record
				record.Customer = Customer
				record.TotalPayment = TotalPayment
				record.TotalPaid = TotalPaid
				record.TotalSelfPay = TotalSelfPay
				record.SelfPayNotes = SelfPayNotes
				record.TotalInsurance = TotalInsurance
				record.InsuranceNotes = InsuranceNotes
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvReceipt(Customer = Customer, TotalPayment = TotalPayment, TotalPaid = TotalPaid, TotalSelfPay = TotalSelfPay, SelfPayNotes = SelfPayNotes, TotalInsurance = TotalInsurance, InsuranceNotes = InsuranceNotes, Status='')
			result_msg = "Record added"
			result = 1
		record_id = record.id
	except:
		result = 0
		result_msg="Operation failed!"
		record_id = ''
		raise
	return dict(result=result, result_msg=result_msg, id=record_id)
	
@expose(format='json')
def ReceiptDel(Id, id='', **kw):
	"""	If the Receipt has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvReceipt.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.CatalogItems)) == 0:
				record.destroySelf()
				result=1
				result_msg = "Record deleted"
			else:
				record.Status = 'deleted'
				result=1
				result_msg = "Record marked deleted"
		else:
			result=0
			result_msg="Couldn't find the record"
	except:
		result=0
		result_msg = "Failed to modify the record"
		raise
	return dict(result=result, result_msg=result_msg)
			
@expose(format='json')
def ReceiptUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvReceipt.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	if int_id > 0:
		#Check to see if the record can be completely deleted (ie. no references exist)
		if record.Status == 'deleted':
			record.Status = ''
			result=1
			result_msg = "Record un-deleted"				
		else:
			result=0
			result_msg = "Record is already active"
	else:
		result=0
		result_msg="Couldn't find the record"
	return dict(result=result, result_msg=result_msg)

@expose(format='json')
def ReceiptMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvReceipt.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	del_item_count = 0 #Count the number of items which are linked but deleted
	if int_id > 0:
		if (int_id > 0) and hasattr(record,ColName):
			col_items = getattr(record,ColName)
			records = []
			for item in col_items:
				if item.Status == 'deleted':
					del_item_count += 1
				else:
					if ColName == 'Items':
						line_text = item.StockItem.Name + ' Qty: ' + str(item.Quantity)
					elif ColName == 'CatalogItems':
						line_text = item.Name()
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def ReceiptSearch(self, Name='', CreateTime='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvCustomer.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvReceipt.q.CustomerID == model.InvCustomer.q.id,"
	if CreateTime != '':
		qArgs+="model.InvReceipt.q.CreateTime.contains('"+ CreateTime + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvReceipt.select(AND ('+qArgs[0:len(qArgs)-1]+'),orderBy=[-model.InvReceipt.q.ModifyTime])')
	else:
		items = model.InvReceipt.select(orderBy=[-model.InvReceipt.q.ModifyTime])
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Customer.Name+' *** MARKED DELETED *** Rs. ' + str(item.TotalPayment)
				results.append({'id':item.id, 'text':text, 'Name':item.Customer.Name+' *** MARKED DELETED ***', 'Description':str(item.TotalPayment)})
			else:
				text = item.Customer.Name+' Rs. ' + str(item.TotalPayment)
				results.append({'id':item.id, 'text':text, 'Name':item.Customer.Name, 'Description':str(item.TotalPayment)})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name, 'Description':str(item.TotalPayment)})
	return dict(results=results, field_num=field_num, items=items)

@expose(format='json')
def ReceiptGetLocationsForItem(self, CatalogItemID='', LocationID='', **kw):
	items = []
	if CatalogItemID != '':
		locations = model.InvStockLocation.select(AND (model.InvStockItem.q.CatalogItemID == int(CatalogItemID), \
			model.InvStockLocation.q.LocationID == int(LocationID), model.InvStockLocation.q.StockItemID == \
			model.InvStockItem.q.id, model.InvStockLocation.q.IsConsumed == False, model.InvLocation.q.IsStore == True \
			),distinct=True)
		for location in locations:
			if location.QtyAvailable() > 0:
				if location.StockItem.ExpireDate == None:
					items.append(dict(StockLocationID=location.id, Name=location.Location.Name, Description=location.Location.Description, \
						LocationQty=location.QtyAvailable(), Product=location.StockItem.Name, ExpireDate=''))
				else:
					items.append(dict(StockLocationID=location.id, Name=location.Location.Name, Description=location.Location.Description, \
						LocationQty=location.QtyAvailable(), Product=location.StockItem.Name, ExpireDate= \
						location.StockItem.ExpireDate.strftime('%Y-%m-%d')))
	return dict(items=items)

@expose()
def ReceiptAddNewItems(self, **kw):
	raise cherrypy.HTTPRedirect('StockTransferCreateNew')

@expose(html='care2x.templates.receiptadditems')
def ReceiptAddItems(self, Id='', id='', **kw):
	if Id!='':
		id=Id
	if id == '':
		next_link = "/inventory"
		error = "The link information is incomplete for adding receipt items."
		raise  cherrypy.HTTPRedirect('/inventory/ProgrammingError?error=%s&next_link=%s'% (error, next_link))			
	RequestedCatalogItems = []
	data = model.InvReceiptItems.select(model.InvReceiptItems.q.ReceiptID == int(id))
	for item in data:
		if not item.IsSatisfied():
			RequestedCatalogItems.append(dict(id=item.id, Name=item.Name(), CatalogItemID=item.CatalogItemID, \
				Quantity=item.Quantity, UnitCost=item.UnitCost, Discount = item.Discount))
	Locations = []
	records = model.InvLocation.select()
	for record in records:
		Locations.append(dict(id=record.id, Name=record.Name, Description=record.Description))
	return dict(Name='ReceiptAddItems', Label='Select items', RequestedCatalogItems=RequestedCatalogItems, \
		Locations	= Locations)

@expose()
def ReceiptAddItemsSave(self, TransferQty=[], CatalogItemID=[], ReceiptItemsID=[], Discount=[], \
	StockLocationID=[], IsPaid=[], counter=[], **kw):
	#Find out if there is a LocationID for the customer
	#Create a new stock location entry, mark it sold and consumed and link it to the receipt
	#Create a transfer record and record the movement of stock to the customer
	#Update the StockLocation entry
	#Update the ReceiptItems entry
	#Update the Receipt entry
	def MakeEntry(TransferQty, CatalogItemID, ReceiptItemsID, Discount, StockLocationID, IsPaid):
		receiptitem = model.InvReceiptItems.get(int(ReceiptItemsID))
		receipt = receiptitem.Receipt
		customer = receipt.Customer
		stocklocation = model.InvStockLocation.get(int(StockLocationID))
		#Figure out payment
		if IsPaid=='on':
			TotalPaid = float(TransferQty)*receiptitem.UnitCost - float(Discount)
		else:
			TotalPaid = 0.0
		# Get the new stock location
		if customer.InventoryLocationID != None:
			NewLocationID = customer.InventoryLocationID
		else:
			NewLocationID = stocklocation.LocationID
		# Create a stock location entry
		purchaseditem = model.InvStockLocation(StockItemID = stocklocation.StockItemID, LocationID = NewLocationID, \
			ReceiptID = receiptitem.id, TotalPaid = TotalPaid, Quantity = float(TransferQty), IsConsumed = True, IsSold = True)
		# Create stock transfer
		newtransfer = model.InvStockTransfer(FromStockLocationID = stocklocation.id, ToStockLocation = purchaseditem.id,\
			Qty = float(TransferQty), IsComplete = True)
		# Update old stock location
		stocklocation.Quantity = stocklocation.Quantity - float(TransferQty)
		# Update overall stock entry *****For now, rely on the QtyAvailable function
		#stocklocation.StockItem.Quantity = stocklocation.StockItem.Quantity - float(TransferQty)
		# Update receiptitems entry
		receiptitem.Discount = float(Discount)
	#log = logging.getLogger("care2x.controllers")
	#log.debug("!!!!!!!!! IsPaid variable: %s" % IsPaid)
	if len(counter) < 2:
		#log.debug("@@@@@@@@@@@@@@@@@@ SINGLE ENTRY")
		MakeEntry(TransferQty, CatalogItemID, ReceiptItemsID, Discount, StockLocationID, IsPaid)
		receiptitem = model.InvReceiptItems.get(int(ReceiptItemsID))
		receipt = receiptitem.Receipt
	else:
		#log.debug("@@@@@@@@@@@@@@@@@@ MULTI ENTRIES")
		for qty, catalogid, receiptitem, discount, stocklocation, paid in zip(TransferQty, CatalogItemID, ReceiptItemsID,\
				Discount, StockLocationID, IsPaid):
			MakeEntry(qty, catalogid, receiptitem, discount, stocklocation, paid)
		receiptitem = model.InvReceiptItems.get(int(ReceiptItemsID[0]))
		receipt = receiptitem.Receipt
	# Update Receipt entry
	receipt.TotalPayment = receipt.TotalPaymentCalc()
	receipt.TotalPaid = receipt.TotalPaidCalc()
	raise cherrypy.HTTPRedirect('/inventory/StockTransferCreateNew')