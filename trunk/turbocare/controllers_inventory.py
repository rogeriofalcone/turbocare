import logging
import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model
import model_inventory
#import report_CatalogItems

log = logging.getLogger("turbocare.controllers")

def get_barcode(id):
	return "/static/images/barcode/" + str(id).zfill(12) + ".png"
	
def drop_inventory():
	objs = []
	for m in dir(model_inventory):
		if m in ('SQLObject','InheritableSQLObject'): continue
		c = getattr(model_inventory,m)
		if isinstance(c, type) and issubclass(c,SQLObject): objs.append(m)
	for table in objs:
		c = getattr(model_inventory,table)
		try:
			c.dropTable()
		except:
			pass
	return 1

def create_inventory():
	objs = []
	for m in dir(model_inventory):
		if m in ('SQLObject','InheritableSQLObject'): continue
		c = getattr(model_inventory,m)
		if isinstance(c, type) and issubclass(c,SQLObject): objs.append(m)
	for table in objs:
		c = getattr(model_inventory,table)
		print table
		c.createTable()
	return 1
	

class Inventory(controllers.RootController):
	from inventory_catalogitem import *
	from inventory_AddressCitytown import *
	from inventory_GrpCompound import *
	from inventory_GrpCustomer import *
	from inventory_GrpLocation import *
	from inventory_GrpPackaging import *
	from inventory_GrpStock import *
	from inventory_GrpVendor import *
	from inventory_Vendor import *
	from inventory_Location import *
	from inventory_Receipt import * # untested
	from inventory_ReceiptItems import * # untested
	from inventory_Customer import *
	from inventory_CatalogCompound import *
	from inventory_Packaging import *
	from inventory_StockLocation import *
	from inventory_Quote import *
	from inventory_QuoteItems import *
	from inventory_QuoteRequest import *
	from inventory_QuoteRequestItems import *
	from inventory_PurchaseOrder import *
	from inventory_POItems import * 
	from inventory_GoodsReceived import * 
	from inventory_StockCompoundQty import * # untested
	from inventory_StockCompound import *
	from inventory_CatalogCompoundQty import * # untested
	from inventory_StockTransfer import *
	from inventory_StockItem import *
	from inventory_StockTransferRequest import *
	from inventory_StockTransferRequestItem import *
	from inventory_CustomerPayment import *
#===== Inventory App Stuff ====================================================

	@expose(format='json')
	def InventoryAppMenu(self, **kw):
		mCatalog = dict(label='Item Master', url='javascript:inv.openObjListing("/inventory/CatalogItem",null)', menu=[dict(label='Browse tree', url='javascript:inv.openObj("/inventory/CatalogItem")')])
		mStock = dict(label='Stock', url='javascript:inv.openObjListing("/inventory/StockItem",null)', menu=[dict(label='Browse tree', url='javascript:inv.openObj("/inventory/StockItem")'), dict(label='Compound', url='javascript:inv.openObjListing("/inventory/StockCompound",null)'), dict(label='Transfers', url='javascript:inv.openObjListing("/inventory/StockTransfer",null)'), dict(label='Transfer Request', url='javascript:inv.openObjListing("/inventory/StockTransferRequest",null)')])
		mVendor = dict(label='Vendor', url='javascript:inv.openObjListing("/inventory/Vendor",null)')
		mCustomer = dict(label='Customer', url='javascript:inv.openObjListing("/inventory/Customer",null)')
		mStores = dict(label='Locations', url='javascript:inv.openObjListing("/inventory/Location",null)')
		mQuotes = dict(label='Quotes', url='javascript:inv.openObjListing("/inventory/Quote",null)')
		mQuoteRequests = dict(label='Quote requests', url='javascript:inv.openObjListing("/inventory/QuoteRequest",null)')
		mPurchaseOrders = dict(label='Purhcase Orders', url='javascript:inv.openObjListing("/inventory/PurchaseOrder",null)')
		#Configuration sub-menu
		smPermissions = dict(label='Permissions', url='')
		smCatalogGroups = dict(label='Catalog Groups', url='javascript:inv.openObjListing("/inventory/GrpStock")')
		smPackaging = dict(label='Packaging', url='javascript:inv.openObjListing("/inventory/Packaging")')
		smCatalogCompounds = dict(label='Catalog Compounds', url='javascript:inv.openObjListing("/inventory/CatalogCompound",null)')
		smCustomerGroups = dict(label='Customer Groups', url='javascript:inv.openObjListing("/inventory/GrpCustomer")')
		smVendorGroups = dict(label='Vendor Groups', url='javascript:inv.openObjListing("/inventory/GrpVendor")')
		smLocationGroups = dict(label='Location Groups', url='javascript:inv.openObjListing("/inventory/GrpLocation")')
		smCompoundGroups = dict(label='Compound Groups', url='javascript:inv.openObjListing("/inventory/GrpCompound")')
		smAddressCitytown = dict(label='Address city/town', url='javascript:inv.openObjListing("/inventory/AddressCitytown")')
		smPackagingGroups = dict(label='Packaging Groups', url='javascript:inv.openObjListing("/inventory/GrpPackaging")')
		config_menu = [smAddressCitytown, smCatalogCompounds, smPackaging, smPermissions, smCatalogGroups, smCustomerGroups, smVendorGroups, smLocationGroups, smCompoundGroups, smPackagingGroups]
		mConfiguration = dict(label='Configuration', url='', menu=config_menu)
		mMain = [mCatalog, mStock, mVendor, mCustomer, mStores, mQuotes, mQuoteRequests, mPurchaseOrders, mConfiguration]
		
		return dict(menu=mMain)

	@expose(html='turbocare.templates.json_form')
	def index(self, **kw):
		start_script = 'inv.AppMenu("/inventory/InventoryAppMenu")'
		javascript = widgets.JSSource(start_script)
		return dict(data=javascript.display(),title="Inventory Management")
	
	@expose(html='turbocare.templates.programmingerror')
	def ProgrammingError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		if next_link == '':
			next_link = "/inventory"
		return dict(error_message = error, next_link=next_link)

	@expose(html='turbocare.templates.dataentryerror')
	def DataEntryError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		if next_link == '':
			next_link = "/inventory"
		return dict(error_message = error, next_link=next_link)
	
	ReportCatalogItems = report_CatalogItems.ReportCatalogItems
