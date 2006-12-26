import logging
import simplejson
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
def CustomerPayment(self, id='',Id='', Op='', CustomerID='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCustomerPayment.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	#Vendor -> Customer
	#Amount NEW
	#ValidOn -> DatePaid
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Notes_data = record.Notes
		DatePaid_data = record.DatePaid
		Amount_data = record.Amount
		#ForeignKeys
		try:
			Customer_data = record.CustomerID
			Customer_display = record.Customer.Name + ' ('+str(record.CustomerID)+')'
		except AttributeError: 
			Customer_data = ''
			Customer_display = 'None'
		#MultiJoin and RelatedJoin
	else:
		Id_data = ''
		Name_data = 'New entry'
		Notes_data = ''
		DatePaid_data = model.cur_date_time()
		Amount_data = '0.0'
		#ForeignKeys
		if CustomerID != '':			
			Customer_data = CustomerID
			Customer_display = model.InvCustomer.get(int(CustomerID)).Name
		else:
			Customer_data = ''
			Customer_display = 'None'
		#MultiJoin and RelatedJoin
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="cp_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="cp_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	DatePaid = dict(id="cp_DatePaid", name="DatePaid", label="Date paid", type="DateTime",attr=dict(), data=DatePaid_data)
	Amount = dict(id="cp_Amount", name="Amount", label="Amount", type="Currency",attr=dict(), data=Amount_data)
	Notes = dict(id="cp_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	#ForeignKeys
	SrchCustomerName = dict(id="cp_SrchCustomerName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Customer = dict(id="cp_Customer", name="Customer", label="Customer", type="ForeignKey",attr=dict(srchUrl="CustomerSearch",lookupUrl="CustomerGet", edit_url='Customer', srchFields=[SrchCustomerName]), data=Customer_data, init_display=Customer_display)
	#MultiJoin
	#Fields
	fields = [Id, Name, Customer, Amount, DatePaid, Notes]
	#Configure any of the links that might need configuring
	if id == '':
		CustomerPaymentMenu = 'CustomerPaymentMenu'
	else:
		CustomerPaymentMenu = 'CustomerPaymentMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='CustomerPayment', Label='Customer payment entry', Fields=fields, FieldsSrch=[Name], Read='CustomerPayment', Add='CustomerPaymentSave', Del='CustomerPaymentDel', UnDel='CustomerPaymentUnDel', Edit='CustomerPayment', Save='CustomerPaymentSave', SrchUrl='CustomerPaymentSearch', MenuBar=CustomerPaymentMenu)

@expose(format='json')
def CustomerPaymentMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("CustomerPayment")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("CustomerPayment")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("CustomerPayment")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("CustomerPayment?id='+id+'&Op=CopyIntoNew")'),  dict(label='Add/Edit Items', url='javascript:inv.openPickList("CustomerPaymentAddCustomerPaymentItems?id='+id+'")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def CustomerPaymentGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCustomerPayment.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'DatePaid':validators.String(), 'Notes':validators.String(), 'Customer':validators.Int(), 'Amount':validators.Number()})
def CustomerPaymentSave(self, Customer, Amount=0.0, Id='', id='', DatePaid='', Notes='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCustomerPayment.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if DatePaid != '':
		if len(DatePaid) > 10:
			ConvertTime = time.strptime(DatePaid[0:15],'%Y-%m-%d %H:%M')
		else:
			ConvertTime = time.strptime(DatePaid,'%Y-%m-%d')
	DatePaid = datetime(ConvertTime.tm_year,ConvertTime.tm_mon,ConvertTime.tm_mday)
	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				#Updating the record
				record.DatePaid = DatePaid
				record.Notes = Notes
				record.Amount = Amount
				record.Customer = Customer
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvCustomerPayment(Amount=Amount, Customer=Customer, Notes=Notes, DatePaid=DatePaid, Status='')
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
def CustomerPaymentDel(Id, id='', **kw):
	"""	If the CustomerPayment has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCustomerPayment.get(int_id)
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
def CustomerPaymentUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCustomerPayment.get(int_id)
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
def CustomerPaymentMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCustomerPayment.get(int_id)
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
					if ColName == 'Items':
						line_text = item.CatalogItem.Name + ' at Rs. ' + str(item.Price)
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

	
@expose(format='json')
def CustomerPaymentSearch(self, Name='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvCustomerPayment.q.CustomerID == model.InvCustomer.q.id,"
		qArgs+="model.InvCustomer.q.Name.contains('%s')," % Name
	if len(qArgs) > 0:
		items = eval('model.InvCustomerPayment.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvCustomerPayment.select()
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



