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
def QuoteRequest(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvQuoteRequest.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Notes_data = record.Notes
		RequestDate_data = record.RequestDate
		#MultiJoin and RelatedJoin
		RequestItems_data = 'There are ' + str(len(record.RequestItems)) + ' records'
		Vendors_data = 'There are ' + str(len(record.Vendors)) + ' records'
	else:
		Id_data = ''
		Name_data = ''
		Notes_data = ''
		RequestDate_data = ''
		#MultiJoin and RelatedJoin
		RequestItems_data = 'There are no records'
		Vendors_data = ''
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		Name_data = 'New'
		#MultiJoin and RelatedJoin
		RequestItems_data = 'There are ' + str(len(record.RequestItems)) + ' records'
		Vendors_data = 'There are ' + str(len(record.Vendors)) + ' records'
		id = ''
	#Construct our display fields
	Id = dict(id="qr_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="qr_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	RequestDate = dict(id="qr_RequestDate", name="RequestDate", label="Request date", type="DateTime",attr=dict(), data=RequestDate_data)
	Notes = dict(id="qr_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	#RelatedJoin
	SrchVendorName = dict(id="qr_SrchVendorName", name="Name", label="Group name", type="String",attr=dict(length=25), data='')
	Vendors = dict(id="qr_Vendors", name="Vendors", label="Vendors", type="RelatedJoin", attr=dict(displayUrl="QuoteRequestVendors", listUrl="QuoteRequestVendors", srchUrl="VendorSearch", saveUrl='QuoteRequestVendorsSave', srchFields=[SrchVendorName]), data=Vendors_data)
	#MultiJoin
	RequestItems = dict(id="qr_RequestItems", name="RequestItems", label="RequestItems", type="MultiJoin",attr=dict(displayUrl="QuoteRequestMultiJoinList",listUrl="QuoteRequestMultiJoinList",linkUrl="QuoteRequestItems"), data=RequestItems_data)
	#Fields
	fields = [Id, Name, RequestDate, Notes, Vendors, RequestItems]
	#Configure any of the links that might need configuring
	if id == '':
		QuoteRequestMenu = 'QuoteRequestMenu'
	else:
		QuoteRequestMenu = 'QuoteRequestMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='QuoteRequest', Label='Quote request entry', Fields=fields, FieldsSrch=[Name], Read='QuoteRequest', Add='QuoteRequestSave', Del='QuoteRequestDel', UnDel='QuoteRequestUnDel', Edit='QuoteRequest', Save='QuoteRequestSave', SrchUrl='QuoteRequestSearch', MenuBar=QuoteRequestMenu)

@expose(format='json')
def QuoteRequestMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("QuoteRequest")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("QuoteRequest")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='Vendors', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("QuoteRequest")', \
			menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("QuoteRequest?id='+id+'&Op=CopyIntoNew")'), \
			dict(label='Add Items', url='javascript:inv.openPickList("QuoteRequestAddCatalogItems?id='+id+'")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='Vendors', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def QuoteRequestGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteRequest.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'RequestDate':validators.String(), 'Notes':validators.String()})
def QuoteRequestSave(self, Id='', id='', RequestDate='', Notes='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteRequest.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if RequestDate != '':
		if len(RequestDate) > 10:
			RequestDate = time.strftime('%Y-%m-%d',time.strptime(RequestDate,'%Y-%m-%d %H:%M'))
		else:
			RequestDate = time.strftime('%Y-%m-%d',time.strptime(RequestDate,'%Y-%m-%d'))
		
	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				#Updating the record
				record.RequestDate = RequestDate
				record.Notes = Notes
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvQuoteRequest(RequestDate=RequestDate, Notes=Notes, Status='')
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
def QuoteRequestDel(Id, id='', **kw):
	"""	If the QuoteRequest has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteRequest.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.Vendors) + len(record.RequestItems)) == 0:
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
def QuoteRequestUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteRequest.get(int_id)
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
def QuoteRequestMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvQuoteRequest.get(int_id)
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
					if ColName == 'RequestItems':
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
def QuoteRequestVendorsSave(self, id='', field_num='', new_option_select='', **kw):
	if id != '':
		try:
			int_id = int(id)
			record = model.InvQuoteRequest.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	
	if int_id > 0:
		if record.Status == 'deleted':
			display = "RECORD MARKED DELETED: No updates allowed"
		else:
			#remove all related items from the field
			for vendor in record.Vendors:
				record.removeInvVendor(vendor)
			#Now add all the groups we were given
			if len(new_option_select) > 0:
				new_option_select = set(new_option_select.split(","))
				for option in new_option_select:
					record.addInvVendor(int(option))
			#Make our return list
			rel_items = []
			for vendor in record.Vendors:
				rel_items.append(dict(id=vendor.id, text=vendor.Name))
			display = "There are " + str(len(record.Vendors)) + " records linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='None', record={}, rel_items=[], field_num=field_num)
		
@expose(format='json')
def QuoteRequestVendors(self, Id, field_num, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteRequest.get(int_id)
			rel_items = []
			for vendor in record.Vendors:
				rel_items.append(dict(id=vendor.id, text=vendor.Name))
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		display = "There are " + str(len(record.Vendors)) + " records linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='There are no records linked', record={},rel_items=[], field_id=field_num)		

@expose(format='json')
def QuoteRequestSearch(self, Name='', VendorName='', RequestDate='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvQuoteRequestItems.q.CatalogItem.Name.contains('"+ Name + "'),"
	if VendorName != '':
		qArgs+="model.InvQuoteRequest.q.Vendors.Name.contains('"+ VendorName + "'),"
	if RequestDate != '':
		qArgs+="model.InvQuoteRequest.q.RequestDate.contains('"+ RequestDate + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvQuoteRequest.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvQuoteRequest.select()
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
	
@expose(format='json')
def QuoteRequestAddCatalogItems(self, Id='', id='', data='', **kw):
	"""	Id/id is the id of the QuoteRequest
	"""
	result_msg = ''
	if Id !='':
		id = Id
	if data!='' and id!='':
		QuoteRequest = int(id)
		data = simplejson.loads(data)
		#Update current entries
		qr_items = model.InvQuoteRequestItems.select(model.InvQuoteRequestItems.q.QuoteRequestID == QuoteRequest)
		tmp_data = []
		for qr_item in qr_items:
			updated = False
			for item in data:
				if (item.has_key('CatalogItemID') and (item['CatalogItemID'] == qr_item.CatalogItemID)) or ((not item.has_key('CatalogItemID')) and item['id'] == qr_item.CatalogItemID):
					updated = True
					record = model.InvQuoteRequestItems.get(qr_item.id)
					try:
						Quantity = int(item['Qty'])
					except ValueError:
						Quantity = 0
					record.Qty = Quantity
					record.Notes = item['Notes']
					tmp_data.append(item)
			if not updated:
				qr_item.destroySelf()
		#Add new entries
		for item in tmp_data:
			data.remove(tmp_data)
		for item in data:
			try:
				Quantity = int(item['Qty'])
			except ValueError:
				Quantity = 0
			if item.has_key('CatalogItemID'):
				try:
					CatalogItem = int(item['CatalogItemID'])
				except:
					raise
			else:
				try:
					CatalogItem = int(item['id'])
				except:
					raise
			if len(list(model.InvQuoteRequestItems.select("inv_quote_request_items.quote_request_id="+str(id)+" AND inv_quote_request_items.catalog_item_id="+str(item['id'])))) == 0:
				new_item = model.InvQuoteRequestItems(QuoteRequest=QuoteRequest, CatalogItem=CatalogItem, Qty=Quantity, Notes=item['Notes'], Status='')

	Qty = dict(id="qri_Qty", name="Qty", label="Qty", type="Numeric",attr=dict(length=5), data='')
	Notes = dict(id="qri_Notes", name="Notes", label="Notes", type="String",attr=dict(length=10), data='')		
	Name = dict(id="qri_Name", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	IsSelectable = dict(id="qri_IsSelectable", name="IsSelectable", label="IsSelectable", type="Hidden",attr=dict(length=25), data='true')
	InvGrpStockNames = []
	for item in model.InvGrpStock.select():
		InvGrpStockNames.append(item.Name)
	SrchCatalogGroups = dict(id="qri_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect",attr=dict(Groups=InvGrpStockNames), data='')
	return dict(id=id, Name='QuoteRequestAddCatalogItems', Label='Inventory Catalog Select', FieldsSrch=[Name, SrchCatalogGroups, IsSelectable], Inputs=[Qty, Notes], SrchUrl='CatalogItemSearch', DataUrl='QuoteRequestItemsSearch', Url='QuoteRequestAddCatalogItems', UrlVars='id='+id, result_msg=result_msg, SrchNow=False)

