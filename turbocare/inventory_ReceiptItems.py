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
def ReceiptItems(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvReceiptItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		UnitCost_data = str(record.UnitCost)
		Discount_data = str(record.Discount)
		Quantity_data = str(record.Quantity)
		#ForeignKeys
		try:
			Receipt_data = record.ReceiptID
			Receipt_display = record.Receipt.Name() + ' ('+str(record.ReceiptID)+')'
		except AttributeError: 
			Receipt_data = ''
			Receipt_display = 'None'
		try:
			CatalogItem_data = record.CatalogItemID
			CatalogItem_display = record.CatalogItem.Name + ' ('+str(record.CatalogItemID)+')'
		except AttributeError: 
			CatalogItem_data = ''
			CatalogItem_display = 'None'
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are ' + str(len(record.StockItems)) + ' records'
	else:
		Id_data = ''
		Name_data = ''
		UnitCost_data = ''
		Discount_data = ''
		Quantity_data = ''
		#ForeignKeys
		Receipt_data = ''
		Receipt_display = 'None'
		CatalogItem_data = ''
		CatalogItem_display = 'None'
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="ri_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="ri_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	UnitCost = dict(id="ri_UnitCost", name="UnitCost", label="Unit cost", type="Currency",attr=dict(), data=UnitCost_data)
	Discount = dict(id="ri_Discount", name="Discount", label="Discount", type="Currency",attr=dict(), data=Discount_data)
	Quantity = dict(id="ri_Quantity", name="Quantity", label="Quantity", type="Currency",attr=dict(), data=Quantity_data)
	#ForeignKeys
	SrchCustomerName = dict(id="ri_SrchCustomerName", name="Name", label="Customer name", type="String",attr=dict(length=25), data='')
	Receipt = dict(id="ri_Receipt", name="Receipt", label="Receipt", type="ForeignKey",attr=dict(srchUrl="ReceiptSearch",lookupUrl="ReceiptGet", edit_url='Receipt', srchFields=[SrchCustomerName]), data=Receipt_data, init_display=Receipt_display)
	SrchCatalogItemName = dict(id="ri_SrchCatalogItemName", name="Catalog item name", label="Name", type="String",attr=dict(length=25), data='')
	CatalogItem = dict(id="ri_CatalogItem", name="CatalogItem", label="Catalog item", \
		type="ForeignKey",attr=dict(srchUrl="CatalogItemSearch",lookupUrl="CatalogItemGet", edit_url='CatalogItem', \
		srchFields=[SrchCatalogItemName]), data=CatalogItem_data, init_display=CatalogItem_display)
	#MultipleJoin
	StockItems = dict(id="ri_StockItems", name="StockItems", label="Stock location items", type="MultiJoin",attr=dict(displayUrl="ReceiptItemsMultiJoinList",listUrl="ReceiptItemsMultiJoinList",linkUrl="StockLocation"), data=StockItems_data)
	#Fields
	fields = [Id, Name, Receipt, CatalogItem, StockItems, UnitCost, Discount, Quantity]
	#Configure any of the links that might need configuring
	if id == '':
		ReceiptItemsMenu = 'ReceiptItemsMenu'
	else:
		ReceiptItemsMenu = 'ReceiptItemsMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='ReceiptItems', Label='Receipt items entry', Fields=fields, FieldsSrch=[Name], Read='ReceiptItems', Add='ReceiptItemsSave', Del='ReceiptItemsDel', UnDel='ReceiptItemsUnDel', Edit='ReceiptItems', Save='ReceiptItemsSave', SrchUrl='ReceiptItemsSearch', MenuBar=ReceiptItemsMenu)

@expose(format='json')
def ReceiptItemsMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("ReceiptItems")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("ReceiptItems")')])
		mView = dict(label='View', url='javascript:inv.openObjView()')
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Report 1', url=''), dict(label='Report 2', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("ReceiptItems")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("ReceiptItems?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()')
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Report 1', url=''), dict(label='Report 2', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def ReceiptItemsGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvReceiptItems.get(int_id)
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
@validate(validators={'Id':validators.String(),'id':validators.String(), 'UnitCost':validators.Number(), 'Discount':validators.Number(), 'Quantity':validators.Number(), 'CatalogItem':validators.Int(), 'Receipt':validators.Int()})
def ReceiptItemsSave(self, Receipt, CatalogItem, Id='', id='', UnitCost=0.0, Discount=0.0, Quantity=0.0, **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvReceiptItems.get(int_id)
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
				record.Receipt = Receipt
				record.CatalogItem = CatalogItem
				record.UnitCost = UnitCost
				record.Discount = Discount
				record.Quantity = Quantity
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvReceiptItems(Receipt=Receipt, CatalogItem=CatalogItem, UnitCost=UnitCost, \
				Discount=Discount, Quantity=Quantity)
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
def ReceiptItemsDel(Id, id='', **kw):
	"""	If the ReceiptItems has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvReceiptItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.StockItems)) == 0:
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
def ReceiptItemsUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvReceiptItems.get(int_id)
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
def ReceiptItemsMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvReceiptItems.get(int_id)
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
					line_text = 'UNKNOWN'
					if ColName == 'StockItems':
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
def ReceiptItemsSearch(self, Name='', CatalogItemName='', CustomerName='', field_num='', show_del=True, **kw):
	qArgs = ""
	if CatalogItemName != '':
		Name = CatalogItemName
	if Name != '':
		qArgs+="model.InvCatalogItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvCatalogItem.q.id == model.InvReceiptItems.q.CatalogItemID,"
	if CustomerName != '':
		qArgs+="model.InvCustomer.q.Name.contains('"+ CustomerName + "'),"
		qArgs+="model.InvCustomer.q.id == model.InvReceipt.q.CustomerID,"
		qArgs+="model.InvReceipt.q.id == model.InvReceiptItems.q.ReceiptID,"
	if len(qArgs) > 0:
		items = eval('model.InvReceiptItems.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvReceiptItems.select()
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Name()
				results.append({'id':item.id, 'text':text, 'Name':item.Name()+' *** MARKED DELETED ***', 'Description':''})
			else:
				text = item.Name()
				results.append({'id':item.id, 'text':text, 'Name':item.Name(), 'Description':''})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			text = item.Name()
			results.append({'id':item.id, 'text':text, 'Name':item.Name(), 'Description':''})
	return dict(results=results, field_num=field_num, items=items)
	

