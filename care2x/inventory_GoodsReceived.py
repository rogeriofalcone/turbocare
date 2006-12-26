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
def GoodsReceived(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvGoodsReceived.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Notes_data = record.Notes
		DateReceived_data = record.DateReceived
		#ForeignKeys
		try:
			PurchaseOrder_data = record.PurchaseOrderID
			PurchaseOrder_display = record.PurchaseOrder.Name() + ' ('+str(record.PurchaseOrderID)+')'
		except AttributeError: 
			PurchaseOrder_data = ''
			PurchaseOrder_display = 'None'
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are ' + str(len(record.StockItems)) + ' records'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Notes_data = ''
		DateReceived_data = ''
		#ForeignKeys
		PurchaseOrder_data = ''
		PurchaseOrder_display = 'None'
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="gr_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="gr_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	DateReceived = dict(id="gr_DateReceived", name="DateReceived", label="Date received", type="DateTime",attr=dict(), data=DateReceived_data)
	Notes = dict(id="gr_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	#ForeignKeys
	SrchVendorName = dict(id="gr_SrchVendorName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	PurchaseOrder = dict(id="gr_PurchaseOrder", name="PurchaseOrder", label="Purchase order", type="ForeignKey",attr=dict(srchUrl="PurchaseOrderSearch",lookupUrl="PurchaseOrderGet", edit_url='PurchaseOrder', srchFields=[SrchVendorName]), data=PurchaseOrder_data, init_display=PurchaseOrder_display)
	#MultiJoin
	StockItems = dict(id="gr_StockItems", name="StockItems", label="Stock items", type="MultiJoin",attr=dict(displayUrl="GoodsReceivedMultiJoinList",listUrl="GoodsReceivedMultiJoinList",linkUrl="StockItem"), data=StockItems_data)
	#Fields
	fields = [Id, Name, DateReceived, Notes, PurchaseOrder, StockItems]
	#Configure any of the links that might need configuring
	if id == '':
		GoodsReceivedMenu = 'GoodsReceivedMenu'
	else:
		GoodsReceivedMenu = 'GoodsReceivedMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='GoodsReceived', Label='Goods received entry', Fields=fields, FieldsSrch=[Name], Read='GoodsReceived', Add='GoodsReceivedSave', Del='GoodsReceivedDel', UnDel='GoodsReceivedUnDel', Edit='GoodsReceived', Save='GoodsReceivedSave', SrchUrl='GoodsReceivedSearch', MenuBar=GoodsReceivedMenu)

@expose(format='json')
def GoodsReceivedMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("GoodsReceived")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("GoodsReceived")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("GoodsReceived")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("GoodsReceived?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def GoodsReceivedGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGoodsReceived.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'DateReceived':validators.String(), 'Notes':validators.String(), 'PurchaseOrder':validators.Int()})
def GoodsReceivedSave(self, PurchaseOrder, Id='', id='', DateReceived='', Notes='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGoodsReceived.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if DateReceived != '':
		if len(DateReceived) > 10:
			DateReceived = datetime.fromtimestamp(time.mktime(time.strptime(DateReceived,'%Y-%m-%d %H:%M')))
		else:
			DateReceived = datetime.fromtimestamp(time.mktime(time.strptime(DateReceived,'%Y-%m-%d')))
		
	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				#Updating the record
				record.PurchaseOrder = PurchaseOrder
				record.Notes = Notes
				record.DateReceived = DateReceived
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvGoodsReceived(DateReceived=DateReceived, PurchaseOrder=PurchaseOrder, Notes=Notes, Status='')
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
def GoodsReceivedDel(Id, id='', **kw):
	"""	If the GoodsReceived has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGoodsReceived.get(int_id)
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
def GoodsReceivedUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGoodsReceived.get(int_id)
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
def GoodsReceivedMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvGoodsReceived.get(int_id)
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
					if ColName == 'StockItems':
						line_text = item.GRName()
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def GoodsReceivedSearch(self, Name='', VendorName='', ValidOn='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.PurchaseOrder.q.Vendor.Name.contains('"+ Name + "'),"
	if VendorName != '':
		qArgs+="model.PurchaseOrder.q.Vendor.Name.contains('"+ VendorName + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvGoodsReceived.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvGoodsReceived.select()
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
