import logging
from datetime import datetime, date
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
def StockTransfer(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockTransfer.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Qty_data = str(record.Qty)
		IsComplete_data = record.IsComplete
		DateTransferred_data = record.DateTransferred
		#ForeignKeys
		try:
			FromStockLocation_data = record.FromStockLocation.id
			FromStockLocation_display = record.FromStockLocation.NameItemLoc() + ' ('+str(record.FromStockLocation.id)+')'
		except AttributeError: 
			FromStockLocation_data = ''
			FromStockLocation_display = 'None'
		try:
			ToStockLocation_data = record.ToStockLocation.id
			ToStockLocation_display = record.ToStockLocation.NameItemLoc() + ' ('+str(record.ToStockLocation.id)+')'
		except AttributeError: 
			ToStockLocation_data = ''
			ToStockLocation_display = 'None'
		try:
			StockTransferRequestItem_data = record.StockTransferRequestItem.id
			StockTransferRequestItem_display = record.StockTransferRequestItem.Name() + ' ('+str(record.StockTransferRequestItem.id)+')'
		except AttributeError: 
			StockTransferRequestItem_data = ''
			StockTransferRequestItem_display = 'None'
		#MultiJoin and RelatedJoin
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Qty_data = ''
		IsComplete_data = ''
		DateTransferred_data = ''
		#ForeignKeys
		FromStockLocation_data = ''
		FromStockLocation_display = 'None'
		ToStockLocation_data = ''
		ToStockLocation_display = 'None'
		StockTransferRequestItem_data = ''
		StockTransferRequestItem_display = 'None'
		#MultiJoin and RelatedJoin
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#MultiJoin and RelatedJoin
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="st_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="st_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	IsComplete = dict(id="st_IsComplete", name="IsComplete", label="Is complete",type="Bool",attr={}, data=IsComplete_data)
	DateTransferred = dict(id="st_DateTransferred", name="DateTransferred", label="Date transferred", type="DateTime",attr=dict(), data=DateTransferred_data)
	Qty = dict(id="st_Qty", name="Qty", label="Qty", type="Numeric",attr=dict(length=50), data=Qty_data)
	#ForeignKeys
	SrchStockItemName = dict(id="st_SrchStockItemName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	SrchFromName = dict(id="st_SrchFromName", name="LocationName", label="Name", type="String",attr=dict(length=25), data='')
	FromStockLocation = dict(id="st_FromStockLocation", name="FromStockLocation", label="From location", type="ForeignKey",attr=dict(srchUrl="StockLocationSearch",lookupUrl="StockLocationGet", edit_url='StockLocation', srchFields=[SrchFromName]), data=FromStockLocation_data, init_display=FromStockLocation_display)
	SrchToName = dict(id="st_SrchToName", name="LocationName", label="Name", type="String",attr=dict(length=25), data='')
	ToStockLocation = dict(id="st_ToStockLocation", name="ToStockLocation", label="To location", type="ForeignKey",attr=dict(srchUrl="StockLocationSearch",lookupUrl="StockLocationGet", edit_url='StockLocation', srchFields=[SrchToName]), data=ToStockLocation_data, init_display=ToStockLocation_display)
	SrchLocationName  = dict(id="st_SrchLocationName", name="ForLocationName", label="Location name", type="String",attr=dict(length=25), data='')
	SrchCatalogItemName  = dict(id="st_SrchCatalogItemName", name="CatalogItemName", label="Catalog item name", type="String",attr=dict(length=25), data='')
	StockTransferRequestItem = dict(id="st_StockTransferRequestItem", name="StockTransferRequestItem", label="Stock item request", type="ForeignKey",attr=dict(srchUrl="StockTransferRequestItemSearch",lookupUrl="StockTransferRequestItemGet", edit_url='StockTransferRequestItem', srchFields=[SrchLocationName, SrchCatalogItemName]), data=StockTransferRequestItem_data, init_display=StockTransferRequestItem_display)
	#Fields
	fields = [Id, Name, IsComplete, DateTransferred, Qty, StockTransferRequestItem, FromStockLocation, ToStockLocation]
	#Configure any of the links that might need configuring
	if id == '':
		StockTransferMenu = 'StockTransferMenu'
	else:
		StockTransferMenu = 'StockTransferMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='StockTransfer', Label='Stock transfer entry', Fields=fields, FieldsSrch=[Name], Read='StockTransfer', Add='StockTransferSave', Del='StockTransferDel', UnDel='StockTransferUnDel', Edit='StockTransfer', Save='StockTransferSave', SrchUrl='StockTransferSearch', MenuBar=StockTransferMenu)

@expose(format='json')
def StockTransferMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockTransfer")', menu=[ \
			dict(label='Fill in requests', url='StockTransferCreateNew')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockTransfer")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockTransfer?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def StockTransferGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransfer.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'IsComplete':validators.StringBool(), 'DateTransferred':validators.String(), 'Qty':validators.Number(), 'StockTransferRequestItem':validators.Int(), 'FromStockLocation':validators.Int(), 'ToStockLocation':validators.Int()})
