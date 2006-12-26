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
def StockTransferRequestItem(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockTransferRequestItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Notes_data = record.Notes
		Qty_data = str(record.Qty)
		IsTransferred_data = record.IsTransferred
		IsOnOrder_data = record.IsOnOrder
		#ForeignKeys
		try:
			StockTransferRequest_data = record.StockTransferRequest.id
			StockTransferRequest_display = record.StockTransferRequest.Name()
		except AttributeError: 
			StockTransferRequest_data = ''
			StockTransferRequest_display = 'None'
		try:
			PurchaseOrder_data = record.PurchaseOrder.id
			PurchaseOrder_display = record.PurchaseOrder.Name() + ' ('+str(record.PurchaseOrder.id)+')'
		except AttributeError: 
			PurchaseOrder_data = ''
			PurchaseOrder_display = 'None'
		try:
			CatalogItem_data = record.CatalogItem.id
			CatalogItem_display = record.CatalogItem.Name + ' ('+str(record.CatalogItem.id)+')'
		except AttributeError: 
			CatalogItem_data = ''
			CatalogItem_display = 'None'
		#MultiJoins
		StockTransfers_data = 'There are ' + str(len(record.StockTransfers)) + ' records'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Notes_data = ''
		IsTransferred_data = ''
		IsOnOrder_data = ''
		Qty_data = ''
		#ForeignKeys
		StockTransferRequest_data = ''
		StockTransferRequest_display = 'None'
		PurchaseOrder_data = ''
		PurchaseOrder_display = 'None'
		CatalogItem_data = ''
		CatalogItem_display = 'None'
		StockTransfers_data = ''
		StockTransfers_display = 'None'
		#MultiJoin and RelatedJoin
		StockTransfer_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#MultiJoin and RelatedJoin
		StockTransfers_data = 'There are no records'
		#regular fields
		Name_data = ''
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="stri_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="stri_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	Notes = dict(id="stri_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	Qty = dict(id="stri_Qty", name="Qty", label="Qty", type="Numeric",attr=dict(length=50), data=Qty_data)
	IsTransferred = dict(id="ci_IsTransferred", name="IsTransferred", label="Is transferred",type="Bool",attr={}, data=IsTransferred_data)
	IsOnOrder = dict(id="ci_IsOnOrder", name="IsOnOrder", label="Is on order",type="Bool",attr={}, data=IsOnOrder_data)
	#ForeignKeys
	SrchTransferLocationName = dict(id="stri_SrchTransferLocationName", name="LocationName", label="Location name", type="String",attr=dict(length=25), data='')
	StockTransferRequest = dict(id="stri_StockTransferRequest", name="StockTransferRequest", label="Stock transfer request", type="ForeignKey",attr=dict(srchUrl="StockTransferRequestSearch",lookupUrl="StockTransferRequestGet", edit_url='StockTransferRequest', srchFields=[SrchTransferLocationName]), data=StockTransferRequest_data, init_display=StockTransferRequest_display)
	SrchPOVendor = dict(id="stri_SrchPOVendor", name="Name", label="Vendor name", type="String",attr=dict(length=25), data='')
	PurchaseOrder = dict(id="stri_PurchaseOrder", name="PurchaseOrder", label="Purchase order", type="ForeignKey",attr=dict(srchUrl="PurchaseOrderSearch",lookupUrl="PurchaseOrderGet", edit_url='PurchaseOrderRequest', srchFields=[SrchPOVendor]), data=PurchaseOrder_data, init_display=PurchaseOrder_display)
	SrchCatalogItem = dict(id="stri_SrchCatalogItem", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	CatalogItem = dict(id="stri_CatalogItem", name="CatalogItem", label="Catalog item", type="ForeignKey",attr=dict(srchUrl="CatalogItemSearch",lookupUrl="CatalogItemGet", edit_url='CatalogItem', srchFields=[SrchCatalogItem]), data=CatalogItem_data, init_display=CatalogItem_display)
	#MultiJoins
	StockTransfers = dict(id="st_StockTransfers", name="StockTransfers", label="Stock transfers", type="MultiJoin",attr=dict(displayUrl="StockTransferRequestItemMultiJoinList",listUrl="StockTransferRequestItemMultiJoinList",linkUrl="StockTransfer"), data=StockTransfers_data)
	#Fields
	fields = [Id, Name, StockTransferRequest, CatalogItem, Qty, IsTransferred, StockTransfers, Notes, IsOnOrder, PurchaseOrder]
	#Configure any of the links that might need configuring
	if id == '':
		StockTransferRequestItemMenu = 'StockTransferRequestItemMenu'
	else:
		StockTransferRequestItemMenu = 'StockTransferRequestItemMenu?id=' + id
	#Special search fields
	SrchLocationName  = dict(id="stri_SrchLocationName", name="ForLocationName", label="Location name", type="String",attr=dict(length=25), data='')
	#RETURN VALUES HERE
	return dict(id=id, Name='StockTransferRequestItem', Label='Stock transfer request item entry', Fields=fields, FieldsSrch=[SrchLocationName], Read='StockTransferRequestItem', Add='StockTransferRequestItemSave', Del='StockTransferRequestItemDel', UnDel='StockTransferRequestItemUnDel', Edit='StockTransferRequestItem', Save='StockTransferRequestItemSave', SrchUrl='StockTransferRequestItemSearch', MenuBar=StockTransferRequestItemMenu)

@expose(format='json')
def StockTransferRequestItemMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockTransferRequestItem")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockTransferRequestItem")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockTransferRequestItem")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockTransferRequestItem?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def StockTransferRequestItemGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransferRequestItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)

@expose(format='json')
def StockTransferRequestItemMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockTransferRequestItem.get(int_id)
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
					if ColName == 'StockTransfers':
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
@validate(validators={'Id':validators.String(),'id':validators.String(), 'IsTransferred':validators.StringBool(), 'IsOnOrder':validators.StringBool(), 'Qty':validators.Number(), 'Notes':validators.String(), 'StockTransferRequest':validators.Int(), 'PurchaseOrder':validators.Int(), 'CatalogItem':validators.Int()})
def StockTransferRequestItemSave(self, StockTransferRequest, CatalogItem, PurchaseOrder=None, Id='', id='', Qty=0, Notes='', IsOnOrder=False, IsTransferred=False, **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransferRequestItem.get(int_id)
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
				record.CatalogItem = CatalogItem
				record.PurchaseOrder = PurchaseOrder
				record.StockTransferRequest = StockTransferRequest
				record.Notes = Notes
				record.Qty = Qty
				record.IsOnOrder = IsOnOrder
				record.IsTransferred = IsTransferred
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvStockTransferRequestItem(CatalogItem=CatalogItem, PurchaseOrder=PurchaseOrder, StockTransferRequest=StockTransferRequest, Notes=Notes, Qty=Qty, IsOnOrder=IsOnOrder, IsTransferred=IsTransferred, Status='')
			result_msg = "Record added"
			result = 1
		#Run checks for transfer completions
		record.CheckAllComplete()
		record_id = record.id
	except:
		result = 0
		result_msg="Operation failed!"
		record_id = ''
		raise
	return dict(result=result, result_msg=result_msg, id=record_id)
	
@expose(format='json')
def StockTransferRequestItemDel(Id, id='', **kw):
	"""	If the StockTransferRequestItem has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransferRequestItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			record.destroySelf()
			result=1
			result_msg = "Record deleted"
		else:
			result=0
			result_msg="Couldn't find the record"
	except:
		result=0
		result_msg = "Failed to modify the record"
		raise
	return dict(result=result, result_msg=result_msg)
			
@expose(format='json')
def StockTransferRequestItemSearch(self, Name='', CatalogItemName='', ForLocationName='', field_num='', id='', show_del=True, **kw):
	qArgs = ""
	if CatalogItemName!="":
		Name = CatalogItemName
	if Name != '':
		qArgs+="model.InvCatalogItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvCatalogItem.q.id == model.InvStockTransferRequestItem.q.CatalogItemID,"
	if ForLocationName != '':
		qArgs+="model.InvLocation.q.Name.contains('"+ ForLocationName + "'),"
		qArgs+="model.InvStockTransferRequest.q.ForLocationID == model.InvLocation.q.id,"
		qArgs+="model.InvStockTransferRequestItem.q.StockTransferRequestID == model.InvStockTransferRequest.q.id,"
	if id != '':
		qArgs+="model.InvStockTransferRequestItem.q.StockTransferRequestID == " + id + ","
	if len(qArgs) > 0:
		items = eval('model.InvStockTransferRequestItem.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvStockTransferRequestItem.select()
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
