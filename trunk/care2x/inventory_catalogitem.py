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
def CatalogItem(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCatalogItem.get(int_id)
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
		Accounting_data = record.Accounting
		IsFixedAsset_data = record.IsFixedAsset
		IsService_data = record.IsService
		IsForSale_data = record.IsForSale
		IsSelectable_data = record.IsSelectable
		IsDispensable_data = record.IsDispensable
		Tax_data = record.Tax
		MinStockAmt_data = record.MinStockAmt
		ReorderAmt_data = record.ReorderAmt
		try:
			Compound_data = record.Compound.id
			Compound_display = record.Compound.Name + ' ('+str(record.Compound.id)+')'
		except AttributeError: 
			Compound_data = ''
			Compound_display = 'None'
		try:
			ParentItem_data = record.ParentItem.id
			ParentItem_display = record.ParentItem.Name + ' ('+str(record.ParentItem.id)+')'
		except AttributeError: 
			ParentItem_data = ''
			ParentItem_display = 'None'
		try:
			Packaging_data = record.Packaging.id
			Packaging_display = record.Packaging.Name + ' ('+str(record.Packaging.id)+')'
		except AttributeError: 
			Packaging_data = ''
			Packaging_display = 'None'
		#MultipleJoins
		ChildItems_data = 'There are ' + str(len(record.ChildItems)) + ' records'
		StockItems_data = 'There are ' + str(len(record.StockItems)) + ' records'
		CatalogGroups_data = 'There are ' + str(len(record.CatalogGroups)) + ' record(s)'
		if record.Status == 'deleted':
			DisplayMessage_data = "NOTE: This record is marked deleted!"
		else:
			DisplayMessage_data = ""
		#Tax label
		if record.IsService:
			tax_label = 'Service tax'
		else:
			tax_label = 'VAT'
	else:
		Id_data = ''
		Name_data = ''
		Description_data = ''
		Accounting_data = ''
		IsFixedAsset_data = ''
		IsService_data = ''
		IsForSale_data = ''
		IsSelectable_data = ''
		IsDispensable_data = ''
		Tax_data = ''
		MinStockAmt_data = ''
		ReorderAmt_data = ''
		ParentItem_data = ''
		ParentItem_display = 'None'
		Compound_data = ''
		Compound_display = 'None'
		Packaging_data = ''
		Packaging_display = 'None'
		ChildItems_data = 'There are no records'
		CatalogGroups_data = 'There are no records'
		StockItems_data = 'There are no records'
		DisplayMessage_data = ''
		tax_label = 'Tax'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		ChildItems_data = 'There are no records'
		CatalogGroups_data = 'There are no records'
		StockItems_data = 'There are no records'
		Id_data = ''
		id = ''
	elif Op == 'NewSubItem':
		ChildItems_data = 'There are no records'
		CatalogGroups_data = 'There are no records'
		StockItems_data = 'There are no records'
		ParentItem_data = Id_data
		ParentItem_display = record.Name + ' ('+str(record.id)+')'
		Name_data = ''
		Description_data = ''
		IsSelectable_data = ''
		Id_data = ''
		id=''
	#Construct our display fields
	Id = dict(id="ci_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="ci_Name", name="Name", label="Name", type="String",attr=dict(length=25), data=Name_data)
	Description = dict(id="ci_Description", name="Description", label="Description", type="Text",attr=dict(cols=30,rows=3), data=Description_data)
	Accounting = dict(id="ci_Accounting", name="Accounting", label="Account", type="String",attr=dict(length=25), data=Accounting_data)
	IsFixedAsset = dict(id="ci_IsFixedAsset", name="IsFixedAsset", label="Fixed asset",type="Bool",attr={}, data=IsFixedAsset_data)
	IsService = dict(id="ci_IsService", name="IsService", label="Service",type="Bool",attr={}, data=IsService_data)
	IsForSale = dict(id="ci_IsForSale", name="IsForSale", label="For sale",type="Bool",attr={}, data=IsForSale_data)
	IsSelectable = dict(id="ci_IsSelectable", name="IsSelectable", label="Selectable",type="Bool",attr={}, data=IsSelectable_data)
	IsDispensable = dict(id="ci_IsDispensable", name="IsDispensable", label="Dispensable",type="Bool",attr={}, data=IsDispensable_data)
	MinStockAmt = dict(id="ci_MinStockAmt", name="MinStockAmt", label='Min Stock Amt', type="Numeric",attr={}, data=MinStockAmt_data)
	ReorderAmt = dict(id="ci_ReorderAmt", name="ReorderAmt", label='Reorder Amt',type="Numeric",attr={}, data=ReorderAmt_data)
	Tax = dict(id="ci_Tax", name="Tax", label=tax_label,type="Numeric",attr={}, data=Tax_data)
	SrchPidName = dict(id="ci_SrchPidName", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	ParentItem = dict(id="ci_ParentItem", name="ParentItem", label="Parent catalog item", type="ForeignKey",attr=dict(srchUrl="CatalogItemSearch",lookupUrl="CatalogItemGet",srchFields=[SrchPidName]), data=ParentItem_data, init_display=ParentItem_display)
	#ForeignKey
	CompoundSrch = dict(id="ci_CompoundSrch", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Compound = dict(id="ci_Compound", name="Compound", label="Compound list", type="ForeignKey",attr=dict(srchUrl="CatalogCompoundSearch",lookupUrl="CatalogCompoundGet", edit_url='CatalogCompound', srchFields=[CompoundSrch]), data=Compound_data, init_display=Compound_display)
	PackagingSrch = dict(id="ci_PackagingSrch", name="Name", label="Name", type="String",attr=dict(length=25), data='')
	Packaging = dict(id="ci_Packaging", name="Packaging", label="Packaging type", type="ForeignKey",attr=dict(srchUrl="PackagingSearch",lookupUrl="PackagingGet",edit_url='Packaging', srchFields=[PackagingSrch]), data=Packaging_data, init_display=Packaging_display)
	#MultiJoin
	ChildItems = dict(id="ci_ChildItems", name="ChildItems", label="Child items", type="MultiJoin",attr=dict(displayUrl="CatalogItemMultiJoinList",listUrl="CatalogItemMultiJoinList",linkUrl="CatalogItem"), data=ChildItems_data)
	StockItems = dict(id="ci_StockItems", name="StockItems", label="Stock items", type="MultiJoin",attr=dict(displayUrl="CatalogItemMultiJoinList",listUrl="CatalogItemMultiJoinList",linkUrl="StockItem"), data=StockItems_data)
	#RelatedJoin
	SrchInvGrpName = dict(id="ci_SrchInvGrpName", name="Name", label="Group name", type="String",attr=dict(length=25), data='')
	CatalogGroups = dict(id="ci_CatalogGroups", name="CatalogGroups", label="Catalog groups", type="RelatedJoin", attr=dict(displayUrl="CatalogItemInvGroups", listUrl="CatalogItemInvGroups", srchUrl="InvGroupSearch", saveUrl='CatalogItemInvGroupSave', srchFields=[SrchInvGrpName]), data=CatalogGroups_data)
	DisplayMessage = dict(id="ci_DisplayMessage", name="DisplayMessage", type="Display",attr=dict(css_class='displaymsg'), data=DisplayMessage_data)		
	fields = [Id, Name, Description, CatalogGroups, ChildItems, Accounting, Tax, MinStockAmt, ReorderAmt, Compound, Packaging, StockItems, \
		ParentItem, IsFixedAsset, IsService, IsForSale, IsSelectable, IsDispensable]
	#Configure any of the links that might need configuring
	if id == '':
		CatalogItemMenu = 'CatalogItemMenu'
	else:
		CatalogItemMenu = 'CatalogItemMenu?id=' + id
	#Extra search fields
	InvGrpStockNames = []
	for item in model.InvGrpStock.select():
		InvGrpStockNames.append(item.Name)
	SrchCatalogGroups = dict(id="ci_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect",attr=dict(Groups=InvGrpStockNames), data='')
	#RETURN VALUES HERE
	return dict(id=id, Name='CatalogItem', Label='Inventory Catalog', Fields=fields, FieldsSrch=[Name, SrchCatalogGroups], Read='CatalogItem', Add='CatalogItemSave', Del='CatalogItemDel', UnDel='CatalogItemUnDel', Edit='CatalogItem', Save='CatalogItemSave', SrchUrl='CatalogItemSearch', MenuBar=CatalogItemMenu, TreeView='CatalogItemTree')

@expose(format='json')
def CatalogItemMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("CatalogItem")', menu=[dict(label='New sub item', url='javascript:inv.openObjForm("CatalogItem")'), dict(label='Copy into new', url='javascript:inv.openObjForm("CatalogItem")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Stock items', url=''), dict(label='Locations', url=''), dict(label='Purchase orders', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[
			dict(label='Quantity Report', url='/inventory/ReportCatalogItems'), dict(label='Price quotes', url=''), dict(label='Locations', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		record = model.InvCatalogItem.get(int(id))
		if record.CompoundID == None:
			mNew = dict(label='New', url='javascript:inv.openObjForm("CatalogItem")', menu=[dict(label='New sub item', url='javascript:inv.openObjForm("CatalogItem?id='+id+'&Op=NewSubItem")'), dict(label='Copy into new', url='javascript:inv.openObjForm("CatalogItem?id='+id+'&Op=CopyIntoNew")')])
		else:
			mNew = dict(label='New', url='javascript:inv.openObjForm("CatalogItem")', menu=[\
				dict(label='New sub item', url='javascript:inv.openObjForm("CatalogItem?id='+id+'&Op=NewSubItem")'),\
				dict(label='Copy into new', url='javascript:inv.openObjForm("CatalogItem?id='+id+'&Op=CopyIntoNew")'),\
				dict(label='Create new stock compound', url='StockItemCompoundCreateNew?id='+id)])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Stock items', url=''), dict(label='Locations', url=''), dict(label='Purchase orders', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView("CatalogItem")', menu=[dict(label='Purchase history', url=''), dict(label='Price quotes', url=''), dict(label='Store locations', url='')])
		mOps = dict(label='Special', url='', menu=[dict(label='Copy groups from Parents',url='javascript:inv.saveData("CatalogItemInheritGroups","id='+id+'")')])
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mOps, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def CatalogItemTree(self, **kw):
	def GetChildren(parent_item):
		nodes = []
		for item in parent_item.ChildItems:
			if item.Status != 'deleted':
				if len(item.ChildItems) > 0:
					children = GetChildren(item)
					nodes.append(dict(label=item.Name, href="javascript:inv.openObjView('CatalogItem?id="+str(item.id)+"')", nodes=children))
				else:
					nodes.append(dict(label=item.Name, href="javascript:inv.openObjView('CatalogItem?id="+str(item.id)+"')"))				
		return nodes
	nodes = []
	catalog = model.InvCatalogItem.select(model.InvCatalogItem.q.ParentItemID == None)
	for item in catalog:
		if item.Status != 'deleted':
			if len(item.ChildItems) > 0:
				children = GetChildren(item)
				nodes.append(dict(label=item.Name, href="javascript:inv.openObjView('CatalogItem?id="+str(item.id)+"')", nodes=children))
			else:
				nodes.append(dict(label=item.Name, href="javascript:inv.openObjView('CatalogItem?id="+str(item.id)+"')"))
	return dict(nodes=nodes)
		
@expose(format='json')
def CatalogItemGet(self, Id, field_id, **kw):
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
			record = model.InvCatalogItem.get(int_id)
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
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Name':validators.String(), 'Description':validators.String(), 'Accounting':validators.String(), 'Compound':validators.Int(), 'Packaging':validators.Int(), 'ParentItem':validators.Int(), 'IsSelectable':validators.StringBool(), 'IsDispensable':validators.StringBool(), 'IsFixedAsset':validators.StringBool(), 'IsService':validators.StringBool(), 'IsForSale':validators.StringBool(),'Tax':validators.Number(),'MinStockAmt':validators.Number(),'ReorderAmt':validators.Number()})
def CatalogItemSave(self, Compound, Packaging, ParentItem, Id = '',id = '', Name = '', Description = '', MinStockAmt=0.0, ReorderAmt=0.0, Tax = 0.0, Accounting = '',  IsSelectable = True, IsDispensable = True, IsFixedAsset = False, IsService = False, IsForSale = False, **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogItem.get(int_id)
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
				record.Accounting = Accounting
				record.Compound = Compound
				record.Packaging = Packaging
				record.ParentItem = ParentItem
				record.IsFixedAsset = IsFixedAsset
				record.IsService = IsService
				record.IsForSale = IsForSale
				record.IsSelectable = IsSelectable
				record.IsDispensable = IsDispensable
				record.Tax = Tax
				record.ReorderAmt = ReorderAmt
				record.MinStockAmt = MinStockAmt
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvCatalogItem(Name = Name,ReorderAmt = ReorderAmt, MinStockAmt = MinStockAmt, IsDispensable=IsDispensable, IsSelectable = IsSelectable, Description = Description, Accounting = Accounting, Compound = Compound, Packaging = Packaging, ParentItem = ParentItem, IsFixedAsset = IsFixedAsset, IsService = IsService, IsForSale = IsForSale, Tax = Tax, Status='')
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
def CatalogItemDel(Id, id='', **kw):
	"""	If the CatalogItem has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.ChildItems) + len(record.StockItems) + len(record.Requests) + len(record.Quotes) + \
				len(record.QuoteRequestItems) + len(record.POItems) + len(record.CatalogCompoundQtys) + \
				len(record.StockTransferRequestItems) + len(record.ReceiptItems)) == 0:
				#remove any groups the record might belong to
				for group in record.CatalogGroups:
					record.removeInvGrpStock(group)
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
def CatalogItemUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogItem.get(int_id)
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
def CatalogItemInvGroupSave(self, id='', field_num='', new_option_select='', **kw):
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCatalogItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	
	if int_id > 0:
		if record.Status == 'deleted':
			display = "RECORD MARKED DELETED: No updates allowed"
		else:
			#remove all related items from the field
			for group in record.CatalogGroups:
				record.removeInvGrpStock(group)
			#Now add all the groups we were given
			if len(new_option_select) > 0:
				new_option_select = set(new_option_select.split(","))
				for option in new_option_select:
					record.addInvGrpStock(int(option))
			#Make our return list
			rel_items = []
			for group in record.CatalogGroups:
				rel_items.append(dict(id=group.id, text=group.Name))
			display = "There are " + str(len(record.CatalogGroups)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='None', record={}, rel_items=[], field_num=field_num)
		
@expose(format='json')
def CatalogItemInvGroups(self, Id, field_num, **kw):
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvCatalogItem.get(int_id)
			rel_items = []
			for group in record.CatalogGroups:
				rel_items.append(dict(id=group.id, text=group.Name))
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	if int_id > 0:
		display = "There are " + str(len(record.CatalogGroups)) + " record(s) linked"
		return dict(display=display, record=record, rel_items=rel_items, field_num=field_num)
	else:	
		return dict(display='There are no records linked', record={},rel_items=[], field_id=field_num)		
	
@expose(format='json')
def CatalogItemMultiJoinList(self, id='', Id='', ColName='', field_num='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCatalogItem.get(int_id)
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
					if ColName == 'ChildItems':
						listing_text = item.Name + ', ' + item.Description
					elif ColName == 'StockItems':
						listing_text = item.DisplayName()
					records.append(dict(id=item.id, listing=listing_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def CatalogItemSearch(self, Name='', Description='', Groups='', field_num='',IsForSale='false', IsSelectable='false', show_del=True, **kw):
	log = logging.getLogger("care2x.controllers")
	qArgs = ""
	if Name != '':
		qArgs+="model.InvCatalogItem.q.Name.contains('"+ Name + "'),"
	if Description != '':
		qArgs+="model.InvCatalogItem.q.Description.contains('"+ Description + "'),"
	if IsSelectable.lower() == 'true':
		qArgs+="model.InvCatalogItem.q.IsSelectable == True,"
	if IsForSale.lower() == 'true':
		qArgs+="model.InvCatalogItem.q.IsForSale == True,"
	if Groups != '':
		Groups = set(Groups.split(","))
		orArgs = ''
		for group in Groups:
			orArgs+="model.InvGrpStock.q.Name == '"+group+"',"
		qArgs+= "OR ("+orArgs[0:len(orArgs)-1]+"),"
		qArgs+="model.InvGrpStock.q.id == model.InvViewJoinCatalogItemGrpStock.q.GrpStockId,"
		qArgs+="model.InvCatalogItem.q.id == model.InvViewJoinCatalogItemGrpStock.q.CatalogItemId,"
		#qArgs+="model.InvCatalogItem.q.id == table.inv_catalog_item_inv_grp_stock.inv_catalog_item_id,"
		#clauseTables.append("inv_catalog_item_inv_grp_stock")
	if len(qArgs) > 0:
		#log.debug("!!!!!!!!!!!!!!!! " + qArgs)
		items = eval('model.InvCatalogItem.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvCatalogItem.select()
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Name+' *** MARKED DELETED ***, '+item.Description
				results.append({'id':item.id, 'text':text, 'Name':item.Name+' *** MARKED DELETED ***', 'Description':item.Description})
			else:
				text = item.Name+', '+item.Description
				results.append({'id':item.id, 'text':text, 'Name':item.Name, 'Description':item.Description})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name, 'Description':item.Description})
	return dict(results=results, field_num=field_num, items=items)

@expose(format='json')
def CatalogItemSearch_old(self, Name='', Description='', Groups='', field_num='', IsSelectable=False, show_del=True, **kw):
	sqls = []
	tables = []
	if Name != '':
		val = model.sql_filter(my_table='inv_catalog_item', colName='name', var=Name)
		tables += val['clauseTables']
		sqls.append(val['sql'])
	if Description != '':
		val = model.sql_filter(my_table='inv_catalog_item', colName='description', var=Name)
		tables += val['clauseTables']
		sqls.append(val['sql'])
	if Groups != '':
		Groups = set(Groups.split(","))
		val = model.sql_related_join(my_table='inv_catalog_item', mid_table='inv_catalog_item_inv_grp_stock', join_table='inv_grp_stock', keys=Groups, colName='name')
		tables += val['clauseTables']
		sqls.append(val['sql'])
	if IsSelectable:
		val = model.sql_filter(my_table='inv_catalog_item', colName='name', var=IsSelectable)
		tables += val['clauseTables']
		sqls.append(val['sql'])
	if len(sqls) > 0:
		val = model.sql_merge(sqls=sqls, clauseTables=tables)
		items = model.InvCatalogItem.select(val['sql'], clauseTables=val['clauseTables'], distinct=True)
	else:
		items = model.InvCatalogItem.select()
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.Name+' *** MARKED DELETED ***, '+item.Description
				results.append({'id':item.id, 'text':text, 'Name':item.Name+' *** MARKED DELETED ***', 'Description':item.Description})
			else:
				text = item.Name+', '+item.Description
				results.append({'id':item.id, 'text':text, 'Name':item.Name, 'Description':item.Description})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name, 'Description':item.Description})
	return dict(results=results, field_num=field_num, items=items)
	
@expose(format='json')
def CatalogItemInheritGroups(self, id='', Id='', **kw):
	#	Append the list of groups from all the items parent items to
	#	this item.
	#
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvCatalogItem.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	
	if int_id > 0:
		if record.Status == 'deleted':
			display = "RECORD MARKED DELETED: No updates allowed"
		else:
			#record all groups into an array
			group_list = []
			#1st for the groups I already have
			for group in record.CatalogGroups:
				group_list.append(group)
			#2nd for the groups in my parents
			cur_rec = record.ParentItem
			while cur_rec:
				for group in cur_rec.CatalogGroups:
					group_list.append(group)
				cur_rec = cur_rec.ParentItem
			#remove all related items from the field
			for group in record.CatalogGroups:
				record.removeInvGrpStock(group)
			#Now add all the groups we were given
			if len(group_list) > 0:
				group_set = set(group_list)
				for group in group_set:
					record.addInvGrpStock(group)
		return dict(id=id, result_msg="Record updated", result=1)
	else:	
		return dict(id=id, result_msg="ERROR: update failed!", result=0)
	
@expose(format='json')
def InvGroupSearch(self, Name='', Description='',Groups='', field_num='', **kw):
	qArgs = ""
	if Name != '':
		qArgs+="model.InvGrpStock.q.Name.contains('"+ Name + "'),"
	if Description != '':
		qArgs+="model.InvGrpStock.q.Description.contains('"+ Description + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvGrpStock.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
	else:
		items = model.InvGrpStock.select()
	results = []
	for item in items:
		results.append(dict(id=item.id, text=item.Name))
	return dict(results=results, field_num=field_num)		
