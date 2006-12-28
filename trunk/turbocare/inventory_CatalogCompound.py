import logging
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
def CatalogCompound(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCatalogCompound.get(int_id)
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
		ResultQty_data = str(record.ResultQty)
		#ForeignKey
		try:
			Location_data = record.ConsumedLocationID
			Location_display = record.ConsumedLocation.Name + ' ('+str(record.ConsumedLocationID)+')'
		except AttributeError: 
			Location_data = ''
			Location_display = 'None'
		#MultipleJoin and relatedJoins
		Groups_data = 'There are ' + str(len(record.Groups)) + ' records'
		ItemQtys_data = 'There are ' + str(len(record.ItemQtys)) + ' records'
	else:
		Id_data = ''
		Name_data = ''
		Description_data = ''
		ResultQty_data = ''
		#ForeignKey
		Location_data = ''
		Location_display = 'None'
		#MultipleJoin and relatedJoins
		Groups_data = 'There are no records'
		ItemQtys_data = 'There are no records'
	if Op == 'CopyIntoNew':
		Groups_data = 'There are no records'
		ItemQtys_data = 'There are no records'
		Id_data = ''
		id = ''
	#Construct our display fields
	Id = dict(id="cc_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="cc_Name", name="Name", label="Name", type="String",attr=dict(length=25), data=Name_data)
	Description = dict(id="cc_Description", name="Description", label="Description", type="Text",attr=dict(cols=40,rows=3), data=Description_data)
	ResultQty = dict(id="cc_ResultQty", name="ResultQty", label="Result qty", type="Numeric",attr=dict(), data=ResultQty_data)
	#ForeignKey
	SrchLocationName = dict(id="cc_SrchLocationName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	ConsumedLocation = dict(id="cc_ConsumedLocation", name="ConsumedLocation", label="Compound location", type="ForeignKey",attr=dict(srchUrl="LocationSearch",lookupUrl="LocationGet", edit_url='Location', srchFields=[SrchLocationName]), data=Location_data, init_display=Location_display)
	#MultipleJoin
	ItemQtys = dict(id="ci_ItemQtys", name="ItemQtys", label="Item qtys", type="MultiJoin",attr=dict(displayUrl="CatalogCompoundMultiJoinList",listUrl="CatalogCompoundMultiJoinList",linkUrl="CatalogCompoundQty"), data=ItemQtys_data)
	#RelatedJoin
	SrchGroups = dict(id="cc_SrchGroups", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Groups = dict(id="cc_Groups", name="Groups", label="Groups", type="RelatedJoin", attr=dict(displayUrl="CatalogCompoundGroups", listUrl="CatalogCompoundGroups", srchUrl="GrpCompoundSearch", saveUrl='CatalogCompoundGroupsSave', srchFields=[SrchGroups]), data=Groups_data)
	fields = [Id, Name, Description, ResultQty, ConsumedLocation, ItemQtys, Groups]
	#Configure any of the links that might need configuring
	if id == '':
		CatalogCompoundMenu = 'CatalogCompoundMenu'
	else:
		CatalogCompoundMenu = 'CatalogCompoundMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='CatalogCompound', Label='Catalog Compound', Fields=fields, FieldsSrch=[Name], Read='CatalogCompound', Add='CatalogCompoundSave', Del='CatalogCompoundDel', UnDel='CatalogCompoundUnDel', Edit='CatalogCompound', Save='CatalogCompoundSave', SrchUrl='CatalogCompoundSearch', MenuBar=CatalogCompoundMenu)

@expose(format='json')
def CatalogCompoundMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("CatalogCompound")', menu=[dict(label='Copy into new', url='javascript:inv.openObjForm("CatalogCompound")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("CatalogCompound")', menu=[\
			dict(label='Copy into new', url='javascript:inv.openObjForm("CatalogCompound?id='+id+'&Op=CopyIntoNew")'),\
			dict(label='Add ingredients', url='javascript:inv.openPickList("CatalogCompoundAddQty?id='+id+'")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Items', url='')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def CatalogCompoundGet(self, id='', Id='', field_id='', field_num='', **kw):
	if id !='':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogCompound.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		if record.Status == 'deleted':
			display = record.Name + ' ('+str(record.id)+') **MARKED DELETED***'
		else:
			display = record.Name + ' ('+str(record.id)+')'
		return dict(display=display, record=record, field_id=field_id)
	else:	
		return dict(display='None', record={}, field_id=field_id)

@expose(format='json')
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Name':validators.String(), 'Description':validators.String(), 'ConsumedLocation':validators.Int()})
def CatalogCompoundSave(self, Id = '',id = '', Name = '', Description = '', ConsumedLocation=None, **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogCompound.get(int_id)
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
				record.ConsumedLocation = ConsumedLocation
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvCatalogCompound(Name = Name, ConsumedLocation=ConsumedLocation, Description = Description, Status='')
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
def CatalogCompoundDel(Id, id='', **kw):
	"""	If the CatalogCompound has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogCompound.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.ItemQtys) == 0):
				for item in record.Groups:
					record.removeInvGrpCompound(item)
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
def CatalogCompoundUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogCompound.get(int_id)
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
def CatalogCompoundGroupsSave(self, id='',Id='', field_num='', new_option_select='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCatalogCompound.get(int_id)
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
				record.removeInvGrpCompound(item)
			#Now add all the groups we were given
			if len(new_option_select) > 0:
				new_option_select = set(new_option_select.split(","))
				for option in new_option_select:
					record.addInvGrpCompound(int(option))
			#Make our return list
			rel_items = []
			for group in record.Groups:
				rel_items.append(dict(id=group.id, text=group.Name))
			display = "There are " + str(len(record.Groups)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='None', record={}, rel_items=[], field_num=field_num)
		
@expose(format='json')
def CatalogCompoundGroups(self, Id, field_num, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogCompound.get(int_id)
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
def CatalogCompoundMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCatalogCompound.get(int_id)
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
					if ColName == 'ItemQtys':
						list_text = item.Name()
					records.append(dict(id=item.id, listing=list_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def CatalogCompoundSearch(self, id='', Id='', Name='', Description='',Groups=[], field_num='', show_del=True, **kw):
	qArgs = ""
	if Id != '':
		id = Id
	if Name != '':
		qArgs+="model.InvCatalogCompound.q.Name.contains('"+ Name + "'),"
	if Description != '':
		qArgs+="model.InvCatalogCompound.q.Description.contains('"+ Description + "'),"
	if id != '':
		qArgs+="model.InvCatalogCompound.q.id == " + id + ","
	if len(qArgs) > 0:
		items = eval('model.InvCatalogCompound.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvCatalogCompound.select()
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
def CatalogCompoundSaveQty(self, id='', Id='', data='', **kw):
	result_msg = ''
	if Id !='':
		id = Id
	if data!='' and id!='':
		CatalogCompoundID = int(id)
		data = simplejson.loads(data)
		#Update current entries
		qty_items = model.InvCatalogCompoundQty.select(model.InvCatalogCompoundQty.q.CatalogCompoundID == CatalogCompoundID)
		tmp_data = []
		for qty_item in qty_items:
			updated = False
			for item in data:
				if (item.has_key('CatalogItemID') and (item['CatalogItemID'] == qty_item.CatalogItemID)) or \
					((not item.has_key('CatalogItemID')) and item['id'] == qty_item.CatalogItemID):
					updated = True
					record = model.InvCatalogCompoundQty.get(qty_item.id)
					try:
						Quantity = int(item['Qty'])
					except ValueError:
						Quantity = 0
					record.Qty = Quantity
					record.Description = item['Description']
					tmp_data.append(item)
			if not updated:
				qty_item.destroySelf()
		for item in tmp_data:
			data.remove(item)
		#Add new entries
		for item in data:
			try:
				Quantity = int(item['Qty'])
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
			if len(list(model.InvCatalogCompoundQty.select(AND (model.InvCatalogCompoundQty.q.CatalogItemID == \
				CatalogItemID, model.InvCatalogCompoundQty.q.CatalogCompoundID == CatalogCompoundID)))) == 0:
				new_item = model.InvCatalogCompoundQty(CatalogCompoundID=CatalogCompoundID, CatalogItemID=CatalogItemID, \
					Qty=Quantity, Description=item['Description'])
	return dict(result_msg=result_msg)

@expose(format='json')
def CatalogCompoundAddQty(self, id='', Id='', data='', **kw):
	result_msg = ''
	if Id != '':
		id = Id
	Qty = dict(id="cc_Qty", name="Qty", label="Quantity", type="String", attr=dict(length=25), data='')
	Description = dict(id="cc_SrchDescription", name="Description", label="Description", type="String", attr=dict(length=25), data='')
	Name = dict(id="cc_SrchName", name="Name", label="Name", type="String", attr=dict(length=25), data='')
	InvGrpStockNames = []
	for item in model.InvGrpStock.select():
		InvGrpStockNames.append(item.Name)
	SrchCatalogGroups = dict(id="cc_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect", attr=dict(Groups=InvGrpStockNames), data='')
	return dict(id=id, Name='CatalogCompoundAddQty', Label='Select items from catalog', \
		FieldsSrch=[Name, SrchCatalogGroups], Inputs=[Qty, Description], SrchUrl='CatalogItemSearch', \
		DataUrl='CatalogCompoundQtySearch', Url='CatalogCompoundSaveQty', UrlVars='id='+id, result_msg=result_msg, \
		SrchNow=False, NoAjax=False)

