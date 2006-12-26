import logging
from datetime import datetime, date
import simplejson
import time
import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model

@expose(format='json')
def PurchaseOrder(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvPurchaseOrder.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Notes_data = record.Notes
		POSentOnDate_data = record.POSentOnDate
		ExpectedDeliveryDate_data = record.ExpectedDeliveryDate
		#ForeignKeys
		try:
			Vendor_data = record.Vendor.id
			Vendor_display = record.Vendor.Name + ' ('+str(record.Vendor.id)+')'
		except AttributeError: 
			Vendor_data = ''
			Vendor_display = 'None'
		#MultiJoin and RelatedJoin
		Items_data = 'There are ' + str(len(record.Items)) + ' records'
		GoodsReceived_data = 'There are ' + str(len(record.GoodsReceived)) + ' records'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Notes_data = ''
		POSentOnDate_data = ''
		ExpectedDeliveryDate_data = ''
		#ForeignKeys
		Vendor_data = ''
		Vendor_display = 'None'
		#MultiJoin and RelatedJoin
		Items_data = 'There are no records'
		GoodsReceived_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#MultiJoin and RelatedJoin
		Items_data = 'There are no records'
		GoodsReceived_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="po_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="po_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	POSentOnDate = dict(id="po_POSentOnDate", name="POSentOnDate", label="PO sent on", type="DateTime",attr=dict(), data=POSentOnDate_data)
	ExpectedDeliveryDate = dict(id="po_ExpectedDeliveryDate", name="ExpectedDeliveryDate", label="Expected delivery date", type="DateTime",attr=dict(), data=ExpectedDeliveryDate_data)
	Notes = dict(id="po_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	#ForeignKeys
	SrchVendorName = dict(id="po_SrchVendorName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Vendor = dict(id="po_Vendor", name="Vendor", label="Vendor", type="ForeignKey",attr=dict(srchUrl="VendorSearch",lookupUrl="VendorGet", edit_url='Vendor', srchFields=[SrchVendorName]), data=Vendor_data, init_display=Vendor_display)
	#MultiJoin
	Items = dict(id="po_Items", name="Items", label="Items", type="MultiJoin",attr=dict(displayUrl="PurchaseOrderMultiJoinList",listUrl="PurchaseOrderMultiJoinList",linkUrl="POItems"), data=Items_data)
	GoodsReceived = dict(id="po_GoodsReceived", name="GoodsReceived", label="Goods received", type="MultiJoin",attr=dict(displayUrl="PurchaseOrderMultiJoinList",listUrl="PurchaseOrderMultiJoinList",linkUrl="GoodsReceived"), data=GoodsReceived_data)
	#Fields
	fields = [Id, Name, POSentOnDate, ExpectedDeliveryDate, Notes, Vendor, GoodsReceived, Items]
	#Configure any of the links that might need configuring
	if id == '':
		PurchaseOrderMenu = 'PurchaseOrderMenu'
	else:
		PurchaseOrderMenu = 'PurchaseOrderMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='PurchaseOrder', Label='Purchase order entry', Fields=fields, FieldsSrch=[Name], Read='PurchaseOrder', Add='PurchaseOrderSave', Del='PurchaseOrderDel', UnDel='PurchaseOrderUnDel', Edit='PurchaseOrder', Save='PurchaseOrderSave', SrchUrl='PurchaseOrderSearch', MenuBar=PurchaseOrderMenu)

@expose(format='json')
def PurchaseOrderMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("PurchaseOrder")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("PurchaseOrder")'), dict(label='New POs', url='javascript:inv.openPickList("PurchaseOrderCreateNewStep1")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("PurchaseOrder")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("PurchaseOrder?id='+id+'&Op=CopyIntoNew")'), dict(label='Make goods received', url='javascript:inv.openPickList("PurchaseOrderAddGoodsReceived?id='+id+'")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def PurchaseOrderGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPurchaseOrder.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'POSentOnDate':validators.String(), 'ExpectedDeliveryDate':validators.String(), 'Notes':validators.String(), 'Vendor':validators.Int()})
def PurchaseOrderSave(self, Vendor, Id='', id='', POSentOnDate='', ExpectedDeliveryDate='', Notes='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPurchaseOrder.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if POSentOnDate != '':
		if len(POSentOnDate) > 10:
			POSentOnDate = datetime.fromtimestamp(time.mktime(time.strptime(POSentOnDate[0:10],'%Y-%m-%d')))
		else:
			POSentOnDate = datetime.fromtimestamp(time.mktime(time.strptime(POSentOnDate,'%Y-%m-%d')))
	if ExpectedDeliveryDate != '':
		if len(ExpectedDeliveryDate) > 10:
			ExpectedDeliveryDate = datetime.fromtimestamp(time.mktime(time.strptime(ExpectedDeliveryDate,'%Y-%m-%d %H:%M')))
		else:
			ExpectedDeliveryDate = datetime.fromtimestamp(time.mktime(time.strptime(ExpectedDeliveryDate,'%Y-%m-%d')))
		
	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				#Updating the record
				record.ExpectedDeliveryDate = ExpectedDeliveryDate
				record.POSentOnDate = POSentOnDate
				record.Notes = Notes
				record.Vendor = Vendor
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvPurchaseOrder(ExpectedDeliveryDate=ExpectedDeliveryDate, Vendor=Vendor, Notes=Notes, POSentOnDate=POSentOnDate, Status='')
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
def PurchaseOrderDel(Id, id='', **kw):
	"""	If the PurchaseOrder has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPurchaseOrder.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.GoodsReceived) + len(record.Items)) == 0:
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
def PurchaseOrderUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPurchaseOrder.get(int_id)
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
def PurchaseOrderMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvPurchaseOrder.get(int_id)
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
						line_text = item.CatalogItem.Name + ': ' +str(item.QuantityReceived)+ ' of ' +str(item.QuantityRequested)+ ' received at Rs. ' + str(item.ActualPrice)
					elif ColName == 'GoodsReceived':
						line_text = str(len(item.StockItems)) + ' items received on ' + item.DateReceived.strftime('%Y-%m-%d')
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def PurchaseOrderSearch(self, Name='', VendorName='', POSentOnDate='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.Vendor.q.Name.contains('"+ Name + "'),"
	if VendorName != '':
		qArgs+="model.Vendor.q.Name.contains('"+ VendorName + "'),"
	if POSentOnDate != '':
		qArgs+="model.InvPurchaseOrder.q.POSentOnDate.contains('"+ POSentOnDate + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvPurchaseOrder.select(AND ('+qArgs[0:len(qArgs)-1]+'),orderBy=[-model.InvPurchaseOrder.q.POSentOnDate])')
	else:
		items = model.InvPurchaseOrder.select(orderBy=[-model.InvPurchaseOrder.q.POSentOnDate])
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Name()
				results.append({'id':item.id, 'text':text, 'Name':item.Name(), 'Description':''})
			else:
				text = item.Name()
				results.append({'id':item.id, 'text':text, 'Name':item.Name(), 'Description':''})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name(), 'Description':''})
	return dict(results=results, field_num=field_num, items=items)
	
@expose(format='json')
def PurchaseOrderCreateNewStep1(self, data='', **kw):
	if data != '':
		raise cherrypy.HTTPRedirect('PurchaseOrderCreateNewStep2?data='+data)
	result_msg = ''
	id=''
	Name = dict(id="qri_Name", name="Name", label="Name", type="String", attr=dict(length=25), data='')
	IsSelectable = dict(id="qri_IsSelectable", name="IsSelectable", label="IsSelectable", type="Hidden", attr=dict(length=25), data='true')
	InvGrpStockNames = []
	for item in model.InvGrpStock.select():
		InvGrpStockNames.append(item.Name)
	SrchCatalogGroups = dict(id="po_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect", attr=dict(Groups=InvGrpStockNames), data='')
	return dict(id=id, Name='PurchaseOrderCreateNewStep1', Label='Select items from catalog',\
		FieldsSrch=[Name, SrchCatalogGroups,IsSelectable], Inputs=[], SrchUrl='CatalogItemSearch', \
		DataUrl='', Url='PurchaseOrderCreateNewStep1', UrlVars='', result_msg=result_msg, \
		SrchNow=False, NoAjax=True)

@expose(format='json')
@validate(validators={'CatalogItemId':validators.Int()})
def PurchaseOrderGetVendorsForItem(self, CatalogItemId=None, **kw):
	items = []
	if CatalogItemId != None:
		vendors = model.InvVendor.select(AND (model.InvQuote.q.VendorID == model.InvVendor.q.id, model.InvQuoteItems.q.QuoteID == model.InvQuote.q.id, model.InvQuoteItems.q.CatalogItemID == model.InvCatalogItem.q.id, model.InvCatalogItem.q.id == int(CatalogItemId)),distinct=True)
		for vendor in vendors:
			quote_items = model.InvQuoteItems.select(AND (model.InvQuoteItems.q.CatalogItemID == int(CatalogItemId), model.InvQuoteItems.q.QuoteID == model.InvQuote.q.id, model.InvQuote.q.VendorID == vendor.id),orderBy=-model.InvQuote.q.ValidOn)
			quote_item = quote_items[0]
			items.append(dict(id=vendor.id, Name=vendor.Name, Description=vendor.Description, Price=quote_item.Price, Ranking=quote_item.Ranking, Product=quote_item.Product, Notes=quote_item.Notes, ValidOn=quote_item.Quote.ValidOn.strftime('%Y-%m-%d')))
	return dict(items=items)

@expose(html='care2x.templates.purchaseorder')
def PurchaseOrderCreateNewStep2(self, data='', **kw):
	CatalogItems = []
	data = simplejson.loads(data)
	for item in data:
		CatalogItems.append(dict(id=item['id'], Name=item['Name'], Description=item['Description'], Quantity="", Notes=""))
	return dict(Name='PurchaseOrderCreateNewStep2', Label='Purchase order create', CatalogItems=CatalogItems)
	
@expose()
def PurchaseOrderCreateNewSave(self, CatalogItem=[], Vendor=[], QuantityRequested=[], QuotePrice=[], Notes=[], **kw):
	POs = {}
	for cat_id, ven_id, qtyreq, qtprce, note in zip(CatalogItem, Vendor, QuantityRequested, QuotePrice, Notes):
		if POs.has_key(ven_id):
			PurchaseOrderId = POs[ven_id]
		else:
			PurchaseOrder = model.InvPurchaseOrder(VendorID = int(ven_id), Status="")
			PurchaseOrderId = PurchaseOrder.id
			POs[ven_id] = PurchaseOrderId
		POItem = model.InvPOItems(PurchaseOrderID = int(PurchaseOrderId), CatalogItemID = int(cat_id), QuantityRequested = float(qtyreq), QuotePrice = float(qtprce), Notes = note, Status='')
	raise cherrypy.HTTPRedirect('/inventory')

@expose(format='json')
def PurchaseOrderGoodsReceivedSearch(self, Id='', id='', **kw):
	qArgs = ""
	if Id != '':
		id = Id
	
	#Find the purchase order items
	if id != '':
		items = model.InvPOItems.select(model.InvPOItems.q.PurchaseOrderID == int(id))
	results = []
	for item in items:
		if item.Status == 'deleted':
			text = item.Name()
			results.append({'id':item.id, 'text':text, 'Name':item.Name(), 'Description':''})
		else:
			text = item.Name()
			results.append({'id':item.id, 'text':text, 'Name':item.Name(), 'Description':''})
	#Return a modified listing
	po = model.InvPurchaseOrder.get(int(id))
	mod_items = []
	for item in items:
		mod_item = {}
		mod_item['PurchaseOrderID'] = item.PurchaseOrderID
		mod_item['id'] = item.id
		quote_items = model.InvQuoteItems.select(AND (model.InvQuoteItems.q.CatalogItemID == item.CatalogItemID, \
			model.InvQuoteItems.q.QuoteID == model.InvQuote.q.id, model.InvQuote.q.VendorID == po.VendorID),\
			orderBy=-model.InvQuote.q.ValidOn)
		mod_item['Name'] = quote_items[0].Product
		mod_item['edActualPrice'] = quote_items[0].Price
		mod_item['edQuantityReceived'] = item.QuantityRequested
		mod_item['edMRP'] = quote_items[0].Price
		mod_items.append(mod_item)
	return dict(results=results, items=mod_items)
	
@expose()
def PurchaseOrderSaveGoodsReceived(self, Id='', id='', data='', **kw):
	result_msg = ''
	if Id !='':
		id = Id
	if data!='':
		data = simplejson.loads(data)
		PurchaseOrderId = int(data[0]['PurchaseOrderID'])
		# Create new Goods received entry (InvGoodsReceived)
		gr_record = model.InvGoodsReceived(PurchaseOrderID = PurchaseOrderId)
		for item in data:
			# Calculate the expire date
			if item['ExpireDate'] != '':
				ExpireDate = datetime.fromtimestamp(time.mktime(time.strptime(item['ExpireDate'][0:10],'%Y-%m-%d')))
			else:
				ExpireDate = None
			# Update PurchaseOrder Items (InvPOItems)
			po_item = model.InvPOItems.get(int(item['id']))
			po_item.QuantityReceived += int(item['edQuantityReceived'])
			po_item.ActualPrice = float(item['edActualPrice'])
			# Create new Stock items (InvStockItems)
			stk_item = model.InvStockItem(CatalogItemID = po_item.CatalogItemID, PurchaseOrderID = gr_record.id, \
				Name = item['Name'], Quantity = int(item['edQuantityReceived']), BatchNumber = item['BatchNumber'], \
				ExpireDate = ExpireDate, PurchasePrice=float(item['edActualPrice']), SalePrice=\
				float(item['edActualPrice']), MRP=float(item['edMRP']), Status="")
			# TODO: Create a location entry for the stock item, for now, stick everything in the first location found
			# ************************* FIX THIS *****************************
			location = model.InvLocation.select()[0]
			stk_location = model.InvStockLocation(StockItemID = stk_item.id, LocationID = location.id, Quantity = stk_item.Quantity, Status="")
	return dict(id=id, Name='PurchaseOrderSaveGoodsReceived', Label='Goods received saved', result_msg="Goods received added")

@expose(format='json')
def PurchaseOrderAddGoodsReceived(self, Id='', id='', data='', **kw):
	result_msg = ""
	
	#Input variables
	#for InvPOItems
	QuantityReceived = dict(id="po_QuantityReceived", name="edQuantityReceived", label="Quantity received", type="Numeric", attr=dict(length=10), data='')
	ActualPrice = dict(id="po_ActualPrice", name="edActualPrice", label="Actual price", type="Numeric", attr=dict(length=10), data='')
	MRP = dict(id="po_MRP", name="edMRP", label="M.R.P.", type="Numeric", attr=dict(length=10), data='')
	#for InvGoodsReceived
	#PurchaseOrderID = dict(id="po_PurchaseOrderID", name="PurchaseOrderID", label="PurchaseOrderID", type="Hidden", attr=dict(length=10), data='')
	Notes = dict(id="po_Notes", name="edNotes", label="Notes", type="String", attr=dict(length=40), data='')
	#for InvStockItem
	#CatalogItemID = dict(id="po_CatalogItemID", name="CatalogItemID", label="CatalogItemID", type="Hidden", attr=dict(length=10), data='')
	#POItemsID = dict(id="po_POItemsID", name="POItemsID", label="POItemsID", type="Hidden", attr=dict(length=10), data='')
	Name = dict(id="po_Name", name="Name", label="Name (product)", type="String", attr=dict(length=30), data='') 
	#(pull from product off of quote?)
	#Quantity = dict(id="po_Quantity", name="Quantity", label="Quantity", type="Numeric", attr=dict(length=10), data='') 
	#(same as QuantityReceived)
	BatchNumber = dict(id="po_BatchNumber", name="BatchNumber", label="Batch number", type="String", attr=dict(length=30), data='')
	ExpireDate = dict(id="po_ExpireDate", name="ExpireDate", label="Expire date", type="DateTime", attr=dict(length=10), data='')
	#Search variable
	SrchId = dict(id="po_SrchId", name="id", label="Purchase order id", type="StringRO", attr=dict(length=25), data=id)
	return dict(id=id, Name='PurchaseOrderAddGoodsReceived', Label='Goods received entry', FieldsSrch=[SrchId],\
		Inputs=[QuantityReceived, ActualPrice, MRP, Name, BatchNumber, ExpireDate, Notes], \
		SrchUrl='PurchaseOrderGoodsReceivedSearch', DataUrl='', Url='PurchaseOrderSaveGoodsReceived', \
		UrlVars='id='+id, result_msg=result_msg, SrchNow=True)
