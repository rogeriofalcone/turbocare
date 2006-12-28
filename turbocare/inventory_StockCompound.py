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
def StockCompound(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockCompound.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		DateProduced_data = record.DateProduced
		#ForeignKeys
		try:
			CatalogCompound_data = record.CatalogCompound.id
			CatalogCompound_display = record.CatalogCompound.Name + ' ('+str(record.CatalogCompound.id)+')'
		except AttributeError: 
			CatalogCompound_data = ''	
			CatalogCompound_display = 'None'
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are ' + str(len(record.StockItems)) + ' records'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		DateProduced_data = ''
		#ForeignKeys
		CatalogCompound_data = ''	
		CatalogCompound_display = 'None'
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="sc_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="sc_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	DateProduced = dict(id="sc_DateProduced", name="DateProduced", label="Date produced", type="DateTime",attr=dict(), data=DateProduced_data)
	#ForeignKeys
	SrchCatalogCompoundName = dict(id="sc_SrchCatalogCompoundName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	CatalogCompound = dict(id="sc_CatalogCompound", name="CatalogCompound", label="Catalog compound", type="ForeignKey",attr=dict(srchUrl="CatalogCompoundSearch",lookupUrl="CatalogCompoundGet", edit_url='CatalogCompound', srchFields=[SrchCatalogCompoundName]), data=CatalogCompound_data, init_display=CatalogCompound_display)
	#MultiJoin
	StockItems = dict(id="sc_StockItems", name="StockItems", label="Stock items", type="MultiJoin",attr=dict(displayUrl="StockCompoundMultiJoinList",listUrl="StockCompoundMultiJoinList",linkUrl="StockItemQty"), data=StockItems_data)
	#Fields
	fields = [Id, Name, DateProduced, CatalogCompound, StockItems]
	#Configure any of the links that might need configuring
	if id == '':
		StockCompoundMenu = 'StockCompoundMenu'
	else:
		StockCompoundMenu = 'StockCompoundMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='StockCompound', Label='Stock compound entry', Fields=fields, FieldsSrch=[Name], Read='StockCompound', Add='StockCompoundSave', Del='StockCompoundDel', UnDel='StockCompoundUnDel', Edit='StockCompound', Save='StockCompoundSave', SrchUrl='StockCompoundSearch', MenuBar=StockCompoundMenu)

@expose(format='json')
def StockCompoundMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockCompound")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockCompound")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockCompound")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockCompound?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def StockCompoundGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockCompound.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'DateProduced':validators.String(),  'CatalogCompound':validators.Int()})
def StockCompoundSave(self, CatalogCompound, Id='', id='', DateProduced='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockCompound.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if DateProduced != '':
		if len(DateProduced) > 10:
			DateProduced = datetime.fromtimestamp(time.mktime(time.strptime(DateProduced,'%Y-%m-%d %H:%M')))
		else:
			DateProduced = datetime.fromtimestamp(time.mktime(time.strptime(DateProduced,'%Y-%m-%d')))
		
	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				#Updating the record
				record.DateProduced = DateProduced
				record.CatalogCompound = CatalogCompound
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvStockCompound(DateProduced=DateProduced, CatalogCompound=CatalogCompound, Status='')
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
def StockCompoundDel(Id, id='', **kw):
	"""	If the StockCompound has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockCompound.get(int_id)
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
def StockCompoundUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockCompound.get(int_id)
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
def StockCompoundMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockCompound.get(int_id)
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
						line_text = item.item.Name()
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def StockCompoundSearch(self, Name='', CatalogCompoundName='', DateProduced='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvCatalogCompound.q.Name.contains('"+ Name + "'),"
	if CatalogCompoundName != '':
		qArgs+="model.InvCatalogCompound.q.Name.contains('"+ CatalogCompoundName + "'),"
	if DateProduced != '':
		qArgs+="model.InvStockItem.q.DateProduced.contains('"+ DateProduced + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvStockItem.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvCatalogCompound.select()
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
