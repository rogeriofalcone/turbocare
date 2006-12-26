import logging
from datetime import datetime, date
import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model

@expose(format='json')
def StockLocation(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockLocation.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
#		if record.Status == 'deleted':
#			Name_data += ' *** MARKED DELETED ***'
		IsConsumed_data = record.IsConsumed
		IsSold_data = record.IsSold
		Quantity_data = str(record.Quantity)
		#ForeignKeys
		try:
			StockItem_data = record.StockItem.id
			StockItem_display = record.StockItem.Name + ' ('+str(record.StockItem.id)+')'
		except AttributeError: 
			StockItem_data = ''
			StockItem_display = 'None'
		try:
			Location_data = record.Location.id
			Location_display = record.Location.Name + ' ('+str(record.Location.id)+')'
		except AttributeError: 
			Location_data = ''
			Location_display = 'None'
		try:
			Receipt_data = record.Receipt.id
			Receipt_display = record.Receipt.Name()
		except AttributeError: 
			Receipt_data = ''
			Receipt_display = 'None'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
		#MultiJoins
		TransfersFromHere_data = 'There are ' + str(len(record.TransfersFromHere)) + ' records'
		TransfersToHere_data = 'There are ' + str(len(record.TransfersToHere)) + ' records'
		Compounds_data = 'There are ' + str(len(record.Compounds)) + ' records'
	else:
		Id_data = ''
		Name_data = ''
		IsConsumed_data = ''
		IsSold_data = ''
		Quantity_data = ''
		#ForeignKeys
		StockItem_data = ''
		StockItem_display = 'None'
		Location_data = ''
		Location_display = 'None'
		Receipt_data = ''
		Receipt_display = 'None'
		#MultiJoin and RelatedJoin
		TransfersFromHere_data = 'There are no records'
		TransfersToHere_data = 'There are no records'
		Compounds_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		TransfersFromHere_data = 'There are no records'
		TransfersToHere_data = 'There are no records'
		Quantity_data = ''
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="sl_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="sl_Name", name="Name", label="Name", type="StringRO",attr=dict(), data=Name_data)
	Quantity = dict(id="sl_Quantity", name="Quantity", label="Quantity", type="Numeric",attr=dict(), data=Quantity_data)
	IsConsumed = dict(id="sl_IsConsumed", name="IsConsumed", label="Is consumed", type="Bool",attr=dict(), data=IsConsumed_data)
	IsSold = dict(id="sl_IsSold", name="IsSold", label="Is sold", type="Bool",attr=dict(), data=IsSold_data)
	#ForeignKeys
	SrchStockName = dict(id="sl_SrchStockName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	StockItem = dict(id="sl_StockItem", name="StockItem", label="Stock item", type="ForeignKey",attr=dict(srchUrl="StockItemSearch",lookupUrl="StockItemGet", edit_url='StockItem', srchFields=[SrchStockName]), data=StockItem_data, init_display=StockItem_display)
	SrchLocationName = dict(id="sl_SrchLocationName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Location = dict(id="sl_Location", name="Location", label="Location", type="ForeignKey",attr=dict(srchUrl="LocationSearch",lookupUrl="LocationGet", edit_url='Location', srchFields=[SrchLocationName]), data=Location_data, init_display=Location_display)
	SrchCustomerName = dict(id="sl_SrchCustomerName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Receipt = dict(id="sl_Receipt", name="Receipt", label="Receipt", type="ForeignKey",attr=dict(srchUrl="ReceiptItemsSearch",lookupUrl="ReceiptItemsGet", edit_url='ReceiptItems', srchFields=[SrchCustomerName]), data=Receipt_data, init_display=Receipt_display)
	#MultiJoins
	TransfersFromHere = dict(id="sl_TransfersFromHere", name="TransfersFromHere", label="Transfers from here", type="MultiJoin",attr=dict(displayUrl="StockLocationMultiJoinList",listUrl="StockLocationMultiJoinList",linkUrl="StockTransfer"), data=TransfersFromHere_data)
	TransfersToHere = dict(id="sl_TransfersToHere", name="TransfersToHere", label="Transfers to here", type="MultiJoin",attr=dict(displayUrl="StockLocationMultiJoinList",listUrl="StockLocationMultiJoinList",linkUrl="StockTransfer"), data=TransfersToHere_data)
	Compounds = dict(id="sl_Compounds", name="Compounds", label="Compounds", type="MultiJoin",attr=dict(displayUrl="StockLocationMultiJoinList",listUrl="StockLocationMultiJoinList",linkUrl="StockCompoundQty"), data=Compounds_data)
	#Fields
	fields = [Id, Name, Quantity, IsConsumed, IsSold, StockItem, Location, Receipt, TransfersFromHere, TransfersToHere, Compounds]
	#Configure any of the links that might need configuring
	if id == '':
		StockLocationMenu = 'StockLocationMenu'
	else:
		StockLocationMenu = 'StockLocationMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='StockLocation', Label='Stock location entry', Fields=fields, FieldsSrch=[Name], Read='StockLocation', Add='StockLocationSave', Del='StockLocationDel', UnDel='StockLocationUnDel', Edit='StockLocation', Save='StockLocationSave', SrchUrl='StockLocationSearch', MenuBar=StockLocationMenu)

@expose(format='json')
def StockLocationMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockLocation")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockLocation")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Receipts', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Receipts', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockLocation")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockLocation?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Receipts', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Receipts', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def StockLocationGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockLocation.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		if record.Status == 'deleted':
			display = record.Name()
		else:
			display = record.Name()
		return dict(display=display, record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Quantity':validators.Number(), 'IsConsumed':validators.StringBool(), 'IsSold':validators.StringBool(), 'StockItem':validators.Int(), 'Location':validators.Int(), 'Receipt':validators.Int()})
def StockLocationSave(self, StockItem, Location, Receipt=None, Id='', id='', Quantity=0, IsConsumed=False, IsSold=False, **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockLocation.get(int_id)
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
				#Updating the record
				record.StockItem = StockItem
				record.Location = Location
				record.Receipt = Receipt
				record.Quantity = Quantity
				record.IsConsumed = IsConsumed
				record.IsSold = IsSold
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvStockLocation(StockItem=StockItem, Location=Location, Receipt=Receipt, Quantity=Quantity, IsConsumed=IsConsumed, IsSold=IsSold, Status='')
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
def StockLocationDel(Id, id='', **kw):
	"""	StockLocation is never really deleted.  It's always just marked as deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockLocation.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			if record.ReceiptID == None:
				record.destroySelf()
				result_msg = "Record deleted"
			else:
				record.Status = 'deleted'
				result_msg = "Record marked deleted"
			result=1
		else:
			result=0
			result_msg="Couldn't find the record"
	except:
		result=0
		result_msg = "Failed to modify the record"
		raise
	return dict(result=result, result_msg=result_msg)
			
@expose(format='json')
def StockLocationUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockLocation.get(int_id)
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
def StockLocationMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockLocation.get(int_id)
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
					if ColName == 'TransfersFromHere':
						line_text = item.Name()
					elif ColName == 'TransfersToHere':
						line_text = item.Name()
					elif ColName == 'Compounds':
						line_text = item.Name()
					else:
						line_text = 'UNKNOWN: column name "%s" not found' % ColName
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def StockLocationSearch(self, Name='', StockItemName='', LocationName='', CustomerName='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvStockItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvStockItem.q.id == model.InvStockLocation.q.StockItemID,"
	if StockItemName != '':
		qArgs+="model.InvStockItem.q.Name.contains('"+ StockItemName + "'),"
		qArgs+="model.InvStockItem.q.id == model.InvStockLocation.q.StockItemID,"
	if LocationName != '':
		qArgs+="model.InvLocation.q.Name.contains('"+ LocationName + "'),"
		qArgs+="model.InvStockLocation.q.LocationID == model.InvLocation.q.id,"
	if CustomerName != '':
		qArgs+="model.InvCustomer.q.Name.contains('"+ CustomerName + "'),"
		qArgs+="model.InvCustomer.q.id == model.InvReceipt.q.CustomerID,"
		qArgs+="model.InvReceipt.q.id == model.InvStockLocation.q.ReceiptID,"
	if len(qArgs) > 0:
		items = eval('model.InvStockLocation.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvStockLocation.select()
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
