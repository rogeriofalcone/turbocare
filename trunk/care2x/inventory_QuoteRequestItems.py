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
def QuoteRequestItems(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvQuoteRequestItems.get(int_id)
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
		#ForeignKeys
		try:
			QuoteRequest_data = record.QuoteRequest.id
			QuoteRequest_display = record.QuoteRequest.Name()
		except AttributeError: 
			QuoteRequest_data = ''
			QuoteRequest_display = 'None'
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
		Qty_data = ''
		#ForeignKeys
		QuoteRequest_data = ''
		QuoteRequest_display = 'None'
		CatalogItem_data = ''
		CatalogItem_display = 'None'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#ForeignKeys
		CatalogItem_data = ''
		CatalogItem_display = 'None'
		#MultiJoin and RelatedJoin
		Items_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="qri_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="qri_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	Qty = dict(id="qri_Qty", name="Qty", label="Qty", type="Numeric",attr=dict(), data=Qty_data)
	Notes = dict(id="qri_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	#ForeignKeys
	SrchQRVendor = dict(id="qri_SrchQRVendor", name="VendorName", label="Name", type="String",attr=dict(length=25), data='')
	QuoteRequest = dict(id="qri_QuoteRequest", name="QuoteRequest", label="Quote request", type="ForeignKey",attr=dict(srchUrl="QuoteRequestSearch",lookupUrl="QuoteRequestGet", edit_url='QuoteRequest', srchFields=[SrchQRVendor]), data=QuoteRequest_data, init_display=QuoteRequest_display)
	SrchCatalogItem = dict(id="qri_SrchCatalogItem", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	CatalogItem = dict(id="qri_CatalogItem", name="CatalogItem", label="Catalog item", type="ForeignKey",attr=dict(srchUrl="CatalogItemSearch", lookupUrl="CatalogItemGet", edit_url='CatalogItem', srchFields=[SrchCatalogItem]), data=CatalogItem_data, init_display=CatalogItem_display)
	#Fields
	fields = [Id, Name, Qty, Notes, QuoteRequest, CatalogItem]
	#Configure any of the links that might need configuring
	if id == '':
		QuoteRequestItemsMenu = 'QuoteRequestItemsMenu'
	else:
		QuoteRequestItemsMenu = 'QuoteRequestItemsMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='QuoteRequestItems', Label='Quote request items entry', Fields=fields, FieldsSrch=[Name], Read='QuoteRequestItems', Add='QuoteRequestItemsSave', Del='QuoteRequestItemsDel', UnDel='QuoteRequestItemsUnDel', Edit='QuoteRequestItems', Save='QuoteRequestItemsSave', SrchUrl='QuoteRequestItemsSearch', MenuBar=QuoteRequestItemsMenu)

@expose(format='json')
def QuoteRequestItemsMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("QuoteRequestItems")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("QuoteRequestItems")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("QuoteRequestItems")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("QuoteRequestItems?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def QuoteRequestItemsGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteRequestItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Qty':validators.Int(), 'Notes':validators.String(), 'QuoteRequest':validators.Int(), 'CatalogItem':validators.Int()})
def QuoteRequestItemsSave(self, QuoteRequest, CatalogItem, Id='', id='', Qty='', Notes='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteRequestItems.get(int_id)
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
				record.Qty = Qty
				record.Notes = Notes
				record.QuoteRequest = QuoteRequest
				record.CatalogItem = CatalogItem
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvQuoteRequestItems(CatalogItem=CatalogItem, QuoteRequest=QuoteRequest, Notes=Notes, Qty=Qty, Status='')
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
def QuoteRequestItemsDel(Id, id='', **kw):
	"""	If the QuoteRequestItems has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteRequestItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
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
def QuoteRequestItemsUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteRequestItems.get(int_id)
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
def QuoteRequestItemsMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvQuoteRequestItems.get(int_id)
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
					if ColName != '':
						line_text = ''
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def QuoteRequestItemsSearch(self, Id='', id='', Name='', VendorName='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Id != '':
		id = Id
	if Name != '':
		qArgs+="model.InvQuoteRequestItems.q.CatalogItem.Name.contains('"+ Name + "'),"
	if VendorName != '':
		qArgs+="model.InvVendors.q.Name.contains('"+ VendorName + "'),"
	if id != '':
		qArgs+="model.InvQuoteRequestItems.q.QuoteRequestID == "+ id + ","
	if len(qArgs) > 0:
		items = eval('model.InvQuoteRequestItems.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvQuoteRequestItems.select()
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
