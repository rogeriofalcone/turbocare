import logging
from datetime import datetime, date
import simplejson
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
def StockTransferRequest(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockTransferRequest.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Notes_data = record.Notes
		RequestedBy_data = record.RequestedBy
		RequestedOn_data = record.RequestedOn
		RequiredBy_data = record.RequiredBy
		#ForeignKeys
		try:
			ForLocation_data = record.ForLocation.id
			ForLocation_display = record.ForLocation.Name + ' ('+str(record.ForLocation.id)+')'
		except AttributeError: 
			ForLocation_data = ''
			ForLocation_display = 'None'
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
		RequestedBy_data = model.cur_user_id()
		RequestedOn_data = model.cur_date_time().strftime('%Y-%m-%d')
		RequiredBy_data = model.cur_date_time().strftime('%Y-%m-%d')
		#ForeignKeys
		ForLocation_data = ''
		ForLocation_display = 'None'
		#MultiJoin and RelatedJoin
		Items_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		#ForeignKeys
		Name_data = ''
		RequestedBy_data = model.cur_user_id()
		RequestedOn_data = model.cur_date_time().strftime('%Y-%m-%d')
		RequiredBy_data = model.cur_date_time().strftime('%Y-%m-%d')
		#MultiJoin and RelatedJoin
		Items_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="str_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="str_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	RequestedBy = dict(id="str_RequestedBy", name="RequestedBy", label="Requested by", type="StringRO",attr=dict(length=50), data=RequestedBy_data)
	RequestedOn = dict(id="str_RequestedOn", name="RequestedOn", label="Requested on", type="DateTime",attr=dict(), data=RequestedOn_data)
	RequiredBy = dict(id="str_RequiredBy", name="RequiredBy", label="Required by", type="DateTime",attr=dict(), data=RequiredBy_data)
	Notes = dict(id="str_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	#ForeignKeys
	SrchLocationName = dict(id="str_SrchLocationName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	ForLocation = dict(id="str_ForLocation", name="ForLocation", label="ForLocation", type="ForeignKey",attr=dict(srchUrl="LocationSearch",lookupUrl="LocationGet", edit_url='Location', srchFields=[SrchLocationName]), data=ForLocation_data, init_display=ForLocation_display)
	#MultiJoin
	Items = dict(id="str_Items", name="Items", label="Items", type="MultiJoin",attr=dict(displayUrl="StockTransferRequestMultiJoinList",listUrl="StockTransferRequestMultiJoinList", linkUrl="StockTransferRequestItem"), data=Items_data)
	#Fields
	fields = [Id, Name, RequestedBy, RequestedOn, RequiredBy, ForLocation, Items, Notes]
	#Configure any of the links that might need configuring
	if id == '':
		StockTransferRequestMenu = 'StockTransferRequestMenu'
	else:
		StockTransferRequestMenu = 'StockTransferRequestMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='StockTransferRequest', Label='Stock transfer request entry', Fields=fields, FieldsSrch=[Name], Read='StockTransferRequest', Add='StockTransferRequestSave', Del='StockTransferRequestDel', UnDel='StockTransferRequestUnDel', Edit='StockTransferRequest', Save='StockTransferRequestSave', SrchUrl='StockTransferRequestSearch', MenuBar=StockTransferRequestMenu)

@expose(format='json')
def StockTransferRequestMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockTransferRequest")', menu=[ \
			dict(label='Fill in requests', url='StockTransferCreateNew')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("StockTransferRequest")', \
			menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("StockTransferRequest?id='+id+'&Op=CopyIntoNew")'), \
			dict(label='Add Items', url='javascript:inv.openPickList("StockTransferRequestAddStockItems?id='+id+'")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def StockTransferRequestGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransferRequest.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'RequestedOn':validators.String(), 'RequiredBy':validators.String(), 'Notes':validators.String(), 'ForLocation':validators.Int()})
def StockTransferRequestSave(self, ForLocation, Id='', id='', RequestedOn='', RequiredBy='',  Notes='', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransferRequest.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if RequestedOn != '':
		if len(RequestedOn) > 16:
			RequestedOn = datetime.fromtimestamp(time.mktime(time.strptime(RequestedOn,'%Y-%m-%d %H:%M:%S')))
		elif len(RequestedOn) > 10:
			RequestedOn = datetime.fromtimestamp(time.mktime(time.strptime(RequestedOn,'%Y-%m-%d %H:%M')))
		else:
			RequestedOn = datetime.fromtimestamp(time.mktime(time.strptime(RequestedOn,'%Y-%m-%d')))
	if RequiredBy != '':
		if len(RequiredBy) > 16:
			RequiredBy = datetime.fromtimestamp(time.mktime(time.strptime(RequiredBy,'%Y-%m-%d %H:%M:%S')))
		elif len(RequiredBy) > 10:
			RequiredBy = datetime.fromtimestamp(time.mktime(time.strptime(RequiredBy,'%Y-%m-%d %H:%M')))
		else:
			RequiredBy = datetime.fromtimestamp(time.mktime(time.strptime(RequiredBy,'%Y-%m-%d')))
		
	try:
		if int_id > 0:
			if record.Status == 'deleted':
				result_msg="Cannot update a deleted record."
				result = 0
			else:
				#Updating the record
				record.RequestedOn = RequestedOn
				record.RequiredBy = RequiredBy
				record.ForLocation = ForLocation
				record.Notes = Notes
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvStockTransferRequest(Notes=Notes, ForLocation=ForLocation, RequiredBy=RequiredBy, RequestedOn=RequestedOn, RequestedBy=model.cur_user_id(), Status='')
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
def StockTransferRequestDel(Id, id='', **kw):
	"""	If the StockTransferRequest has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransferRequest.get(int_id)
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
def StockTransferRequestUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvStockTransferRequest.get(int_id)
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
def StockTransferRequestMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvStockTransferRequest.get(int_id)
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
						line_text = item.Name()
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

def SortItems(self, items):
	sorted_items = []
	def Insert(item, items):
		if len(items) == 0:
			items.append(item)
		elif len(items) == 1:
			if items[0].Sort() <= item.Sort():
				items.append(item)
			else:
				items.insert(0,item)
		elif len(items) == 2:
			if items[0].Sort() >= item.Sort():
				items.insert(0,item)
			elif items[1].Sort >= item.Sort():
				items.insert(1,item)
			else:
				items.append(item)
		elif items[0].Sort() >= item.Sort():
			items.insert(0,item)
		elif items[len(items)-1].Sort() <= item.Sort():
			items.append(item)
		else:
			mid = int(len(items)/2)
			if items[mid].Sort() > item.Sort():
				items = Insert(item,items[0:mid]) + items[mid:]
			else:
				items = items[0:mid] + Insert(item,items[mid:])
		return items
	sorted_items = []
	for item in items:
		Insert(item,sorted_items)
	return sorted_items

@expose(format='json')
def StockTransferRequestSearch(self, Name='', LocationName='', RequestedOn='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvCatalogItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvStockTransferRequestItem.q.CatalogItemID == model.InvCatalogItem.q.id,"
		qArgs+="model.InvStockTransferRequestItem.q.StockTransferRequestID == model.InvStockTransferRequest.q.id,"
	if LocationName != '':
		qArgs+="model.InvLocation.q.Name.contains('"+ LocationName + "'),"
	if RequestedOn != '':
		qArgs+="model.InvStockTransferRequest.q.RequestedOn.contains('"+ RequestedOn + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvStockTransferRequest.select(AND ('+qArgs[0:len(qArgs)-1]+'),orderBy=[model.InvStockTransferRequest.q.Status, model.InvStockTransferRequest.q.RequiredBy, model.InvStockTransferRequest.q.RequestedOn])')
	else:
		items = model.InvStockTransferRequest.select(orderBy=[model.InvStockTransferRequest.q.Sort])
	#sorted_items = self.SortItems(items)
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

@expose()
def StockTransferRequestSaveStockItems(self, Id='', id='', data='', **kw):
	result_msg = ''
	if Id !='':
		id = Id
	if data!='' and id!='':
		StockTransferRequestID = int(id)
		data = simplejson.loads(data)
		#Update current entries
		str_items = model.InvStockTransferRequest.select(model.InvStockTransferRequestItem.q.StockTransferRequestID == StockTransferRequestID)
		tmp_data = []
		for str_item in str_items:
			updated = False
			for item in data:
				if (item.has_key('CatalogItemID') and (item['CatalogItemID'] == str_item.CatalogItemID)) or ((not item.has_key('CatalogItemID')) and item['id'] == str_item.CatalogItemID):
					updated = True
					record = model.InvStockTransferRequestItem.get(str_item.id)
					try:
						Quantity = int(item['edQty'])
					except ValueError:
						Quantity = 0
					record.Qty = Quantity
					record.Notes = item['edNotes']
					tmp_data.append(item)
			if not updated:
				str_item.destroySelf()
		#Remove updated items from the list
		for item in tmp_data:
			data.remove(tmp_data)
		#Add new entries
		for item in data:
			try:
				Quantity = int(item['edQty'])
			except ValueError:
				Quantity = 0
			if item.has_key('CatalogItemID'):
				try:
					CatalogItemID = int(item['CatalogItemID'])
				except:
					raise
			else:
				try:
					CatalogItemID = int(item['id'])
				except:
					raise
			if len(list(model.InvStockTransferRequestItem.select("inv_stock_transfer_request_item.stock_transfer_request_id="+str(id)+" AND inv_stock_transfer_request_item.catalog_item_id="+str(item['id'])))) == 0:
				new_item = model.InvStockTransferRequestItem(StockTransferRequestID=StockTransferRequestID, CatalogItemID=CatalogItemID, Qty=Quantity, Notes=item['edNotes'])
	return dict(id=id, Name='StockTransferRequestSaveStockItems', Label='Stock transfer request items saved', result_msg="Stock transfer request items added")

@expose(format='json')
def StockTransferRequestAddStockItems(self, Id='', id='', data='', **kw):
	result_msg = ""
	
	Qty = dict(id="str_QuantityReceived", name="edQty", label="Quantity requesting", type="Numeric", attr=dict(length=10), data='')
	Notes = dict(id="str_Notes", name="edNotes", label="Notes", type="String", attr=dict(length=40), data='')
	#Search variables
	Name = dict(id="qri_Name", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	InvGrpStockNames = []
	for item in model.InvGrpStock.select():
		InvGrpStockNames.append(item.Name)
	SrchCatalogGroups = dict(id="qri_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect",attr=dict(Groups=InvGrpStockNames), data='')
	return dict(id=id, Name='StockTransferRequestAddStockItems', Label='Stock transfer request item selection', \
		FieldsSrch=[Name, SrchCatalogGroups], Inputs=[Qty, Notes], SrchUrl='CatalogItemSearch', \
		DataUrl='StockTransferRequestItemSearch', Url='StockTransferRequestSaveStockItems', UrlVars='id='+id, result_msg=result_msg, SrchNow=False)

@expose(html='care2x.templates.procedure')
def UpdateTransferRequestSortOrder(self, **kw):
	start_time = datetime.now()
	items = model.InvStockTransferRequest.select()
	for item in items:
		item.Sort = item.CalcSort()
	diff = datetime.now() - start_time
	message = 'Transfer request sort-order re-calculation took %d days and %d seconds' % (diff.days, diff.seconds)
	return dict(message=message)
