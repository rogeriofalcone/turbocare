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
def Vendor(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvVendor.get(int_id)
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
		Phone1_data = record.Phone1
		Phone2_data = record.Phone2
		Fax_data = record.Fax
		Email1_data = record.EMail1
		Email2_data = record.Email2
		AddressLabel_data = record.AddressLabel
		ContactName_data = record.ContactName
		#ForeignKeys
		try:
			City_data = record.City.id
			City_display = record.City.Name + ' ('+str(record.City.id)+')'
		except AttributeError: 
			City_data = ''
			City_display = 'None'
		#MultiJoin and RelatedJoin
		Quotes_data = 'There are ' + str(len(record.Quotes)) + ' records'
		QuoteRequests_data = 'There are ' + str(len(record.QuoteRequests)) + ' records'
		PurchaseOrders_data = 'There are ' + str(len(record.PurchaseOrders)) + ' record(s)'
		Groups_data = 'There are ' + str(len(record.Groups)) + ' record(s)'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Description_data = ''
		Phone1_data = ''
		Phone2_data = ''
		Fax_data = ''
		Email1_data = ''
		Email2_data = ''
		AddressLabel_data = ''
		ContactName_data = ''
		#ForeignKeys
		City_data = ''
		City_display = 'None'
		#MultiJoin and RelatedJoin
		Quotes_data = 'There are no records'
		QuoteRequests_data = 'There are no records'
		PurchaseOrders_data = 'There are no record'
		Groups_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#ForeignKeys
		City_data = ''
		City_display = 'None'
		#MultiJoin and RelatedJoin
		Quotes_data = 'There are no records'
		QuoteRequests_data = 'There are no records'
		PurchaseOrders_data = 'There are no record'
		Groups_data = 'There are no records'
		Id_data = ''
		id = ''
	elif Op == 'NewSubItem':
		#ForeignKeys
		City_data = ''
		City_display = 'None'
		#MultiJoin and RelatedJoin
		Quotes_data = 'There are no records'
		QuoteRequests_data = 'There are no records'
		PurchaseOrders_data = 'There are no record'
		Groups_data = 'There are no records'
		Name_data = ''
		Description_data = ''
		Id_data = ''
		id=''
	#Construct our display fields
	Id = dict(id="v_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="v_Name", name="Name", label="Name", type="String",attr=dict(length=25), data=Name_data)
	Description = dict(id="v_Description", name="Description", label="Description", type="Text",attr=dict(cols=30,rows=3), data=Description_data)
	Phone1 = dict(id="v_Phone1", name="Phone1", label="Phone 1", type="String",attr=dict(length=20), data=Phone1_data)
	Phone2 = dict(id="v_Phone2", name="Phone2", label="Phone 2", type="String",attr=dict(length=20), data=Phone2_data)
	Fax = dict(id="v_Fax", name="Fax", label="Fax", type="String",attr=dict(length=20), data=Fax_data)
	Email1 = dict(id="v_Email1", name="EMail1", label="Email 1", type="String",attr=dict(length=20), data=Email1_data)
	Email2 = dict(id="v_Email2", name="Email2", label="Email 2", type="String",attr=dict(length=20), data=Email2_data)
	AddressLabel = dict(id="v_AddressLabel", name="AddressLabel", label="Address label", type="Text",attr=dict(cols=40, rows=4), data=AddressLabel_data)
	ContactName = dict(id="v_ContactName", name="ContactName", label="Contact name", type="String",attr=dict(length=50), data=ContactName_data)
	#ForeignKeys
	SrchCityName = dict(id="v_SrchCityName", name="Name", label="City", type="String",attr=dict(length=25), data='')
	SrchCityDistrict = dict(id="v_SrchCityDistrict", name="District", label="District", type="String",attr=dict(length=25), data='')
	City = dict(id="v_City", name="City", label="City", type="ForeignKey",attr=dict(srchUrl="AddressCitytownSearch",lookupUrl="AddressCitytownGet", edit_url='AddressCitytown', srchFields=[SrchCityName, SrchCityDistrict]), data=City_data, init_display=City_display)
	#MultiJoin
	Quotes = dict(id="v_Quotes", name="Quotes", label="Quotes", type="MultiJoin",attr=dict(displayUrl="VendorMultiJoinList",listUrl="VendorMultiJoinList",linkUrl="Vendor"), data=Quotes_data)
	PurchaseOrders = dict(id="v_PurchaseOrders", name="PurchaseOrders", label="Purchase orders", type="MultiJoin",attr=dict(displayUrl="VendorMultiJoinList",listUrl="VendorMultiJoinList",linkUrl="Vendor"), data=PurchaseOrders_data)
	#RelatedJoin
	SrchYear = dict(id="v_SrchYear", name="RequestDate", label="Year", type="String",attr=dict(length=4), data=datetime.now().strftime('%Y'))
	QuoteRequests = dict(id="v_QuoteRequests", name="QuoteRequests", label="Quote requests", type="RelatedJoin", attr=dict(displayUrl="VendorQuoteRequests", listUrl="VendorQuoteRequests", srchUrl="QuoteRequestSearch", saveUrl='VendorQuoteRequestsSave', srchFields=[SrchYear]), data=QuoteRequests_data)
	SrchGrpName = dict(id="v_SrchGrpName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Groups = dict(id="v_Groups", name="Groups", label="Groups", type="RelatedJoin", attr=dict(displayUrl="VendorGroups", listUrl="VendorGroups", srchUrl="GrpVendorSearch", saveUrl='VendorGroupSave', srchFields=[SrchGrpName]), data=Groups_data)
	#Fields
	fields = [Id, Name, Description, Phone1, Phone2, Email1, Email2, Fax, City, AddressLabel, ContactName, Quotes, QuoteRequests, PurchaseOrders, Groups]
	#Configure any of the links that might need configuring
	if id == '':
		VendorMenu = 'VendorMenu'
	else:
		VendorMenu = 'VendorMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='Vendor', Label='Vendor entry', Fields=fields, FieldsSrch=[Name], Read='Vendor', Add='VendorSave', Del='VendorDel', UnDel='VendorUnDel', Edit='Vendor', Save='VendorSave', SrchUrl='VendorSearch', MenuBar=VendorMenu)

@expose(format='json')
def VendorMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("Vendor")', menu=[dict(label='New sub item', url='javascript:inv.openObjForm("Vendor")'), dict(label='Copy into new', url='javascript:inv.openObjForm("Vendor")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Quotes', url=''), dict(label='Purchase orders', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Purchase history', url=''), dict(label='Price quotes', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("Vendor")', menu=[dict(label='New sub item', url='javascript:inv.openObjForm("Vendor?id='+id+'&Op=NewSubItem")'), dict(label='Copy into new', url='javascript:inv.openObjForm("Vendor?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Quotes', url=''), dict(label='Purchase orders', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Purchase history', url=''), dict(label='Price quotes', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def VendorGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvVendor.get(int_id)
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
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Name':validators.String(), 'Description':validators.String(), 'Phone1':validators.String(), 'Phone2':validators.String(), 'Fax':validators.String(), 'EMail1':validators.String(), 'Email2':validators.String(), 'AddressLabel':validators.String(), 'ContactName':validators.String(), 'City':validators.Int()})
def VendorSave(self, City, Id='', id='', Name='', Description='', Phone1='', Phone2='', Fax='', EMail1='', Email2='', AddressLabel='', ContactName='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvVendor.get(int_id)
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
				record.Phone1 = Phone1
				record.Phone2 = Phone2
				record.Fax = Fax
				record.EMail1 = EMail1
				record.Email2 = Email2
				record.City = City
				record.AddressLabel = AddressLabel
				record.ContactName = ContactName
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvVendor(Name=Name, Description=Description, Phone1=Phone1, Phone2=Phone2, Fax=Fax, EMail1=EMail1, Email2=Email2, AddressLabel=AddressLabel, ContactName=ContactName, City=City, Status='')
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
def VendorDel(Id, id='', **kw):
	"""	If the Vendor has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvVendor.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.Quotes) + len(record.QuoteRequests) + len(record.PurchaseOrders)) == 0:
				#remove any groups the record might belong to
				for group in record.Groups:
					record.removeInvGrpVendor(group)
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
def VendorUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvVendor.get(int_id)
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
def VendorGroupSave(self, id='', field_num='', new_option_select='', **kw):
	if id != '':
		try:
			int_id = int(id)
			record = model.InvVendor.get(int_id)
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
				record.removeInvGrpVendor(group)
			#Now add all the groups we were given
			if len(new_option_select) > 0:
				new_option_select = set(new_option_select.split(","))
				for option in new_option_select:
					record.addInvGrpVendor(int(option))
			#Make our return list
			rel_items = []
			for group in record.Groups:
				rel_items.append(dict(id=group.id, text=group.Name))
			display = "There are " + str(len(record.Groups)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='None', record={}, rel_items=[], field_num=field_num)
		
@expose(format='json')
def VendorGroups(self, Id, field_num, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvVendor.get(int_id)
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
def VendorQuoteRequestsSave(self, id='', field_num='', new_option_select='', **kw):
	if id != '':
		try:
			int_id = int(id)
			record = model.InvVendor.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	
	if int_id > 0:
		if record.Status == 'deleted':
			display = "RECORD MARKED DELETED: No updates allowed"
		else:
			#remove all related items from the field
			for item in record.QuoteRequests:
				record.removeInvQuoteRequest(item)
			#Now add all the groups we were given
			if len(new_option_select) > 0:
				new_option_select = set(new_option_select.split(","))
				for option in new_option_select:
					record.addInvQuoteRequest(int(option))
			#Make our return list
			rel_items = []
			for item in record.QuoteRequests:
				rel_items.append(dict(id=item.id, text=item.Name))
			display = "There are " + str(len(record.QuoteRequests)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='None', record={}, rel_items=[], field_num=field_num)
		
@expose(format='json')
def VendorQuoteRequests(self, Id, field_num, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvVendor.get(int_id)
			rel_items = []
			for item in record.QuoteRequests:
				rel_items.append(dict(id=item.id, text=item.Name))
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		display = "There are " + str(len(record.QuoteRequests)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='There are no records linked', record={},rel_items=[], field_id=field_num)		

@expose(format='json')
def VendorMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvVendor.get(int_id)
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
					if ColName == 'PurchaseOrders':
						line_text = "Sent on: " + item.POSentOnDate
					if ColName == 'Quotes':
						line_text = "Valid on: " + item.ValidOn
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def VendorSearch(self, Name='', Description='', AddressLabel='', CatalogItemId='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvVendor.q.Name.contains('"+ Name + "'),"
	if Description != '':
		qArgs+="model.InvVendor.q.Description.contains('"+ Description + "'),"
	if AddressLabel != '':
		qArgs+="model.InvVendor.q.AddressLabel.contains('"+ AddressLabel + "'),"
	if CatalogItemId != '':
		qArgs = 'AND (model.InvQuote.q.VendorID == model.InvVendor.q.id, model.InvQuoteItems.q.QuoteID == model.InvQuote.q.id, model.InvQuoteItems.q.CatalogItemID == model.InvCatalogItem.q.id, model.InvCatalogItem.q.id == '+CatalogItemId+'),'
	if len(qArgs) > 0:
		items = eval('model.InvVendor.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvVendor.select()
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Name+' *** MARKED DELETED ***, ' + item.Description
				results.append({'id':item.id, 'text':text, 'Name':item.Name+' *** MARKED DELETED ***', 'Description':item.Description})
			else:
				text = item.Name + ', ' + item.Description
				results.append({'id':item.id, 'text':text, 'Name':item.Name, 'Description':item.Description})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name, 'Description':item.Description})
	return dict(results=results, field_num=field_num, items=items)
