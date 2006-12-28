import logging
from datetime import datetime, date
import time
import simplejson
import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model

@expose(format='json')
def StockItem(self, id='',Id='', Op='', CatalogItemID='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name
		if record.Status == 'deleted':
			Name_data += ' *** MARKED DELETED ***'
		Quantity_data = str(record.Quantity)
		PurchasePrice_data = str(record.PurchasePrice)
		SalePrice_data = str(record.SalePrice)
		BatchNumber_data = record.BatchNumber
		MRP_data = record.MRP
		VATAmount_data = record.VATAmount()
		CostDifference_data = record.CostDifference()
		if record.ExpireDate != None:
			ExpireDate_data = record.ExpireDate.strftime('%Y-%m-%d')
		else:
			ExpireDate_data = ''
		if record.CompoundDateProduced != None:
			CompoundDateProduced_data = record.CompoundDateProduced.strftime('%Y-%m-%d')
		else:
			CompoundDateProduced_data = ''
		#ForeignKey
		try:
			CatalogItem_data = record.CatalogItem.id
			CatalogItem_display = record.CatalogItem.Name + ' ('+str(record.CatalogItem.id)+')'
		except AttributeError: 
			CatalogItem_data = ''
			CatalogItem_display = 'None'
		try:
			PurchaseOrder_data = record.PurchaseOrder.id
			PurchaseOrder_display = record.PurchaseOrder.Name()
		except AttributeError: 
			PurchaseOrder_data = ''
			PurchaseOrder_display = 'None'
		try:
			StockCompound_data = record.StockCompound.id
			StockCompound_display = record.StockCompound.CatalogCompound.Name + ' ('+str(record.StockCompound.id)+')'
		except AttributeError: 
			StockCompound_data = ''
			StockCompound_display = 'None'
		#MultipleJoin or RelatedJoin
		Locations_data = 'There are ' + str(len(record.Locations)) + ' records'
		CompoundQtys_data = 'There are ' + str(len(record.CompoundQtys)) + ' records'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Quantity_data = ''
		PurchasePrice_data = ''
		SalePrice_data = ''
		BatchNumber_data = ''
		ExpireDate_data = ''
		CompoundDateProduced_data = ''
		MRP_data = ''
		VATAmount_data = ''
		CostDifference_data = ''
		#Foreign key
		CatalogItem_data = ''
		CatalogItem_display = 'None'
		PurchaseOrder_data = ''
		PurchaseOrder_display = 'None'
		StockCompound_data = ''
		StockCompound_display = 'None'
		#MultiJoin or RelatedJoin
		Locations_data = 'There are no records'
		CompoundQtys_data = 'There are no records'
		DisplayMessage_data = ''
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		Locations_data = 'There are no records'
		Compounds_data = 'There are no records'
		CompoundQtys_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="si_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="si_Name", name="Name", label="Name", type="String",attr=dict(length=25), data=Name_data)
	Quantity = dict(id="si_Quantity", name="Quantity", label="Quantity", type="Numeric",attr=dict(), data=Quantity_data)
	PurchasePrice = dict(id="si_PurchasePrice", name="PurchasePrice", label="Purchase price", type="Numeric",attr=dict(), data=PurchasePrice_data)
	SalePrice = dict(id="si_SalePrice", name="SalePrice", label="Sale price", type="Numeric",attr=dict(), data=SalePrice_data)
	BatchNumber = dict(id="si_BatchNumber", name="BatchNumber", label="Batch number", type="String",attr=dict(length=25), data=BatchNumber_data)
	ExpireDate = dict(id="si_ExpireDate", name="ExpireDate", label="Expire date",type="DateTime",attr={}, data=ExpireDate_data)
	CompoundDateProduced = dict(id="CompoundDateProduced", name="CompoundDateProduced", label="Compound date produced",type="DateTime",attr={}, data=CompoundDateProduced_data)
	MRP = dict(id="si_MRP", name="MRP", label="MRP", type="Numeric",attr=dict(), data=MRP_data)
	CostDifference = dict(id="si_CostDifference", name="CostDifference", label="Cost difference", type="StringRO",attr=dict(), data=CostDifference_data)
	VATAmount = dict(id="si_VATAmount", name="VATAmount", label="VAT Amount", type="StringRO",attr=dict(), data=VATAmount_data)
	#ForeignKey
	SrchCatalogName = dict(id="si_SrchCatalogName", name="SrchCatalogName", label="Name", type="String",attr=dict(length=25), data='')
	CatalogItem = dict(id="si_CatalogItem", name="CatalogItem", label="Catalog item", type="ForeignKey",attr=dict(srchUrl="CatalogItemSearch",lookupUrl="CatalogItemGet",srchFields=[SrchCatalogName], edit_url='CatalogItem'), data=CatalogItem_data, init_display=CatalogItem_display)
	SrchPOVendor = dict(id="si_SrchPOVendor", name="Name", label="PO Vendor", type="String",attr=dict(length=25), data='')
	PurchaseOrder = dict(id="si_PurchaseOrder", name="PurchaseOrder", label="Purchase order", type="ForeignKey",attr=dict(srchUrl="PurchaseOrderSearch",lookupUrl="PurchaseOrderGet",srchFields=[SrchPOVendor], edit_url='PurchaseOrder'), data=PurchaseOrder_data, init_display=PurchaseOrder_display)
	#SrchCompoundName = dict(id="si_SrchCompoundName", name="Name", label="Compound name", type="String",attr=dict(length=25), data='')
	#StockCompound = dict(id="si_StockCompound", name="StockCompound", label="Stock compound", type="ForeignKey",attr=dict(srchUrl="StockCompoundSearch",lookupUrl="StockCompoundGet",srchFields=[SrchCompoundName], edit_url='StockCompound'), data=StockCompound_data, init_display=StockCompound_display)
	#MultipleJoin
	Locations = dict(id="si_Locations", name="Locations", label="Locations", type="MultiJoin",attr=dict(displayUrl="StockItemMultiJoinList",listUrl="StockItemMultiJoinList",linkUrl="StockLocation"), data=Locations_data)
	CompoundQtys = dict(id="si_CompoundQtys", name="CompoundQtys", label="Compound items", type="MultiJoin",attr=dict(displayUrl="StockItemMultiJoinList",listUrl="StockItemMultiJoinList",linkUrl="StockCompoundQty"), data=CompoundQtys_data)
	DisplayMessage = dict(id="si_DisplayMessage", name="DisplayMessage", type="Display",attr=dict(css_class='displaymsg'), data=DisplayMessage_data)		
	fields = [Id, Name, Quantity, PurchasePrice, SalePrice, MRP, BatchNumber, ExpireDate, CatalogItem, PurchaseOrder, \
		CompoundDateProduced, CompoundQtys, Locations, CostDifference, VATAmount]
	#Configure any of the links that might need configuring
	if id == '':
		StockItemMenu = 'StockItemMenu'
	else:
		StockItemMenu = 'StockItemMenu?id=' + id
	#CatalogItemID search field
	SrchCatalogItemID = dict(id="si_SrchCatalogItemID", name="CatalogItemID", label="Catalog item id", type="Hidden",attr=dict(length=5), data=CatalogItemID)
	#RETURN VALUES HERE
	return dict(id=id, Name='StockItem', Label='Inventory Items', Fields=fields, FieldsSrch=[Name, SrchCatalogItemID], Read='StockItem', Add='StockItemSave', Del='StockItemDel', UnDel='StockItemUnDel', Edit='StockItem', Save='StockItemSave', SrchUrl='StockItemSearch', MenuBar=StockItemMenu, TreeView='StockItemTree')

@expose(format='json')
def StockItemMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockItem")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockItem")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Purchase Order', url=''), dict(label='Locations', url=''), dict(label='Compounds', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Purchase history', url=''), dict(label='Price quotes', url=''), dict(label='Locations', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockItem")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockItem?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Purchase Order', url=''), dict(label='Locations', url=''), dict(label='Compounds', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView("StockItem")', menu=[dict(label='Purchase history', url=''), dict(label='Price quotes', url=''), dict(label='Store locations', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def StockItemTree(self, **kw):
	def StockItemRecords(catid):
		return model.InvStockItem.select(AND (model.InvStockItem.q.CatalogItemID==catid, model.InvStockItem.q.Status=="")).count()
	def GetChildren(parent_item):
		nodes = []
		for item in parent_item.ChildItems:
			if item.Status != 'deleted':
				ItemName = item.Name + " (" + str(StockItemRecords(item.id)) + " records)"
				if len(item.ChildItems) > 0:
					children = GetChildren(item)
					nodes.append(dict(label=ItemName, href="javascript:inv.openObjListing('StockItem?CatalogItemID="+str(item.id)+"')", nodes=children))
				else:
					nodes.append(dict(label=ItemName, href="javascript:inv.openObjListing('StockItem?CatalogItemID="+str(item.id)+"')"))				
		return nodes
	nodes = []
	catalog = model.InvCatalogItem.select(model.InvCatalogItem.q.ParentItemID == None)
	for item in catalog:
		if item.Status != 'deleted':
			ItemName = item.Name + " (" + str(StockItemRecords(item.id)) + " records)"
			if len(item.ChildItems) > 0:
				children = GetChildren(item)
				nodes.append(dict(label=ItemName, href="javascript:inv.openObjListing('StockItem?CatalogItemID="+str(item.id)+"')", nodes=children))
			else:
				nodes.append(dict(label=ItemName, href="javascript:inv.openObjListing('StockItem?CatalogItemID="+str(item.id)+"')"))
	return dict(nodes=nodes)
	
@expose(format='json')
def StockItemGet(self, id='', Id='', field_id='', field_num = '', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		if record.Status == 'deleted':
			display = record.Name + ' ('+str(record.id)+') **MARKED DELETED***'
		else:
			display = record.Name + ' ('+str(record.id)+')'
		return dict(display=display, record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)

@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Name':validators.String(), 'PurchasePrice':validators.Number(), 'SalePrice':validators.Number(), 'Quantity':validators.Number(), 'BatchNumber':validators.String(), 'ExpireDate':validators.String(), 'CompoundDateProduced':validators.String(), 'CatalogItem':validators.Int(), 'PurchaseOrder':validators.Int(),'MRP':validators.Number()})
def StockItemSave(self, CatalogItem, PurchaseOrder=None, MRP=0, ExpireDate='', CompoundDateProduced='', Id = '',id = '', Name = '', Quantity = 0, SalePrice=0, PurchasePrice=0, BatchNumber = '', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if ExpireDate != '':
		if len(ExpireDate) > 10:
			ExpireDate = datetime.fromtimestamp(time.mktime(time.strptime(ExpireDate,'%Y-%m-%d %H:%M')))
		else:
			ExpireDate = datetime.fromtimestamp(time.mktime(time.strptime(ExpireDate,'%Y-%m-%d')))
	else:
		ExpireDate = None
	if CompoundDateProduced != '':
		if len(CompoundDateProduced) > 10:
			CompoundDateProduced = datetime.fromtimestamp(time.mktime(time.strptime(CompoundDateProduced,'%Y-%m-%d %H:%M')))
		else:
			CompoundDateProduced = datetime.fromtimestamp(time.mktime(time.strptime(CompoundDateProduced,'%Y-%m-%d')))
	else:
		CompoundDateProduced = None

	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				#Updating the record
				record.Name = Name
				record.Quantity = Quantity
				record.SalePrice = SalePrice
				record.PurchasePrice = PurchasePrice
				record.BatchNumber = BatchNumber
				record.ExpireDate = ExpireDate
				record.CatalogItem = CatalogItem
				record.PurchaseOrder = PurchaseOrder
				record.MRP = MRP
				#record.StockCompound = StockCompound
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvStockItem(Name = Name, Quantity = Quantity, BatchNumber = BatchNumber, \
				ExpireDate = ExpireDate, CatalogItem = CatalogItem, PurchaseOrder = PurchaseOrder, \
				PurchasePrice=PurchasePrice, MRP=MRP, SalePrice=SalePrice, Status='')
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
def StockItemDel(Id, id='', **kw):
	"""	If the StockItem has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			CanDestroy = True
			for location in record.Locations:
				if location.IsConsumed or location.IsSold:
					CanDestroy = False
				elif len(location.Compounds) > 0:
					CanDestroy = False
			if CanDestroy:
				#If the item is a compounded item who's production is cancelled, then we have to undo a lot of things
				if record.CatalogItem.CompoundID != None:
					#Go through all the locations
					for CompoundItem in record.CompoundQtys:
						#Undo the transfer(s)
						Transfers = model.InvStockTransfer.select(model.InvStockTransfer.q.ToStockLocationID==\
							CompoundItem.StockLocationID)
						for transfer in Transfers:
							if not (transfer.FromStockLocation.IsConsumed or transfer.FromStockLocation.IsSold):
								transfer.FromStockLocation.Quantity += transfer.Qty
							else:
								transfer.FromStockLocation.Quantity += transfer.Qty
								transfer.FromStockLocation.Status = 'Error: %s quantity ' % str(transfer.Qty)
							transfer.destroySelf()
						StockLocation = model.InvStockLocation.get(CompoundItem.StockLocationID)
						StockLocation.destroySelf()
						CompoundItem.destroySelf()
				#remove the item at locations
				for location in record.Locations:
					location.destroySelf()
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
def StockItemUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockItem.get(int_id)
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
def StockItemMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockItem.get(int_id)
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
					if ColName == 'Locations':
						list_text = item.Name()
					elif ColName == 'Transfers':
						list_text = 'From ' + item.FromLocation.Name + ' to ' + item.ToLocation.Name + ' on ' + item.DateTransferred.strftime('%Y-%m-%d')
					elif ColName == 'CompoundQtys':
						list_text = item.Name()
					records.append(dict(id=item.id, listing=list_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def StockItemSearch(self, Name='', BatchNumber='',CatalogItemID='', Groups=[], field_num='', show_del=True, inputs=[], **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvStockItem.q.Name.contains('"+ Name + "'),"
	if BatchNumber != '':
		qArgs+="model.InvStockItem.q.BatchNumber.contains('"+ BatchNumber + "'),"
	if CatalogItemID != '':
		qArgs+="model.InvStockItem.q.CatalogItemID == " + CatalogItemID + ","
	if len(qArgs) > 0:
		items = eval('model.InvStockItem.select(AND ('+qArgs[0:len(qArgs)-1]+'),orderBy=[model.InvStockItem.q.Status,\
			model.InvStockItem.q.ExpireDate, model.InvStockItem.q.CreateTime])')
	else:
		items = model.InvStockItem.select(orderBy=[model.InvStockItem.q.Status, model.InvStockItem.q.ExpireDate, \
			model.InvStockItem.q.CreateTime])
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Name+' *** MARKED DELETED *** '+item.CreateTime.strftime('%Y-%m-%d')
				results.append({'id':item.id, 'text':text, 'Name':item.Name+' *** MARKED DELETED ***', 'Description':item.CreateTime.strftime('%Y-%m-%d')})
			else:
				text = item.Name+' '+item.CreateTime.strftime('%Y-%m-%d')
				results.append({'id':item.id, 'text':text, 'Name':item.Name, 'Description':item.CreateTime.strftime('%Y-%m-%d')})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name, 'Description':item.CreateTime.strftime('%Y-%m-%d')})
	return dict(results=results, field_num=field_num, items=items,inputs=inputs)


@expose(format='json')
def StockItemCompoundGetLocationsForItem(self, CatalogItemID='', LocationID='', **kw):
	items = []
	#log = logging.getLogger("care2x.controllers")
	#log.debug("!!!!!!!!!!!!!! CatalogItemID, LocationID: %s, %s." % (CatalogItemID, LocationID))
	if (CatalogItemID != '') and (LocationID !=''):
		locations = model.InvStockLocation.select(AND (model.InvStockItem.q.CatalogItemID == int(CatalogItemID), \
			model.InvStockLocation.q.StockItemID == model.InvStockItem.q.id, model.InvStockLocation.q.LocationID \
			== int(LocationID), model.InvStockLocation.q.IsConsumed == False),distinct=True)
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

@expose(html='care2x.templates.stockcompound')
def StockItemCompoundCreateNew(self, id='', Id='', **kw):
	if Id != '':
		id = Id
	if id == '':
		error = "No Catalog item specified for creating a compound"
		raise cherrypy.HTTPRedirect('/inventory/ProgrammingError?error='+error)		
	CatalogItems = []
	record = model.InvCatalogItem.get(int(id))
	if record.CompoundID == None:
		error = "The Catalog item selected is not a compounded item"
		raise cherrypy.HTTPRedirect('/inventory/ProgrammingError?error='+error)
	data = model.InvCatalogCompoundQty.select(AND (model.InvCatalogCompoundQty.q.CatalogCompoundID == \
		record.CompoundID, model.InvCatalogCompoundQty.q.Status != "deleted"))
	for item in data:
		CatalogItems.append(dict(id=item.id, CompoundID=id, Name=item.Name(), CatalogItemID=item.CatalogItemID, Description=item.Description, \
			Qty=item.Qty))
	Locations = []
	records = model.InvLocation.select()
	for record in records:
		Locations.append(dict(id=record.id, Name=record.Name, Description=record.Description))
	return dict(Name='StockItemCompoundCreateNew', Label='Make stock compounds', CatalogItems=CatalogItems, \
		Locations=Locations)

@expose()
def StockItemCompoundSave(self, TransferQty=[], id=[], CatalogItemID=[], CompoundID=[], TotalQty=[],\
	StockLocationID=[], counter=[], **kw):
	def MakeEntry(TransferQty, id, CatalogItemID, CompoundID, TotalQty, StockLocationID, NewStockItemID):
		#attempt to transfer the stock to the compound location
		catalogitem = model.InvCatalogItem.get(int(CompoundID))
		catalogcompound = model.InvCatalogCompound.get(catalogitem.CompoundID)
		stocklocation = model.InvStockLocation.get(int(StockLocationID))
		StockItemID = stocklocation.StockItemID
		if catalogcompound.ConsumedLocationID != None:
			TransferToLocationID = catalogcompound.ConsumedLocationID
			deststocklocation = model.InvStockLocation(StockItemID = StockItemID, LocationID = TransferToLocationID,\
					Quantity = float(TransferQty), IsConsumed = True)
			stocklocation.Quantity = stocklocation.Quantity - float(TransferQty)
			#create stocktransfer entry
			stocktransfer = model.InvStockTransfer(FromStockLocationID = stocklocation.id, ToStockLocation = \
				deststocklocation.id, Qty = float(TransferQty), IsComplete = True)
		else:
			#transfer the item to a separate record at the same location and mark it consumed
			deststocklocation = model.InvStockLocation(StockItemID = StockItemID, LocationID = stocklocation.LocationID,\
					Quantity = float(TransferQty), IsConsumed = True)
			stocklocation.Quantity = stocklocation.Quantity - float(TransferQty)
			#create stocktransfer entry
			stocktransfer = model.InvStockTransfer(FromStockLocationID = stocklocation.id, ToStockLocation = \
				deststocklocation.id, Qty = float(TransferQty), IsComplete = True)
		#Create a stock compound entry
		stckcompound = model.InvStockCompoundQty(StockLocationID = deststocklocation.id, StockCompoundID = NewStockItemID, \
			Qty = float(TransferQty))
	log = logging.getLogger("care2x.controllers")
	#Single entry (rare occurance)
	if len(counter) == 0:
		next_link = "/inventory"
		error = "You didn't enter any data!"
		raise  cherrypy.HTTPRedirect('/inventory/DataEntryError?error=%s&next_link=%s'% (error, next_link))			
	elif len(counter) < 2:
		#check to make sure the item satisfies the requirements
		catalogitem = model.InvCatalogItem.get(int(CompoundID))
		compound = model.InvCatalogCompound.get(catalogitem.CompoundID)
		record = model.InvCatalogCompoundQty.get(int(id))
		stock = model.InvStockLocation.get(int(StockLocationID))
		TotalRequired = record.Qty*(float(TotalQty))
		if (float(TransferQty) == TotalRequired) and (stock.QtyAvailable() >= TotalRequired) and (len(list(compound.ItemQtys)) == 1):
			#Make the item
			newstockitem = model.InvStockItem(Name = compound.Name, CatalogItemID = catalogitem.id, SalePrice = 0,
				PurchasePrice = 0, Quantity = float(TotalQty))
			# Make a stock location item for the new stock item
			newstocklocation = model.InvStockLocation(StockItemID = newstockitem.id, Location = stock.LocationID, \
				Quantity = newstockitem.Quantity)
			MakeEntry(TransferQty, id, CatalogItemID, CompoundID, TotalQty, StockLocationID, newstockitem.id)
			cost = 0.0
			for item in newstockitem.Compounds:
				cost += item.StockItem.PurchasePrice
			cost = cost/float(TotalQty)
			newstockitem.SalePrice = cost
		else:
			next_link = "StockItemCompoundCreateNew?id=%s" % str(catalogitem.id)
			error = "The entry couldn't be completed because:"
			if len(list(compound.ItemQtys)) > 1:
				error+="   You entered 1 item when %s items are needed" % str(len(list(compound.ItemQtys)))
			if float(TransferQty) != TotalRequired:
				error+="   You are using %s of %s when %s is required" % (TransferQty, stock.StockItem.Name, 
					str(TotalRequired))
			if (stock.QtyAvailable < TotalRequired):
				error+="   You are using %s of %s when only %s is available" % (TransferQty, stock.StockItem.Name, 
					str(stock.QtyAvailable()))				
			raise  cherrypy.HTTPRedirect('/inventory/DataEntryError?error=%s&next_link=%s'% (error, next_link))			
	#Multiple entries (more common)
	else:
		#check that the data satisfies requirements for making the item
		catalogitem = model.InvCatalogItem.get(int(CompoundID[0]))
		compound = model.InvCatalogCompound.get(catalogitem.CompoundID)
		compounditems = {}
		for qty, cat_cmp_id, catalogid, compoundid, totalqty, stocklocationid in zip(TransferQty, id, CatalogItemID, \
			CompoundID, TotalQty, StockLocationID):
			cmpditem = {}
			record = model.InvCatalogCompoundQty.get(int(cat_cmp_id))
			stock = model.InvStockLocation.get(int(stocklocationid))
			if stock.QtyAvailable() < float(qty):
				next_link = "StockItemCompoundCreateNew?id=%s" % str(catalogitem.id)
				error = "The entry couldn't be completed because you are using %s of %s when only %s is available." \
					% (str(qty), stock.StockItem.Name, str(stock.QtyAvailable()))
				raise  cherrypy.HTTPRedirect('/inventory/DataEntryError?error=%s&next_link=%s'% (error, next_link))			
			TotalRequired = record.Qty*(float(totalqty))
			if compounditems.has_key(cat_cmp_id):
				cmpditem = compounditems['cat_cmp_id']
				cmpditem['TotalUsed'] += float(qty)
			else:
				cmpditem['id'] = cat_cmp_id
				cmpditem['TotalRequired'] = TotalRequired
				cmpditem['TotalUsed'] = float(qty)
				compounditems[cat_cmp_id] = cmpditem
			if stock.QtyAvailable() < float(qty):
				next_link = "StockItemCompoundCreateNew?id=%s" % str(catalogitem.id)
				error = "The entry couldn't be completed because you are using %s for %s when only %s is required." \
					% (str(cmpditem['TotalUsed']), record.CatalogItem.Name, str(cmpditem['TotalRequired']))
				raise  cherrypy.HTTPRedirect('/inventory/DataEntryError?error=%s&next_link=%s'% (error, next_link))			
		if len(compounditems) != len(list(compound.ItemQtys)):
				log.debug(cmpditem)
				next_link = "StockItemCompoundCreateNew?id=%s" % str(catalogitem.id)
				error = "The entry couldn't be completed because the compound has %s items and only %s items are being entered." \
					% (str(len(list(compound.ItemQtys))), str(len(cmpditem)))
				raise  cherrypy.HTTPRedirect('/inventory/DataEntryError?error=%s&next_link=%s'% (error, next_link))						
		for item in compounditems:
			#log.debug(compounditems)
			#log.debug("!!!!! " + item)
			if compounditems[item]['TotalRequired'] != compounditems[item]['TotalUsed']:
				next_link = "StockItemCompoundCreateNew?id=%s" % str(catalogitem.id)
				catalogitem = model.InvCatalogCompoundQty.get(int(compounditems[item]['id']))
				error = "The entry couldn't be completed because you are using %s for %s when only %s is required." \
					% (str(compounditems[item]['TotalUsed']), catalogitem.CatalogItem.Name, str(compounditems[item]['TotalRequired']))
				raise  cherrypy.HTTPRedirect('/inventory/DataEntryError?error=%s&next_link=%s'% (error, next_link))						
		#create the items
		newstockitem = model.InvStockItem(Name = compound.Name, CatalogItemID = catalogitem.id, SalePrice = 0,
			PurchasePrice = 0, Quantity = float(TotalQty[0]))
		# Make a stock location item for the new stock item
		stocklocation = model.InvStockLocation.get(int(StockLocationID[0]))
		newstocklocation = model.InvStockLocation(StockItemID = newstockitem.id, Location = stocklocation.LocationID, \
			Quantity = newstockitem.Quantity)
		for qty, cat_cmp_id, catalogid, compoundid, totalqty, stocklocationid in zip(TransferQty, id, CatalogItemID, \
			CompoundID, TotalQty, StockLocationID):
			MakeEntry(qty, cat_cmp_id, catalogid, compoundid, totalqty, stocklocationid, newstockitem.id)
		cost = 0.0
		for item in newstockitem.CompoundQtys:
			cost += (item.StockLocation.StockItem.PurchasePrice*item.Qty)
		cost = cost/float(TotalQty[0])
		newstockitem.SalePrice = cost
	raise cherrypy.HTTPRedirect('/inventory')
