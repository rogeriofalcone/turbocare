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
def Quote(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvQuote.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Notes_data = record.Notes
		ValidOn_data = record.ValidOn
		#ForeignKeys
		try:
			Vendor_data = record.Vendor.id
			Vendor_display = record.Vendor.Name + ' ('+str(record.Vendor.id)+')'
		except AttributeError: 
			Vendor_data = ''
			Vendor_display = 'None'
		try:
			QuoteRequest_data = record.QuoteRequest.id
			QuoteRequest_display = record.QuoteRequest.Name() + ' ('+str(record.QuoteRequest.id)+')'
		except AttributeError: 
			QuoteRequest_data = ''
			QuoteRequest_display = 'None'
		#MultiJoin and RelatedJoin
		Items_data = 'There are ' + str(len(record.Items)) + ' records'
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
		Vendor_data = ''
		Vendor_display = 'None'
		QuoteRequest_data = ''
		QuoteRequest_display = 'None'
		#MultiJoin and RelatedJoin
		Items_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#ForeignKeys
		Vendor_data = ''
		Vendor_display = 'None'
		#MultiJoin and RelatedJoin
		Items_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="q_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="q_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	ValidOn = dict(id="q_ValidOn", name="ValidOn", label="Valid on", type="DateTime",attr=dict(), data=ValidOn_data)
	Notes = dict(id="q_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	#ForeignKeys
	SrchVendorName = dict(id="q_SrchVendorName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Vendor = dict(id="q_Vendor", name="Vendor", label="Vendor", type="ForeignKey",attr=dict(srchUrl="VendorSearch",lookupUrl="VendorGet", edit_url='Vendor', srchFields=[SrchVendorName]), data=Vendor_data, init_display=Vendor_display)
	SrchQRVendorName = dict(id="q_SrchQRVendorName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	QuoteRequest = dict(id="q_QuoteRequest", name="QuoteRequest", label="Quote request", type="ForeignKey",attr=dict(srchUrl="QuoteRequestSearch",lookupUrl="QuoteRequestGet", edit_url='QuoteRequest', srchFields=[SrchQRVendorName]), data=QuoteRequest_data, init_display=QuoteRequest_display)
	#MultiJoin
	Items = dict(id="q_Items", name="Items", label="Items", type="MultiJoin",attr=dict(displayUrl="QuoteMultiJoinList",listUrl="QuoteMultiJoinList",linkUrl="QuoteItems"), data=Items_data)
	#Fields
	fields = [Id, Name, ValidOn, Notes, Vendor, QuoteRequest, Items]
	#Configure any of the links that might need configuring
	if id == '':
		QuoteMenu = 'QuoteMenu'
	else:
		QuoteMenu = 'QuoteMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='Quote', Label='Quote entry', Fields=fields, FieldsSrch=[Name], Read='Quote', Add='QuoteSave', Del='QuoteDel', UnDel='QuoteUnDel', Edit='Quote', Save='QuoteSave', SrchUrl='QuoteSearch', MenuBar=QuoteMenu)

@expose(format='json')
def QuoteMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("Quote")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("Quote")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("Quote")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("Quote?id='+id+'&Op=CopyIntoNew")'),  dict(label='Add/Edit Items', url='javascript:inv.openPickList("QuoteAddQuoteItems?id='+id+'")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def QuoteGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuote.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'ValidOn':validators.String(), 'Notes':validators.String(), 'Vendor':validators.Int(), 'QuoteRequest':validators.Int()})
def QuoteSave(self, Vendor, QuoteRequest, Id='', id='', ValidOn='', Notes='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuote.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if ValidOn != '':
		if len(ValidOn) > 10:
			ValidOn = time.strftime('%Y-%m-%d',time.strptime(ValidOn,'%Y-%m-%d %H:%M'))
		else:
			ValidOn = time.strftime('%Y-%m-%d',time.strptime(ValidOn,'%Y-%m-%d'))
		
	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				#Updating the record
				record.ValidOn = ValidOn
				record.Notes = Notes
				record.Vendor = Vendor
				record.QuoteRequest = QuoteRequest
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvQuote(QuoteRequest=QuoteRequest, Vendor=Vendor, Notes=Notes, ValidOn=ValidOn, Status='')
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
def QuoteDel(Id, id='', **kw):
	"""	If the Quote has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuote.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.Items)) == 0:
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
def QuoteUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuote.get(int_id)
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
def QuoteMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvQuote.get(int_id)
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
def QuoteAddQuoteItems(self, Id='', id='', data='', **kw):
	result_msg = ''
	if Id !='':
		id = Id
	if data!='' and id!='':
		QuoteID = int(id)
		data = simplejson.loads(data)
		#Update current entries
		q_items = model.InvQuoteItems.select(model.InvQuoteItems.q.QuoteID == QuoteID)
		tmp_data = []
		for q_item in q_items:
			updated = False
			for item in data:
				if (item.has_key('QuoteID') and (item['QuoteID'] == q_item.QuoteID)):
					updated = True
					record = model.InvQuoteItems.get(q_item.id)
					record.Product = item['Product']
					record.Price = float(item['Price'])
					record.Ranking = int(item['Ranking'])
					record.Notes = item['Notes']
					tmp_data.append(item)
			if not updated:
				q_item.destroySelf()
		#Add new entries
		for item in tmp_data:
			data.remove(tmp_data)
		for item in data:
			try:
				Ranking = int(item['Ranking'])
			except ValueError:
				Ranking = 100
			try:
				Price = float(item['Price'])
			except ValueError:
				Price = 0.0
			try:
				CatalogItemID = int(item['CatalogItemID'])
			except:
				raise
			if len(list(model.InvQuoteItems.select("inv_quote_items.quote_id="+str(id)+" AND inv_quote_items.catalog_item_id="+str(item['CatalogItemID'])))) == 0:
				new_item = model.InvQuoteItems(QuoteID=QuoteID, CatalogItemID=CatalogItemID, Ranking=Ranking, Price=Price, Product=item['Product'], Notes=item['Notes'], Status='')
	#find the quote request where to get the items from
	if id != '':
		record = model.InvQuote.get(int(id))
		QuoteRequestID = str(record.QuoteRequestID)
	else:
		QuoteRequestID = ''
	#Input variables
	Product = dict(id="qi_Product", name="Product", label="Product", type="String", attr=dict(length=10), data='')
	Price = dict(id="qi_Price", name="Price", label="Price", type="Numeric", attr=dict(length=5), data='')
	Ranking = dict(id="qi_Ranking", name="Ranking", label="Ranking", type="Numeric", attr=dict(length=2), data='')
	Notes = dict(id="qi_Notes", name="Notes", label="Notes", type="String", attr=dict(length=10), data='')
	#Search variable
	SrchId = dict(id="qi_SrchId", name="id", label="Quote request id", type="StringRO", attr=dict(length=25), data=QuoteRequestID)
	return dict(id=id, Name='QuoteAddQuoteItems', Label='Vendor quote entry', FieldsSrch=[SrchId], Inputs=[Price, Ranking, Product, Notes], SrchUrl='QuoteRequestItemsSearch', DataUrl='QuoteItemsSearch', Url='QuoteAddQuoteItems', UrlVars='id='+id, result_msg=result_msg, SrchNow=True)
	
@expose(format='json')
def QuoteSearch(self, Name='', VendorName='', ValidOn='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvVendor.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvVendor.q.id==model.InvQuote.q.VendorID,"
	if VendorName != '':
		qArgs+="model.InvVendor.q.Name.contains('"+ VendorName + "'),"
		qArgs+="model.InvVendor.q.id==model.InvQuote.q.VendorID,"
	if ValidOn != '':
		qArgs+="model.InvQuote.q.ValidOn.contains('"+ ValidOn + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvQuote.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvQuote.select()
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



