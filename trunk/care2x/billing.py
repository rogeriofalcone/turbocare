import turbogears
import cherrypy
import time
from datetime import date, datetime
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from model import BillingItem, hub
from sqlobject.sqlbuilder import *
from sqlobject import *
from math import *
import pprint

class BillingItemFields(widgets.WidgetsDeclaration):
	item_code = widgets.TextField(label="Item Code", validators=validators.NotEmpty, attrs={'size':5})
	item_description = widgets.TextArea(label="Description", cols=40, rows=3)
	item_unit_cost = widgets.TextField(label="Unit Cost", validators=validators.Number())
	item_type = widgets.TextField(label="Item Type", validators=validators.NotEmpty, attrs={'size':10})
	max_discount = widgets.TextField(label="Max Discount",validators=validators.Number())
	item_status = widgets.HiddenField("item_status")
	item_id = widgets.HiddenField("item_id")
	modify_id = widgets.HiddenField("modify_id")
	modify_time = widgets.HiddenField("modify_time")
	create_id = widgets.HiddenField("create_id")
	create_time = widgets.HiddenField("create_time")
	new = widgets.HiddenField("new")
	
class Billing:

	@expose(html="care2x.templates.search")
	def list_item(self, **kw):
		""" The kw (keyword) dictionary can have search parameters
			If there is a "search" key, then the function will
			try to setup a search.  The city: name, district, 
			zipcode, block and isocountryid will all be searchable.
			Each key will also have another key indicating the
			type of search (exact match, wild card, starts with,
			ends with).
			e.g.
			kw['name'] = 'Dimap'
			kw['name_search'] = 'wild card'
		"""
		if (kw.has_key('search')):
			item_select = table.care_billing_item
			if (kw.has_key('description')):
				itemdescription = kw['description']
				if kw['description_search'] == 'wild card':
					item_select = BillingItem.select(BillingItem.q.Description.contains(itemdescription))
				elif kw['description_search'] == 'starts with':
					item_select = BillingItem.select(BillingItem.q.Description.startswith(itemdescription))
				elif kw['description_search'] == 'ends with':
					item_select = BillingItem.select(BillingItem.q.Description.endswith(itemdescription))
				else:
					item_select = BillingItem.select(BillingItem.q.Description==itemdescription)
			item_list = list(item_select)
		else:
			item_list = list(BillingItem.select(orderBy=BillingItem.q.ItemCode))
		
			items = [{ 'id':item.id, 'itemcode':item.ItemCode, 'itemdescription':item.ItemDescription, 'itemunitcost':item.ItemUnitCost, 'itemtype':item.ItemType, 'itemdiscountmaxallowed':item.ItemDiscountMaxAllowed, 'itemstatus':item.ItemStatus} for item in item_list]
		# Do a paging on our results
		cur_page = "/billing/list_item" #Change this to match the page you're on
		if kw.has_key('lines_per_page'):
			lines_per_page = int(kw['lines_per_page'])
		else:
			lines_per_page = 3
		if kw.has_key('page_number'):
			page_number = int(kw['page_number'])
		else:
			page_number = 1
		max_page = len(items)/lines_per_page #Change this to match your item list (and also the line below)
		if fmod(len(items),lines_per_page) > 0:
			max_page += 1
		first_url = turbogears.url(cur_page,page_number=1,lines_per_page=lines_per_page)
		last_url =  turbogears.url(cur_page,page_number=max_page,lines_per_page=lines_per_page)
		if page_number == 1:
			prev_url =  turbogears.url(cur_page,page_number=1,lines_per_page=lines_per_page)
		else:
			prev_url =  turbogears.url(cur_page,page_number=page_number - 1,lines_per_page=lines_per_page)
		if page_number == max_page:
			next_url =  turbogears.url(cur_page,page_number=max_page,lines_per_page=lines_per_page)
		else:
			next_url =  turbogears.url(cur_page,page_number=page_number + 1,lines_per_page=lines_per_page)
		
		start_ind = page_number * lines_per_page - lines_per_page
		end_ind = page_number * lines_per_page
		
		return dict(items=items[start_ind:end_ind],first_url=first_url,next_url=next_url,prev_url=prev_url,last_url=last_url,max_page=max_page,page_number=page_number)

	@expose(html="care2x.templates.form")
	def billing_item(self, id = "", **kw):
		billing_item_fields = BillingItemFields()
		widgets = billing_item_fields.declared_widgets
		data = {}
		if id != "":
			flash("editing item number " + str(id))
			item = BillingItem.get(int(id))
			widgets[6].attrs = dict(value=item.id)
			widgets[0].attrs = dict(value=item.ItemCode)
			widgets[1].default = item.ItemDescription
			widgets[2].attrs = dict(value=item.ItemUnitCost)
			widgets[3].attrs = dict(value=item.ItemType)
			widgets[4].attrs = dict(value=item.ItemDiscountMaxAllowed)
			widgets[5].attrs = dict(value=item.ItemStatus)	
			widgets[7].attrs = dict(value=item.ModifyTime)
			widgets[8].attrs = dict(value=item.ModifyId)
			widgets[9].attrs = dict(value=item.CreateTime)
			widgets[10].attrs = dict(value=item.CreateId)
			widgets[11].attrs = dict(value='False')
		else:
			widgets[6].attrs = dict(value='')
			widgets[0].attrs = dict(value='')
			widgets[1].attrs = dict(text='')
			widgets[2].attrs = dict(value='')
			widgets[3].attrs = dict(value='')
			widgets[4].attrs = dict(value='')
			widgets[5].attrs = dict(value='')
			widgets[7].attrs = dict(value='')
			widgets[8].attrs = dict(value='')
			widgets[9].attrs = dict(value='')
			widgets[10].attrs = dict(value='')
			widgets[11].attrs = dict(value='True')
		form_billing_item = turbogears.widgets.TableForm(fields = billing_item_fields, submit_text = "OK")
		return dict(form=form_billing_item, action='billing_item')

	@expose()
	@validate(validators=dict(new=validators.Bool(),itemunitcost=validators.Number(),itemdiscountmaxallowed=validators.Number()))
	def save_item(self, **kw):

		cur_datetime = date.today()
		if kw['createtime'] == '':
			kw['createtime'] = cur_datetime
		hub.begin()
		if kw['new']:
			item = BillingItem(ItemCode = kw['itemcode'],
				ItemDescription = kw['itemdescription'],
				ItemUnitCost = kw['itemunitcost'],
				ItemType = kw['itemtype'],
				ItemDiscountMaxAllowed = kw['itemdiscountmaxallowed'],
				ItemStatus = kw['itemstatus'],
				ModifyTime = cur_datetime,
				ModifyId = 'wesley',
				CreateTime = cur_datetime,
				CreateId = 'wesley')
		else:
			if kw['createtime'] == "":
				createtime = cur_time
			else:
				time_strct = time.strptime(keywords['createtime'],'%Y-%m-%d %H:%M:%S')
				createtime = datetime(time_strct.tm_year, time_strct.tm_mon, time_strct.tm_mday, time_strct.tm_hour, time_strct.tm_min, time_strct.tm_sec)
			item = BillingItem.get(kw['id'])
			item.ItemDescription = kw['itemdescription']
			item.ItemUnitCost = kw['itemunitcost']
			item.ItemType = kw['itemtype']
			item.ItemDiscountMaxAllowed = kw['itemdiscountmaxallowed']
			item.ItemStatus = kw['itemstatus']
			item.ModifyTime = cur_datetime
			item.ModifyId = 'wesley'
			item.CreateTime = kw['createtime']
			item.CreateId = kw['createid']

		hub.commit() 
		hub.end() 
		turbogears.flash("Changes saved!") 
		raise cherrypy.HTTPRedirect(turbogears.url("/billing/edit_item?id=" + str(item.id))) 
		
	@expose(html="care2x.templates.welcome")	
	def index(self, **keywords):
		flash("This is the billing index")
		return dict(now="Yesterday")
	
	@expose()	
	def validation_error(self, funcname, kw, errors):
		turbogears.flash("What the hell happened! Function name: " + funcname + ", Errors: " + pprint.pformat(errors))
		raise cherrypy.HTTPRedirect(turbogears.url("/billing/index"))
