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
def POItems(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvPOItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Notes_data = record.Notes
		QuantityRequested_data = str(record.QuantityRequested)
		QuantityReceived_data = str(record.QuantityReceived)
		QuotePrice_data = str(record.QuotePrice)
		ActualPrice_data = str(record.ActualPrice)
		#ForeignKeys
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
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Notes_data = ''
		QuantityRequested_data = ''
		QuantityReceived_data = ''
		QuotePrice_data = ''
		ActualPrice_data = ''
		#ForeignKeys
		PurchaseOrder_data = ''
		PurchaseOrder_display = 'None'
		CatalogItem_data = ''
		CatalogItem_display = 'None'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="poi_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="poi_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	Notes = dict(id="poi_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	QuotePrice = dict(id="poi_QuotePrice", name="QuotePrice", label="Quote price", type="Currency",attr=dict(length=50), data=QuotePrice_data)
	ActualPrice = dict(id="poi_ActualPrice", name="ActualPrice", label="Actual price", type="Currency",attr=dict(length=50), data=ActualPrice_data)
	QuantityRequested = dict(id="poi_QuantityRequested", name="QuantityRequested", label="Quantity requested", type="Numeric",attr=dict(length=50), data=QuantityRequested_data)
	QuantityReceived = dict(id="poi_QuantityReceived", name="QuantityReceived", label="Quantity received", type="Numeric",attr=dict(length=50), data=QuantityReceived_data)
	#ForeignKeys
	SrchPOVendorName = dict(id="poi_SrchPOVendorName", name="VendorName", label="Vendor name", type="String",attr=dict(length=25), data='')
	PurchaseOrder = dict(id="poi_PurchaseOrder", name="PurchaseOrder", label="Purchase order", type="ForeignKey",attr=dict(srchUrl="PurchaseOrderSearch",lookupUrl="PurchaseOrderGet", edit_url='PurchaseOrder', srchFields=[SrchPOVendorName]), data=PurchaseOrder_data, init_display=PurchaseOrder_display)
	SrchCatalogName = dict(id="poi_SrchCatalogName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	CatalogItem = dict(id="poi_CatalogItem", name="CatalogItem", label="Catalog item", type="ForeignKey",attr=dict(srchUrl="CatalogItemSearch",lookupUrl="CatalogItemGet", edit_url='CatalogItem', srchFields=[SrchCatalogName]), data=CatalogItem_data, init_display=CatalogItem_display)
	#Fields
	fields = [Id, Name, Notes, QuotePrice, ActualPrice, QuantityRequested, QuantityReceived, PurchaseOrder, CatalogItem]
	#Configure any of the links that might need configuring
	if id == '':
		POItemsMenu = 'POItemsMenu'
	else:
		POItemsMenu = 'POItemsMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='POItems', Label='Puchase order items entry', Fields=fields, FieldsSrch=[Name], Read='POItems', Add='POItemsSave', Del='POItemsDel', UnDel='POItemsUnDel', Edit='POItems', Save='POItemsSave', SrchUrl='POItemsSearch', MenuBar=POItemsMenu)

@expose(format='json')
def POItemsMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("POItems")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("POItems")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("POItems")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("POItems?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def POItemsGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPOItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Notes':validators.String(), 'QuantityRequested':validators.Number(), 'QuantityReceived':validators.Number(), 'QuotePrice':validators.Number(), 'ActualPrice':validators.Number(), 'PurchaseOrder':validators.Int(), 'CatalogItem':validators.Int()})
def POItemsSave(self, PurchaseOrder, CatalogItem, Id='', id='', ActualPrice=0.0, QuotePrice=0.0, QuantityReceived=0, QuantityRequested=0, Notes='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPOItems.get(int_id)
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
				record.QuantityRequested = QuantityRequested
				record.Notes = Notes
				record.QuantityReceived = QuantityReceived
				record.QuotePrice = QuotePrice
				record.ActualPrice = ActualPrice
				record.CatalogItem = CatalogItem
				record.PurchaseOrder = PurchaseOrder
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvPOItems(CatalogItemID=CatalogItem, PurchaseOrderID=PurchaseOrder, ActualPrice=ActualPrice, QuotePrice=QuotePrice, Notes=Notes, QuantityReceived=QuantityReceived, QuantityRequested=QuantityRequested, Status='')
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
def POItemsDel(Id, id='', **kw):
	"""	If the POItems has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPOItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#No references for these objects, so I'll delete completely
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
def POItemsMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvPOItems.get(int_id)
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
					line_text = 'Something'
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def POItemsSearch(self, Name='',CatalogItemName='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvCatalogItem.q.Name.contains('"+ Name + "'),"
	if CatalogItemName != '':
		qArgs+="model.InvCatalogItem.q.Name.contains('"+ CatalogItemName + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvPOItems.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvPOItems.select()
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
