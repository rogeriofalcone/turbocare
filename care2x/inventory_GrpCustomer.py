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
def GrpCustomer(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvGrpCustomer.get(int_id)
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
		Customers_data = 'There are ' + str(len(record.Customers)) + ' records'
	else:
		Id_data = ''
		Name_data = ''
		Description_data = ''
		Customers_data = 'There are no records'
	#Construct our display fields
	Id = dict(id="gcc_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="gcc_Name", name="Name", label="Name", type="String",attr=dict(length=25), data=Name_data)
	Description = dict(id="gcc_Description", name="Description", label="Description", type="Text",attr=dict(cols=40,rows=3), data=Description_data)
	SrchCustomers = dict(id="gcc_Customers", name="Name", label="Customers", type="String",attr=dict(length=25), data='')
	Customers = dict(id="gcc_Customers", name="Customers", label="Customers", type="RelatedJoin", attr=dict(displayUrl="GrpCustomerCustomers", listUrl="GrpCustomerCustomers", srchUrl="GrpCustomerCustomerSearch", saveUrl='GrpCustomerCustomerSave', srchFields=[SrchCustomers]), data=Customers_data)
	fields = [Id, Name, Description, Customers]
	#Configure any of the links that might need configuring
	if id == '':
		GrpCustomerMenu = 'GrpCustomerMenu'
	else:
		GrpCustomerMenu = 'GrpCustomerMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='GrpCustomer', Label='Customer Groups', Fields=fields, FieldsSrch=[Name], Read='GrpCustomer', Add='GrpCustomerSave', Del='GrpCustomerDel', UnDel='GrpCustomerUnDel', Edit='GrpCustomer', Save='GrpCustomerSave', SrchUrl='GrpCustomerSearch', MenuBar=GrpCustomerMenu)

@expose(format='json')
def GrpCustomerMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("GrpCustomer")', menu=[dict(label='New sub item', url='javascript:inv.openObjForm("GrpCustomer")'), dict(label='Copy into new', url='javascript:inv.openObjForm("GrpCustomer")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Customers', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Customers', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("GrpCustomer")', menu=[dict(label='New sub item', url='javascript:inv.openObjForm("GrpCustomer?id='+id+'&Op=NewSubItem")'), dict(label='Copy into new', url='javascript:inv.openObjForm("GrpCustomer?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Customers', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Customers', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def GrpCustomerGet(self, Id, field_id, **kw):
#	INPUTS:
#	Id: the unique id for the catalog item
#	field_id: the id of the location where to put the results, pass-thru
#	OUTPUTS:
#	display: For displaying a simple text of the record
#	record: The whole object passed as a json output
#	field_id: passed through from input for the call-back function's convenience
#
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGrpCustomer.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		display = record.Name + ' ('+str(record.id)+') **MARKED DELETED***'
		return dict(display=display, record=record, field_id=field_id)
	else:	
		return dict(display='None', record={}, field_id=field_id)
	
@expose(format='json')
def GrpCustomerCustomerGet(self, Id, field_id, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGrpCustomer.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		if record.Status == 'deleted':
			display = record.Name + ' ('+str(record.id)+') ** MARKED DELETED ***'
		else:	
			display = record.Name + ' ('+str(record.id)+')'
		return dict(display=display, record=record, field_id=field_id)
	else:	
		return dict(display='None', record={}, field_id=field_id)

@expose(format='json')
def GrpCustomerPackagingGet(self, Id, field_id, **kw):
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
			display = record.Name + ' ('+str(record.id)+') *** MARKED DELETED ***'
		else:
			display = record.Name + ' ('+str(record.id)+')'
		return dict(display=display, record=record, field_id=field_id)
	else:	
		return dict(display='None', record={}, field_id=field_id)

@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Name':validators.String(), 'Description':validators.String()})
def GrpCustomerSave(self, Id = '',id = '', Name = '', Description = '', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGrpCustomer.get(int_id)
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
			record = model.InvGrpCustomer(Name = Name, Description = Description, Status='')
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
def GrpCustomerDel(Id, id='', **kw):
	"""	If the GrpCustomer has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGrpCustomer.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.Customers) == 0):
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
def GrpCustomerUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGrpCustomer.get(int_id)
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
def GrpCustomerCustomerSave(self, id='', field_num='', new_option_select='', **kw):
	if id != '':
		try:
			int_id = int(id)
			record = model.InvGrpCustomer.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	
	if int_id > 0:
		if record.Status == 'deleted':
			display = "RECORD MARKED DELETED: No updates allowed"
		else:
			#remove all related items from the field
			for item in record.Customers:
				record.removeInvCustomer(item)
			#Now add all the groups we were given
			if len(new_option_select) > 0:
				new_option_select = set(new_option_select.split(","))
				for option in new_option_select:
					record.addInvCustomer(int(option))
			#Make our return list
			rel_items = []
			for group in record.Customers:
				rel_items.append(dict(id=group.id, text=group.Name))
			display = "There are " + str(len(record.Customers)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='None', record={}, rel_items=[], field_num=field_num)
		
@expose(format='json')
def GrpCustomerCustomers(self, Id, field_num, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvGrpCustomer.get(int_id)
			rel_items = []
			for item in record.Customers:
				rel_items.append(dict(id=item.id, text=item.Name))
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		display = "There are " + str(len(record.Customers)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='There are no records linked', record={},rel_items=[], field_id=field_num)		

@expose(format='json')
def GrpCustomerSearch(self, Name='', Description='',Groups=[], field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvGrpCustomer.q.Name.contains('"+ Name + "'),"
	if Description != '':
		qArgs+="model.InvGrpCustomer.q.Description.contains('"+ Description + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvGrpCustomer.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvGrpCustomer.select()
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

@expose(format='json')
def GrpCustomerCustomerSearch(self, Name='', AddressLabel='', field_num='', **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvCustomer.q.Name.contains('"+ Name + "'),"
	if AddressLabel != '':
		qArgs+="model.InvCustomer.q.AddressLabel.contains('"+ AddressLabel + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvCustomer.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvCustomer.select()
	results = []
	for item in items:
		if item.Status != 'deleted':
			results.append({'id':item.id, 'text':item.Name + "(" + item.AddressLabel + ")"})
	return dict(results=results, field_num=field_num)
	
