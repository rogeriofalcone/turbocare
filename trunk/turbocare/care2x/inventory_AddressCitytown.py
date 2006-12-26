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
def AddressCitytown(self, id='',Id='', Op='', **kw):
	if Id != '':
		id = Id
	if id != '':
		try:
			int_id = int(id)
			record = model.InvAddressCitytown.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
	#Find initial values for our data record
	District = StringCol(length=60,default=None)#char 60
	State = StringCol(length=60, default='Nagaland')#char 60

	if int_id > 0:
		Id_data = record.id
		Name_data = record.Name
		if record.Status == 'deleted':
			Name_data += ' *** MARKED DELETED ***'
		ZipCode_data = record.ZipCode
		IsoCountryId_data = record.IsoCountryId
		Block_data = record.Block
		District_data = record.District
		State_data = record.State
		Vendors_data = 'There are ' + str(len(record.Vendors)) + ' records'
		Customers_data = 'There are ' + str(len(record.Customers)) + ' records'
	else:
		Id_data = ''
		Name_data = ''
		ZipCode_data = ''
		IsoCountryId_data = ''
		Block_data = ''
		District_data = ''
		State_data = ''
		Vendors_data = 'There are no records'
		Customers_data = 'There are no records'
	#Special manipulations for new records
	if Op == 'CopyIntoNew':
		Id_data = ''
		id = ''
	elif Op == 'NewSubItem':
		Name_data = ''
		ZipCode_data = record.ZipCode
		IsoCountryId_data = record.IsoCountryId
		Block_data = ''
		District_data = record.District
		State_data = record.State
		Id_data = ''
		id=''
	#Construct our display fields
	Id = dict(id="act_Id", name="Id", label="Id", type="Hidden",attr={}, data=Id_data)
	Name = dict(id="act_Name", name="Name", label="City name", type="String",attr=dict(length=25), data=Name_data)
	Block = dict(id="act_Block", name="Block", label="Block", type="String",attr=dict(length=25), data=Block_data)
	ZipCode = dict(id="act_ZipCode", name="ZipCode", label="Pin code", type="String",attr=dict(length=25), data=ZipCode_data)
	IsoCountryId = dict(id="act_IsoCountryId", name="IsoCountryId", label="Country id",type="String",attr=dict(length=3), data=IsoCountryId_data)
	District = dict(id="act_District", name="District", label="District",type="String",attr=dict(length=25), data=District_data)
	State = dict(id="act_State", name="State", label="State",type="String",attr=dict(length=25), data=State_data)
	Vendors = dict(id="act_Vendors", name="Vendors", label="Vendors", type="MultiJoin",attr=dict(displayUrl="AddressCitytownMultiJoinList",listUrl="AddressCitytownMultiJoinList",linkUrl="Vendor"), data=Vendors_data)
	Customers = dict(id="act_ChildItems", name="Customers", label="Customers", type="MultiJoin",attr=dict(displayUrl="AddressCitytownMultiJoinList",listUrl="AddressCitytownMultiJoinList",linkUrl="Customer"), data=Customers_data)
	fields = [Id, Block, Name, District, ZipCode, State, IsoCountryId, Vendors, Customers]
	#Configure any of the links that might need configuring
	if id == '':
		AddressCitytownMenu = 'AddressCitytownMenu'
	else:
		AddressCitytownMenu = 'AddressCitytownMenu?id=' + id
	#RETURN VALUES HERE
	return dict(id=id, Name='AddressCitytown', Label='City/town locations', Fields=fields, FieldsSrch=[Name,District], Read='AddressCitytown', Add='AddressCitytownSave', Del='AddressCitytownDel', UnDel='AddressCitytownUnDel', Edit='AddressCitytown', Save='AddressCitytownSave', SrchUrl='AddressCitytownSearch', MenuBar=AddressCitytownMenu)

