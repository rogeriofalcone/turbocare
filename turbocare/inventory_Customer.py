import logging
from datetime import datetime, date
import simplejson
import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model

@expose(format='json')
def Customer(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCustomer.get(int_id)
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
		Phone1_data = record.Phone1
		Phone2_data = record.Phone2
		Fax_data = record.Fax
		Email1_data = record.EMail1
		Email2_data = record.Email2
		AddressLabel_data = record.AddressLabel
		CreditAmount_data = str(record.CreditAmount)
		Accounting_data = record.Accounting
		ExternalID_data = record.ExternalID
		#ForeignKeys
		try:
			City_data = record.City.id
			City_display = record.City.Name + ' ('+str(record.City.id)+')'
		except AttributeError: 
			City_data = ''
			City_display = 'None'
		try:
			InventoryLocation_data = record.InventoryLocation.id
			InventoryLocation_display = record.InventoryLocation.Name + ' ('+str(record.InventoryLocation.id)+')'
		except AttributeError: 
			InventoryLocation_data = ''
			InventoryLocation_display = 'None'
		#MultiJoin and RelatedJoin
		Receipts_data = 'There are ' + str(len(record.Receipts)) + ' records'
		Groups_data = 'There are ' + str(len(record.Groups)) + ' record(s)'
		Payments_data = 'There are ' + str(len(record.Payments)) + ' Record(s)'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Phone1_data = ''
		Phone2_data = ''
		Fax_data = ''
		Email1_data = ''
		Email2_data = ''
		AddressLabel_data = ''
		CreditAmount_data = ''
		Accounting_data = ''
		ExternalID_data = ''
		#ForeignKeys
		City_data = ''
		City_display = 'None'
		InventoryLocation_data = ''
		InventoryLocation_display = 'None'
		#MultiJoin and RelatedJoin
		Receipts_data = 'There are no records'
		Groups_data = 'There are no records'
		Payments_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#ForeignKeys
		City_data = ''
		City_display = 'None'
		InventoryLocation_data = ''
		InventoryLocation_display = 'None'
		#MultiJoin and RelatedJoin
		Receipts_data = 'There are no records'
		Groups_data = 'There are no records'
		Payments_data = 'There are no records'
		Id_data = ''
		id = ''
	elif Op == 'NewSubItem':
		#ForeignKeys
		City_data = ''
		City_display = 'None'
		InventoryLocation_data = ''
		InventoryLocation_display = 'None'
		#MultiJoin and RelatedJoin
		Receipts_data = 'There are no records'
		Groups_data = 'There are no records'
		Payments_data = 'There are no records'
		Name_data = ''
		ExternalID_data = ''
		Id_data = ''
		id=''
	#Construct our display fields
	Id = dict(id="c_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="c_Name", name="Name", label="Name", type="String",attr=dict(length=50), data=Name_data)
	CreditAmount = dict(id="c_CreditAmount", name="CreditAmount", label="Credit amount", type="Currency",attr=dict(), data=CreditAmount_data)
	Phone1 = dict(id="c_Phone1", name="Phone1", label="Phone 1", type="String",attr=dict(length=20), data=Phone1_data)
	Phone2 = dict(id="c_Phone2", name="Phone2", label="Phone 2", type="String",attr=dict(length=20), data=Phone2_data)
	Fax = dict(id="c_Fax", name="Fax", label="Fax", type="String",attr=dict(length=20), data=Fax_data)
	Email1 = dict(id="c_Email1", name="EMail1", label="Email 1", type="String",attr=dict(length=20), data=Email1_data)
	Email2 = dict(id="c_Email2", name="Email2", label="Email 2", type="String",attr=dict(length=20), data=Email2_data)
	AddressLabel = dict(id="c_AddressLabel", name="AddressLabel", label="Address label", type="Text",attr=dict(cols=40, rows=4), data=AddressLabel_data)
	Accounting = dict(id="c_Accounting", name="Accounting", label="Accounting", type="String",attr=dict(length=50), data=Accounting_data)
	ExternalID = dict(id="c_ExternalID", name="ExternalID", label="External ID", type="String",attr=dict(length=50), data=ExternalID_data)
	#ForeignKeys
	SrchCityName = dict(id="c_SrchCityName", name="Name", label="City", type="String",attr=dict(length=25), data='')
	SrchCityDistrict = dict(id="c_SrchCityDistrict", name="District", label="District", type="String",attr=dict(length=25), data='')
	City = dict(id="c_City", name="City", label="City", type="ForeignKey",attr=dict(srchUrl="AddressCitytownSearch",lookupUrl="AddressCitytownGet", edit_url='AddressCitytown', srchFields=[SrchCityName, SrchCityDistrict]), data=City_data, init_display=City_display)
	SrchLocationName = dict(id="c_SrchLocationName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	InventoryLocation = dict(id="c_InventoryLocation", name="InventoryLocation", label="Inventory location", type="ForeignKey",attr=dict(srchUrl="LocationSearch",lookupUrl="LocationGet", edit_url='Location', srchFields=[SrchLocationName]), data=InventoryLocation_data, init_display=InventoryLocation_display)
	#MultiJoin
	Receipts = dict(id="c_Receipts", name="Receipts", label="Receipts", type="MultiJoin",attr=dict(displayUrl="CustomerMultiJoinList",listUrl="CustomerMultiJoinList",linkUrl="Receipt"), data=Receipts_data)
	Payments = dict(id="c_Payments", name="Payments", label="Payments", type="MultiJoin",attr=dict(displayUrl="CustomerMultiJoinList",listUrl="CustomerMultiJoinList",linkUrl="CustomerPayment"), data=Payments_data)
	#RelatedJoin
	SrchGrpName = dict(id="c_SrchGrpName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Groups = dict(id="c_Groups", name="Groups", label="Groups", type="RelatedJoin", attr=dict(displayUrl="CustomerGroups", listUrl="CustomerGroups", srchUrl="GrpCustomerSearch", saveUrl='CustomerGroupSave', srchFields=[SrchGrpName]), data=Groups_data)
	#Fields
	fields = [Id, Name, CreditAmount, Phone1, Phone2, Email1, Email2, Fax, City, AddressLabel, Accounting, ExternalID, InventoryLocation, Receipts, Payments, Groups]
	#Configure any of the links that might need configuring
	if id == '':
		CustomerMenu = 'CustomerMenu'
	else:
		CustomerMenu = 'CustomerMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='Customer', Label='Customer entry', Fields=fields, FieldsSrch=[Name], Read='Customer', Add='CustomerSave', Del='CustomerDel', UnDel='CustomerUnDel', Edit='Customer', Save='CustomerSave', SrchUrl='CustomerSearch', MenuBar=CustomerMenu)

@expose(format='json')
def CustomerMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("Customer")', menu=[dict(label='New sub item', url='javascript:inv.openObjForm("Customer")'), dict(label='Copy into new', url='javascript:inv.openObjForm("Customer")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Receipts', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Receipts', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("Customer")', menu=[\
			dict(label='New sub item', url='javascript:inv.openObjForm("Customer?id='+id+'&Op=NewSubItem")'), \
			dict(label='Copy into new', url='javascript:inv.openObjForm("Customer?id='+id+'&Op=CopyIntoNew")'),\
			dict(label='Add payment', url='javascript:inv.openObjForm("CustomerPayment?CustomerID='+id+'")'),\
			dict(label='Add Receipt', url='javascript:inv.openPickList("CustomerAddReceipt?id='+id+'")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Receipts', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Receipts', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def CustomerGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCustomer.get(int_id)
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
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Name':validators.String(), 'ExternalID':validators.String(), 'CreditAmount':validators.Number(), 'Phone1':validators.String(), 'Phone2':validators.String(), 'Fax':validators.String(), 'EMail1':validators.String(), 'Email2':validators.String(), 'AddressLabel':validators.String(), 'Accounting':validators.String(), 'City':validators.Int(), 'InventoryLocation':validators.Int()})
def CustomerSave(self, City, InventoryLocation, Id='', id='', Name='', CreditAmount=0, ExternalID='', Phone1='', Phone2='', Fax='', EMail1='', Email2='', AddressLabel='', Accounting='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCustomer.get(int_id)
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
				record.CreditAmount = CreditAmount
				record.Phone1 = Phone1
				record.Phone2 = Phone2
				record.Fax = Fax
				record.EMail1 = EMail1
				record.Email2 = Email2
				record.City = City
				record.AddressLabel = AddressLabel
				record.Accounting = Accounting
				record.InventoryLocation = InventoryLocation
				record.ExternalID = ExternalID
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvCustomer(Name=Name, CreditAmount=CreditAmount, ExternalID=ExternalID, Phone1=Phone1, Phone2=Phone2, Fax=Fax, EMail1=EMail1, Email2=Email2, AddressLabel=AddressLabel, Accounting=Accounting, City=City, InventoryLocation = InventoryLocation, Status='')
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
def CustomerDel(Id, id='', **kw):
	"""	If the Customer has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCustomer.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.Receipts) + len(record.Payments)) == 0:
				#remove any groups the record might belong to
				for group in record.Groups:
					record.removeInvGrpCustomer(group)
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
def CustomerUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCustomer.get(int_id)
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
def CustomerGroupSave(self, id='', field_num='', new_option_select='', **kw):
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCustomer.get(int_id)
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
				record.removeInvGrpCustomer(group)
			#Now add all the groups we were given
			if len(new_option_select) > 0:
				new_option_select = set(new_option_select.split(","))
				for option in new_option_select:
					record.addInvGrpCustomer(int(option))
			#Make our return list
			rel_items = []
			for group in record.Groups:
				rel_items.append(dict(id=group.id, text=group.Name))
			display = "There are " + str(len(record.Groups)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='None', record={}, rel_items=[], field_num=field_num)
		
@expose(format='json')
def CustomerGroups(self, Id, field_num, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCustomer.get(int_id)
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
def CustomerMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCustomer.get(int_id)
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
					if ColName == 'Receipts':
						#line_text = str(len(item.Items)) + ' items at Rs. ' + str(item.TotalPayment) + ' purchased on ' + item.CreateTime.strftime('%Y-%m-%d')
						line_text = item.Name()
					elif ColName == 'Payments':
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
def CustomerSearch(self, Name='', Accounting='', AddressLabel='', ExternalID='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvCustomer.q.Name.contains('"+ Name + "'),"
	if ExternalID != '':
		qArgs+="model.InvCustomer.q.ExternalID.contains('"+ ExternalID + "'),"
	if Accounting != '':
		qArgs+="model.InvCustomer.q.Accounting.contains('"+ Accounting + "'),"
	if AddressLabel != '':
		qArgs+="model.InvCustomer.q.AddressLabel.contains('"+ AddressLabel + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvCustomer.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvCustomer.select()
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Name+' *** MARKED DELETED ***'
				results.append({'id':item.id, 'text':text, 'Name':item.Name+' *** MARKED DELETED ***', 'Description':item.Accounting})
			else:
				text = item.Name
				results.append({'id':item.id, 'text':text, 'Name':item.Name, 'Description':item.Accounting})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name, 'Description':item.Accounting})
	return dict(results=results, field_num=field_num, items=items)
	
@expose()
def CustomerSaveReceipt(self, Id='', id='', data='', **kw):
	result_msg = ''
	if Id !='':
		id = Id
	if data!='' and id!='':
		CustomerID = int(id)
		data = simplejson.loads(data)
		#Create a new receipt entry
		receipt = model.InvReceipt(CustomerID = CustomerID, TotalPayment = 0.0, TotalPaid = 0.0, TotalSelfPay = 0.0,\
			TotalInsurance = 0.0)
		totalcost = 0.0
		for item in data:
			try:
				Quantity = int(item['Quantity'])
			except ValueError:
				Quantity = 0
			try:
				CatalogItemID = int(item['id'])
			except:
				raise
			if len(list(model.InvReceiptItems.select(AND (model.InvReceiptItems.q.CatalogItemID == CatalogItemID,\
				model.InvReceiptItems.q.ReceiptID == receipt.id)))) == 0:
				new_item = model.InvReceiptItems(ReceiptID=receipt.id, CatalogItemID=CatalogItemID, Quantity=Quantity)
				totalcost += new_item.UnitCost*Quantity
		receipt.TotalPayment = totalcost
	return dict(id=id, Name='CustomerSaveReceipt', Label='New receipt saved', result_msg="New receipt made")

@expose(format='json')
def CustomerAddReceipt(self, Id='', id='', data='', **kw):
	result_msg = ""
	
	Quantity = dict(id="c_Quantity", name="Quantity", label="Quantity requesting", type="Numeric", attr=dict(length=10), data='')
	Discount = dict(id="c_Discount", name="Discount", label="Discount", type="Numeric", attr=dict(length=10), data='')
	UnitCost = dict(id="c_UnitCost", name="UnitCost", label="Unit cost", type="StringRO", attr=dict(length=10), data='')
	#Search variables
	Name = dict(id="c_Name", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	InvGrpStockNames = []
	for item in model.InvGrpStock.select():
		InvGrpStockNames.append(item.Name)
	SrchCatalogGroups = dict(id="c_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect",attr=dict(Groups=InvGrpStockNames), data='')
	return dict(id=id, Name='CustomerAddReceipt', Label='Create a receipt', \
		FieldsSrch=[Name, SrchCatalogGroups], Inputs=[Quantity], SrchUrl='CatalogItemSearch', \
		DataUrl='', Url='CustomerSaveReceipt', \
		UrlVars='id='+id, result_msg=result_msg, SrchNow=False)

