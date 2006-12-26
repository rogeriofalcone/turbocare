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
def StockCompoundQty(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockCompoundQty.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Qty_data = str(record.Qty)
		#ForeignKeys
		try:
			StockLocation_data = record.StockLocation.id
			StockLocation_display = record.StockLocation.Name() + ' ('+str(record.StockLocation.id)+')'
		except AttributeError: 
			StockLocation_data = ''
			StockLocation_display = 'None'
		try:
			StockCompound_data = record.StockCompound.id
			StockCompound_display = record.StockCompound.Name + ' ('+str(record.StockCompound.id)+')'
		except AttributeError: 
			StockCompound_data = ''
			StockCompound_display = 'None'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Notes_data = ''
		ValidOn_data = ''
		#ForeignKeys
		StockLocation_data = ''
		StockLocation_display = 'None'
		StockCompound_data = ''
		StockCompound_display = 'None'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#ForeignKeys
		StockLocation_data = ''
		StockLocation_display = 'None'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="scq_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="scq_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	Qty = dict(id="scq_Qty", name="Qty", label="Qty", type="Numeric",attr=dict(length=50), data=Qty_data)
	#ForeignKeys
	SrchStockLocationName = dict(id="scq_SrchStockItemName", name="StockItemName", label="Stock name", type="String",attr=dict(length=25), data='')
	StockLocation = dict(id="scq_StockLocation", name="StockLocation", label="Stock location", type="ForeignKey",attr=dict(srchUrl="StockLocationSearch",lookupUrl="StockLocationGet", edit_url='StockLocation', srchFields=[SrchStockLocationName]), data=StockLocation_data, init_display=StockLocation_display)
	SrchStockCompoundName = dict(id="scq_SrchStockCompoundName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	StockCompound = dict(id="scq_StockCompound", name="StockCompound", label="Stock compound", type="ForeignKey",attr=dict(srchUrl="StockCompoundSearch",lookupUrl="StockCompoundGet", edit_url='StockCompound', srchFields=[SrchStockCompoundName]), data=StockCompound_data, init_display=StockCompound_display)
	#Fields
	fields = [Id, Name, Qty, StockLocation, StockCompound]
	#Configure any of the links that might need configuring
	if id == '':
		StockCompoundQtyMenu = 'StockCompoundQtyMenu'
	else:
		StockCompoundQtyMenu = 'StockCompoundQtyMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='StockCompoundQty', Label='Stock compound Qty entry', Fields=fields, FieldsSrch=[Name], Read='StockCompoundQty', Add='StockCompoundQtySave', Del='StockCompoundQtyDel', UnDel='StockCompoundQtyUnDel', Edit='StockCompoundQty', Save='StockCompoundQtySave', SrchUrl='StockCompoundQtySearch', MenuBar=StockCompoundQtyMenu)

@expose(format='json')
def StockCompoundQtyMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockCompoundQty")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockCompoundQty")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockCompoundQty")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockCompoundQty?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def StockCompoundQtyGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockCompoundQty.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Qty':validators.Number(), 'StockLocation':validators.Int(), 'StockCompound':validators.Int()})
def StockCompoundQtySave(self, StockItem, StockCompound, Id='', id='', Qty=0, **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockCompoundQty.get(int_id)
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
				record.StockLocation = StockLocation
				record.StockCompound = StockCompound
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvStockCompoundQty(StockCompound=StockCompound, StockLocation=StockLocation, Qty=Qty, Status='')
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
def StockCompoundQtyDel(Id, id='', **kw):
	"""	If the StockCompoundQty has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockCompoundQty.get(int_id)
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
def StockCompoundQtySearch(self, Name='', StockName='', CompoundName='', field_num='', show_del=True, **kw):
	qArgs = ""
	# Both StockName and Name search for the stock item which is consumed in making the final product
	if StockName != '':
		Name = StockName
	if Name != '':
		qArgs+="model.InvStockItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvStockItem.q.id == model.InvStockLocation.q.StockItemID,"
		qArgs+="model.InvStockLocation.q.id == model.InvStockCompoundQty.q.StockLocationID,"
	if CompoundName != '':
		qArgs+="model.InvStockItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvStockItem.q.id == model.InvStockCompoundQty.q.StockCompoundID,"
	if len(qArgs) > 0:
		items = eval('model.InvStockCompoundQty.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvStockCompoundQty.select()
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
