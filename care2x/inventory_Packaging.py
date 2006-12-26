import logging

import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model

@expose(format='json')
def Packaging(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvPackaging.get(int_id)
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
		#MultipleJoin and relatedJoins
		Groups_data = 'There are ' + str(len(record.Groups)) + ' records'
		CatalogItems_data = 'There are ' + str(len(record.CatalogItems)) + ' records'
	else:
		Id_data = ''
		Name_data = ''
		Description_data = ''
		#MultipleJoin and relatedJoins
		Groups_data = 'There are no records'
		CatalogItems_data = 'There are no records'
	if Op == 'CopyIntoNew':
		Groups_data = 'There are no records'
		CatalogItems_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="p_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="p_Name", name="Name", label="Name", type="String",attr=dict(length=25), data=Name_data)
	Description = dict(id="p_Description", name="Description", label="Description", type="Text",attr=dict(cols=40,rows=3), data=Description_data)
	#MultipleJoin
	CatalogItems = dict(id="ci_CatalogItems", name="CatalogItems", label="Catalog items", type="MultiJoin",attr=dict(displayUrl="PackagingMultiJoinList",listUrl="PackagingMultiJoinList",linkUrl="CatalogItem"), data=CatalogItems_data)
	#RelatedJoin
	SrchGroups = dict(id="p_SrchGroups", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Groups = dict(id="p_Groups", name="Groups", label="Groups", type="RelatedJoin", attr=dict(displayUrl="PackagingGroups", listUrl="PackagingGroups", srchUrl="GrpPackagingSearch", saveUrl='PackagingGroupsSave', srchFields=[SrchGroups]), data=Groups_data)
	fields = [Id, Name, Description, Groups, CatalogItems]
	#Configure any of the links that might need configuring
	if id == '':
		PackagingMenu = 'PackagingMenu'
	else:
		PackagingMenu = 'PackagingMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='Packaging', Label='Packaging', Fields=fields, FieldsSrch=[Name], Read='Packaging', Add='PackagingSave', Del='PackagingDel', UnDel='PackagingUnDel', Edit='Packaging', Save='PackagingSave', SrchUrl='PackagingSearch', MenuBar=PackagingMenu)

@expose(format='json')
def PackagingMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("Packaging")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("Packaging")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("Packaging")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("Packaging?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def PackagingGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id !='':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPackaging.get(int_id)
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
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Name':validators.String(), 'Description':validators.String()})
def PackagingSave(self, Id = '',id = '', Name = '', Description = '', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPackaging.get(int_id)
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
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvPackaging(Name = Name, Description = Description, Status='')
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
def PackagingDel(Id, id='', **kw):
	"""	If the Packaging has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPackaging.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.CatalogItems) == 0):
				for item in record.Groups:
					record.removeInvGrpPackaging(item)
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
def PackagingUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPackaging.get(int_id)
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
def PackagingGroupsSave(self, id='',Id='', field_num='', new_option_select='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvPackaging.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	
	if int_id > 0:
		if record.Status == 'deleted':
			display = "RECORD MARKED DELETED: No updates allowed"
		else:
			#remove all related items from the field
			for item in record.Groups:
				record.removeInvGrpPackaging(item)
			#Now add all the groups we were given
			if len(new_option_select) > 0:
				new_option_select = set(new_option_select.split(","))
				for option in new_option_select:
					record.addInvGrpPackaging(int(option))
			#Make our return list
			rel_items = []
			for group in record.Groups:
				rel_items.append(dict(id=group.id, text=group.Name))
			display = "There are " + str(len(record.Groups)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='None', record={}, rel_items=[], field_num=field_num)
		
@expose(format='json')
def PackagingGroups(self, Id, field_num, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvPackaging.get(int_id)
			rel_items = []
			for item in record.Groups:
				rel_items.append(dict(id=item.id, text=item.Name))
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
def PackagingMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvPackaging.get(int_id)
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
					if CoName == 'CatalogItems':
						list_text = item.Name + ', ' + item.Description
					records.append(dict(id=item.id, listing=list_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def PackagingSearch(self, Name='', Description='',Groups=[], field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvPackaging.q.Name.contains('"+ Name + "'),"
	if Description != '':
		qArgs+="model.InvPackaging.q.Description.contains('"+ Description + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvPackaging.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvPackaging.select()
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Name+' *** MARKED DELETED *** ' + item.Description
				results.append({'id':item.id, 'text':text, 'Name':item.Name+' *** MARKED DELETED ***', 'Description':item.Description})
			else:
				text = item.Name+', ' + item.Description
				results.append({'id':item.id, 'text':text, 'Name':item.Name, 'Description':item.Description})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name, 'Description':item.Description})
	return dict(results=results, field_num=field_num, items=items)
	
