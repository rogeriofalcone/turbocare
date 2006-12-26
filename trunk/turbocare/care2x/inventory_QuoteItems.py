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
def QuoteItems(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvQuoteItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name()
		Notes_data = record.Notes
		Product_data = record.Product
		Price_data = record.Price
		Ranking_data = record.Ranking
		#ForeignKeys
		try:
			Quote_data = record.Quote.id
			Quote_display = record.Quote.Name() + ' ('+str(record.Quote.id)+')'
		except AttributeError: 
			Quote_data = ''
			Quote_display = 'None'
		try:
			CatalogItem_data = record.CatalogItem.id
			CatalogItem_display = record.CatalogItem.Name + ' ('+str(record.CatalogItem.id)+')'
		except AttributeError: 
			CatalogItem_data = ''
			CatalogItem_display = 'None'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
	else:
		Id_data = ''
		Name_data = ''
		Notes_data = ''
		Product_data = ''
		Price_data = ''
		Ranking_data = ''
		#ForeignKeys
		Quote_data = ''
		Quote_display = 'None'
		CatalogItem_data = ''
		CatalogItem_display = 'None'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="qi_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="qi_Name", name="Name", label="Name", type="StringRO",attr=dict(length=50), data=Name_data)
	Product = dict(id="qi_Product", name="Product", label="Product name", type="String",attr=dict(length=50), data=Product_data)
	Notes = dict(id="qi_Notes", name="Notes", label="Notes", type="String",attr=dict(length=50), data=Notes_data)
	Price = dict(id="qi_Price", name="Price", label="Price", type="Currency",attr=dict(length=50), data=Price_data)
	Ranking = dict(id="qi_Ranking", name="Ranking", label="Ranking", type="Numeric",attr=dict(length=50), data=Ranking_data)
	#ForeignKeys
	SrchQuoteVendorName = dict(id="qi_SrchQuoteVendorName", name="VendorName", label="Vendor name", type="String",attr=dict(length=25), data='')
	Quote = dict(id="qi_Quote", name="Quote", label="Quote", type="ForeignKey",attr=dict(srchUrl="QuoteSearch",lookupUrl="QuoteGet", edit_url='Quote', srchFields=[SrchQuoteVendorName]), data=Quote_data, init_display=Quote_display)
	SrchCatalogName = dict(id="qi_SrchCatalogName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	CatalogItem = dict(id="qi_CatalogItem", name="CatalogItem", label="Catalog item", type="ForeignKey",attr=dict(srchUrl="CatalogItemSearch",lookupUrl="CatalogItemGet", edit_url='CatalogItem', srchFields=[SrchCatalogName]), data=CatalogItem_data, init_display=CatalogItem_display)
	#Fields
	fields = [Id, Name, Product, Notes, Price, Ranking, Quote, CatalogItem]
	#Configure any of the links that might need configuring
	if id == '':
		QuoteItemsMenu = 'QuoteItemsMenu'
	else:
		QuoteItemsMenu = 'QuoteItemsMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='QuoteItems', Label='Quote items entry', Fields=fields, FieldsSrch=[Name], Read='QuoteItems', Add='QuoteItemsSave', Del='QuoteItemsDel', UnDel='QuoteItemsUnDel', Edit='QuoteItems', Save='QuoteItemsSave', SrchUrl='QuoteItemsSearch', MenuBar=QuoteItemsMenu)

@expose(format='json')
def QuoteItemsMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("QuoteItems")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("QuoteItems")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("QuoteItems")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("QuoteItems?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url=''), dict(label='History', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def QuoteItemsGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		return dict(display=record.Name(), record=record, field_id=field_id, field_num=field_num)
	else:	
		return dict(display='None', record={}, field_id=field_id, field_num=field_num)
	
@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Product':validators.String(), 'Notes':validators.String(), 'Price':validators.Number(), 'Ranking':validators.Int(), 'Quote':validators.Int(), 'CatalogItem':validators.Int()})
def QuoteItemsSave(self, Quote, CatalogItem, Id='', id='', Product='', Notes='', Ranking=-1, **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteItems.get(int_id)
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
				record.Product = Product
				record.Notes = Notes
				record.Price = Price
				record.Ranking = Ranking
				record.Quote = Quote
				record.CatalogItem = CatalogItem
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvQuoteItems(CatalogItem=CatalogItem, Quote=Quote, Ranking=Ranking, Price=Price, Notes=Notes, Product=Product, Status='')
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
def QuoteItemsDel(Id, id='', **kw):
	"""	If the QuoteItems has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvQuoteItems.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#No references for these objects, so I'll delete completely
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
def QuoteItemsMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvQuoteItems.get(int_id)
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
					line_text = 'Something'
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def QuoteItemsSearch(self, Id='', id='', Name='',CatalogItemName='', VendorName='', field_num='', show_del=True, **kw):
	qArgs = ""
	if Id != '':
		id = Id
	if Name != '':
		qArgs+="model.InvQuoteItems.q.CatalogItem.Name.contains('"+ Name + "'),"
	if VendorName != '':
		qArgs+="model.InvQuoteItems.q.Quote.Vendor.Name.contains('"+ VendorName + "'),"
	if CatalogItemName != '':
		qArgs+="model.InvQuoteItems.q.CatalogItem.Name.contains('"+ CatalogItemName + "'),"
	if id != '':
		qArgs+="model.InvQuoteItems.q.QuoteID == "+ id + ","
	if len(qArgs) > 0:
		items = eval('model.InvQuoteItems.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvQuoteItems.select()
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
