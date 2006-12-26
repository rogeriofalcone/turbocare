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
def CatalogCompoundQty(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCatalogCompoundQty.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Description_data = record.Description
		Qty_data = str(record.Qty)
		#ForeignKeys
		try:
			CatalogItem_data = record.CatalogItem.id
			CatalogItem_display = record.CatalogItem.Name + ' ('+str(record.CatalogItem.id)+')'
		except AttributeError: 
			CatalogItem_data = ''
			CatalogItem_display = 'None'
		try:
			CatalogCompound_data = record.CatalogCompound.id
			CatalogCompound_display = record.CatalogCompound.Name + ' ('+str(record.CatalogCompound.id)+')'
		except AttributeError: 
			CatalogCompound_data = ''
			CatalogCompound_display = 'None'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Description_data = ''
		Qty_data = ''
		#ForeignKeys
		CatalogItem_data = ''
		CatalogItem_display = 'None'
		CatalogCompound_data = ''
		CatalogCompound_display = 'None'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="ccq_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="ccq_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	Qty = dict(id="ccq_Qty", name="Qty", label="Qty", type="Numeric",attr=dict(), data=Qty_data)
	Description = dict(id="ccq_Description", name="Description", label="Description", type="Text",attr=dict(cols=40,rows=3), data=Description_data)
	#ForeignKeys
	SrchCompoundName = dict(id="ccq_SrchCompoundName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	CatalogCompound = dict(id="ccq_CatalogCompound", name="CatalogCompound", label="Catalog compound", type="ForeignKey",attr=dict(srchUrl="CatalogCompoundSearch",lookupUrl="CatalogCompoundGet", edit_url='CatalogCompound', srchFields=[SrchCompoundName]), data=CatalogCompound_data, init_display=CatalogCompound_display)
	SrchCatalogItemName = dict(id="ccq_CatalogItem", name="Name", label="Catalog item", type="String",attr=dict(length=25), data='')
	CatalogItem = dict(id="ccq_CatalogItem", name="CatalogItem", label="Catalog item", type="ForeignKey",attr=dict(srchUrl="CatalogItemSearch",lookupUrl="CatalogItemGet", edit_url='CatalogItemRequest', srchFields=[SrchCatalogItemName]), data=CatalogItem_data, init_display=CatalogItem_display)
	#Fields
	fields = [Id, Name, Qty, Description, CatalogCompound, CatalogItem]
	#Configure any of the links that might need configuring
	if id == '':
		CatalogCompoundQtyMenu = 'CatalogCompoundQtyMenu'
	else:
		CatalogCompoundQtyMenu = 'CatalogCompoundQtyMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='CatalogCompoundQty', Label='Catalog compound qty entry', Fields=fields, FieldsSrch=[Name], Read='CatalogCompoundQty', Add='CatalogCompoundQtySave', Del='CatalogCompoundQtyDel', UnDel='CatalogCompoundQtyUnDel', Edit='CatalogCompoundQty', Save='CatalogCompoundQtySave', SrchUrl='CatalogCompoundQtySearch', MenuBar=CatalogCompoundQtyMenu)

@expose(format='json')
def CatalogCompoundQtyMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("CatalogCompoundQty")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("CatalogCompoundQty")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("CatalogCompoundQty")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("CatalogCompoundQty?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def CatalogCompoundQtyGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogCompoundQty.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Qty':validators.Number(), 'Description':validators.String(), 'CatalogCompound':validators.Int(), 'CatalogItem':validators.Int()})
def CatalogCompoundQtySave(self, CatalogCompound, CatalogItem, Id='', id='', Qty=0, Description='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogCompoundQty.get(int_id)
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
				record.Description = Description
				record.CatalogCompound = CatalogCompound
				record.CatalogItem = CatalogItem
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvCatalogCompoundQty(CatalogItem=CatalogItem, CatalogCompound=CatalogCompound, Description=Description, Qty=Qty, Status='')
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
def CatalogCompoundQtyDel(Id, id='', **kw):
	"""	If the CatalogCompoundQty has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogCompoundQty.get(int_id)
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
def CatalogCompoundQtySearch(self, Name='', CatalogItemName='', CompoundName='', id='', Id='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Id != '':
		id = Id
	if  id != '':
		qArgs+="model.InvCatalogCompoundQty.q.CatalogCompoundID == " + id + ","
	if Name != '':
		qArgs+="model.InvCatalogCompound.q.Name.contains('"+ Name + "'),"
	if CompoundName != '':
		qArgs+="model.InvCatalogCompound.q.Name.contains('"+ CompoundName + "'),"
	if CatalogItemName != '':
		qArgs+="model.InvCatalogItem.q.contains('"+ CatalogItemName + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvCatalogCompoundQty.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvCatalogCompoundQty.select()
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