def StockTransferSave(self, ToStockLocation, FromStockLocation, StockTransferRequestItem=None, Qty=0, Id='', id='', DateTransferred='', IsComplete=False, **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransfer.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if DateTransferred != '':
		if len(DateTransferred) > 12:
			DateTransferred = datetime.fromtimestamp(time.mktime(time.strptime(DateTransferred,'%Y-%m-%d %H:%M:%S')))
		elif len(DateTransferred) > 10:
			DateTransferred = datetime.fromtimestamp(time.mktime(time.strptime(DateTransferred,'%Y-%m-%d %H:%M')))
		else:
			DateTransferred = datetime.fromtimestamp(time.mktime(time.strptime(DateTransferred,'%Y-%m-%d')))
		
	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				#Updating the record
				record.DateTransferred = DateTransferred
				record.ToStockLocation = ToStockLocation
				record.FromStockLocation = FromStockLocation
				record.StockTransferRequestItem = StockTransferRequestItem
				record.IsComplete = IsComplete
				record.Qty = Qty
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvStockTransfer(Qty=Qty, StockTransferRequestItem=StockTransferRequestItem, \
				FromStockLocation=FromStockLocation, ToStockLocation=ToStockLocation, IsComplete=IsComplete,\
				DateTransferred=DateTransferred, Status='')
			result_msg = "Record added"
		#Run checks for transfer completions
		record.CheckCompleted()
		if record.StockTransferRequestItemID != None:
			record.StockTransferRequestItem.CheckAllComplete()
		result = 1
		record_id = record.id
	except:
		result = 0
		result_msg="Operation failed!"
		record_id = ''
		raise
	return dict(result=result, result_msg=result_msg, id=record_id)
	
@expose(format='json')
def StockTransferDel(Id, id='', **kw):
	"""	If the StockTransfer has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransfer.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if not record.IsComplete:
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
def StockTransferUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransfer.get(int_id)
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
def StockTransferMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockTransfer.get(int_id)
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
					if ColName == 'Requests':
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
def StockTransferSearch(self, Name='', StockItemName='', FromLocationName='', ToLocationName='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvStockItem.q.Name.contains('"+ Name + "'),"
	if StockItemName != '':
		qArgs+="model.InvStockItem.q.Name.contains('"+ StockItemName + "'),"
	if FromLocationName != '':
		qArgs+="model.InvLocation.q.Name.contains('"+ FromLocationName + "'),"
	if ToLocationName != '':
		qArgs+="model.InvLocation.q.Name.contains('"+ ToLocationName + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvStockTransfer.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvStockTransfer.select()
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
def StockTransferGetLocationsForItem(self, StockTransferRequestItemID='', **kw):
	items = []
	if StockTransferRequestItemID != '':
		record = model.InvStockTransferRequestItem.get(int(StockTransferRequestItemID))
		CatalogItemID = record.CatalogItemID
		ForLocationID = record.StockTransferRequest.ForLocationID
		locations = model.InvStockLocation.select(AND (model.InvStockItem.q.CatalogItemID == CatalogItemID, \
			model.InvStockLocation.q.LocationID == model.InvLocation.q.id, model.InvStockLocation.q.StockItemID == \
			model.InvStockItem.q.id, model.InvStockLocation.q.IsConsumed == False, model.InvLocation.q.IsStore == True, \
			model.InvStockLocation.q.LocationID !=ForLocationID),distinct=True)
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
def StockTransferCreateNewRedirect(self, **kw):
	raise cherrypy.HTTPRedirect('StockTransferCreateNew')

@expose(html='care2x.templates.stocktransfer')
def StockTransferCreateNew(self, **kw):
	RequestedCatalogItems = []
	data = model.InvStockTransferRequestItem.select(AND (model.InvStockTransferRequestItem.q.IsTransferred == False, \
		model.InvStockTransferRequestItem.q.Status == "", model.InvStockTransferRequestItem.q.IsOnOrder == False), \
		orderBy=model.InvStockTransferRequestItem.q.StockTransferRequestID)
	for item in data:
		if not item.IsSatisfied():
			RequestedCatalogItems.append(dict(id=item.id, Name=item.Name(), CatalogItemID=item.CatalogItemID, Notes=item.Notes, \
				Qty=item.Qty, RequestedOn=item.StockTransferRequest.RequestedOn.strftime('%Y-%m-%d'), RequiredBy = \
				item.StockTransferRequest.RequiredBy.strftime('%Y-%m-%d'), ForLocationID=item.StockTransferRequest.ForLocationID, \
				ForLocationName=item.StockTransferRequest.ForLocation.Name))
	return dict(Name='StockTransferCreateNew', Label='Make stock transfers', RequestedCatalogItems=RequestedCatalogItems)
	
@expose()
def StockTransferCreateNewSave(self, TransferQty=[], ForLocationID=[], StockTransferRequestItemID=[], CatalogItemID=[], \
	StockLocationID=[], counter=[], **kw):
	def MakeEntry(TransferQty, ForLocationID, StockTransferRequestItemID, CatalogItemID, StockLocationID):
		item_request = model.InvStockTransferRequestItem.get(int(StockTransferRequestItemID))
		from_stk_location = model.InvStockLocation.get(int(StockLocationID))
		Qty = int(float(TransferQty))
		#log.debug("@@@@@@@@@@@@@@@@@@ CatalogItemID: "+ str(from_stk_location.StockItem.CatalogItemID) + " == " + CatalogItemID)
		if from_stk_location.StockItem.CatalogItemID == int(CatalogItemID):
			#log.debug("@@@@@@@@@@@@@@@@@@ TransferQty: "+ str(from_stk_location.QtyAvailable()) + \
			#	" => >" + TransferQty + "<")
			if Qty <= from_stk_location.QtyAvailable():
				#Look for any StockLocation entries at the destination with the same StockItem ID which are not sold or consumed
				dest_stk_locations = model.InvStockLocation.select(AND (model.InvStockLocation.q.IsConsumed == \
					False, model.InvStockLocation.q.IsSold == False, model.InvStockLocation.q.LocationID == \
					int(ForLocationID), model.InvStockLocation.q.StockItemID == from_stk_location.StockItemID))
				if len(list(dest_stk_locations))>0:
					#log.debug("@@@@@@@@@@@@@@@@@@ Found existing stock location")
					to_stk_location = dest_stk_locations[0]
					#Create a StockTransfer entry and then update the first found stock location entry with the quantity
					stocktransfer = model.InvStockTransfer(FromStockLocationID=from_stk_location.id, \
						ToStockLocationID=to_stk_location.id, StockTransferRequestItemID=item_request.id, Qty=Qty)
					to_stk_location.Quantity += Qty
					#remove the selected amount from the originating stock location
					from_stk_location.Quantity = from_stk_location.Quantity - Qty
				else:
					#log.debug("@@@@@@@@@@@@@@@@@@ Create new stock location")
					#Create a stock location entry and then create a stock transfer entry then subtract the amount from the originating location
					to_stk_location = model.InvStockLocation(StockItemID=from_stk_location.StockItem.id, LocationID=\
						int(ForLocationID),Quantity=Qty)
					stocktransfer = model.InvStockTransfer(FromStockLocationID=from_stk_location.id, \
						ToStockLocationID=to_stk_location.id, StockTransferRequestItemID=item_request.id, Qty=Qty)
					from_stk_location.Quantity = from_stk_location.Quantity - Qty
	#log = logging.getLogger("care2x.controllers")
	if len(counter) < 2:
		#log.debug("@@@@@@@@@@@@@@@@@@ SINGLE ENTRY")
		MakeEntry(TransferQty.strip(), ForLocationID.strip(), StockTransferRequestItemID.strip(), CatalogItemID.strip(), \
			StockLocationID.strip())
	else:
		#log.debug("@@@@@@@@@@@@@@@@@@ MULTI ENTRIES")
		for qty, forlocation, itemrequest, catalogid, fromlocationid in zip(TransferQty, ForLocationID, StockTransferRequestItemID, \
			CatalogItemID, StockLocationID):
			MakeEntry(qty, forlocation.strip(), itemrequest.strip(), catalogid.strip(), fromlocationid.strip())
	raise cherrypy.HTTPRedirect('/inventory/StockTransferCreateNew')