@expose(format='json')
def AddressCitytownMenu(self, id='',Id='', **kw):
	if Id != '':
		id = Id
	if id=='':
		mNew = dict(label='New', url='javascript:inv.openObjForm("AddressCitytown")', menu=[dict(label='New sub item', url='javascript:inv.openObjForm("AddressCitytown")'), dict(label='Copy into new', url='javascript:inv.openObjForm("AddressCitytown")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Stock items', url=''), dict(label='Locations', url=''), dict(label='Purchase orders', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView()', menu=[dict(label='Purchase history', url=''), dict(label='Price quotes', url=''), dict(label='Locations', url='')])
		mMenuBar = [mNew, mView, mReports]
	else:
		mNew = dict(label='New', url='javascript:inv.openObjForm("AddressCitytown")', menu=[dict(label='New sub item', url='javascript:inv.openObjForm("AddressCitytown?id='+id+'&Op=NewSubItem")'), dict(label='Copy into new', url='javascript:inv.openObjForm("AddressCitytown?id='+id+'&Op=CopyIntoNew")')])
		mView = dict(label='View', url='javascript:inv.openObjView()', menu=[dict(label='Stock items', url=''), dict(label='Locations', url=''), dict(label='Purchase orders', url='')])
		mReports = dict(label='Reports', url='javascript:inv.openObjView("AddressCitytown")', menu=[dict(label='Purchase history', url=''), dict(label='Price quotes', url=''), dict(label='Store locations', url='')])		
		mRecord = dict(label='Delete', url='javascript:inv.deleteObj()', menu=[dict(label='Un-Delete', url='javascript:inv.undeleteObj()')])
		mMenuBar = [mNew, mView, mReports, mRecord]
	return dict(menu=mMenuBar)
		
@expose(format='json')
def AddressCitytownGet(self, Id, field_id, field_num='', **kw):
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
			record = model.InvAddressCitytown.get(int_id)
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
@validate(validators={'Id':validators.String(),'id':validators.String(), 'Name':validators.String(), 'ZipCode':validators.String(), 'IsoCountryId':validators.String(), 'Block':validators.String(), 'District':validators.String(), 'State':validators.String()})
def AddressCitytownSave(self, Id = '',id = '', Name = '', State = '', District = '', ZipCode = '', IsoCountryId='', Block = '', **kw):
#		log.debug("Is Service: " + str(IsService))
#		log.debug("IsForSale: " + str(IsForSale))
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvAddressCitytown.get(int_id)
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
				record.ZipCode = ZipCode
				record.IsoCountryId = IsoCountryId
				record.Block = Block
				record.District = District
				record.State = State
				result_msg="Record saved"
				result = 1
		else:
			record = model.InvAddressCitytown(Name = Name, ZipCode = ZipCode, IsoCountryId = IsoCountryId, Block = Block, District = District, State = State, Status='')
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
def AddressCitytownDel(Id, id='', **kw):
	"""	If the AddressCitytown has nothing joined to it, then I'll go 
		through and actually delete the record from the system, 
		otherwise, I'll just mark the record deleted.
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvAddressCitytown.get(int_id)
		except (ValueError, SQLObjectNotFound):
			int_id = -1
	else:
		int_id = -1
		
	try:
		if int_id > 0:
			#Check to see if the record can be completely deleted (ie. no references exist)
			if (len(record.Vendors) + len(record.Customers)) == 0:
				#remove any groups the record might belong to
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
def AddressCitytownUnDel(Id, id='', **kw):
	"""	If the Item is marked deleted, this will un-delete it
	""" 
	if id != '':
		Id = id
	if Id != '':
		try:
			int_id = int(Id)
			record = model.InvAddressCitytown.get(int_id)
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
def AddressCitytownMultiJoinList(self, Id='', ColName='', field_num='', **kw):
	if id != '':
		try:
			int_id = int(Id)
			record = model.InvAddressCitytown.get(int_id)
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
					if ColName == 'Vendors':
						line_text = item.Name + ', ' + item.Description
					elif ColName == 'Costomers':
						line_text = item.Name + ', from: ' + item.City.Name
					records.append(dict(id=item.id, listing=line_text))
			display = 'There are ' + str(len(col_items)-del_item_count) + ' records'
		else:
			records = []
			display = 'There are no items'
		return dict(display=display, field_num=field_num, col_items=records)
	else:	
		return dict(display='There are no items', field_num=field_num, col_items=[])		

@expose(format='json')
def AddressCitytownSearch(self, Name='', City='', ZipCode='', Block='', District='', State='', field_num='', show_del=True, **kw):
	qArgs = ""
	if City!='':
		Name = City
	if Name != '':
		qArgs+="model.InvAddressCitytown.q.Name.contains('"+ Name + "'),"
	if ZipCode != '':
		qArgs+="model.InvAddressCitytown.q.ZipCode.contains('"+ ZipCode + "'),"
	if Block != '':
		qArgs+="model.InvAddressCitytown.q.Block.contains('"+ Block + "'),"
	if District != '':
		qArgs+="model.InvAddressCitytown.q.District.contains('"+ District + "'),"
	if State != '':
		qArgs+="model.InvAddressCitytown.q.State.contains('"+ State + "'),"
	if len(qArgs) > 0:
		items = eval('model.InvAddressCitytown.select(AND ('+qArgs[0:len(qArgs)-1]+'),orderBy=[model.InvAddressCitytown.q.Name])')
	else:
		items = model.InvAddressCitytown.select(orderBy=[model.InvAddressCitytown.q.Name])
	results = []
	del_count = 0
	for item in items:
		if show_del:
			if item.Status == 'deleted':
				text = item.DisplayName()
				results.append({'id':item.id, 'text':text,  'Name':item.Name+' *** MARKED DELETED ***', 'Description':'B: '+item.Block + 'P: '+item.ZipCode + 'D: '+item.District})
			else:
				text = item.DisplayName()
				results.append({'id':item.id, 'text':text,  'Name':item.Name+' *** MARKED DELETED ***', 'Description':'B: '+item.Block + 'P: '+item.ZipCode + 'D: '+item.District})
		elif item.Status == 'deleted':
			del_count += 1
		else:
			results.append({'id':item.id, 'Name':item.Name, 'Description':'B: '+item.Block + 'P: '+item.ZipCode + 'D: '+item.District})
	return dict(results=results, field_num=field_num, items=items)
