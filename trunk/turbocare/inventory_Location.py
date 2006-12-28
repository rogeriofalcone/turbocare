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
def Location(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvLocation.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name
		if record.Status == 'deleted':
			Name_data += ' *** MARKED DELETED ***'
		Description_data = record.Description
		CanReceive_data = record.CanReceive
		CanSell_data = record.CanSell
		IsStore_data = record.IsStore
		IsConsumed_data = record.IsConsumed
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are ' + str(len(record.StockItems)) + ' records'
		Groups_data = 'There are ' + str(len(record.Groups)) + ' records'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Description_data = ''
		AddressLabel_data = ''
		CanReceive_data = ''
		CanSell_data = ''
		IsStore_data = ''
		IsConsumed_data = ''
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are no records'
		Groups_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#MultiJoin and RelatedJoin
		StockItems_data = 'There are no records'
		Groups_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="l_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="l_Name", name="Name", label="Name", type="String",attr=dict(length=50), data=Name_data)
	Description = dict(id="l_Description", name="Description", label="Description", type="Text",attr=dict(cols=40,rows=4), data=Description_data)
	CanReceive = dict(id="l_CanReceive", name="CanReceive", label="Can receive", type="Bool",attr=dict(), data=CanReceive_data)
	CanSell = dict(id="l_CanSell", name="CanSell", label="Can sell", type="Bool",attr=dict(), data=CanSell_data)
	IsStore = dict(id="l_IsStore", name="IsStore", label="Is store", type="Bool",attr=dict(), data=IsStore_data)
	IsConsumed = dict(id="l_IsConsumed", name="IsConsumed", label="Is consumed", type="Bool",attr=dict(), data=IsConsumed_data)
	#MultiJoin
	StockItems = dict(id="l_StockItems", name="StockItems", label="Stock items", type="MultiJoin",attr=dict(displayUrl="LocationMultiJoinList",listUrl="LocationMultiJoinList",linkUrl="StockLocation"), data=StockItems_data)
	#RelatedJoin
	SrchGrpName = dict(id="l_SrchGrpName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Groups = dict(id="l_Groups", name="Groups", label="Groups", type="RelatedJoin", attr=dict(displayUrl="LocationGroups", listUrl="LocationGroups", srchUrl="GrpLocationSearch", saveUrl='LocationGroupSave', srchFields=[SrchGrpName]), data=Groups_data)
	#Fields
	fields = [Id, Name, Description, CanReceive, CanSell, IsConsumed, IsStore, StockItems, Groups]
	#Configure any of the links that might need configuring
	if id == '':
		LocationMenu = 'LocationMenu'
	else:
		LocationMenu = 'LocationMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='Location', Label='Location entry', Fields=fields, FieldsSrch=[Name], Read='Location', Add='LocationSave', Del='LocationDel', UnDel='LocationUnDel', Edit='Location', Save='LocationSave', SrchUrl='LocationSearch', MenuBar=LocationMenu)

@expose(format='json')
def LocationMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("Location")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("Location")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='Transfers', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("Location")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("Location?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='Transfers', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def LocationGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvLocation.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		if record.Status == 'deleted':
			display = record.Name + ' ('+str(record.id)+') **MARKED DELETED***'
		else:
			display = record.Name + ' ('+str(record.id)+')'
		return dict(display=display, record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Name':validators.String(), 'Description':validators.String(),\
'CanReceive':validators.StringBool(), 'CanSell':validators.StringBool(), 'IsConsumed':validators.StringBool(), 'IsStore':validators.StringBool()})
def LocationSave(self, Id='', id='', Name='', Description='', CanReceive=False, CanSell=False, IsConsumed=False, \
IsStore=False, **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvLocation.get(int_id)
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
				record.Name = Name
				record.Description = Description
				record.CanReceive = CanReceive
				record.CanSell = CanSell
				record.IsConsumed = IsConsumed
				record.IsStore = IsStore
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvLocation(Name=Name, Description=Description, CanReceive=CanReceive, IsStore=IsStore, CanSell=CanSell, IsConsumed=IsConsumed, Status='')
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
def LocationDel(Id, id='', **kw):
	"""	If the Location has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvLocation.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if len(record.StockItems) == 0:
				#remove any groups the record might belong to
				for group in record.Groups:
					record.removeInvGrpLocation(group)
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
def LocationUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvLocation.get(int_id)
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
def LocationGroupSave(self, id='', field_num='', new_option_select='', **kw):
	if id != '':
		try:
			int_id = int(id)
			record = model.InvLocation.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	
	if int_id > 0:
		if record.Status == 'deleted':
			display = "RECORD MARKED DELETED: No updates allowed"
		else:
			#remove all related items from the field
			for group in record.Groups:
				record.removeInvGrpLocation(group)
			#Now add all the groups we were given
			if len(new_option_select) > 0:
				new_option_select = set(new_option_select.split(","))
				for option in new_option_select:
					record.addInvGrpLocation(int(option))
			#Make our return list
			rel_items = []
			for group in record.Groups:
				rel_items.append(dict(id=group.id, text=group.Name))
			display = "There are " + str(len(record.Groups)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='None', record={}, rel_items=[], field_num=field_num)
		
@expose(format='json')
def LocationGroups(self, Id, field_num, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvLocation.get(int_id)
			rel_items = []
			for group in record.Groups:
				rel_items.append(dict(id=group.id, text=group.Name))
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		display = "There are " + str(len(record.Groups)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='There are no records linked', record={},rel_items=[], field_id=field_num)		

@expose(format='json')
def LocationMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvLocation.get(int_id)
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
						line_text = 'To ' + item.ToLocation.Name + ' on ' + item.DateTransferred.strftime('%Y-%m-%d')
					elif ColName == 'TransfersToHere':
						line_text = 'From ' + item.FromLocation.Name + ' on ' + item.DateTransferred.strftime('%Y-%m-%d')
					elif ColName == 'StockItems':
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
def LocationSearch(self, Name='', Description='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvLocation.q.Name.contains('"+ Name + "'),"
	if Description != '':
		qArgs+="model.InvLocation.q.Description.contains('"+ Description + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvLocation.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvLocation.select()
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Name+' *** MARKED DELETED ***'
				results.append({'id':item.id, 'text':text, 'Name':item.Name+' *** MARKED DELETED ***', 'Description':item.Description})
			else:
				text = item.Name
				results.append({'id':item.id, 'text':text, 'Name':item.Name, 'Description':item.Description})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name, 'Description':item.Description})
	return dict(results=results, field_num=field_num, items=items)
