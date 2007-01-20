import logging
import sys
import simplejson
import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears import exception_handler
import model
import datetime, time
from datetime import datetime, timedelta
from model import DATE_FORMAT
from printer_inventory import *
from report import PurchaseOrder, QuoteRequest
import utils

log = logging.getLogger("turbocare.controllers")
conn = model.hub.getConnection()

# What a store needs to do
# Inventory management:
#	1. Modify the catalog (item master)
#	2. Create Quote requests
#	3. Fill in Quotes
#	4. Make Purchase Orders
#	5. Mark Goods Received


class Store(turbogears.controllers.Controller):
	LocationID = '' # The particular dispensing counter where the person is located
	LocationName = ''
	LocationURL = ''
	
	def __init__(self, LocationID, LocationURL):
		'''	Initialize the store to a location id which acts as a filter
		'''
		self.LocationID = LocationID
		self.LocationName = model.InvLocation.get(LocationID).Name
		self.LocationURL = LocationURL

	@expose(html='turbocare.templates.store_menu')
	def index(self, **kw):
		Location = model.InvLocation.get(int(self.LocationID))
		return dict(LocationName=self.LocationName, IsStore=Location.IsStore, CanReceive=Location.CanReceive)
	
	@expose(format='json')
	def PopUpMenu(self, **kw):
		''' Return information about the current location for the pop up menu '''
		Location = model.InvLocation.get(int(self.LocationID))
		results = {}
		results['LocationName'] = self.LocationName
		results['StockMonitor'] = True
		if Location.IsStore:
			if identity.has_permission("stores_catalog_view"):
				results['CatalogItemsEditor'] = True
			if identity.has_permission("stores_po_view"):
				results['PurchaseOrdersEditor'] = True
			if Location.CanReceive:
				if identity.has_permission("stores_gr_view"):
					results['GoodsReceivedEditor'] = True
			if identity.has_permission("stores_quoterequest_view"):
				results['QuoteRequestsEditor'] = True
			if identity.has_permission("stores_quote_view"):
				results['QuotesEditor'] = True
			if identity.has_permission("stores_stock_view"):
				results['StockItemsEditor'] = True
			if identity.has_permission("stores_stocktransferrequest_view"):
				results['StockTransferRequestsEditor'] = True
			if identity.has_permission("stores_vendor_view"):
				results['VendorsEditor'] = True
		if identity.has_permission("stores_stocktransfer_view"):
			results['StockTransfersEditor'] = True
		return results
	
	@expose(html='turbocare.templates.programmingerror')
	def ProgrammingError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		if next_link == '':
			next_link = "/"
		return dict(error_message = error, next_link=next_link)
	
	@expose(html='turbocare.templates.programmingerror')
	def idFail(error):
		error= "Not Permited to do operation"
		log.debug(error)
		next_link = "/"
		return dict(error_message = error, next_link=next_link)


	@expose(html='turbocare.templates.dataentryerror')
	def DataEntryError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		if next_link == '':
			next_link = "/"
		return dict(error_message = error, next_link=next_link)
			
	def UndoStockTransfers(self, StockLocationID):
		'''	Remove all stock transfers from a stock location
			Update all locations where we got stock from and cancel
			the transfers.
			
			Completed transfers will not be removed!!!!!
		'''
		del_list = []
		record = model.InvStockLocation.get(StockLocationID)
		for transfer in record.TransfersToHere:
			if not transfer.IsComplete:
				log.debug('UNDO STOCK TRANSFER: returning stock to original location')
				transfer.FromStockLocation.Quantity += transfer.Qty
				transfer.Status = 'deleted'
				del_list.append(transfer.id)
		for id in del_list:
			log.debug('UNDO STOCK TRANSFER: deleting stock transfer record')
			transfer = model.InvStockTransfer.get(id)
			transfer.destroySelf()

	@expose(html='turbocare.templates.store_catalogitemseditor')
	@validate(validators={'CatalogItemID':validators.Int(),'StockItemID':validators.Int()})
	@identity.require(identity.has_permission("stores_catalog_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")

	def CatalogItemsEditor(self, CatalogItemID=None, StockItemID=None, **kw):
		def Checked(value):
			if value:
				return "checked"
			else:
				return None
		parentitems = []
		childitems = []
		cataloggroups = []
		stockitems = [] # Get a list of stock items for the selected CatalogItem
		# If we have a StockItemID and no CatalogItemID, then get the CatalogItemID from the StockItem
		if CatalogItemID == None and StockItemID != None:
			CatalogItemID = model.InvStockItem.get(StockItemID).CatalogItemID
		if CatalogItemID == None: # Initial screen when no item is selected
			#Get childitems
			catalogitems = model.InvCatalogItem.select(AND (model.InvCatalogItem.q.ParentItemID==None, \
				model.InvCatalogItem.q.Status != 'deleted'),orderBy=[model.InvCatalogItem.q.Name])
			for item in catalogitems:
				childitems.append(dict(id=item.id, name=item.Name))
			# Make a blank entry
			DisplayName = 'CREATE A NEW ENTRY'
			Name = ''
			Description = ''
			Accounting = ''
			IsFixedAsset = None
			IsService = None
			IsForSale = 'checked'
			IsDispensable = 'checked'
			IsSelectable = 'checked'
			MinStockAmt = ''
			ReorderAmt = ''
			Tax = ''
			ParentItemName = ''
			ParentItemID = ''
			CompoundName = ''
			CompoundID = ''
			PackagingName = ''
			PackagingID = ''
		else:
			catalogitem = model.InvCatalogItem.get(CatalogItemID)
			# Do some obvious record fixing
			if catalogitem.ParentItemID == catalogitem.id: # This circular reference can cause major memory problems.
				catalogitem.ParentItemID = None
			# Get childitems
			catalogitems = model.InvCatalogItem.select(AND (model.InvCatalogItem.q.ParentItemID==CatalogItemID, \
				model.InvCatalogItem.q.Status != 'deleted'),orderBy=[model.InvCatalogItem.q.Name])
			for item in catalogitems:
				childitems.append(dict(id=item.id, name=item.Name))
			# Get parent items list
			ParentID = catalogitem.ParentItemID
			parentitems.append(dict(id=None, name="Top"))
			while ParentID != None:
				parentitem = model.InvCatalogItem.get(ParentID)
				parentitems.append(dict(id=parentitem.id, name=parentitem.Name))
				ParentID = parentitem.ParentItemID
			# Get catalog groups
			for group in catalogitem.CatalogGroups:
				cataloggroups.append(dict(id=group.id, name=group.Name))
			# Get the regular variables
			DisplayName = '%s (%d)' % (catalogitem.Name, catalogitem.id)
			Name = catalogitem.Name
			Description = catalogitem.Description
			Accounting = catalogitem.Accounting
			IsFixedAsset = Checked(catalogitem.IsFixedAsset)
			IsService = Checked(catalogitem.IsService)
			IsForSale = Checked(catalogitem.IsForSale)
			IsDispensable = Checked(catalogitem.IsDispensable)
			IsSelectable = Checked(catalogitem.IsSelectable)
			MinStockAmt = catalogitem.MinStockAmt
			ReorderAmt = catalogitem.ReorderAmt
			Tax = catalogitem.Tax
			if catalogitem.ParentItemID != None:
				ParentItemName = catalogitem.ParentItem.Name
			else:
				ParentItemName = ''
			ParentItemID = catalogitem.ParentItemID
			if catalogitem.CompoundID != None:
				CompoundName = catalogitem.Compound.Name
			else:
				CompoundName = ''
			CompoundID = catalogitem.CompoundID
			if catalogitem.PackagingID != None:
				PackagingName = catalogitem.Packaging.Name
			else:
				PackagingName = ''
			PackagingID = catalogitem.PackagingID
			# Get the stock items for the catalog item
			items = model.InvStockItem.select(model.InvStockItem.q.CatalogItemID==CatalogItemID,\
				orderBy=[model.InvStockItem.q.Sort])
			for item in items:
				try:
					stockitems.append(dict(ItemID=item.id, ItemName=item.Name, ItemQtyPurchased=item.Quantity,\
					ItemQtyAvailable=item.QtyAvailable(), ItemQtySold=item.QtySold(), ItemExpireDate=\
					item.ExpireDate.strftime(DATE_FORMAT), ItemStatus=item.Status))
				except AttributeError:
					stockitems.append(dict(ItemID=item.id, ItemName=item.Name, ItemQtyPurchased=item.Quantity,\
					ItemQtyAvailable=item.QtyAvailable(), ItemQtySold=item.QtySold(), ItemExpireDate=None,\
					ItemStatus=item.Status))
			total_QtyPurchased, total_QtyAvailable, total_QtySold = 0,0,0
			for item in stockitems:
				total_QtyPurchased += item['ItemQtyPurchased']
				total_QtyAvailable += item['ItemQtyAvailable']
				total_QtySold += item['ItemQtySold']
			stockitems.append(dict(ItemID=None, ItemName='Total', ItemQtyPurchased=total_QtyPurchased,\
				ItemQtyAvailable=total_QtyAvailable, ItemQtySold=total_QtySold, ItemExpireDate='',\
				ItemStatus=''))
		return dict(childitems=childitems, parentitems=parentitems, cataloggroups=cataloggroups,DisplayName=\
			DisplayName, Name=Name, Description=Description,Accounting=Accounting,IsFixedAsset=IsFixedAsset,\
			IsService=IsService,IsForSale=IsForSale,IsDispensable=IsDispensable,IsSelectable=IsSelectable,\
			MinStockAmt=MinStockAmt,ReorderAmt=ReorderAmt,Tax=Tax,ParentItemName=ParentItemName,\
			ParentItemID=ParentItemID,CompoundName=CompoundName,CompoundID=CompoundID,\
			PackagingName=PackagingName,PackagingID=PackagingID,CatalogItemID=CatalogItemID,\
			stockitems=stockitems)

	@expose()
	@validate(validators={'Name':validators.String(),'Description':validators.String(),'Accounting':validators.String(),\
		'ParentItemID':validators.Int(),'CompoundID':validators.Int(),'PackagingID':validators.Int(),\
		'CatalogItemID':validators.Int(),'IsFixedAsset':validators.Bool(),'IsService':validators.Bool(),\
		'IsForSale':validators.Bool(),'IsDispensable':validators.Bool(),'IsSelectable':validators.Bool(),\
		'MinStockAmt':validators.Number(),'ReorderAmt':validators.Number(),'Tax':validators.Number()})
	@identity.require(identity.has_permission("stores_catalog_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")

	def CatalogItemsEditorSave(self, Name='New Name', Description='',Accounting='',IsFixedAsset=None,\
			IsService=None,IsForSale=None,IsDispensable=None,IsSelectable=None,MinStockAmt=None,\
			ReorderAmt=None,Tax=None,ParentItemID=None,CompoundID=None,PackagingID=None,\
			CatalogItemID=None, CatalogGroups=[], CatalogGroupCount=[], Operation='', **kw):
		'''	Create/Update a CatalogItem entry
			NOTE: in the future, check for any attempts to make a circular reference with the ParentItemID
		'''
		log.debug('CatalogItemsEditorSave')
		log.debug('....Operation: %s' % Operation)
		if Operation == 'Save' and CatalogItemID!=None:
			# Update the CatalogItem
			catalogitem = model.InvCatalogItem.get(CatalogItemID)
			catalogitem.Name = Name
			catalogitem.Description = Description
			catalogitem.Accounting = Accounting
			if ParentItemID != CatalogItemID: # Only update the catalog item id if we're not setting it to itself
				catalogitem.ParentItemID = ParentItemID
			catalogitem.CompoundID = CompoundID
			catalogitem.PackagingID = PackagingID
			catalogitem.IsFixedAsset = IsFixedAsset
			catalogitem.IsService = IsService
			catalogitem.IsForSale = IsForSale
			catalogitem.IsDispensable = IsDispensable
			catalogitem.IsSelectable = IsSelectable
			catalogitem.MinStockAmt = MinStockAmt
			catalogitem.ReorderAmt = ReorderAmt
			catalogitem.Tax = Tax
			# Remove any Catalog groups which we're not using
			# convert our CatalogGroups list to an integer list
			if isinstance(CatalogGroups, basestring): # Then it is a single line entry
				CatalogGroups = [int(CatalogGroups)]
			else: # It's an array entry
				CatalogGroups = [int(x) for x in CatalogGroups]
			for group in catalogitem.CatalogGroups:
				if not (group.id in CatalogGroups):
					catalogitem.removeInvGrpStock(group)
			# Add any catalog groups which we don't already have
			current_groups = [x.id for x in catalogitem.CatalogGroups]
			for groupid in CatalogGroups:
				if not (groupid in current_groups):
					catalogitem.addInvGrpStock(groupid)
			turbogears.flash('Record updated')
		elif Operation == 'Cancel':
			# Don't make any changes, just load the page again with the CatalogItemID
			pass
		elif (Operation in ['New', 'New sub item']) or (Operation == 'Save' and CatalogItemID==None):
			# Make a new unique entry but with a copy of the current supplied values
			if Name in ['', None]:
				Name = "New Catalog Item"
			catalogitem = model.InvCatalogItem(Name=Name,Description=Description,Accounting=\
				Accounting,IsFixedAsset=IsFixedAsset,IsService=IsService,IsForSale=IsForSale,IsDispensable=\
				IsDispensable,IsSelectable=IsSelectable,MinStockAmt=MinStockAmt,ReorderAmt=ReorderAmt,\
				Tax=Tax,ParentItemID=ParentItemID,CompoundID=CompoundID,PackagingID=PackagingID)
			# Add the catalog groups
			# convert our CatalogGroups list to an integer list
			if isinstance(CatalogGroups, basestring): # Then it is a single line entry
				CatalogGroups = [int(CatalogGroups)]
			else: # It's an array entry
				CatalogGroups = [int(x) for x in CatalogGroups]
			for groupid in CatalogGroups:
				catalogitem.addInvGrpStock(groupid)
			# Reset the ParentItemID if we want a sub-item
			if Operation == 'New sub item':
				catalogitem.ParentItemID = CatalogItemID
			# Set the CatalogItemID to the new item
			CatalogItemID = catalogitem.id
			turbogears.flash('New record added')
		elif Operation == 'Delete' and CatalogItemID != None:
			# Attempt to delete the current entry, and at the very least, mark the entry deleted
			catalogitem = model.InvCatalogItem.get(CatalogItemID)
			CatalogItemID = catalogitem.ParentItemID
			if (len(catalogitem.ChildItems) + len(catalogitem.StockItems) + len(catalogitem.Requests) + len(catalogitem.Quotes) + \
				len(catalogitem.QuoteRequestItems) + len(catalogitem.POItems) + len(catalogitem.CatalogCompoundQtys) + \
				len(catalogitem.StockTransferRequestItems) + len(catalogitem.ReceiptItems)) == 0:
				#remove any groups the record might belong to
				for group in catalogitem.CatalogGroups:
					catalogitem.removeInvGrpStock(group)
				catalogitem.destroySelf()
				turbogears.flash('Record deleted!')
			else:
				catalogitem.Status = 'deleted'
				turbogears.flash('Record marked deleted!')
		if CatalogItemID in ['', None]:
			raise cherrypy.HTTPRedirect('CatalogItemsEditor')
		else:
			raise cherrypy.HTTPRedirect('CatalogItemsEditor?CatalogItemID=%d' % CatalogItemID)

	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_catalog_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CatalogItemsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Find CatalogItems who's name partially matches the QuickSearchText
		'''
		catalogitems = model.InvCatalogItem.select(model.InvCatalogItem.q.Name.contains(str(QuickSearchText)),
			orderBy=[model.InvCatalogItem.q.Name])
		results = []
		for item in catalogitems:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)
		
	@expose(format='json')
	@validate(validators={'CatalogItemID':validators.Int()})
	@identity.require(identity.has_permission("stores_catalog_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CatalogItemsEditorGroupSelect(self, CatalogItemID=None, **kw):
		'''	Load the CatalogItem Group Options
			Mark items which are already selected as selected
		'''
		cur_groups = []
		if CatalogItemID!=None:
			catalogitem = model.InvCatalogItem.get(CatalogItemID)
			for group in catalogitem.CatalogGroups:
				cur_groups.append(group.id)
		groups = model.InvGrpStock.select(orderBy=[model.InvGrpStock.q.Name])
		results = []
		for group in groups:
			results.append(dict(id=group.id, text=group.Name, selected=(group.id in cur_groups)))
		return dict(results=results)
	
	@expose(format='json')
	@identity.require(identity.has_permission("stores_catalog_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CatalogItemsEditorParentItemSelect(self, SearchText='', **kw):
		'''	Load the CatalogItem Options
		'''
		SearchText = str(SearchText)
		items = model.InvCatalogItem.select(model.InvCatalogItem.q.Name.contains(SearchText),
			orderBy=[model.InvCatalogItem.q.Name])
		results = []
		for item in items:
			results.append(dict(id=item.id, text='%s (%d)' % (item.Name,item.id)))
		return dict(results=results, function_name='CatalogItemsEditorParentItemSelect')

	@expose(format='json')
	@identity.require(identity.has_permission("stores_catalog_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CatalogItemsEditorCompoundSelect(self, SearchText='', **kw):
		'''	Load the Compound options
		'''
		SearchText = str(SearchText)
		items = model.InvCatalogCompound.select(model.InvCatalogCompound.q.Name.contains(SearchText),
			orderBy=[model.InvCatalogCompound.q.Name])
		results = []
		for item in items:
			results.append(dict(id=item.id, text='%s (%d)' % (item.Name,item.id)))
		return dict(results=results, function_name='CatalogItemsEditorCompoundSelect')

	@expose(format='json')
	@identity.require(identity.has_permission("stores_catalog_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def CatalogItemsEditorPackagingSelect(self, SearchText='', **kw):
		'''	Load the Packaging Options
		'''
		SearchText = str(SearchText)
		items = model.InvPackaging.select(model.InvPackaging.q.Name.contains(SearchText),
			orderBy=[model.InvPackaging.q.Name])
		results = []
		for item in items:
			results.append(dict(id=item.id, text='%s (%d)' % (item.Name,item.id)))
		return dict(results=results, function_name='CatalogItemsEditorPackagingSelect')

	@expose(html='turbocare.templates.store_purchaseorderseditor')
	@validate(validators={'PurchaseOrderID':validators.Int()})
	@identity.require(identity.has_permission("stores_po_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrdersEditor(self, PurchaseOrderID=None, **kw):
		'''	Displays a list of current purchase orders
			Search for previous purchase orders and create a new one based on a past one (Quantity & Catalog items and vendors)
			Creating/Editing of Purchase orders
			Creating a new set of purchase orders (from a list of catalog items)
			Editing the items in the purchase order
			Printing purchase orders
		'''
		log.debug('PurchaseOrdersEditor')
		def Checked(value):
			''' Convenience function '''
			if value:
				return "checked"
			else:
				return None
		# Generate a quick list of Purchase orders to pick
		newPOs = [] # POs which are not yet sent
		sentPOs = [] # POs which are just sent
		unfinishedPOs = [] # POs which are receiving, but not yet completed
		oldPOs = [] # POs which are completed, but recent (the last 8 completed)
		items = model.InvPurchaseOrder.select(orderBy=[-model.InvPurchaseOrder.q.CreateTime])
		for item in items:
			try:
				#log.debug('....PO id: %d' % item.id)
				if item.Vendor == None or len(item.Items)==0 or item.POSentOnDate == None or item.POSentOnDate == '':
					newPOs.append(dict(id=item.id,name=item.Name()))
				elif item.POSentOnDate != None and item.PercentComplete() <= 0.0:
					# log.debug('....Sent PO added')
					sentPOs.append(dict(id=item.id,name=item.Name()))
				elif item.POSentOnDate != None and (0 < item.PercentComplete() < 1):
					unfinishedPOs.append(dict(id=item.id,name=item.Name()))
				elif item.PercentComplete() == 1 and len(oldPOs) < 8:
					oldPOs.append(dict(id=item.id,name=item.Name()))
			except SQLObjectNotFound, errorstr:
				errorArr = errorstr[0].split(' ')
				table = errorArr[2]
				id = errorArr[6]
				if table == 'InvVendor':
					turbogears.flash("Error: It seems that the Vendor (id=%s) doesn't exist on Purchase Order id=%d.  You'll need to figure out which Vendor should be attached to this Purchase Order" % (id,item.id))
					item.VendorID = None
		# Configure display for Purchase order
		if PurchaseOrderID == None: # Initial screen when no item is selected
			# Make a blank entry
			Name = 'CREATE A NEW ENTRY'
			VendorName = ''
			VendorID = ''
			items = [] #MultipleJoin("InvPOItems",joinColumn="purchase_order_id")
			goodsreceived = [] #MultipleJoin("InvGoodsReceived",joinColumn="purchase_order_id")
			POSentOnDate = ''
			ExpectedDeliveryDate = ''
			Notes = ''
		else:
			try:
				purchaseorder = model.InvPurchaseOrder.get(PurchaseOrderID)
			except SQLObjectNotFound, errorstr:
				errorArr = errorstr[0].split(' ')
				table = errorArr[2]
				id = errorArr[6]
				if table == 'InvVendor':
					turbogears.flash("Error: It seems that the Vendor (id=%s) doesn't exist.  You'll need to figure out which Vendor should be attached to this Purchase Order" % id)
					purchaseorder.VendorID = None
			# Get the regular variables
			Name = purchaseorder.Name()
			VendorID = purchaseorder.VendorID
			if VendorID != None:
				VendorName = purchaseorder.Vendor.Name
			else:
				VendorName = 'Not Assigned'
			items = [] #MultipleJoin("InvPOItems",joinColumn="purchase_order_id")
			for item in purchaseorder.Items:
				if item.Status != 'deleted':
					items.append(dict(POItemID=item.id,POItemName=item.Name(),POItemQuantityRequested=\
						item.QuantityRequested, POItemQuantityReceived=item.QuantityReceived, \
						POItemQuotePrice=item.QuotePrice, POItemActualPrice=item.ActualPrice,\
						POItemNotes=item.Notes, POItemCounter=1,POItemCatalogItemID=item.CatalogItemID)) #N.B. POItemCounter is used to count how many items are submitted
			goodsreceived = [] #MultipleJoin("InvGoodsReceived",joinColumn="purchase_order_id")
			for gr in purchaseorder.GoodsReceived:
				goodsreceived.append(dict(id=gr.id, name=gr.Name()))
			POSentOnDate = purchaseorder.POSentOnDate
			ExpectedDeliveryDate = purchaseorder.ExpectedDeliveryDate
			Notes = purchaseorder.Notes
		# Produce a list of CatalogItems which we might want to make an order for (the top 20)
		catalogitemsList = model.InvCatalogItem.select(model.InvCatalogItem.q.IsSelectable==True,\
			orderBy=[model.InvCatalogItem.q.Sort])
		catalogitems = []
		for item in catalogitemsList:
			POInfo = item.LatestPO()
			name = item.Name
			stock = "In Stock: %d" % item.QtyAvailable()
			reorder = "Reorder in %d days" % item.DaysUntilReorder()
			if POInfo['POSentOnDate'] != None:
				if POInfo['QuantityRequested'] in [None,0]:
					lastpo = "Last PO on %s (No Items?)" % (POInfo['POSentOnDate'].strftime(DATE_FORMAT))
				else:
					lastpo = "Last PO on %s (%r%%)" % (POInfo['POSentOnDate'].strftime(DATE_FORMAT),	\
						POInfo['QuantityReceived']/POInfo['QuantityRequested']*100)
			else:
				lastpo = ''
			catalogitems.append(dict(id=item.id, name=name, stock=stock, reorder=reorder, lastpo=lastpo))
			if len(catalogitems) > 20:
				break
		# Get a list of CatalogGroups (InvGrpStock)
		cataloggroupsList = model.InvGrpStock.select(model.InvGrpStock.q.Status != 'deleted',
			orderBy=[model.InvGrpStock.q.Name])
		cataloggroups = []
		for group in cataloggroupsList:
			cataloggroups.append(dict(id=group.id,name=group.Name))
		return dict(newPOs=newPOs, sentPOs=sentPOs, unfinishedPOs=unfinishedPOs, oldPOs=oldPOs, Name=Name,\
			VendorName=VendorName, VendorID=VendorID, items=items, goodsreceived=goodsreceived, \
			POSentOnDate=POSentOnDate, ExpectedDeliveryDate=ExpectedDeliveryDate, Notes=Notes,\
			catalogitems=catalogitems, cataloggroups=cataloggroups, PurchaseOrderID=PurchaseOrderID)
			
	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_po_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrdersEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Find PurchaseOrders that have CatalogItems who's name partially matches the QuickSearchText
		'''
		purchaseorders = model.InvPurchaseOrder.select(AND (model.InvCatalogItem.q.Name.contains(str(QuickSearchText)),\
			model.InvCatalogItem.q.id==model.InvPOItems.q.CatalogItemID, model.InvPOItems.q.PurchaseOrderID==\
			model.InvPurchaseOrder.q.id,model.InvPurchaseOrder.q.Status!='deleted'),orderBy=[model.InvPurchaseOrder.q.Sort])
		results = []
		for item in purchaseorders:
			results.append(dict(id=item.id, text=item.Name()))
		return dict(results=results)

	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_po_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrdersEditorCatalogItemSelect(self, CatalogItemName='', CatalogItemGroups=[], **kw):
		'''	Find CatalogItems who's name partially matches the QuickSearchText
		'''
		log.debug('PurchaseOrdersEditorCatalogItemSelect')
		qArgs = ""
		if CatalogItemName != '':
			qArgs+="model.InvCatalogItem.q.Name.contains('"+ CatalogItemName + "'),"
		qArgs+="model.InvCatalogItem.q.IsSelectable == True,"
		qArgs+="model.InvCatalogItem.q.Status != 'deleted',"
		if len(CatalogItemGroups)>0:
			CatalogItemGroups = set(CatalogItemGroups.split(","))
			# log.debug(CatalogItemGroups)
			orArgs = ''
			for group in CatalogItemGroups:
				orArgs+="model.InvGrpStock.q.id == '"+group+"',"
			qArgs+= "OR ("+orArgs[0:len(orArgs)-1]+"),"
			qArgs+="model.InvGrpStock.q.id == model.InvViewJoinCatalogItemGrpStock.q.GrpStockId,"
			qArgs+="model.InvCatalogItem.q.id == model.InvViewJoinCatalogItemGrpStock.q.CatalogItemId,"
			#qArgs+="model.InvCatalogItem.q.id == table.inv_catalog_item_inv_grp_stock.inv_catalog_item_id,"
			#clauseTables.append("inv_catalog_item_inv_grp_stock")
		log.debug('....qArgs %s' % qArgs)
		if len(qArgs) > 0:
			#log.debug("!!!!!!!!!!!!!!!! " + qArgs)
			catalogitems = eval('model.InvCatalogItem.select(AND ('+qArgs[0:len(qArgs)-1]+'),\
				orderBy=[model.InvCatalogItem.q.Sort])')
		else:
			catalogitems = model.InvCatalogItem.select(orderBy=[model.InvCatalogItem.q.Sort])
		results = []
		for item in catalogitems:
			POInfo = item.LatestPO()
			name = item.Name
			stock = "In Stock: %d" % item.QtyAvailable()
			reorder = "Reorder in %d days" % item.DaysUntilReorder()
			if POInfo['POSentOnDate'] != None:
				if POInfo['QuantityRequested'] != 0:
					lastpo = "Last PO on %s (%r%%)" % (POInfo['POSentOnDate'].strftime(DATE_FORMAT),	\
						POInfo['QuantityReceived']/POInfo['QuantityRequested']*100)
				else:
					lastpo = "Last PO on %s (0 Qty requested)" % POInfo['POSentOnDate'].strftime(DATE_FORMAT)
			else:
				lastpo = ''
			results.append(dict(id=item.id, name=name, stock=stock, reorder=reorder, lastpo=lastpo))
			if len(results) > 199:
				break
		log.debug('....Result length: %d' % len(results))
		return dict(results=results)
	
	@expose(html='turbocare.templates.purchaseorder')
	@identity.require(identity.has_permission("stores_po_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrderCreate(self, CatalogItemID=[], Counter=[], **kw):
		'''	Take a list of CatalogItems and prepare them for creating a PurchaseOrder
		'''
		if len(Counter) == 0:
			turbogears.flash('No Items Selected')
			raise cherrypy.HTTPRedirect('PurchaseOrdersEditor')
		else:
			if isinstance(CatalogItemID, basestring):
				CatalogItemID = [int(CatalogItemID)]
			else:
				CatalogItemID = [int(x) for x in CatalogItemID]
			CatalogItems = []
			for ID in CatalogItemID:
				item = model.InvCatalogItem.get(ID)
				CatalogItems.append(dict(id=item.id, Name=item.Name, Description=item.Description, Quantity=item.ReorderAmt, Notes=""))			
		return dict(PreviousLink="PurchaseOrdersEditor", Label='Purchase order create', CatalogItems=CatalogItems)
	
	@expose()
	@identity.require(identity.has_permission("stores_po_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrderCreateNewSave(self, CatalogItem=[], Vendor=[], QuantityRequested=[], QuotePrice=[], Notes=[],Counter=[], **kw):
		'''	Save the selected items into new purchase orders.
			If we create more than one, then we'll select the first
			and display that in the PurchaseOrdersEditor
		'''
		log.debug('PurchaseOrderCreateNewSave')
		POs = {}
		# Convert our lists to the correct data type
		if isinstance(Vendor, basestring):
			Vendor = [int(Vendor)]
		else:
			Vendor = [int(x) for x in Vendor]
		if isinstance(CatalogItem, basestring):
			CatalogItem = [int(CatalogItem)]
		else:
			CatalogItem = [int(x) for x in CatalogItem]
		if isinstance(QuantityRequested,basestring):
			QuantityRequested= [float(QuantityRequested)]
		else:
			QuantityRequested= [float(x) for x in QuantityRequested]
		if isinstance(QuotePrice,basestring):
			QuotePrice= [float(QuotePrice)]
		else:
			QuotePrice= [float(x) for x in QuotePrice]
		if isinstance(Notes,basestring):
			Notes= [str(Notes)]
		else:
			Notes= [str(x) for x in Notes]
		if len(Counter) == 0:
			turbogears.flash("Some values were not entered correctly (and so the PO(s) might be incomplete)")
			cherrypy.HTTPRedirect('PurchaseOrdersEditor')	
		if len(Counter) == 1: # For POs with only one item
			PurchaseOrder = model.InvPurchaseOrder(VendorID = Vendor[0])
			POItem = model.InvPOItems(PurchaseOrderID=PurchaseOrder.id, CatalogItemID=CatalogItem[0],\
				 QuantityRequested = QuantityRequested[0], QuotePrice = QuotePrice[0], Notes = Notes[0], Status='')
			POID = str(PurchaseOrder.id)
		else: #for POs with more than one item
			for cat_id, ven_id, qtyreq, qtprce, note in zip(CatalogItem, Vendor, QuantityRequested, QuotePrice, Notes):
				if POs.has_key(ven_id):
					PurchaseOrderId = POs[ven_id]
				else:
					PurchaseOrder = model.InvPurchaseOrder(VendorID = int(ven_id), Status="")
					PurchaseOrderId = PurchaseOrder.id
					POs[ven_id] = PurchaseOrderId
				try:
					QR = qtyreq
					QP = qtprce
				except ValueError:
					turbogears.flash("Some values were not entered correctly (and so the PO(s) might be incomplete)")
					raise cherrypy.HTTPRedirect('PurchaseOrdersEditor')
				POItem = model.InvPOItems(PurchaseOrderID = int(PurchaseOrderId), CatalogItemID = int(cat_id), QuantityRequested = \
					QR, QuotePrice = QP, Notes = note, Status='')
			POID = POs.values()[0]
		raise cherrypy.HTTPRedirect('PurchaseOrdersEditor?PurchaseOrderID=%s' % POID)
		
	@expose(format='json')
	@validate(validators={'CatalogItemId':validators.Int()})
	@identity.require(identity.has_permission("stores_po_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrderGetVendorsForItem(self, CatalogItemId=None, **kw):
		items = []
		if CatalogItemId != None:
			vendors = model.InvVendor.select(AND (model.InvQuote.q.VendorID == model.InvVendor.q.id, model.InvQuoteItems.q.QuoteID == model.InvQuote.q.id, model.InvQuoteItems.q.CatalogItemID == model.InvCatalogItem.q.id, model.InvCatalogItem.q.id == int(CatalogItemId)),distinct=True,orderBy=[model.InvVendor.q.Name])
			for vendor in vendors:
				quote_items = model.InvQuoteItems.select(AND (model.InvQuoteItems.q.CatalogItemID == int(CatalogItemId), model.InvQuoteItems.q.QuoteID == model.InvQuote.q.id, model.InvQuote.q.VendorID == vendor.id),orderBy=-model.InvQuote.q.ValidOn)
				quote_item = quote_items[0]
				items.append(dict(id=vendor.id, Name=vendor.Name, Description=vendor.Description, Price=quote_item.Price, Ranking=quote_item.Ranking, Product=quote_item.Product, Notes=quote_item.Notes, ValidOn=quote_item.Quote.ValidOn.strftime('%Y-%m-%d')))
		return dict(items=items)

	@expose(html='turbocare.templates.store_purchaseorderseditor')
	@validate(validators={'PurchaseOrderID':validators.Int(),'Notes':validators.String(),'Operation':validators.String(),\
	'POSentOnDate':validators.String(),'ExpectedDeliveryDate':validators.String()})
	@identity.require(identity.has_permission("stores_po_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrderSave(self, POSentOnDate='',ExpectedDeliveryDate='',Notes='',PurchaseOrderID=None,POItemID=[],\
		POItemQuantityRequested=[],POItemQuantityReceived=[], POItemQuotePrice=[],POItemActualPrice=[],\
		POItemNotes=[],POItemCounter=[], Operation='', **kw):
		'''	Delete or update (modify) an existing Purchase Order
		'''
		log.debug('PurchaseOrderSave')
		# Load our PurchaseOrder
		PO = model.InvPurchaseOrder.get(PurchaseOrderID)
		# Get our operation
		log.debug('....Operation: %s' % Operation)
		if Operation == 'Save':
			# Silly but necessary date manipulations (I really wish the validators for dates worked!!!)
			if POSentOnDate != None and POSentOnDate != '':
				POSentOnDate = datetime.fromtimestamp(time.mktime(time.strptime(POSentOnDate[0:10],DATE_FORMAT)))
			else:
				POSentOnDate = None
			if ExpectedDeliveryDate != None and ExpectedDeliveryDate != '':
				ExpectedDeliveryDate = datetime.fromtimestamp(time.mktime(time.strptime(ExpectedDeliveryDate[0:10],DATE_FORMAT)))
			else:
				ExpectedDeliveryDate = None
			PO.POSentOnDate = POSentOnDate
			PO.ExpectedDeliveryDate = ExpectedDeliveryDate
			PO.Notes = Notes
			# Update the Purchase Order Items
			CurrPOItems = [x.id for x in PO.Items]
			if len(POItemCounter) > 1:
				NewPOItemIDs = [int(x) for x in POItemID]
			elif len(POItemCounter) == 1:
				NewPOItemIDs = [int(POItemID)]
			else:
				NewPOItemIDs = []
			for NewID, QuantityRequested, QuantityReceived, QuotePrice,ActualPrice,POItemNote in \
				zip(NewPOItemIDs,POItemQuantityRequested,POItemQuantityReceived,POItemQuotePrice,\
				POItemActualPrice,POItemNotes):
				if NewID in CurrPOItems: #Update the item
					poitem = model.InvPOItems.get(NewID)
					poitem.QuantityRequested = float(QuantityRequested)
					poitem.QuantityReceived = float(QuantityReceived)
					poitem.QuotePrice = float(QuotePrice)
					poitem.ActualPrice = float(ActualPrice)
					poitem.Notes = str(POItemNote)
				else: #We shouldn't have this, becuase we create new POItems in a different place (using AJAX/AJSON)
					pass
			# Delete any PurchaseOrder Items which have been removed
			log.debug(CurrPOItems)
			log.debug(NewPOItemIDs)
			for POItem in CurrPOItems:
				if not (POItem in NewPOItemIDs):
					poitem = model.InvPOItems.get(POItem)
					if len(poitem.PurchaseOrder.GoodsReceived) > 0 or (poitem.PurchaseOrder.POSentOnDate !=None and poitem.PurchaseOrder.POSentOnDate <= model.cur_date_time()):
						poitem.Status = 'deleted'
					else:
						poitem.destroySelf()
			turbogears.flash('Record updated')
		elif Operation == 'Delete':
			if (PO.POSentOnDate != None and PO.POSentOnDate <= model.cur_date_time()) or len(PO.GoodsReceived) > 0 \
				or len(PO.TransferRequests) > 0:
				PO.Status = 'deleted'
				# Go through the purchase order items and mark them deleted too
				for item in PO.Items:
					item.Status = 'deleted'
				turbogears.flash('Recorded marked deleted')
			else:
				#Delete all items linked to the purchase order
				for item in PO.Items:
					item.destroySelf()
				# Now delete the purchase order
				PO.destroySelf()
				turbogears.flash('Record deleted')
			PurchaseOrderID=None
		elif Operation == 'Make Goods Received':
			# Create a goods received record and then redirect to the Goods received editing screen
			GR = model.InvGoodsReceived(PurchaseOrderID=PurchaseOrderID,DateReceived=model.cur_date_time())
			raise cherrypy.HTTPRedirect('GoodsReceivedEditor?GoodsReceivedID=%d' % GR.id)
		elif Operation == 'Print' and PurchaseOrderID!=None:
			# Redirect the PO to the printing page
			raise cherrypy.HTTPRedirect('PurchaseOrdersEditorPrint?PurchaseOrderID=%d' % PurchaseOrderID)
		# Load the PurchaseOrder
		if PurchaseOrderID != None:
			raise cherrypy.HTTPRedirect('PurchaseOrdersEditor?PurchaseOrderID=%d' % PurchaseOrderID)
		else:
			raise cherrypy.HTTPRedirect('PurchaseOrdersEditor')
			
	@expose(html='turbocare.templates.store_purchaseorderprint')
	@validate(validators={'PurchaseOrderID':validators.Int()})
	@identity.require(identity.has_permission("stores_po_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrdersEditorPrint(self, PurchaseOrderID, Operation=None, PreparedBy='', CheckedBy='',
	ApprovedBy='', ToAddress='', FromAddress='', DeliveryInstructions='', PackingAndForwarding='', **kw):
		'''	Makes a printable web page for the PO.  It can be copy and pasted into
			a word processor document for further modifications.
		'''
		if Operation=='Print':
			PO = model.InvPurchaseOrder.get(PurchaseOrderID)
			report = PurchaseOrder.PurchaseOrderPrintOut(PO=PO, PackingAndForwarding=PackingAndForwarding,
				PreparedBy=PreparedBy,CheckedBy=CheckedBy, ApprovedBy=ApprovedBy,
				ToAddress=ToAddress,FromAddress=FromAddress,DeliveryInstructions=DeliveryInstructions)
			filename = report.P()
			raise cherrypy.HTTPRedirect('/static/reports/%s' % filename)
		else:
			PO = model.InvPurchaseOrder.get(PurchaseOrderID)
			PackingAndForwarding = PO.Notes
			PreparedBy = model.cur_user_name()
			CheckedBy = "Unknown Person"
			ApprovedBy = "Unknown Person"
			ToAddress = PO.Vendor.Name + '\nAttn: ' + PO.Vendor.ContactName + '\n' + PO.Vendor.AddressLabel
			FromAddress = "CIHSR\n4th Mile Road, Dimapur, NL\n11122333\nPH: 111222333444"
			DeliveryInstructions = PO.Vendor.DeliveryInstructions
		return dict(PurchaseOrderID=PurchaseOrderID,PackingAndForwarding=PackingAndForwarding,
		PreparedBy=PreparedBy,CheckedBy=CheckedBy,ApprovedBy=ApprovedBy,ToAddress=ToAddress,
		FromAddress=FromAddress,DeliveryInstructions=DeliveryInstructions)
		
	@expose(format='json')
	@identity.require(identity.has_permission("stores_po_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrdersEditorAddItemsStep1(self, PurchaseOrderID, **kw):
		'''	This generates the form fields that we use in the JavaScript file PickList.js "pick" object
			The form is used to add CatalogItems to a purchase order.
		'''
		id='CIPick' #Used in the javascript code to identify the PickList
		# Search fields
		Name = dict(id="qri_Name", name="Name", label="Name", type="String", attr=dict(length=25), data='')
		# Select box data
		InvGrpStockNames = [x.Name for x in model.InvGrpStock.select(orderBy=[model.InvGrpStock.q.Name])]
		SrchCatalogGroups = dict(id="po_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect", attr=dict(Groups=InvGrpStockNames), data='')
		return dict(id=id, Name='AddItems', Label='Select items from the item master',\
			FieldsSrch=[Name, SrchCatalogGroups], Inputs=[], SrchUrl='PurchaseOrdersEditorAddItemsStep2', \
			DataUrl='', Url='PurchaseOrdersEditorAddItemsStep3', UrlVars='PurchaseOrderID='+PurchaseOrderID, result_msg='ok', \
			SrchNow=False, NoAjax=False, JsonFunction='store.RenderAddItems')

	@expose(format='json')
	@identity.require(identity.has_permission("stores_po_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def PurchaseOrdersEditorAddItemsStep2(self, Name='', Groups='', **kw):
		'''	Search for CatalogItems and return the results to the PickList
		'''
		qArgs = ""
		if Name != '':
			qArgs+="model.InvCatalogItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvCatalogItem.q.IsSelectable == True,"
		qArgs+="model.InvCatalogItem.q.Status != 'deleted',"
		if Groups != '':
			Groups = set(Groups.split(","))
			orArgs = ''
			for group in Groups:
				orArgs+="model.InvGrpStock.q.Name == '"+group+"',"
			qArgs+= "OR ("+orArgs[0:len(orArgs)-1]+"),"
			qArgs+="model.InvGrpStock.q.id == model.InvViewJoinCatalogItemGrpStock.q.GrpStockId,"
			qArgs+="model.InvCatalogItem.q.id == model.InvViewJoinCatalogItemGrpStock.q.CatalogItemId,"
		if len(qArgs) > 0:
			#log.debug("!!!!!!!!!!!!!!!! " + qArgs)
			items = eval('model.InvCatalogItem.select(AND ('+qArgs[0:len(qArgs)-1]+'),orderBy=[model.InvCatalogItem.q.Name])')
		else:
			items = model.InvCatalogItem.select(orderBy=[model.InvCatalogItem.q.Name])
		results = []
		for item in items:
			results.append({'id':item.id, 'text':item.DisplayName(), 'Name':item.Name, 'Description':item.Description})
		return dict(results=results, items=items)
	
	@expose(format='json')
	@validate(validators={'PurchaseOrderID':validators.Int()})
	@identity.require(identity.has_permission("stores_po_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	
	def PurchaseOrdersEditorAddItemsStep3(self, PurchaseOrderID, data='', **kw):
		'''	Save the selected items to the purchase order
			If a new item is added but it is already on the PO, then ignore it
			If a new item is added and it matches a "marked deleted" item, then un-delete the item and re-display
		'''
		# Convert our string to a data structure
		data = simplejson.loads(data)
		# Load the Purchase Order and then make a list of the CatalogItemIDs
		PO = model.InvPurchaseOrder.get(PurchaseOrderID)
		CatalogItems = [x.CatalogItemID for x in PO.Items]
		# Make a list of deleted items, that is, items where the Status == 'deleted'
		DeletedItems = {}
		for item in PO.Items:
			if item.Status == 'deleted':
				DeletedItems[item.CatalogItemID] = item.id
		# Go through all the new items: For existing items, ignore, for new items, add it to the PO,
		#	grabbing defaults and then presenting the data back to the screen in json format
		results = []
		for NewItem in data:
			if not (int(NewItem['id']) in CatalogItems):
				# Get the CatalogItem
				catalogitem = model.InvCatalogItem.get(int(NewItem['id']))
				# Find the latest quote for this item
				QuoteItemID = catalogitem.VendorQuote(PO.VendorID)
				if QuoteItemID == None:
					QuotePrice = 0.0
				else:
					QuotePrice = model.InvQuoteItems.get(QuoteItemID).Price
				if catalogitem.ReorderAmt == None:
					ReorderAmt = 0.0
				else:
					ReorderAmt = catalogitem.ReorderAmt
				# Add the item to the PurchaseOrder
				POItem = model.InvPOItems(PurchaseOrderID=PurchaseOrderID, CatalogItemID=catalogitem.id, \
					QuantityRequested=ReorderAmt,QuotePrice=QuotePrice)
				results.append(dict(POItemID=POItem.id,POItemQuantityRequested=POItem.QuantityRequested,\
					POItemQuantityReceived=0,POItemQuotePrice=QuotePrice,POItemActualPrice=0,POItemNotes='',\
					POItemName=POItem.Name(),POItemCatalogItemID=POItem.CatalogItemID))
			elif (int(NewItem['id']) in CatalogItems) and DeletedItems.has_key(int(NewItem['id'])):
				# Un-delete the item and set to display
				POItem = model.InvPOItems.get(DeletedItems[int(NewItem['id'])])
				POItem.Status = ''
				results.append(dict(POItemID=POItem.id,POItemQuantityRequested=POItem.QuantityRequested,\
					POItemQuantityReceived=0,POItemQuotePrice=POItem.QuotePrice,POItemActualPrice=\
					POItem.ActualPrice,POItemNotes=POItem.Notes,POItemName=POItem.Name(),\
					POItemCatalogItemID=POItem.CatalogItemID))
		return dict(results=results)

	@expose(html='turbocare.templates.store_goodsreceivededitor')
	@validate(validators={'GoodsReceivedID':validators.Int()})
	@identity.require(identity.has_permission("stores_gr_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	
	def GoodsReceivedEditor(self, GoodsReceivedID=None, **kw):
		'''	Displays a list of the latest good received
			Display a list of potential POs to make a goods received entry from
			Editing the items in the purchase order
			Printing purchase orders
		'''
		log.debug('GoodsReceivedEditor')
		# Generate a quick list of Purchase orders to pick
		sentPOs = [] # POs which are just sent
		unfinishedPOs = [] # POs which are receiving, but not yet completed
		items = model.InvPurchaseOrder.select(orderBy=[-model.InvPurchaseOrder.q.CreateTime])
		for item in items:
			#log.debug('....PO id: %d' % item.id)
			if item.Vendor == None or len(item.Items)==0 or item.POSentOnDate == None or item.POSentOnDate == '':
				pass
			elif item.POSentOnDate != None and item.PercentComplete() <= 0.0 and len(item.Items) > 0 and item.Vendor != None:
				# log.debug('....Sent PO added')
				sentPOs.append(dict(id=item.id,name=item.Name()))
			elif item.POSentOnDate != None and (0 < item.PercentComplete() < 1):
				unfinishedPOs.append(dict(id=item.id,name=item.Name()))
		# Get a quick listing of goods received
		latestGRs = [] # Most recent goods received
		# The listing limit is found in the model_inventory.py file
		items = model.InvGoodsReceived.select(orderBy=[-model.InvGoodsReceived.q.DateReceived])
		for item in items[0:model.LATEST_GRS]:
			latestGRs.append(dict(id=item.id,name=item.Name()))
		# Configure display for the Goods received
		if GoodsReceivedID == None: # Initial screen when no item is selected
			# Make a blank entry
			Name = 'Nothing selected'
			PurchaseOrderName = ''
			PurchaseOrderID = ''
			Notes = ''
			items = []
			DateReceived = ''
			Status = ''
		else:
			try:
				goodsreceived = model.InvGoodsReceived.get(GoodsReceivedID)
			except SQLObjectNotFound:
				turbogears.flash('The Goods Received record you requested doesn\'t exist')
				raise cherrypy.HTTPRedirect('GoodsReceivedEditor')
			# Get the regular variables
			Name = goodsreceived.Name()
			PurchaseOrderID = goodsreceived.PurchaseOrderID
			Notes = goodsreceived.Notes
			Status = goodsreceived.Status
			if PurchaseOrderID != None:
				PurchaseOrderName = goodsreceived.PurchaseOrder.Name()
			else:
				PurchaseOrderName = 'ERROR: no purchase order selected'
			items = []
			for item in goodsreceived.StockItems:
				if item.Status != 'deleted':
					items.append(dict(GRItemID=item.id,GRStockItemLocations=len(item.Locations),GRItemName=item.Name,\
					GRItemCatalogItemName=item.CatalogItem.Name,GRItemQuantity=item.Quantity, GRItemPurchasePrice=\
					item.PurchasePrice,GRItemSalePrice=item.SalePrice,GRItemMRP=item.MRP,GRItemBatchNumber=\
					item.BatchNumber,GRItemExpireDate=item.ExpireDate))
			DateReceived = goodsreceived.DateReceived
		return dict(sentPOs=sentPOs, unfinishedPOs=unfinishedPOs, latestGRs=latestGRs, Name=Name,\
			PurchaseOrderName=PurchaseOrderName, PurchaseOrderID=PurchaseOrderID, items=items,\
			Notes=Notes,DateReceived=DateReceived, GoodsReceivedID=GoodsReceivedID, Status=Status)
			
	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_gr_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def GoodsReceivedEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Find PurchaseOrders that have CatalogItems who's name partially matches the QuickSearchText
		'''
		goodsreceived = model.InvGoodsReceived.select(AND (model.InvCatalogItem.q.Name.contains(str(QuickSearchText)),\
			model.InvCatalogItem.q.id==model.InvStockItem.q.CatalogItemID, model.InvStockItem.q.PurchaseOrderID==\
			model.InvGoodsReceived.q.id,model.InvGoodsReceived.q.Status!='deleted'),orderBy=[model.InvGoodsReceived.q.Sort])
		results = []
		for item in goodsreceived:
			results.append(dict(id=item.id, text=item.Name()))
		return dict(results=results)
		
	@expose(format='json')
	@validate(validators={'GoodsReceivedID':validators.Int()})
	@identity.require(identity.has_permission("stores_gr_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")		
	def GoodsReceivedEditorAddItemsStep1(self, GoodsReceivedID, **kw):
		'''	This generates the form fields that we use in the JavaScript file PickList.js "pick" object
			The form is used to add Goods received (stock items)
		'''
		# Find the Purchase Order ID for the goods received
		PurchaseOrderID = model.InvGoodsReceived.get(GoodsReceivedID).PurchaseOrderID
		id='GRPick' #Used in the javascript code to identify the PickList
		# Search fields
		POID = dict(id="grp_ID", name="PurchaseOrderID", label="ID", type="Hidden", attr=dict(length=25), data=PurchaseOrderID)
		# Input fields
		QuantityReceived = dict(id="grp_QuantityReceived", name="edQuantityReceived", label="Quantity received", type="Numeric", attr=dict(length=10), data='')
		ActualPrice = dict(id="grp_ActualPrice", name="edActualPrice", label="Actual price", type="Numeric", attr=dict(length=10), data='')
		MRP = dict(id="grp_MRP", name="edMRP", label="M.R.P.", type="Numeric", attr=dict(length=10), data='')
		# Notes = dict(id="grp_Notes", name="edNotes", label="Notes", type="String", attr=dict(length=40), data='')
		Name = dict(id="grp_Name", name="Name", label="Name (product)", type="String", attr=dict(length=30), data='') 
		BatchNumber = dict(id="grp_BatchNumber", name="BatchNumber", label="Batch number", type="String", attr=dict(length=30), data='')
		ExpireDate = dict(id="grp_ExpireDate", name="ExpireDate", label="Expire date", type="DateTime", attr=dict(length=10), data='')
		return dict(id=id, Name='AddGoodsReceived', Label='Add Goods Received',FieldsSrch=[POID], \
			Inputs=[QuantityReceived, ActualPrice, MRP, Name, BatchNumber, ExpireDate], \
			SrchUrl='GoodsReceivedEditorAddItemsStep2?GoodsReceivedID=%d' % GoodsReceivedID, DataUrl='', Url='GoodsReceivedEditorAddItemsStep3', \
			UrlVars='GoodsReceivedID=%d' % GoodsReceivedID, result_msg='ok', SrchNow=True, NoAjax=False, \
			JsonFunction='store.RenderAddItems')

	@validate(validators={'GoodsReceivedID':validators.Int()})
	@expose(format='json')
	@identity.require(identity.has_permission("stores_gr_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def GoodsReceivedEditorAddItemsStep2(self, GoodsReceivedID, **kw):
		'''	Get the list of POItems and return the results to the PickList
		'''
		PurchaseOrderID = model.InvGoodsReceived.get(GoodsReceivedID).PurchaseOrderID
		qArgs = ""
		qArgs+="model.InvPOItems.q.PurchaseOrderID == %d," % PurchaseOrderID
		qArgs+="model.InvPOItems.q.Status != 'deleted',"
		if len(qArgs) > 0:
			items = eval('model.InvPOItems.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
		else:
			items = []
		results = []
		for item in items:
			text = item.Name()
			results.append({'id':item.id, 'text':text, 'Name':item.Name(), 'Description':''})
		#Return a modified listing
		po = model.InvPurchaseOrder.get(PurchaseOrderID)
		mod_items = []
		for item in items:
			mod_item = {}
			mod_item['PurchaseOrderID'] = PurchaseOrderID
			mod_item['id'] = item.id
			# Find the quote to fill in the blanks for the stock item
			quote_items = model.InvQuoteItems.select(AND (model.InvQuoteItems.q.CatalogItemID == item.CatalogItemID, \
				model.InvQuoteItems.q.QuoteID == model.InvQuote.q.id, model.InvQuote.q.VendorID == po.VendorID),\
				orderBy=-model.InvQuote.q.ValidOn)
			if quote_items.count() > 0:
				mod_item['Name'] = quote_items[0].Product
				mod_item['edActualPrice'] = item.QuotePrice
				mod_item['edMRP'] = quote_items[0].Price
			else:
				mod_item['Name'] = item.CatalogItem.Name
				mod_item['edActualPrice'] = item.QuotePrice
				mod_item['edMRP'] = item.QuotePrice
			# Modify the quantity in case we have some stock already
			goodsreceived = model.InvStockItem.select(AND (model.InvGoodsReceived.q.PurchaseOrderID == PurchaseOrderID,\
				model.InvGoodsReceived.q.id == model.InvStockItem.q.PurchaseOrderID,model.InvStockItem.q.CatalogItemID == \
				item.CatalogItemID),orderBy=[model.InvStockItem.q.Name])
			Quantity = 0.0
			for gritem in goodsreceived:
				Quantity += gritem.Quantity
			Quantity = item.QuantityRequested - Quantity
			if Quantity < 0:
				Quantity = 1
			mod_item['edQuantityReceived'] = Quantity
			mod_item['CatalogItemID'] = item.CatalogItemID
			mod_items.append(mod_item)
		return dict(results=results, items=mod_items)
	
	@expose(format='json')
	@validate(validators={'PurchaseOrderID':validators.Int()})
	@identity.require(identity.has_permission("stores_gr_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")		
	def GoodsReceivedEditorAddItemsStep3(self, GoodsReceivedID, data='', **kw):
		'''	Save the selected items to the goods received
			It won't add duplicate items to the same goods received
		'''
		# Convert our string to a data structure
		data = simplejson.loads(data)
		# Load the goods received and a current list of 
		GR = model.InvGoodsReceived.get(GoodsReceivedID)
		ReceivedItems = [x.CatalogItemID for x in GR.StockItems]
		# Make a list of deleted items, that is, items where the Status == 'deleted'
		DeletedItems = {}
		for item in GR.StockItems:
			if item.Status == 'deleted':
				DeletedItems[item.CatalogItemID] = item.id
		# Go through all the new items: For existing items don't add, for new items, add it to the GR,
		#	grabbing defaults and then presenting the data back to the screen in json format
		results = []
		for NewItem in data:
			if not (int(NewItem['CatalogItemID']) in ReceivedItems):
				# Create a new stock item
				# Convert the ExpireDate
				if NewItem['ExpireDate'] != '':
					ExpireDate = datetime.fromtimestamp(time.mktime(time.strptime( NewItem['ExpireDate'][0:10],DATE_FORMAT)))
				else:
					ExpireDate = None
				StockItem = model.InvStockItem(PurchaseOrderID=GR.id, CatalogItemID=int(NewItem['CatalogItemID']), \
					Name=NewItem['Name'],MRP=float(NewItem['edMRP']), SalePrice=float(NewItem['edActualPrice']), \
					PurchasePrice=float(NewItem['edActualPrice']), Quantity=float(NewItem['edQuantityReceived']), \
					BatchNumber=NewItem['BatchNumber'],	ExpireDate=ExpireDate)
				# Create a new stock location
				StockLocation = model.InvStockLocation(StockItemID=StockItem.id, Location=int(self.LocationID), \
					Quantity=float(NewItem['edQuantityReceived']), IsConsumed=False, IsSold=False)
				# Update POItem entry for ActualPrice and QuantityReceived
				POItem = model.InvPOItems.select(AND (model.InvPOItems.q.PurchaseOrderID==GR.PurchaseOrderID,\
					model.InvPOItems.q.CatalogItemID==StockItem.CatalogItemID))[0]
				stockitems = model.InvStockItem.select(AND (model.InvStockItem.q.PurchaseOrderID==model.InvGoodsReceived.q.id, \
					model.InvGoodsReceived.q.PurchaseOrderID==GR.PurchaseOrderID,model.InvStockItem.q.CatalogItemID==\
					StockItem.CatalogItemID),orderBy=[model.InvStockItem.q.Name])
				ActualPrice, TotalQuantity = 0.0, 0.0
				for item in stockitems:
					ActualPrice = item.PurchasePrice
					TotalQuantity += item.Quantity
				POItem.QuantityReceived = TotalQuantity
				POItem.ActualPrice = ActualPrice
				# return our results
				results.append(dict(GRItemID=StockItem.id,GRStockItemLocations=len(StockItem.Locations),\
					GRItemName=StockItem.Name,GRItemCatalogItemName=StockItem.CatalogItem.Name,\
					GRItemQuantity=StockItem.Quantity, GRItemPurchasePrice=StockItem.PurchasePrice,\
					GRItemSalePrice=StockItem.SalePrice,GRItemMRP=StockItem.MRP,GRItemBatchNumber=\
					StockItem.BatchNumber,GRItemExpireDate=StockItem.ExpireDate))
			elif (int(NewItem['CatalogItemID']) in ReceivedItems) and DeletedItems.has_key(int(NewItem['CatalogItemID'])):
				# Un-delete the item and set to display
				StockItem = model.InvStockItem.get(DeletedItems[int(NewItem['CatalogItemID'])])
				StockItem.Status = ''
				results.append(dict(GRItemID=StockItem.id,GRStockItemLocations=len(StockItem.Locations),\
					GRItemName=StockItem.Name,GRItemCatalogItemName=StockItem.CatalogItem.Name,\
					GRItemQuantity=StockItem.Quantity, GRItemPurchasePrice=StockItem.PurchasePrice,\
					GRItemSalePrice=StockItem.SalePrice,GRItemMRP=StockItem.MRP,GRItemBatchNumber=\
					StockItem.BatchNumber,GRItemExpireDate=StockItem.ExpireDate))
		return dict(results=results)

	@expose()
	@validate(validators={'GoodsReceivedID':validators.Int(),'Notes':validators.String(),'Operation':validators.String(),\
	'DateReceived':validators.String(),'ExpectedDeliveryDate':validators.String()})
	@identity.require(identity.has_permission("stores_gr_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")		
	def GoodsReceivedSave(self, GoodsReceivedID,DateReceived='',Notes='',GRItemID=[],GRItemName=[],\
		GRItemQuantity=[], GRItemPurchasePrice=[],	GRItemSalePrice=[],GRItemMRP=[],GRItemBatchNumber=\
		[],GRItemExpireDate=[],GRItemCounter=[], Operation='', **kw):
		'''	Delete or update (modify) an existing Goods received
			NOTE: the items in a goods received are stock items, so deleting and modifying the 
			stock items after some activity has been done is dangerous.
		'''
		log.debug('GoodsReceivedSave')
		# Load our Goods received record
		GR = model.InvGoodsReceived.get(GoodsReceivedID)
		PurchaseOrderID = GR.PurchaseOrderID
		# Get our operation
		log.debug('....Operation: %s' % Operation)
		if Operation == 'Save':
			# Silly but necessary date manipulations 
			if DateReceived != None and DateReceived != '':
				DateReceived = datetime.fromtimestamp(time.mktime(time.strptime(DateReceived[0:10],DATE_FORMAT)))
			else:
				DateReceived = None
			GR.DateReceived = DateReceived
			GR.Notes = Notes
			turbogears.flash('Record Updated. Note: Modifying Goods received items needs to be done on the Stock Header (Stock Item) record.  Click on the link to edit the record for a particular stock item')
			# REMOVE - Update the Purchase Order Items
			# NEW Policy - No more editing of stock from the Goods Received screen.  Force the user to use
			# the stock item editor so that it's easier for me to maintain the code (because making changes
			# can be tricky to maintain in two places)
#			CurrStock = [x.id for x in GR.StockItems]
#			if len(GRItemCounter) > 1:
#				NewStockItems = [int(x) for x in GRItemID]
#			elif len(GRItemCounter) == 1:
#				NewStockItems = [int(GRItemID)]
#			else:
#				NewStockItems = []
#			for NewID, Quantity, PurchasePrice, SalePrice, MRP,BatchNumber, ExpireDate in \
#				zip(GRItemID,GRItemQuantity, GRItemPurchasePrice,GRItemSalePrice,GRItemMRP,\
#				GRItemBatchNumber,GRItemExpireDate):
#				if int(NewID) in CurrStock: #Update the item
#					if ExpireDate != None and ExpireDate != '':
#						ExpireDate = datetime.fromtimestamp(time.mktime(time.strptime(ExpireDate[0:10],DATE_FORMAT)))
#					else:
#						ExpireDate = None
#					stockitem = model.InvStockItem.get(NewID)
#					stockitem.Quantity = float(Quantity)
#					stockitem.PurchasePrice = float(PurchasePrice)
#					stockitem.SalePrice = float(SalePrice)
#					stockitem.MRP = float(MRP)
#					stockitem.BatchNumber = str(BatchNumber)
#					stockitem.ExpireDate = ExpireDate
#				else: #We shouldn't have this, becuase we create new POItems in a different place (using AJAX/AJSON)
#					pass
			# Delete any StockItems which have been removed
			# log.debug(CurrPOItems)
			# log.debug(NewPOItemIDs)
#			mark_delete_count, delete_count = 0,0
#			for stockitemid in CurrStock:
#				if not (stockitemid in NewStockItems):
#					stockitem = model.InvStockItem.get(NewID)
#					if len(stockitem.Locations) > 0 or (stockitem.TransferCount() > 0):
#						poitem.Status = 'deleted'
#						mark_delete_count += 1
#					else:
#						poitem.destroySelf()
#						delete_count += 1
#			if mark_delete_count == 0 and  delete_count == 0:
#				turbogears.flash('Record updated')
#			else:
#				turbogears.flash('Record updated (%d items marked deleted and %d items deleted' % (mark_delete_count, delete_count))
		elif Operation == 'Delete':
			if not GR.SafeToDelete():
				GR.Status = 'deleted'
				turbogears.flash('Recorded marked deleted')
			else:
				#Delete all stock items linked to the goods received
				delete_count = 0 # I want to count how many related db records are deleted by this action
				for item in GR.StockItems:
					#Delete all the stock location entries for the stock item (should only be one)
					for location in item.Locations:
						#Delete all stock transfers to and from this location (should be none)
						for from_transfer in location.TransfersFromHere:
							delete_count += 1
							from_transfer.destroySelf()
						for to_transfer in location.TransfersToHere:
							delete_count += 1
							to_transfer.destroySelf()
						delete_count += 1
						location.destroySelf()
					delete_count += 1
					item.destroySelf()
				# Now delete the goods received
				delete_count += 1
				GR.destroySelf()
				log.debug('....%d rows removed in GR deletion' % delete_count)
				turbogears.flash('Record deleted (incl. related records, %d rows removed)' % delete_count)
			GoodsReceivedID=None
		elif Operation == 'Un-Delete':
			GR.Status = ''
			turbogears.flash('Record un-deleted.')
		# Now update the purchase order which we're linked to
		utils.UpdatePurchaseOrder(PurchaseOrderID)
		# Load the GoodsReceived
		if GoodsReceivedID != None:
			raise cherrypy.HTTPRedirect('GoodsReceivedEditor?GoodsReceivedID=%d' % GoodsReceivedID)
		else:
			raise cherrypy.HTTPRedirect('GoodsReceivedEditor')
			
	@expose(html='turbocare.templates.store_quoterequestseditor')
	@validate(validators={'QuoteRequestID':validators.Int()})
	@identity.require(identity.has_permission("stores_quoterequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")		
	def QuoteRequestsEditor(self, QuoteRequestID=None, **kw):
		'''	Create/Edit/Delete a Quote request
			Display: current and past quote requests and the most recent quotes
		'''
		log.debug('QuoteRequestsEditor')
		# Current/past quote requests and some recent quotes
		currentQRs = [] # POs which are just sent
		pastQRs = [] # POs which are receiving, but not yet completed
		items = model.InvQuoteRequest.select(orderBy=[-model.InvQuoteRequest.q.CreateTime])
		for item in items:
			try:
				if len(item.Quotes) < len(item.Vendors):
					currentQRs.append(dict(id=item.id,name=item.Name()))
				else:
					pastQRs.append(dict(id=item.id,name=item.Name()))
			except SQLObjectNotFound, errorstr:
				turbogears.flash('Some database errors were cleaned while loading this page.  Please reload the page')
				errorArr = errorstr[0].split(' ')
				table = errorArr[2]
				id = errorArr[6]
				if table == 'InvVendor':
					item.removeInvVendor(int(id))
				else:
					item.removeInvQuote(int(id))
		pastQRs = pastQRs[0:model.LATEST_QRS]
		# Get a quick listing of the latest quotes
		latestQs = [] # Most recent goods received
		# The listing limit is found in the model_inventory.py file
		items = model.InvQuote.select(orderBy=[-model.InvQuote.q.ValidOn])
		for item in items[0:model.LATEST_QS]:
			latestQs.append(dict(id=item.id,name=item.Name()))
		# Configure display for the Goods received
		if QuoteRequestID == None: # Initial screen when no item is selected
			# Make a blank entry
			Name = 'CREATE NEW QUOTE REQUEST'
			QuoteRequestID = ''
			RequestDate = model.cur_date_time().strftime(model.DATE_FORMAT)
			Notes = ''
			vendors = []
			items = []
		else:
			quoterequest = model.InvQuoteRequest.get(QuoteRequestID)
			# Get the regular variables
			Name = quoterequest.Name()
			Notes = quoterequest.Notes
			RequestDate = quoterequest.RequestDate
			vendors = []
			for vendor in quoterequest.Vendors:
				# make a vendor link which is either a shortcut to create a quote from this quote request, or links to the quote which was already made
				Qs = model.InvQuote.select(AND (model.InvQuote.q.QuoteRequestID==QuoteRequestID, \
					model.InvQuote.q.VendorID==vendor.id))
				if Qs.count() > 0:
					linkurl = "QuotesEditor?QuoteID=%d" % Qs[0].id
					linktext = "linked quote"
				else:
					linkurl = "QuotesEditor?VendorID=%d&QuoteRequestID=%d" % (vendor.id,QuoteRequestID)
					linktext = "create quote"
				vendors.append(dict(id=vendor.id,name=vendor.Name, linkurl=linkurl, linktext=linktext))
			items = []
			for item in quoterequest.RequestItems:
				if item.Status != 'deleted':
					items.append(dict(ItemID=item.id, ItemName=item.Name(), ItemQty=item.Qty,\
					ItemNotes=item.Notes))
		return dict(currentQRs=currentQRs, pastQRs=pastQRs, latestQs=latestQs, Name=Name, RequestDate=\
			RequestDate, Notes=Notes, vendors=vendors, items=items, QuoteRequestID=QuoteRequestID)

	@expose(html='turbocare.templates.store_quoterequestprint')
	@validate(validators={'QuoteRequestID':validators.Int()})
	@identity.require(identity.has_permission("stores_quoterequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")		
	def QuoteRequestsEditorPrint(self, QuoteRequestID, Operation=None, PreparedBy='', CheckedBy='',
	ApprovedBy='', FromAddress='', VendorAddresses=[], VendorIDs=[], VendorNotes=[],VendorNames=[], **kw):
		'''	Print a Quote request
		'''
		if Operation=='Print':
			reports = []
			NewVendorIDs = []
			NewVendorNames = []
			NewVendorNotes = []
			NewVendorAddresses = []
			QR = model.InvQuoteRequest.get(QuoteRequestID)
			if isinstance(VendorIDs,basestring): # only a single entry exists
				Vendor = model.InvVendor.get(int(VendorIDs))
				report = QuoteRequest.QuoteRequestPrintOut(QR=QR, Vendor=Vendor, PreparedBy=PreparedBy,
					CheckedBy=CheckedBy, ApprovedBy=ApprovedBy,	ToAddress=VendorAddresses,
					FromAddress=FromAddress, Notes=VendorNotes)
				filename = report.P()
				# NEED to change this technique to something a little more secure
				reports.append(dict(link='/static/reports/%s' % filename,name=Vendor.Name))
				# Re-adding the names, ids, and addresses because they don't propogate properly
				NewVendorIDs.append(VendorIDs)
				NewVendorNames.append(Vendor.Name)
				NewVendorNotes.append(VendorNotes)
				NewVendorAddresses.append(VendorAddresses)
			else:
				for vendorid, ToAddress, Notes  in zip(VendorIDs, VendorAddresses, VendorNotes):
					Vendor = model.InvVendor.get(int(vendorid))
					report = QuoteRequest.QuoteRequestPrintOut(QR=QR, Vendor=Vendor, PreparedBy=PreparedBy,
						CheckedBy=CheckedBy, ApprovedBy=ApprovedBy,	ToAddress=ToAddress,
						FromAddress=FromAddress, Notes=Notes)
					filename = report.P()
					# NEED to change this technique to something a little more secure
					reports.append(dict(link='/static/reports/%s' % filename,name=Vendor.Name))
					# Re-adding the names, ids, and addresses because they don't propogate properly
					NewVendorIDs.append(vendorid)
					NewVendorNames.append(Vendor.Name)
					NewVendorNotes.append(Notes)
					NewVendorAddresses.append(ToAddress)
			VendorIDs = NewVendorIDs
			VendorNames = NewVendorNames
			VendorNotes = NewVendorNotes
			VendorAddresses = NewVendorAddresses
		else:
			QR = model.InvQuoteRequest.get(QuoteRequestID)
			Notes = QR.Notes
			PreparedBy = model.cur_user_name()
			CheckedBy = "Unknown Person"
			ApprovedBy = "Unknown Person"
			VendorAddresses = []
			VendorIDs = []
			VendorNotes = []
			VendorNames = []
			for vendor in QR.Vendors:
				VendorAddresses.append(vendor.Name + '\nAttn: ' + vendor.ContactName + '\n' + vendor.AddressLabel)
				VendorIDs.append(vendor.id)
				VendorNames.append(vendor.Name)
				VendorNotes.append(Notes)
			FromAddress = "CIHSR\n4th Mile Road, Dimapur, NL\n11122333\nPH: 111222333444"
			reports = []
		return dict(QuoteRequestID=QuoteRequestID,PreparedBy=PreparedBy,CheckedBy=CheckedBy,
		ApprovedBy=ApprovedBy,VendorAddresses=VendorAddresses,FromAddress=FromAddress,
		VendorNotes=VendorNotes,VendorIDs=VendorIDs, VendorNames=VendorNames,
		reports=reports)

	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_quoterequest_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")			
	def QuoteRequestsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Find Quote Requests that have CatalogItems who's name partially matches the QuickSearchText
		'''
		quoterequests = model.InvQuoteRequest.select(AND (model.InvCatalogItem.q.Name.contains(str(QuickSearchText)),\
			model.InvCatalogItem.q.id==model.InvQuoteRequestItems.q.CatalogItemID, model.InvQuoteRequestItems.q.QuoteRequestID==\
			model.InvQuoteRequest.q.id,model.InvQuoteRequest.q.Status!='deleted'),orderBy=[model.InvQuoteRequest.q.Sort])
		results = []
		for item in quoterequests:
			results.append(dict(id=item.id, text=item.Name()))
		return dict(results=results)
		
	@expose(format='json')
	@validate(validators={'QuoteRequestID':validators.Int()})
	@identity.require(identity.has_permission("stores_quoterequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")			
	def QuoteRequestsEditorAddItemsStep1(self, QuoteRequestID, **kw):
		'''	This generates the form fields that we use in the JavaScript file PickList.js "pick" object
			The form is used to add catalog items to the quote request
		'''
		id='QRPick' #Used in the javascript code to identify the PickList
		# Search fields
		Name = dict(id="pl_Name", name="Name", label="Name", type="String", attr=dict(length=25), data='')
		# Select box data
		InvGrpStockNames = [x.Name for x in model.InvGrpStock.select(orderBy=[model.InvGrpStock.q.Name])]
		SrchCatalogGroups = dict(id="pl_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect", attr=dict(Groups=InvGrpStockNames), data='')
		return dict(id=id, Name='AddItems', Label='Select items from the item master',\
			FieldsSrch=[Name, SrchCatalogGroups], Inputs=[], SrchUrl='QuoteRequestsEditorAddItemsStep2', \
			DataUrl='', Url='QuoteRequestsEditorAddItemsStep3', UrlVars='QuoteRequestID=%d' % QuoteRequestID, result_msg='ok', \
			SrchNow=False, NoAjax=False, JsonFunction='store.RenderAddItems')

	@validate(validators={'GoodsReceivedID':validators.Int()})
	@expose(format='json')
	@identity.require(identity.has_permission("stores_quoterequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuoteRequestsEditorAddItemsStep2(self, Name='', Groups='', **kw):
		'''	Search for CatalogItems and return the results to the PickList
		'''
		qArgs = ""
		if Name != '':
			qArgs+="model.InvCatalogItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvCatalogItem.q.IsSelectable == True,"
		qArgs+="model.InvCatalogItem.q.Status != 'deleted',"
		if Groups != '':
			Groups = set(Groups.split(","))
			orArgs = ''
			for group in Groups:
				orArgs+="model.InvGrpStock.q.Name == '"+group+"',"
			qArgs+= "OR ("+orArgs[0:len(orArgs)-1]+"),"
			qArgs+="model.InvGrpStock.q.id == model.InvViewJoinCatalogItemGrpStock.q.GrpStockId,"
			qArgs+="model.InvCatalogItem.q.id == model.InvViewJoinCatalogItemGrpStock.q.CatalogItemId,"
		if len(qArgs) > 0:
			items = eval('model.InvCatalogItem.select(AND ('+qArgs[0:len(qArgs)-1]+'),orderBy=[model.InvCatalogItem.q.Name])')
		else:
			items = model.InvCatalogItem.select(orderBy=[model.InvCatalogItem.q.Name])
		results = []
		for item in items:
			results.append({'id':item.id, 'text':item.Name, 'Name':item.Name, 'Description':item.Description})
		return dict(results=results, items=items)
	
	@expose(format='json')
	@validate(validators={'QuoteRequestID':validators.Int()})
	@identity.require(identity.has_permission("stores_quoterequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuoteRequestsEditorAddItemsStep3(self, QuoteRequestID, data='', **kw):
		'''	Save the selected items to the quote request
			If a new item is added but it is already on the QR, then ignore it
			If a new item is added and it matches a "marked deleted" item, then un-delete the item and re-display
		'''
		# Convert our string to a data structure
		data = simplejson.loads(data)
		# Load the Quote Request
		QR = model.InvQuoteRequest.get(QuoteRequestID)
		# Make a list of CatalogItems and deleted items, that is, items where the Status == 'deleted'
		DeletedItems = {}
		CatalogItems = []
		for item in QR.RequestItems:
			if item.Status == 'deleted':
				DeletedItems[item.CatalogItemID] = item.id
			CatalogItems.append(item.CatalogItemID)
		# Go through all the new items: For existing items, ignore, for new items, add it to the QR,
		#	grabbing defaults and then presenting the data back to the screen in json format
		results = []
		for NewItem in data:
			if not (int(NewItem['id']) in CatalogItems):
				# Check for annual consumption and use that value as the quantity
				catalogitem = model.InvCatalogItem.get(int(NewItem['id']))
				FromDate = datetime.now() - timedelta(days=365)
				Quantity = catalogitem.Consumption(FromDate)
				# Add the item to the PurchaseOrder
				Item = model.InvQuoteRequestItems(QuoteRequestID=QuoteRequestID, CatalogItemID=catalogitem.id, \
					Qty=Quantity)
				results.append(dict(ItemID=Item.id,ItemQty=Item.Qty,ItemNotes='',ItemName=Item.Name()))
			elif (int(NewItem['id']) in CatalogItems) and DeletedItems.has_key(int(NewItem['id'])):
				# Un-delete the item and set to display
				Item = model.InvQuoteRequestItems.get(DeletedItems[int(NewItem['id'])])
				Item.Status = ''
				results.append(dict(ItemID=Item.id,ItemQty=Item.Qty,ItemNotes='',ItemName=Item.Name()))
		return dict(results=results)

	@expose(format='json')
	@validate(validators={'QuoteRequestID':validators.Int()})
	@identity.require(identity.has_permission("stores_quoterequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuoteRequestsEditorVendorSelect(self, QuoteRequestID=None, **kw):
		'''	Load the Quote request Vendor Options
			Mark items which are already selected as selected
		'''
		cur_vendors = []
		if QuoteRequestID!=None:
			quoterequest = model.InvQuoteRequest.get(QuoteRequestID)
			for vendor in quoterequest.Vendors:
				cur_vendors.append(vendor.id)
		vendors = model.InvVendor.select(orderBy=[model.InvVendor.q.Name])
		results = []
		for vendor in vendors:
			results.append(dict(id=vendor.id, text=vendor.Name, selected=(vendor.id in cur_vendors)))
		return dict(results=results)
		
	@expose()
	@validate(validators={'QuoteRequestID':validators.Int(),'Notes':validators.String(),'Operation':validators.String(),\
	'RequestDate':validators.String()})
	@identity.require(identity.has_permission("stores_quoterequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuoteRequestsSave(self, QuoteRequestID=None, RequestDate='',Notes='',ItemID=[],ItemQty=[], ItemNotes=[],\
		ItemCounter=[], Vendors=[], VendorsCounter=[], Operation='', **kw):
		'''	Delete or update (modify) an existing Quote request
		'''
		log.debug('QuoteRequestsSave')
		# Load our Goods received record
		if QuoteRequestID == None:
			QR = model.InvQuoteRequest()
			QuoteRequestID = QR.id
		else:
			QR = model.InvQuoteRequest.get(QuoteRequestID)
		# Get our operation
		log.debug('....Operation: %s' % Operation)
		if Operation == 'Save':
			# Silly but necessary date manipulations (I really wish the validators for dates worked!!!)
			if RequestDate != None and RequestDate != '':
				RequestDate = datetime.fromtimestamp(time.mktime(time.strptime(RequestDate[0:10],DATE_FORMAT)))
			else:
				RequestDate = None
			QR.RequestDate = RequestDate
			QR.Notes = Notes
			# Update the quote request Items
			CurrItems = [x.id for x in QR.RequestItems]
			if len(ItemCounter) > 1:
				NewItems = [int(x) for x in ItemID]
			elif len(ItemCounter) == 1:
				NewItems = [int(ItemID)]
			else:
				NewItems = []
			if len(ItemCounter) > 1:
				for NewID, Qty, Notes in	zip(ItemID,ItemQty, ItemNotes):
					if int(NewID) in CurrItems: #Update the item
						qritem = model.InvQuoteRequestItems.get(NewID)
						qritem.Qty = float(Qty)
						qritem.Notes = str(Notes)
					else: #We shouldn't have this, becuase we create new POItems in a different place (using AJAX/AJSON)
						pass
			elif len(ItemCounter) == 1:
				if int(ItemID) in CurrItems: #Update the item
					qritem = model.InvQuoteRequestItems.get(int(ItemID))
					qritem.Qty = float(ItemQty)
					qritem.Notes = str(ItemNotes)
			# Delete any StockItems which have been removed
			mark_delete_count, delete_count = 0,0
			for itemid in CurrItems:
				if not (itemid in NewItems):
					item = model.InvQuoteRequestItems.get(itemid)
					if len(item.QuoteRequest.Quotes) > 0:
						item.Status = 'deleted'
						mark_delete_count += 1
					else:
						log.debug('....Item ID of deleted item: %d' % item.id)
						item.destroySelf()
						delete_count += 1
			# Update Vendor information
			# convert our Vendor list to an integer list
			if isinstance(Vendors, basestring): # an array with only one entry
				Vendors = [int(Vendors)]
			else:
				Vendors = [int(x) for x in Vendors]
			for vendor in QR.Vendors:
				if not (vendor.id in Vendors):
					QR.removeInvVendor(vendor)
			# Add any vendors which we don't already have
			current_vendors = [x.id for x in QR.Vendors]
			for vendorid in Vendors:
				if not (vendorid in current_vendors):
					QR.addInvVendor(vendorid)
			if mark_delete_count == 0 and  delete_count == 0:
				turbogears.flash('Record updated')
			else:
				turbogears.flash('Record updated (%d items marked deleted and %d items deleted)' % (mark_delete_count, delete_count))
		elif Operation == "Copy to New":# Take the current Quote request and make a new quote request that matches it
			QR = model.InvQuoteRequest.get(QuoteRequestID)
			NewQR = model.InvQuoteRequest(RequestDate=model.cur_date_time(),Notes=QR.Notes)
			for item in QR.RequestItems:
				NewItem = model.InvQuoteRequestItems(QuoteRequestID=NewQR.id, CatalogItemID=item.CatalogItemID,\
					Qty=item.Qty,Notes=item.Notes)
			for vendor in QR.Vendors:
				NewQR.addInvVendor(vendor)
			QuoteRequestID = NewQR.id
			turbogears.flash('Request copied into new request')
		elif Operation == 'Delete':
			if len(QR.Quotes) > 0:
				QR.Status = 'deleted'
				turbogears.flash('Recorded marked deleted')
			else:
				#Delete all linked items
				delete_count = 0 # I want to count how many related db records are deleted by this action
				for item in QR.RequestItems: # delete all linked items
					delete_count += 1
					item.destroySelf()
				for vendor in QR.Vendors: # un-link all vendors from this record
					QR.removeInvVendor(vendor)
				# Now delete the record
				delete_count += 1
				QR.destroySelf()
				log.debug('....%d rows removed in QR deletion' % delete_count)
				turbogears.flash('Record deleted (incl. related records, %d rows removed)' % delete_count)
			QuoteRequestID=None
		elif Operation == 'Un-Delete':
			QR.Status = ''
			turbogears.flash('Record un-deleted.')
		elif Operation == 'Print' and QuoteRequestID!=None:
			raise cherrypy.HTTPRedirect('QuoteRequestsEditorPrint?QuoteRequestID=%d' % QuoteRequestID)
		# Load the QuoteRequest
		if QuoteRequestID != None:
			raise cherrypy.HTTPRedirect('QuoteRequestsEditor?QuoteRequestID=%d' % QuoteRequestID)
		else:
			raise cherrypy.HTTPRedirect('QuoteRequestsEditor')
			
	@expose(html='turbocare.templates.store_quoteseditor')
	@validate(validators={'QuoteID':validators.Int(),'QuoteRequestID':validators.Int(),'VendorID':validators.Int()})
	@identity.require(identity.has_permission("stores_quote_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuotesEditor(self, QuoteID=None,QuoteRequestID=None,VendorID=None, **kw):
		'''	Create/Edit/Delete a Quote
			Display: latest quotes
		'''
		log.debug('QuotesEditor')
		# Current/past quote requests and some recent quotes
		latestQs = [] # latest Quotes
		items = model.InvQuote.select(orderBy=[-model.InvQuote.q.CreateTime])
		for item in items:
			latestQs.append(dict(id=item.id,name=item.Name()))
		latestQs = latestQs[0:model.LATEST_QS]
		# Define our main quote variable
		Q = None
		# If we have a QuoteID, we'll use that, but if it's None, we'll check to see if we have a QuoteRequest and Vendor to create a new Quote
		if QuoteID == None and QuoteRequestID!=None and VendorID!=None:
			log.debug('....Creating a new quote')
			QR = model.InvQuoteRequest.get(QuoteRequestID)
			Q = model.InvQuote(VendorID=VendorID,QuoteRequestID=QuoteRequestID,ValidOn=datetime.now())
			for item in QR.RequestItems:
				QItem = model.InvQuoteItems(QuoteID=Q.id,CatalogItemID=item.CatalogItemID,Product=\
					item.CatalogItem.Name, Price=0.0, Ranking=10)
			QuoteID = Q.id
		# Prepare variables for the form
		if QuoteID == None: # Initial screen when no item is selected
			# Make a blank entry
			Name = 'CREATE NEW QUOTE'
			VendorName = ''
			VendorID = ''
			QuoteRequestName = ''
			QuoteRequestID = ''
			QuoteID = ''
			ValidOn = model.cur_date_time().strftime(model.DATE_FORMAT)
			Notes = ''
			items = []
			Status='' # used for showing/hiding the un-delete button
		else:
			if Q==None:
				Q = model.InvQuote.get(QuoteID)
			# Get the regular variables
			Name = Q.Name()
			VendorID = Q.VendorID
			if VendorID != None:
				VendorName = Q.Vendor.Name
			else:
				VendorName = ''
			QuoteRequestID = Q.QuoteRequestID
			if QuoteRequestID != None:
				QuoteRequestName = Q.QuoteRequest.Name()
			else:
				QuoteRequestName = ''
			ValidOn = Q.ValidOn
			Notes = Q.Notes
			items = []
			Status=Q.Status # used for showing/hiding the un-delete button
			for item in Q.Items:
				if item.Status != 'deleted':
					items.append(dict(ItemID=item.id, ItemName=item.ShortName(), ItemProduct=item.Product,\
					ItemRanking=item.Ranking, ItemPrice=item.Price, ItemNotes=item.Notes))
		return dict(latestQs=latestQs, Name=Name, VendorID=VendorID, VendorName=VendorName, ValidOn=ValidOn, \
			QuoteRequestID=QuoteRequestID, QuoteRequestName=QuoteRequestName, Notes=Notes, items=items, \
			QuoteID=QuoteID, Status=Status)
	
	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_quote_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuotesEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Find Quotes that have CatalogItems who's name partially matches the QuickSearchText
			or, if the quotes listing for catalog items is zero, then do a vendor search on the text
		'''
		quotes = model.InvQuote.select(AND (model.InvCatalogItem.q.Name.contains(str(QuickSearchText)),\
			model.InvCatalogItem.q.id==model.InvQuoteItems.q.CatalogItemID, model.InvQuoteItems.q.QuoteID==\
			model.InvQuote.q.id,model.InvQuote.q.Status!='deleted'),orderBy=[model.InvQuote.q.Sort])
		if quotes.count() == 0:
			quotes = model.InvQuote.select(AND (model.InvVendor.q.Name.contains(str(QuickSearchText)),\
				model.InvVendor.q.id==model.InvQuote.q.VendorID,model.InvQuote.q.Status!='deleted'),\
				orderBy=[model.InvQuote.q.Sort])			
		results = []
		for item in quotes:
			results.append(dict(id=item.id, text=item.Name()))
		return dict(results=results)
		
	@expose(format='json')
	@validate(validators={'QuoteID':validators.Int()})
	@identity.require(identity.has_permission("stores_quote_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuotesEditorAddItemsStep1(self, QuoteID, **kw):
		'''	This generates the form fields that we use in the JavaScript file PickList.js "pick" object
			The form is used to add catalog items to the quote
		'''
		id='QPick' #Used in the javascript code to identify the PickList
		# Search fields
		Name = dict(id="pl_Name", name="Name", label="Name", type="String", attr=dict(length=25), data='')
		# Select box data
		InvGrpStockNames = [x.Name for x in model.InvGrpStock.select(orderBy=[model.InvGrpStock.q.Name])]
		SrchCatalogGroups = dict(id="pl_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect", attr=dict(Groups=InvGrpStockNames), data='')
		return dict(id=id, Name='AddItems', Label='Select items from the item master',\
			FieldsSrch=[Name, SrchCatalogGroups], Inputs=[], SrchUrl='QuotesEditorAddItemsStep2', \
			DataUrl='', Url='QuotesEditorAddItemsStep3', UrlVars='QuoteID=%d' % QuoteID, result_msg='ok', \
			SrchNow=False, NoAjax=False, JsonFunction='store.RenderAddItems')

	@expose(format='json')
	@identity.require(identity.has_permission("stores_quote_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuotesEditorAddItemsStep2(self, Name='', Groups='', **kw):
		'''	Search for CatalogItems and return the results to the PickList
		'''
		qArgs = ""
		if Name != '':
			qArgs+="model.InvCatalogItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvCatalogItem.q.IsSelectable == True,"
		qArgs+="model.InvCatalogItem.q.Status != 'deleted',"
		if Groups != '':
			Groups = set(Groups.split(","))
			orArgs = ''
			for group in Groups:
				orArgs+="model.InvGrpStock.q.Name == '"+group+"',"
			qArgs+= "OR ("+orArgs[0:len(orArgs)-1]+"),"
			qArgs+="model.InvGrpStock.q.id == model.InvViewJoinCatalogItemGrpStock.q.GrpStockId,"
			qArgs+="model.InvCatalogItem.q.id == model.InvViewJoinCatalogItemGrpStock.q.CatalogItemId,"
		if len(qArgs) > 0:
			items = eval('model.InvCatalogItem.select(AND ('+qArgs[0:len(qArgs)-1]+'),orderBy=[model.InvCatalogItem.q.Name])')
		else:
			items = model.InvCatalogItem.select(orderBy=[model.InvCatalogItem.q.Name])
		results = []
		for item in items:
			results.append({'id':item.id, 'text':item.Name, 'Name':item.Name, 'Description':item.Description})
		return dict(results=results, items=items)
	
	@expose(format='json')
	@validate(validators={'QuoteID':validators.Int()})
	@identity.require(identity.has_permission("stores_quote_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")					
	def QuotesEditorAddItemsStep3(self, QuoteID, data='', **kw):
		'''	Save the selected items to the quote
			If a new item is added but it is already on the Q, then ignore it
			If a new item is added and it matches a "marked deleted" item, then un-delete the item and re-display
		'''
		# Convert our string to a data structure
		# raise ZeroDivisionError
		log.debug(data)
		data = simplejson.loads(data)
		# Load the Quote
		Q = model.InvQuote.get(QuoteID)
		# Make a list of CatalogItems and deleted items, that is, items where the Status == 'deleted'
		DeletedItems = {}
		CatalogItems = []
		for item in Q.Items:
			if item.Status == 'deleted':
				DeletedItems[item.CatalogItemID] = item.id
			CatalogItems.append(item.CatalogItemID)
		# Go through all the new items: For existing items, ignore, for new items, add it to the Q,
		#	grabbing defaults and then presenting the data back to the screen in json format
		results = []
		for NewItem in data:
			if not (int(NewItem['id']) in CatalogItems):
				# Add the item to the quote
				Item = model.InvQuoteItems(QuoteID=QuoteID,CatalogItemID=int(NewItem['id']), \
					Product=str(NewItem['Name']), Price=0.0, Ranking=10)
				results.append(dict(ItemID=Item.id, ItemName=Item.ShortName(), ItemProduct=Item.Product,\
					ItemRanking=Item.Ranking, ItemPrice=Item.Price, ItemNotes=Item.Notes))
			elif (int(NewItem['id']) in CatalogItems) and DeletedItems.has_key(int(NewItem['id'])):
				# Un-delete the item and set to display
				Item = model.InvQuoteItems.get(DeletedItems[int(NewItem['id'])])
				Item.Status = ''
				results.append(dict(ItemID=Item.id, ItemName=Item.ShortName(), ItemProduct=Item.Product,\
					ItemRanking=Item.Ranking, ItemPrice=Item.Price, ItemNotes=Item.Notes))
		return dict(results=results)
	
	@expose(format='json')
	@identity.require(identity.has_permission("stores_quote_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuotesEditorVendorSelect(self, SearchText='', **kw):
		'''	Load the Vendor Options
		'''
		SearchText = str(SearchText)
		items = model.InvVendor.select(model.InvVendor.q.Name.contains(SearchText),orderBy=[model.InvVendor.q.Name])
		results = []
		for item in items:
			if item.Status != 'deleted':
				results.append(dict(id=item.id, text=item.Name, linkurl="VendorsEditor?VendorID=%d" % item.id))
		return dict(results=results, function_name='QuotesEditorVendorSelect')

	@expose(format='json')
	@identity.require(identity.has_permission("stores_quote_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuotesEditorQuoteRequestSelect(self, SearchText='', **kw):
		'''	Load the QuoteRequest Options
		'''
		SearchText = str(SearchText)
		if SearchText == '':
			quoterequests = model.InvQuoteRequest.select(model.InvQuoteRequest.q.Status!='deleted',\
				orderBy=[-model.InvQuoteRequest.q.RequestDate],distinct=True)
		else:
			quoterequests = model.InvQuoteRequest.select(AND (model.InvCatalogItem.q.Name.contains(SearchText),\
				model.InvCatalogItem.q.id==model.InvQuoteRequestItems.q.CatalogItemID,model.InvQuoteRequest.q.id==\
				model.InvQuoteRequestItems.q.QuoteRequestID,model.InvQuoteRequestItems.q.Status!='deleted'),\
				orderBy=[-model.InvQuoteRequest.q.RequestDate],distinct=True)
		# If no quote requests match with the catalog item name, then try the vendor name
		if quoterequests.count() == 0:# This is computationally instense for the server
			searchVendors = [x.Name for x in model.InvVendor.select(AND (model.InvVendor.q.Name.contains(SearchText),\
				model.InvVendor.q.Status!='deleted'),orderBy=[model.InvVendor.q.Name])]
			searchVendors = set(searchVendors)
			quoterequests = []
			select = model.InvQuoteRequest.select(model.InvQuoteRequest.q.Status!='deleted',\
				orderBy=[-model.InvQuoteRequest.q.RequestDate])
			for row in select:
				VendorNames = set([x.Name for x in row.Vendors])
				if len(searchVendors  & VendorNames) > 0:
					quoterequests.append(row)
		results = []
		for item in quoterequests:
			if item.Status != 'deleted':
				results.append(dict(id=item.id, text=item.Name(), linkurl="QuoteRequestsEditor?QuoteRequestID=%d" % item.id))
		return dict(results=results, function_name='QuotesEditorQuoteRequestSelect')

	@expose()
	@validate(validators={'QuoteID':validators.Int(),'Notes':validators.String(),'Operation':validators.String(),\
	'ValidOn':validators.String(),'VendorID':validators.Int(),'QuoteRequestID':validators.Int()})
	@identity.require(identity.has_permission("stores_quote_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def QuotesSave(self, QuoteID=None, QuoteRequestID=None, VendorID=None, ValidOn='',Notes='',ItemID=[],\
		ItemProduct=[], ItemNotes=[], ItemPrice=[], ItemRanking=[], ItemCounter=[], Operation='', **kw):
		'''	Delete or update (modify) an existing Quote
		'''
		log.debug('QuotesSave')
		# Check if we need to create a record
		if QuoteID == None:
			Q = model.InvQuote(QuoteRequestID=QuoteRequestID,VendorID=VendorID)
			QuoteID = Q.id
		else:
			Q = model.InvQuote.get(QuoteID)
		# Get our operation
		log.debug('....Operation: %s' % Operation)
		if Operation == 'Save':
			# Silly but necessary date manipulations (I really wish the validators for dates worked!!!)
			if ValidOn != None and ValidOn != '':
				ValidOn = datetime.fromtimestamp(time.mktime(time.strptime(ValidOn[0:10],DATE_FORMAT)))
			else:
				ValidOn = None
			Q.ValidOn = ValidOn
			Q.Notes = Notes
			Q.QuoteRequestID = QuoteRequestID
			Q.VendorID = VendorID
			# Update the quote request Items
			CurrItems = [x.id for x in Q.Items]
			if len(ItemCounter) > 1:
				NewItems = [int(x) for x in ItemID]
			elif len(ItemCounter) == 1:
				NewItems = [int(ItemID)]
			else:
				NewItems = []
			if len(ItemCounter) > 1:
				for NewID, Product, Notes, Price, Ranking in zip(ItemID,ItemProduct, ItemNotes,ItemPrice,ItemRanking):
					if int(NewID) in CurrItems: #Update the item
						qitem = model.InvQuoteItems.get(NewID)
						qitem.Product = str(Product)
						qitem.Notes = str(Notes)
						qitem.Price = float(Price)
						qitem.Ranking = int(Ranking)
					else: #We shouldn't have this, becuase we create new POItems in a different place (using AJAX/AJSON)
						pass
			elif len(ItemCounter)==1:
				if int(ItemID) in CurrItems: #Update the item
					qitem = model.InvQuoteItems.get(int(ItemID))
					qitem.Product = str(ItemProduct)
					qitem.Notes = str(ItemNotes)
					if not (ItemPrice in ['', None]):
						qitem.Price = float(ItemPrice)
					if not (ItemRanking in ['', None]):
						qitem.Ranking = int(ItemRanking)
			# Delete any StockItems which have been removed
			mark_delete_count, delete_count = 0,0
			for itemid in CurrItems:
				if not (itemid in NewItems):
					item = model.InvQuoteItems.get(itemid)
					if (datetime.now() - item.Quote.ValidOn).days > 13:
						item.Status = 'deleted'
						mark_delete_count += 1
					else:
						item.destroySelf()
						delete_count += 1
			if mark_delete_count == 0 and  delete_count == 0:
				turbogears.flash('Record updated')
			else:
				turbogears.flash('Record updated (%d items marked deleted and %d items deleted)' % (mark_delete_count, delete_count))
		elif Operation == "Copy to New":# Take the current Quote  and make a new quote that matches it
			Q = model.InvQuote.get(QuoteID)
			NewQ = model.InvQuote(ValidOn=model.cur_date_time(),Notes=Q.Notes,VendorID=Q.VendorID,\
				QuoteRequestID=Q.QuoteRequestID)
			for item in Q.Items:
				NewItem = model.InvQuoteItems(QuoteID=NewQ.id, CatalogItemID=item.CatalogItemID,\
					Price=item.Price,Product=item.Product,Ranking=item.Ranking,Notes=item.Notes)
			QuoteID = NewQ.id
			turbogears.flash('Request copied into new request')
		elif Operation == 'Delete':
			if ((datetime.now().date() - Q.ValidOn).days > 10) or (Q.Status=='deleted'): # prevent deletion of quotes after 10 days in the system
				Q.Status = 'deleted'
				for item in Q.Items: # delete all sub-items
					item.Status = 'deleted'
				turbogears.flash('Recorded marked deleted')
			else:
				#Delete all linked items
				delete_count = 0 # I want to count how many related db records are deleted by this action
				for item in Q.Items:
					delete_count += 1
					item.destroySelf()
				# Now delete the record
				delete_count += 1
				Q.destroySelf()
				log.debug('....%d rows removed in Quotes deletion' % delete_count)
				turbogears.flash('Record deleted (incl. related records, %d rows removed)' % delete_count)
			QuoteID=None
		elif Operation == 'Un-Delete':
			Q.Status = ''
			for item in Q.Items:
				item.Status = ''
			turbogears.flash('Record un-deleted.')
		elif Operation == 'New':
			QuoteID = None
		# Load the QuoteRequest
		if QuoteID != None:
			raise cherrypy.HTTPRedirect('QuotesEditor?QuoteID=%d' % QuoteID)
		else:
			raise cherrypy.HTTPRedirect('QuotesEditor')
			
	@expose(html='turbocare.templates.store_vendorseditor')
	@validate(validators={'VendorID':validators.Int()})
	@identity.require(identity.has_permission("stores_vendor_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")			
	def VendorsEditor(self, VendorID=None, **kw):
		'''	Create/Edit/Delete a Vendor
			Display: purchase orders, quotes, quote requests,
		'''
		log.debug('QuotesEditor')
		latestPOs = [] # latest purchaseorders (for vendor)
		latestQRs = [] # latest quote requests
		latestQs = [] # latest quotes
		groups = [] # Vendor groups
		# Prepare variables for the form
		if VendorID == None: # Initial screen when no item is selected
			# Make a blank entry
			Name = 'NEW VENDOR NAME'
			Description = ''
			ContactName = ''
			Phone1 = ''
			Phone2 = ''
			Fax = ''
			EMail1 = ''
			EMail2 = ''
			AddressLabel = ''
			DeliveryInstructions = ''
			OrderDays = ''
			Status='' # used for showing/hiding the un-delete button
			groups = []
			CityID = ''
			CityName = ''
		else:
			Vendor = model.InvVendor.get(VendorID)
			# Get the regular variables
			Name = Vendor.Name
			Description = Vendor.Description
			ContactName = Vendor.ContactName
			Phone1 = Vendor.Phone1
			Phone2 = Vendor.Phone2
			Fax = Vendor.Fax
			EMail1 = Vendor.EMail1
			EMail2 = Vendor.EMail2
			AddressLabel = Vendor.AddressLabel
			DeliveryInstructions = Vendor.DeliveryInstructions
			OrderDays = Vendor.OrderDays
			Status= Vendor.Status # used for showing/hiding the un-delete button
			# Get catalog groups
			for group in Vendor.Groups:
				groups.append(dict(id=group.id, name=group.Name))			
			CityID = Vendor.CityID
			if CityID != None:
				CityName = Vendor.City.MultiLineName(html=False)
			else:
				CityName = ''
			# Generate a list of Purchase orders
			POs = model.InvPurchaseOrder.select(model.InvPurchaseOrder.q.VendorID==VendorID,orderBy=\
				[-model.InvPurchaseOrder.q.POSentOnDate])
			for po in POs[0:model.LATEST_POS]:
				latestPOs.append(dict(id=po.id, name=po.Name()))
			# Generate a list of Quote requests (trickier to implement this because of the related join)
			QRs = [(x.RequestDate, x.id, x.Name()) for x in Vendor.QuoteRequests]
			QRs.sort()
			QRs.reverse()
			latestQRs = [dict(id=x[1],name=x[2]) for x in QRs[0:model.LATEST_QRS]]
			# Generate a list of Quotes
			Qs = model.InvQuote.select(model.InvQuote.q.VendorID==VendorID,orderBy=[-model.InvQuote.q.ValidOn])
			for q in Qs[0:model.LATEST_QS]:
				latestQs.append(dict(id=q.id,name=q.Name()))
		return dict(latestPOs=latestPOs, latestQRs=latestQRs, latestQs=latestQs,Name=Name, VendorID=VendorID, \
			Description=Description, ContactName=ContactName, Phone1=Phone1, Phone2=Phone2, Fax=Fax, \
			EMail1=EMail1, EMail2=EMail2, AddressLabel=AddressLabel, OrderDays=OrderDays, Status=Status,\
			groups=groups, CityID=CityID, CityName=CityName, DeliveryInstructions=DeliveryInstructions)

	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_vendor_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")			
	def VendorsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Find Vendors
		'''
		vendors = model.InvVendor.select(AND (model.InvVendor.q.Name.contains(str(QuickSearchText)),\
			model.InvVendor.q.Status!='deleted'),orderBy=[model.InvVendor.q.Sort])
		results = []
		for item in vendors:
			results.append(dict(id=item.id, text=item.Name))
		return dict(results=results)

	@expose(format='json')
	@identity.require(identity.has_permission("stores_vendor_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")			
	def VendorsEditorCitySelect(self, SearchText='', **kw):
		'''	Load the City Options
		'''
		SearchText = str(SearchText)
		items = model.InvAddressCitytown.select(model.InvAddressCitytown.q.Name.contains(SearchText),
			orderBy=[model.InvAddressCitytown.q.Name])
		results = []
		for item in items:
			if item.Status != 'deleted':
				results.append(dict(id=item.id, text=item.MultiLineName()))
		return dict(results=results, function_name='VendorsEditorCitySelect')

	@expose(format='json')
	@identity.require(identity.has_permission("stores_vendor_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	@validate(validators={'VendorID':validators.Int()})
	def VendorsEditorVendorSelect(self, VendorID=None, **kw):
		'''	Load the Vendor's Group selection
			Mark items which are already selected as selected
		'''
		cur_groups = []
		if VendorID!=None:
			vendor = model.InvVendor.get(VendorID)
			for group in vendor.Groups:
				cur_groups.append(group.id)
		groups = model.InvGrpVendor.select(orderBy=[model.InvGrpVendor.q.Name])
		results = []
		for group in groups:
			results.append(dict(id=group.id, text=group.Name, selected=(group.id in cur_groups)))
		return dict(results=results)

	@expose()
	@validate(validators={'VendorID':validators.Int(),'CityID':validators.Int(),'Name':validators.String(),\
	'Description':validators.String(),'ContactName':validators.String(),'Phone1':validators.String(),'Phone2':validators.String(),\
	'Fax':validators.String(),'EMail1':validators.String(),'EMail2':validators.String(),'AddressLabel':validators.String(),\
	'OrderDays':validators.Number(),'Operation':validators.String(),'DeliveryInstructions':validators.String()})
	@identity.require(identity.has_permission("stores_vendor_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def VendorsSave(self, VendorID=None, CityID=None, Name='', Description='',ContactName='',Phone1='',\
		Phone2='',Fax='',EMail1='',EMail2='',AddressLabel='',OrderDays=None, Operation='', Groups=[], \
		GroupsCounter=[], DeliveryInstructions=None, **kw):
		'''	Delete or update (modify) an existing Vendor
		'''
		log.debug('VendorsSave')
		# Get our operation
		log.debug('....Operation: %s' % Operation)
		if Operation == 'Save' and VendorID != None: # Update a record
			Vendor = model.InvVendor.get(VendorID)
			Vendor.Name = str(Name)
			Vendor.Description = str(Description)
			Vendor.ContactName = str(ContactName)
			Vendor.Phone1 = str(Phone1)
			Vendor.Phone2 = str(Phone2)
			Vendor.Fax = str(Fax)
			Vendor.EMail1 =str(EMail1)
			Vendor.EMail2 = str(EMail2)
			Vendor.AddressLabel = str(AddressLabel)
			Vendor.DeliveryInstructions = str(DeliveryInstructions)
			Vendor.OrderDays = OrderDays
			Vendor.CityID = CityID
			# Update Groups information
			# convert our group list to an integer list
			if len(GroupsCounter) > 1:
				Groups = [int(x) for x in Groups]
			elif len(GroupsCounter) == 1:
				Groups = [int(Groups)]
			else:
				Groups = []
			# remove groups
			for group in Vendor.Groups:
				if not (group.id in Groups):
					Vendor.removeInvGrpVendor(group)
			# Add any groups which we don't already have
			current_groups = [x.id for x in Vendor.Groups]
			for groupid in Groups:
				if not (groupid in current_groups):
					Vendor.addInvGrpVendor(groupid)
			turbogears.flash('Record updated')
		elif Operation == "Save" and VendorID==None: # Create a new record
			Vendor = model.InvVendor(Name=Name,Description=Description,ContactName=ContactName,Phone1=Phone1,\
				Phone2=Phone2,Fax=Fax,EMail1=EMail1,EMail2=EMail2,AddressLabel=AddressLabel,\
				OrderDays=OrderDays,CityID=CityID,DeliveryInstructions=DeliveryInstructions)
			if len(GroupsCounter) > 1:
				Groups = [int(x) for x in Groups]
			elif len(GroupsCounter) == 1:
				Groups = [int(Groups)]
			else:
				Groups = []
			for groupid in Groups:
				Vendor.addInvGrpVendor(groupid)			
			VendorID = Vendor.id
			turbogears.flash('New record created')
		elif Operation == 'Delete':
			Vendor = model.InvVendor.get(VendorID)
			if not Vendor.SafeToDelete(): # prevent deletion of quotes after 10 days in the system
				Vendor.Status = 'deleted'
				turbogears.flash('Recorded marked deleted')
			else:
				# Remove related groups
				delete_count = 0 # I want to count how many related db records are deleted by this action
				for group in Vendor.Groups:
					Vendor.removeInvGrpVendor(group)
				# I could run through all the MultiJoin and RelatedJoin columns and delete, but they should be empty anyway
				# Now delete the record
				delete_count += 1
				Vendor.destroySelf()
				turbogears.flash('%d Record deleted' % delete_count)
			VendorID=None
		elif Operation == 'Un-Delete':
			Vendor = model.InvVendor.get(VendorID)
			Vendor.Status = ''
			turbogears.flash('Record un-deleted.')
		elif Operation == 'New':
			VendorID = None
		# Load the QuoteRequest
		if VendorID != None:
			raise cherrypy.HTTPRedirect('VendorsEditor?VendorID=%d' % VendorID)
		else:
			raise cherrypy.HTTPRedirect('VendorsEditor')

	@expose(html='turbocare.templates.store_stockitemseditor')
	@validate(validators={'StockItemID':validators.Int()})
	@identity.require(identity.has_permission("stores_stock_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def StockItemsEditor(self, StockItemID=None, **kw):
		'''	Create/Edit/Delete a StockItem
			Display: pending StockTransfer/Requests and POs
		'''
		log.debug('StockItemsEditor')
		pendingSTTs = [] # Stock Transfers To Here
		pendingSTFs = [] # Stock Transfers From Here
		pendingSTRs = [] # Stock transfer requests
		pendingPOs = [] # Purchase orders
		# Prepare variables for the form
		if StockItemID == None: # Initial screen when no item is selected
			# Make a blank entry
			DisplayName = 'CREATE A NEW ENTRY'
			Name = ''
			CatalogItemID = ''
			CatalogItemName = ''
			PurchaseOrderID = ''
			PurchaseOrderName = ''
			MRP = ''
			SalePrice = ''
			PurchasePrice = ''
			Quantity = ''
			BatchNumber = ''
			ExpireDate = ''
			CompoundDateProduced = ''
			compoundqtys = []
			items = []
			Status='' # used for showing/hiding the un-delete button
		else:
			SI = model.InvStockItem.get(StockItemID)
			DisplayName = SI.DisplayName()
			Name = SI.Name
			CatalogItemID = SI.CatalogItemID
			if CatalogItemID!=None:
				CatalogItemName = SI.CatalogItem.Name
			else:
				CatalogItemName = ''
			if SI.PurchaseOrderID==None:
				PurchaseOrderID=None
			else:
				PurchaseOrderID = SI.PurchaseOrder.PurchaseOrderID #It is linked to the Goods Received entry which is linked to the PO
			if PurchaseOrderID!=None:
				PurchaseOrderName = SI.PurchaseOrder.Name()
			else:
				PurchaseOrderName = ''
			MRP = SI.MRP
			SalePrice = SI.SalePrice
			PurchasePrice = SI.PurchasePrice
			Quantity = SI.Quantity
			BatchNumber = SI.BatchNumber
			if SI.ExpireDate == None:
				ExpireDate = ''
			else:
				ExpireDate = SI.ExpireDate.strftime(model.DATE_FORMAT)
			if SI.CompoundDateProduced==None:
				CompoundDateProduced = ''
			else:
				CompoundDateProduced = SI.CompoundDateProduced.strftime(model.DATE_FORMAT)
			compoundqtys = []
			for cmpnd in SI.CompoundQtys:
				compoundqtys.append(cmpnd.Name())
			Status = SI.Status
			items = [(x.Sort, x.id, x.Location.Name, x.QtyAvailable(),x.Description(),x.IsConsumed,x.LocationID==int(self.LocationID))\
				for x in SI.Locations]
			items.sort()
			items = [dict(ItemID=x[1],ItemLocation=x[2],ItemQuantity=x[3],ItemDescription=x[4],ItemIsConsumed=x[5],\
					ItemCanTransfer=x[6]) for x in items]
			# Quick links setup
			LocationID = int(self.LocationID)
			CatalogItemID = SI.CatalogItemID
			# Pending Stock Transfers To Here
			stth = model.InvStockTransfer.select(AND (model.InvStockItem.q.CatalogItemID==CatalogItemID,\
				model.InvStockLocation.q.StockItemID==model.InvStockItem.q.id,\
				model.InvStockTransfer.q.ToStockLocationID==model.InvStockLocation.q.id,\
				model.InvStockLocation.q.LocationID==LocationID,model.InvStockTransfer.q.IsComplete==False),\
				orderBy=[model.InvStockTransfer.q.CreateTime])
			for item in stth:
				pendingSTTs.append(dict(id=item.id, name=item.Name()))
			# Pending Stock Transfers From Here
			stfh = model.InvStockTransfer.select(AND (model.InvStockItem.q.CatalogItemID==CatalogItemID,\
				model.InvStockLocation.q.StockItemID==model.InvStockItem.q.id,\
				model.InvStockTransfer.q.FromStockLocationID==model.InvStockLocation.q.id,\
				model.InvStockLocation.q.LocationID==LocationID,model.InvStockTransfer.q.IsComplete==False),\
				orderBy=[model.InvStockTransfer.q.CreateTime])
			for item in stfh:
				pendingSTFs.append(dict(id=item.id, name=item.Name()))
			# Pending Stock Transfer requests
			strs = model.InvStockTransferRequestItem.select(AND (model.InvStockTransferRequestItem.q.IsTransferred==False,\
				model.InvStockTransferRequestItem.q.CatalogItemID==CatalogItemID,\
				model.InvStockTransferRequestItem.q.StockTransferRequestID==model.InvStockTransferRequest.q.id),\
				orderBy=[model.InvStockTransferRequest.q.RequiredBy])
			for item in strs:
				pendingSTRs.append(dict(id=item.StockTransferRequestID,name=item.Name()))
			# Pending Purchase Orders
			ppos = model.InvPOItems.select(AND (model.InvPOItems.q.CatalogItemID==CatalogItemID,
				model.InvPOItems.q.QuantityRequested>0.0,model.InvPOItems.q.QuantityRequested >\
				model.InvPOItems.q.QuantityReceived,model.InvPOItems.q.PurchaseOrderID==\
				model.InvPurchaseOrder.q.id), orderBy=[model.InvPurchaseOrder.q.POSentOnDate])
			for item in ppos:
				pendingPOs.append(dict(id=item.PurchaseOrderID,name=item.Name()))
		return dict(pendingSTTs=pendingSTTs, pendingSTFs=pendingSTFs, pendingSTRs=pendingSTRs, pendingPOs=\
			pendingPOs, DisplayName=DisplayName, Name=Name, CatalogItemID=CatalogItemID, CatalogItemName=\
			CatalogItemName, PurchaseOrderID=PurchaseOrderID, PurchaseOrderName=PurchaseOrderName, MRP=MRP,\
			SalePrice=SalePrice, PurchasePrice=PurchasePrice, Quantity=Quantity, BatchNumber=BatchNumber, \
			ExpireDate=ExpireDate, CompoundDateProduced=CompoundDateProduced, compoundqtys=compoundqtys, \
			items=items, Status=Status, StockItemID=StockItemID)
	
	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_stock_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")					
	def StockItemsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Find stock items
		'''
		items = model.InvStockItem.select(OR (AND (model.InvStockItem.q.Name.contains(str(QuickSearchText)),\
			model.InvStockItem.q.Status!='deleted'),AND (model.InvCatalogItem.q.Name.contains(str(QuickSearchText)),\
			model.InvStockItem.q.CatalogItemID==model.InvCatalogItem.q.id)),orderBy=[model.InvStockItem.q.Sort],\
			distinct=True)
		results = []
		for item in items:
			results.append(dict(id=item.id, text=item.DisplayName()))
		return dict(results=results)
	
	@expose(format='json')
	@identity.require(identity.has_permission("stores_stock_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")					
	def StockItemsEditorCatalogItemSelect(self, SearchText='', **kw):
		'''	Load the City Options
		'''
		SearchText = str(SearchText)
		if SearchText=='':
			items = []
		else:
			items = model.InvCatalogItem.select(AND (model.InvCatalogItem.q.Name.contains(SearchText),\
				model.InvCatalogItem.q.Status!='deleted',model.InvCatalogItem.q.IsSelectable==True),
				orderBy=[model.InvCatalogItem.q.Name])
		results = []
		for item in items:
				results.append(dict(id=item.id, text=item.Name, linkurl="CatalogItemsEditor?CatalogItemID=%d" % item.id))
		return dict(results=results, function_name='StockItemsEditorCatalogItemSelect')

	@expose()
	@validate(validators={'StockItemID':validators.Int(),'CatalogItemID':validators.Int(),'Name':validators.String(),\
	'MRP':validators.Number(),'SalePrice':validators.Number(),'PurchasePrice':validators.Number(),\
	'Quantity':validators.Number(),'BatchNumber':validators.String(),'ExpireDate':validators.String(),\
	'CompoundDateProduced':validators.String(),'Operation':validators.String()})
	
	@identity.require(identity.has_permission("stores_stock_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def StockItemsSave(self, Name='', CatalogItemID=None, MRP=None, SalePrice=None, PurchasePrice=None, \
		Quantity=None, BatchNumber='', ExpireDate=None, CompoundDateProduced=None, \
		StockItemID=None, Operation='', ItemID=[], ItemCounter=[], **kw):
		'''	Delete or update (modify) a Stock Item
		'''
		log.debug('StockItemsSave')
		# Get our operation
		log.debug('....Operation: %s' % Operation)
		if Operation == 'Save' and StockItemID != None: # Update a record
			SI = model.InvStockItem.get(StockItemID)
			SI.Name = Name
			SI.CatalogItemID = CatalogItemID
			SI.MRP = MRP
			SI.SalePrice = SalePrice
			SI.PurchasePrice = PurchasePrice
			SI.BatchNumber = BatchNumber
			SI.CompoundDateProduced = None
			if ExpireDate != None and ExpireDate != '':
				ExpireDate = datetime.fromtimestamp(time.mktime(time.strptime(ExpireDate[0:10],DATE_FORMAT)))
			else:
				ExpireDate = None
			SI.ExpireDate = ExpireDate
			# Changing the Quantity creates a problem for managing the stock.  The program will find the first non-
			# consumed stock location which matches the current module location and modify the stock locations
			# stock amount at the same time the stock amount is changed.  If there is no local stock location with
			# that amount, then the change is refused.
			QtyMsg = ''
			if SI.Quantity != Quantity:
				DiffQuantity = Quantity - SI.Quantity
				log.debug('.... Quantity change of %d' % DiffQuantity)
				# find the first local stock location which is not consumed or sold
				SLs = model.InvStockLocation.select(AND (model.InvStockLocation.q.IsSold==False,\
					model.InvStockLocation.q.IsConsumed==False, model.InvStockLocation.q.Status!='deleted',\
					model.InvStockLocation.q.LocationID==int(self.LocationID),model.InvStockLocation.q.StockItemID==StockItemID))
				SL = None
				if SLs.count() > 0:
					log.debug('....Stock locations found')
					for location in SLs:
						if location.QtyAvailable() >= -DiffQuantity:
							log.debug('....Suitable location found')
							SL = model.InvStockLocation.get(location.id)
							break
				if SL!=None: # We found a useable record to update, so we can procede
					SL.Quantity += DiffQuantity
					SI.Quantity = Quantity
					QtyMsg = ''
				else: # No useable record found, so don't update the quantity
					log.debug('....No suitable location found')
					QtyMsg = ' Cannot modify stock quantity, not enough stock at this location'
			# Deleting Items is tricky and can only occur when the item is not consumed or sold and has no transfers
			# from the location to another.  If it can be deleted, then all transfers to the location are undone!  You are
			# allowed to delete stock locations at your location
			# Get a list of linked item ids first
			CurrItems = [x.id for x in SI.Locations]
			if len(ItemCounter) > 1:
				NewItems = [int(x) for x in ItemID]
			elif len(ItemCounter) == 1:
				NewItems = [int(ItemID)]
			else:
				NewItems = []
			# Delete any StockLocations which have been removed 
			delete_count = 0
			delete_try = len(CurrItems) - len(NewItems)
			delete_msg = ''
			for itemid in CurrItems:
				if (not (itemid in NewItems)):
					stocklocation = model.InvStockLocation.get(itemid)
					if stocklocation.LocationID == int(self.LocationID):
						result, Msg = utils.DeleteStockLocation(itemid)
						delete_msg += ' (%s)' % Msg
						if result:
							delete_count += 1
					else:
						delete_msg += ' (Cannot delete this item (ID:%d) from %s)' % (itemid, self.LocationName)
			if delete_try != 0:
				Delete = ' %d records were marked to be deleted and %d records were actually deleted with the following messages: %s' % (delete_try, delete_count, delete_msg)
			else:
				Delete = delete_msg
			turbogears.flash('Record updated%s%s' % (QtyMsg,Delete))
		elif Operation == "Save" and StockItemID==None: # Create a new record
			if ExpireDate != None and ExpireDate != '':
				ExpireDate = datetime.fromtimestamp(time.mktime(time.strptime(ExpireDate[0:10],DATE_FORMAT)))
			else:
				ExpireDate = None
			SI = model.InvStockItem(Name=Name, CatalogItemID=CatalogItemID,MRP=MRP,SalePrice=SalePrice,\
				PurchasePrice=PurchasePrice,BatchNumber=BatchNumber,ExpireDate=ExpireDate,Quantity=Quantity,\
				CompoundDateProduced=None)
			# Create a new stock location entry for the stock item
			SL = model.InvStockLocation(StockItemID=SI.id,LocationID=int(self.LocationID),Quantity=Quantity)
			StockItemID = SI.id
			turbogears.flash('New record created')
		elif Operation == 'Delete':
			SI = model.InvStockItem.get(StockItemID)
			if SI.SafeToDelete(): # prevent deletion of quotes after 10 days in the system
				delete_count = 0 # I want to count how many related db records are deleted by this action
				# remove any compoundQtys entries
				for item in SI.CompoundQtys:
					item.destroySelf()
					delete_count += 1
				# remove stock locations
				for item in SI.Locations:
					item.destroySelf()
					delete_count += 1
				# Now delete the record
				delete_count += 1
				SI.destroySelf()
				turbogears.flash('%d Record(s) deleted' % delete_count)
			StockItemID=None
		elif Operation == 'Un-Delete':
			SI = model.InvStockItem.get(StockItemID)
			SI.Status = ''
			turbogears.flash('Record un-deleted.')
		elif Operation == 'New':
			StockItemID = None
		# Load the QuoteRequest
		if StockItemID != None:
			raise cherrypy.HTTPRedirect('StockItemsEditor?StockItemID=%d' % StockItemID)
		else:
			raise cherrypy.HTTPRedirect('StockItemsEditor')

	@expose(html='turbocare.templates.store_stocktransferrequestseditor')
	@validate(validators={'StockTransferRequestID':validators.Int()})
	@identity.require(identity.has_permission("stores_stocktransferrequest_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def StockTransferRequestsEditor(self, StockTransferRequestID=None, **kw):
		'''	Create/Edit/Delete a StockItem
			Display: pending StockTransfer/Requests and POs
		'''
		def Checked(value):
			if value:
				return "checked"
			else:
				return None
		log.debug('StockTransferRequestsEditor')
		pendingSTRs = [] # unfinished Stock Transfers Requests which we can help fill
		pendingSTRForUs = [] # unfinished Stock Transfers For Us
		pendingSTRFromUs = [] # unfinished Stock transfers From us
		pendingPOs = [] # Purchase orders for unfinished stock request items for us
		latestSTRs = [] # Latest stock transfer requests made by the current user
		# Prepare variables for the form
		if StockTransferRequestID == None: # Initial screen when no item is selected
			# Make a blank entry
			Name = 'CREATE A NEW STOCK TRANSFER REQUEST'
			RequestedBy = model.cur_user_name()
			RequestedOn = model.cur_date_time().strftime(DATE_FORMAT)
			RequiredBy = model.cur_date_time().strftime(DATE_FORMAT)
			ForLocation = self.LocationName
			Notes = ''
			Status = ''
			items = []
		else:
			STR = model.InvStockTransferRequest.get(StockTransferRequestID)
			Name = STR.Name()
			RequestedBy = STR.RequestedBy
			RequestedOn = STR.RequestedOn.strftime(DATE_FORMAT)
			RequiredBy = STR.RequiredBy.strftime(DATE_FORMAT)
			ForLocation = STR.ForLocation.Name
			Notes = STR.Notes
			Status = STR.Status
			items = []
			for item in STR.Items:
				# Check if we can fill the item (for stock requests not coming from us
				if STR.ForLocationID!=int(self.LocationID) and (not item.IsTransferred):
					# Check to see if we have enough stock
					currstock = model.InvStockLocation.select(AND (model.InvStockItem.q.CatalogItemID==item.CatalogItemID,\
					model.InvStockItem.q.id==model.InvStockLocation.q.StockItemID, model.InvStockLocation.q.LocationID==\
					int(self.LocationID), model.InvStockLocation.q.IsConsumed==False, model.InvStockLocation.q.IsSold==\
					False, model.InvStockLocation.q.Quantity>0))
					for stock in currstock:
						if stock.QtyAvailable() > 0:
							CanFill = True
							break
					else:
						CanFill = False
				else:
					CanFill = False
				items.append(dict(ItemName=item.Name(),ItemID=item.id,ItemQty=item.Qty,ItemPurchaseOrderID=\
				item.PurchaseOrderID,ItemNotes=item.Notes,ItemIsOnOrder=item.IsOnOrder,ItemIsTransferred=\
				item.IsTransferred,ItemCanFillRequest=CanFill))
		# Quick links setup
		# unfinished Stock Transfers Requests which we can help fill
		# Find requests for items which we have
		stritems = model.InvStockTransferRequestItem.select(AND (model.InvStockTransferRequestItem.q.CatalogItemID==\
			model.InvStockItem.q.CatalogItemID, model.InvStockItem.q.id==model.InvStockLocation.q.StockItemID,\
			model.InvStockLocation.q.LocationID==int(self.LocationID), model.InvStockLocation.q.IsConsumed==False,\
			model.InvStockLocation.q.IsSold==False, model.InvStockLocation.q.Quantity>0,\
			model.InvStockTransferRequestItem.q.IsTransferred==False,\
			model.InvStockTransferRequestItem.q.StockTransferRequestID==model.InvStockTransferRequest.q.id,\
			model.InvStockTransferRequest.q.ForLocationID!=int(self.LocationID),
			model.InvStockTransferRequest.q.Status!='deleted',model.InvStockTransferRequestItem.q.Status!='deleted'),
			orderBy=[model.InvStockTransferRequest.q.RequiredBy])
		# We still need to check the QtyAvailable for each item before displaying
		log.debug('....Stock requests for us: %d' % stritems.count())
		for item in stritems:
			instockitems = model.InvStockLocation.select(AND (model.InvStockItem.q.CatalogItemID==item.CatalogItemID,\
			model.InvStockItem.q.id==model.InvStockLocation.q.StockItemID,model.InvStockLocation.q.IsConsumed==False,\
			model.InvStockLocation.q.IsSold==False,model.InvStockLocation.q.Status!='deleted',\
			model.InvStockLocation.q.LocationID==int(self.LocationID),\
			model.InvStockLocation.q.Quantity>0))
			if instockitems.count() > 0:
				for stock in instockitems:
					if stock.QtyAvailable() > 0:
						pendingSTRs.append(dict(id=item.StockTransferRequestID, name=item.Name()))
		# unfinished Stock Transfers For Us
		stsforus = model.InvStockTransfer.select(AND (model.InvStockTransfer.q.IsComplete==False,\
			model.InvStockTransfer.q.ToStockLocationID==model.InvStockLocation.q.id,model.InvStockLocation.q.LocationID==\
			int(self.LocationID)),orderBy=[model.InvStockTransfer.q.CreateTime])
		for item in stsforus:
			pendingSTRForUs.append(dict(id=item.id, name=item.Name()))
		# unfinished Stock transfers From us NOTE: this does not include items which are sold
		stsfromus = model.InvStockTransfer.select(AND (model.InvStockTransfer.q.IsComplete==False,\
			model.InvStockTransfer.q.FromStockLocationID==model.InvStockLocation.q.id,model.InvStockLocation.q.LocationID==\
			int(self.LocationID)),orderBy=[model.InvStockTransfer.q.CreateTime])
		for item in stsfromus:
			# Do not include items which are sold!
			if item.ToStockLocation.Location.IsConsumed==False:
				pendingSTRFromUs.append(dict(id=item.id,name=item.Name()))
		# Purchase orders for unfinished stock request items for us
		stritems = model.InvStockTransferRequestItem.select(AND (model.InvStockTransferRequest.q.ForLocationID==\
			int(self.LocationID), model.InvStockTransferRequest.q.id==model.InvStockTransferRequestItem.q.StockTransferRequestID,\
			model.InvStockTransferRequestItem.q.IsTransferred==False, model.InvStockTransferRequestItem.q.PurchaseOrderID!=\
			None,model.InvStockTransferRequestItem.q.IsOnOrder==True),orderBy=[model.InvStockTransferRequest.q.RequiredBy])
		for item in stritems:
			pendingPOs.append(dict(id=item.PurchaseOrderID,name=item.Name()))
		# The latest StockTransferRequests from the person
		lateststritems = model.InvStockTransferRequest.select(model.InvStockTransferRequest.q.RequestedBy==\
			str(model.cur_user_name()),orderBy=[model.InvStockTransferRequest.q.RequiredBy])
		if lateststritems.count() > 0:
			for item in lateststritems[0:model.LATEST_STRS]:
				latestSTRs.append(dict(id=item.id,name=item.Name()))
		return dict(pendingSTRs=pendingSTRs, pendingSTRForUs=pendingSTRForUs, pendingSTRFromUs=pendingSTRFromUs,\
			pendingPOs=pendingPOs, Name=Name, RequestedBy=RequestedBy, RequestedOn=RequestedOn, RequiredBy=\
			RequiredBy, ForLocation=ForLocation, Notes=Notes,Status=Status, items=items, latestSTRs=latestSTRs,\
			StockTransferRequestID=StockTransferRequestID)
			
	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_stocktransferrequest_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def StockTransferRequestsEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Find stock items
		'''
		items = model.InvStockTransferRequestItem.select(AND (model.InvCatalogItem.q.Name.contains(str(QuickSearchText)),\
			model.InvCatalogItem.q.id==model.InvStockTransferRequestItem.q.CatalogItemID,\
			model.InvStockTransferRequest.q.id==model.InvStockTransferRequestItem.q.StockTransferRequestID),
			orderBy=[-model.InvStockTransferRequest.q.RequiredBy])
		results = []
		for item in items:
			results.append(dict(id=item.StockTransferRequestID, text=item.Name()))
		return dict(results=results)

	@expose(format='json')
	@validate(validators={'StockTransferRequestID':validators.Int()})
	@identity.require(identity.has_permission("stores_stocktransferrequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def StockTransferRequestsEditorAddItemsStep1(self, StockTransferRequestID, **kw):
		'''	This generates the form fields that we use in the JavaScript file PickList.js "pick" object
			The form is used to add catalog items to the quote request
		'''
		id='PickList' #Used in the javascript code to identify the PickList
		# Search fields
		Name = dict(id="pl_Name", name="Name", label="Item master name", type="String", attr=dict(length=25), data='')
		# Select box data
		InvGrpStockNames = [x.Name for x in model.InvGrpStock.select(orderBy=[model.InvGrpStock.q.Name])]
		SrchCatalogGroups = dict(id="pl_SrchCatalogGroups", name="Groups", label="Groups", type="MultiSelect", attr=dict(Groups=InvGrpStockNames), data='')
		return dict(id=id, Name='AddItems', Label='Select items from the item master',\
			FieldsSrch=[Name, SrchCatalogGroups], Inputs=[], SrchUrl='StockTransferRequestsEditorAddItemsStep2', \
			DataUrl='', Url='StockTransferRequestsEditorAddItemsStep3', UrlVars='StockTransferRequestID=%d' % StockTransferRequestID, result_msg='ok', \
			SrchNow=False, NoAjax=False, JsonFunction='store.RenderAddItems')

	@validate(validators={'GoodsReceivedID':validators.Int()})
	@expose(format='json')
	@identity.require(identity.has_permission("stores_stocktransferrequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")					
	def StockTransferRequestsEditorAddItemsStep2(self, Name='', Groups='', **kw):
		'''	Search for CatalogItems and return the results to the PickList
		'''
		qArgs = ""
		if Name != '':
			qArgs+="model.InvCatalogItem.q.Name.contains('"+ Name + "'),"
		qArgs+="model.InvCatalogItem.q.IsSelectable == True,"
		qArgs+="model.InvCatalogItem.q.Status != 'deleted',"
		if Groups != '':
			Groups = set(Groups.split(","))
			orArgs = ''
			for group in Groups:
				orArgs+="model.InvGrpStock.q.Name == '"+group+"',"
			qArgs+= "OR ("+orArgs[0:len(orArgs)-1]+"),"
			qArgs+="model.InvGrpStock.q.id == model.InvViewJoinCatalogItemGrpStock.q.GrpStockId,"
			qArgs+="model.InvCatalogItem.q.id == model.InvViewJoinCatalogItemGrpStock.q.CatalogItemId,"
		if len(qArgs) > 0:
			items = eval('model.InvCatalogItem.select(AND ('+qArgs[0:len(qArgs)-1]+'),orderBy=[model.InvCatalogItem.q.Name])')
		else:
			items = model.InvCatalogItem.select(orderBy=[model.InvCatalogItem.q.Name])
		results = []
		for item in items:
			results.append({'id':item.id, 'text':item.Name, 'Name':item.Name, 'Description':item.Description})
		return dict(results=results, items=items)
	
	@expose(format='json')
	@validate(validators={'StockTransferRequestID':validators.Int()})
	@identity.require(identity.has_permission("stores_stocktransferrequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def StockTransferRequestsEditorAddItemsStep3(self, StockTransferRequestID, data='', **kw):
		'''	Save the selected items to the stock transfer request
			If a new item is added but it is already on the STR, then ignore it
			If a new item is added and it matches a "marked deleted" item, then un-delete the item and re-display
		'''
		def Checked(value):
			if value:
				return "checked"
			else:
				return None
		# Convert our string to a data structure
		data = simplejson.loads(data)
		# Load the Stock Transfer Request
		STR = model.InvStockTransferRequest.get(StockTransferRequestID)
		# Make a list of CatalogItems and deleted items, that is, items where the Status == 'deleted'
		DeletedItems = {}
		CatalogItems = []
		for item in STR.Items:
			if item.Status == 'deleted':
				DeletedItems[item.CatalogItemID] = item.id
			CatalogItems.append(item.CatalogItemID)
		# Go through all the new items: For existing items, ignore, for new items, add it to the STR,
		#	grabbing defaults and then presenting the data back to the screen in json format
		results = []
		for NewItem in data:
			if not (int(NewItem['id']) in CatalogItems):
				# Check for annual consumption and use that value as the quantity
				catalogitem = model.InvCatalogItem.get(int(NewItem['id']))
				FromDate = datetime.now() - timedelta(days=10)
				Quantity = catalogitem.Consumption(FromDate)
				# Add the item to the STR
				Item = model.InvStockTransferRequestItem(StockTransferRequestID=StockTransferRequestID, CatalogItemID=\
					catalogitem.id, Qty=Quantity)
				results.append(dict(ItemName=Item.Name(),ItemID=Item.id,ItemQty=Item.Qty,ItemPurchaseOrderID=\
					Item.PurchaseOrderID,ItemNotes=Item.Notes,ItemIsOnOrder=Checked(Item.IsOnOrder),ItemIsTransferred=\
					Checked(Item.IsTransferred),ItemCanFillRequest=False))
			elif (int(NewItem['id']) in CatalogItems) and DeletedItems.has_key(int(NewItem['id'])):
				# Un-delete the item and set to display
				Item = model.InvStockTransferRequestItem.get(DeletedItems[int(NewItem['id'])])
				Item.Status = ''
				results.append(dict(ItemName=Item.Name(),ItemID=Item.id,ItemQty=Item.Qty,ItemPurchaseOrderID=\
					Item.PurchaseOrderID,ItemNotes=Item.Notes,ItemIsOnOrder=Item.IsOnOrder,ItemIsTransferred=\
					Item.IsTransferred,ItemCanFillRequest=False))
		return dict(results=results)

	@expose()
	@validate(validators={'StockTransferRequestID':validators.Int(),'RequestedBy':validators.String(),\
	'RequiredBy':validators.String(),'Notes':validators.String(),'Operation':validators.String()})
	@identity.require(identity.has_permission("stores_stocktransferrequest_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def StockTransferRequestsSave(self, StockTransferRequestID=None, RequestedBy='', RequiredBy='', Notes='', \
		Operation='', ItemID=[], ItemQty=[], ItemPurchaseOrderID=[], ItemNotes=[], ItemCounter=[], ItemIsOnOrder=[],\
		ItemIsTransferred=[], **kw):
		'''	Delete or update (modify) a Stock Transfer Request
		'''
		log.debug('StockTransferRequestsSave')
		# Get our operation
		log.debug('....Operation: %s' % Operation)
		# Perform some validation on the date fields
		if RequiredBy != None and RequiredBy != '':
			RequiredBy = datetime.fromtimestamp(time.mktime(time.strptime(RequiredBy[0:10],DATE_FORMAT)))
		else:
			RequiredBy = None
		if Operation == 'Save' and StockTransferRequestID != None: # Update a record
			STR = model.InvStockTransferRequest.get(StockTransferRequestID)
			if STR.ForLocationID==int(self.LocationID): # Prevent the editing of requests for other locations
				STR.RequestedBy = RequestedBy
				STR.RequiredBy = RequiredBy
				STR.Notes = Notes
				# Update the items
				CurrItems = [x.id for x in STR.Items]
				if len(ItemCounter) > 1:
					NewItems = [int(x) for x in ItemID]
				elif len(ItemCounter) == 1:
					NewItems = [int(ItemID)]
				else:
					NewItems = []
				# Update any items
				if len(ItemCounter) > 1:
					log.debug('....%d items to update' % len(ItemCounter))
					log.debug(ItemID)
					log.debug(ItemQty)
					log.debug(ItemPurchaseOrderID)
					log.debug(ItemNotes)
					log.debug(ItemIsOnOrder)
					log.debug(ItemIsTransferred)
					for itemid, qty, poid, notes, isonorder, istransferred in zip(ItemID,ItemQty, ItemPurchaseOrderID, ItemNotes, \
						ItemIsOnOrder, ItemIsTransferred):
						STRitem = model.InvStockTransferRequestItem.get(int(itemid))
						STRitem.Qty = float(qty)
						if poid != '':
							try:
								STRitem.PurchaseOrderID = int(poid)
							except:
								STRitem.PurchaseOrderID = None
						else:
							STRitem.PurchaseOrderID = None
						STRitem.Notes = str(notes)
						STRitem.IsOnOrder = (str(isonorder) == 'True')
						STRitem.IsTransferred = (str(istransferred) == 'True')
				elif len(ItemCounter) == 1:
					STRitem = model.InvStockTransferRequestItem.get(int(ItemID))
					STRitem.Qty = float(ItemQty)
					if ItemPurchaseOrderID in ['',None]:
						STRitem.PurchaseOrderID = None
					else:
						STRitem.PurchaseOrderID = int(ItemPurchaseOrderID)
					STRitem.Notes = str(ItemNotes)
					STRitem.IsOnOrder = (str(ItemIsOnOrder) == 'True')
					STRitem.IsTransferred = (str(ItemIsTransferred) == 'True')
				# Delete any Items which have been removed 
				delete_count = 0
				delete_try = len(CurrItems) - len(NewItems)
				delete_msg = ''
				for itemid in CurrItems: # Go through all of our current items
					if (not (itemid in NewItems)): # If any of our current items aren't in the update list, then delete
						if STR.ForLocationID == int(self.LocationID):
							STRitem = model.InvStockTransferRequestItem.get(itemid)
							if STRitem.IsTransferred==False and len(STRitem.StockTransfers)==0:
								STRitem.destroySelf()
								delete_msg += ' (Item (ID:%d) deleted)' % itemid
								delete_count += 1
							else:
								delete_msg += ' (Cannot delete item (ID:%d) because it has links)' % (itemid, self.LocationName)
						else:
							delete_msg += ' (Cannot delete item (ID:%d) because of the location)'
				if delete_try != 0:
					Delete = ' %d records were marked to be deleted and %d records were actually deleted with the following messages: %s' % (delete_try, delete_count, delete_msg)
				else:
					Delete = delete_msg
				turbogears.flash('Record updated%s' % Delete)
			else: # Warn the user that editing other's records are not allowed
				turbogears.flash('Editing requests for other locations not allowed.')
		elif Operation == "Save" and StockTransferRequestID==None: # Create a new record
			STR = model.InvStockTransferRequest(RequestedBy=RequestedBy,RequestedOn=model.cur_date_time(),\
				RequiredBy=RequiredBy,ForLocationID=int(self.LocationID), Notes=Notes)
			StockTransferRequestID = STR.id
			turbogears.flash('New record created')
		elif Operation == 'Delete':
			STR = model.InvStockTransferRequest.get(StockTransferRequestID)
			if STR.ForLocationID == int(self.LocationID): # Prevent deletions of requests for other locations
				if STR.SafeToDelete(): # Check if the record is safe to delete
					delete_count = 0 # I want to count how many related db records are deleted by this action
					# remove all items (the SafeToDelete should make sure all records are safe to delete)
					for item in STR.Items:
						item.destroySelf()
						delete_count += 1
					# Now delete the record
					delete_count += 1
					STR.destroySelf()
					turbogears.flash('%d Record(s) deleted' % delete_count)
				StockTransferRequestID=None
			else:
				turbogears.flash('Deleting requests for other locations not allowed.')
		elif Operation == 'Un-Delete':
			STR = model.InvStockTransferRequest.get(StockTransferRequestID)
			if STR.ForLocationID == int(self.LocationID): # Prevent deletions of requests for other locations
				STR.Status = ''
				turbogears.flash('Record un-deleted.')
			else:
				turbogears.flash('Un-deleting requests for other locations not allowed.')
		elif Operation == 'New':
			StockTransferRequestID = None
		# Load the QuoteRequest
		if StockTransferRequestID != None:
			raise cherrypy.HTTPRedirect('StockTransferRequestsEditor?StockTransferRequestID=%d' % StockTransferRequestID)
		else:
			raise cherrypy.HTTPRedirect('StockTransferRequestsEditor')

	@expose(html='turbocare.templates.store_stocktransferseditor')
	@validate(validators={'StockTransferID':validators.Int(), 'StockTransferRequestItemID':validators.Int(), \
	'StockLocationID':validators.Int()})
	@identity.require(identity.has_permission("stores_stocktransfer_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def StockTransfersEditor(self, StockTransferID=None, StockTransferRequestItemID=None, StockLocationID=None,\
		**kw):
		'''	Create/Edit/Delete a Stock Transfer
		'''
		log.debug('StockTransfersEditor')
		pendingSTToHere = [] # Pending Transfers To Here
		pendingSTFromHere = [] # Pending Transfers From Here
		log.debug('....Stock transfer id %r' % StockTransferID)
		if StockTransferID != None:
			log.debug('....Check Stock Transfer id')
			try:
				ST = model.InvStockTransfer.get(StockTransferID)
			except SQLObjectNotFound:
				turbogears.flash("Stock transfer (ID:%d) was deleted sometime recently so I can't load it" % StockTransferID)
				StockTransferID = None
		# Prepare variables for the form
		if StockTransferID == None and StockLocationID == None and StockTransferRequestItemID != None:
			# Attempt to setup the stock transfer from a requested item (we will not save the item)
			# Set some defaults
			FromStockLocationID = None
			FromStockLocationName = ''
			StockItemID = None
			StockItemName = ''
			QtyAvailable = 0
			# Get the request
			STRitem = model.InvStockTransferRequestItem.get(StockTransferRequestItemID)
			# Make sure that we don't try to transfer from our location back to ourselves!
			if STRitem.StockTransferRequest.ForLocationID != int(self.LocationID):
				# Make sure that we have available stock
				stockitems = model.InvStockLocation.select(AND (model.InvStockItem.q.CatalogItemID==STRitem.CatalogItemID,\
				model.InvStockItem.q.id==model.InvStockLocation.q.StockItemID,model.InvStockLocation.q.LocationID==\
				int(self.LocationID),model.InvStockLocation.q.IsConsumed==False,model.InvStockLocation.q.IsSold==False,\
				model.InvStockLocation.q.Quantity>0),orderBy=[model.InvStockItem.q.ExpireDate,\
				model.InvStockItem.q.CreateTime])
				if stockitems.count() > 0:
					for item in stockitems:
						# HOW DO WE CHOOSE WHICH STOCK TO TRANSFER ?!?!?!?!?!?!?
						# CURRENT: for items with an expire date, we choose what is closest to expire.  Otherwise, we 
						# choose items that have been in the system the longest.  This is handled by the sort order above.
						if item.QtyAvailable() > 0:
							QtyAvailable = item.QtyAvailable()
							FromStockLocationID = item.id
							FromStockLocationName = item.Name()
							StockItemID = item.StockItemID
							StockITemName = item.StockItem.Name
							break
			if FromStockLocationID != None:
				# If we were successful in finding a matching StockLocation then continue to make the transfer
				# Attempt to find an existing stocklocation with the same stockitem id (not necessary to find, but nice)
				stockitems = model.InvStockLocation.select(AND (model.InvStockLocation.q.StockItemID==StockItemID,
					model.InvStockLocation.q.LocationID==STRitem.StockTransferRequest.ForLocationID, model.InvStockLocation.q.IsConsumed==\
					False,model.InvStockLocation.q.IsSold==False))
				if stockitems.count() > 0: # if we have a destination to store our transfer, we'll set it here
					ToStockLocationID = stockitems[0].id
					ToStockLocationName = stockitems[0].Name()
					ToLocationID = None
					ToLocationName = ''
				else: # No existing stock location, so we'll create it later when we save the transfer
					ToStockLocationID = None
					ToStockLocationName = ''
					ToLocationID = STRitem.StockTransferRequest.ForLocationID
					ToLocationName = STRitem.StockTransferRequest.ForLocation.Name
				Name = 'CREATE A NEW STOCK TRANSFER'
				FromLocationID = self.LocationID
				StockTransferRequestID = STRitem.StockTransferRequestID
				StockTransferRequestName = STRitem.StockTransferRequest.Name()
				if QtyAvailable > STRitem.Qty:
					Qty = STRitem.Qty
				else:
					Qty = QtyAvailable
				StockTransferRequestID = STRitem.StockTransferRequestID
				StockTransferRequestName = STRitem.StockTransferRequest.Name()
				StockTransferRequestItemID = STRitem.id
				DateTransferred = model.cur_date_time().strftime(DATE_FORMAT)
				CompletedStatus = 'Not complete'
				CanComplete = False
				Status = ''				
			else:
				# We couldn't find enough stock at our location for the transfer, so create a blank empty entry
				turbogears.flash('Upon closer inspection, there is not enough stock at this location to fulfill the request.  Sorry, better luck next time.')
				Name = 'CREATE A NEW STOCK TRANSFER'
				FromLocationID = self.LocationID
				StockItemID = ''
				StockItemName = ''
				FromStockLocationID = ''
				FromStockLocationName = ''
				ToLocationID = ''
				ToLocationName = ''
				ToStockLocationID = ''
				ToStockLocationName = ''
				StockTransferRequestID = ''
				StockTransferRequestName = ''
				StockTransferRequestItemID = ''
				Qty = ''
				DateTransferred = ''
				CompletedStatus = 'Not complete'
				CanComplete = False
				Status = ''
		elif StockTransferID == None and StockLocationID != None and StockTransferRequestItemID == None:
			stockitem = model.InvStockLocation.get(StockLocationID)
			if stockitem.LocationID == int(self.LocationID):
				FromStockLocationID = stockitem.id
				FromStockLocationName = stockitem.Name()
				StockItemID = stockitem.StockItemID
				StockItemName = stockitem.StockItem.Name
			else:
				turbogears.flash('Upon closer inspection, the specific item selected is not from this location.')
				FromStockLocationID = ''
				FromStockLocationName = ''				
				StockItemID = ''
				StockItemName = ''
			Name = 'CREATE A NEW STOCK TRANSFER'
			FromLocationID = self.LocationID
			ToLocationID = ''
			ToLocationName = ''
			ToStockLocationID = ''
			ToStockLocationName = ''
			StockTransferRequestID = ''
			StockTransferRequestName = ''
			StockTransferRequestItemID = ''
			Qty = ''
			DateTransferred = ''
			CompletedStatus = 'Not complete'
			CanComplete = False
			Status = ''
		elif StockTransferID == None: # Initial screen when no item is selected
			Name = 'CREATE A NEW STOCK TRANSFER'
			FromLocationID = self.LocationID
			StockItemID = ''
			StockItemName = ''
			FromStockLocationID = ''
			FromStockLocationName = ''
			ToLocationID = ''
			ToLocationName = ''
			ToStockLocationID = ''
			ToStockLocationName = ''
			StockTransferRequestID = ''
			StockTransferRequestName = ''
			StockTransferRequestItemID = ''
			Qty = ''
			DateTransferred = ''
			CompletedStatus = 'Not complete'
			CanComplete = False
			Status = ''
		elif  StockTransferID != None:
			ST = model.InvStockTransfer.get(StockTransferID)
			Name = ST.Name()
			FromLocationID = self.LocationID
			FromStockLocationID = ST.FromStockLocationID
			if FromStockLocationID != None:
				FromStockLocationName = ST.FromStockLocation.Name()
				StockItemID = ST.FromStockLocation.StockItemID
				StockItemName = ST.FromStockLocation.StockItem.Name
			else:
				FromStockLocationName = ''
				StockItemID = ''
				StockItemName = ''
			ToStockLocationID = ST.ToStockLocationID
			if ToStockLocationID != None:
				ToStockLocationName = ST.ToStockLocation.Name()
				ToLocationID = ST.ToStockLocation.LocationID
				ToLocationName = ST.ToStockLocation.Location.Name
			else:
				ToStockLocationName = ''
				ToLocationID = ''
				ToLocationName = ''
			if ST.StockTransferRequestItemID != None:
				StockTransferRequestID = ST.StockTransferRequestItem.StockTransferRequestID
			else:
				StockTransferRequestID = None
			if StockTransferRequestID != None:
				StockTransferRequestName = ST.StockTransferRequestItem.StockTransferRequest.Name()
				StockTransferRequestItemID = ST.StockTransferRequestItemID
			else:
				StockTransferRequestName = ''
				StockTransferRequestItemID = ''
			Qty = ST.Qty
			DateTransferred = ST.DateTransferred.strftime(DATE_FORMAT)
			if ST.IsComplete:
				CompletedStatus = 'Completed'
			else:
				CompletedStatus = 'Not Complete'
			if ToStockLocationID != None:
				if ST.ToStockLocation.LocationID==int(self.LocationID):
					CanComplete = True
				else:
					CanComplete = False
			Status = ST.Status
		# Quick links setup
		# Pending Transfers To Here
		sttohere = model.InvStockTransfer.select(AND (model.InvStockTransfer.q.ToStockLocationID==\
			model.InvStockLocation.q.id,model.InvStockLocation.q.LocationID==int(self.LocationID), \
			model.InvStockTransfer.q.IsComplete==False),orderBy=[model.InvStockTransfer.q.CreateTime])
		for item in sttohere:
			pendingSTToHere.append(dict(id=item.id, name=item.Name()))
		# unfinished Stock Transfers From Us
		stfromhere = model.InvStockTransfer.select(AND (model.InvStockTransfer.q.FromStockLocationID==\
			model.InvStockLocation.q.id,model.InvStockLocation.q.LocationID==int(self.LocationID), \
			model.InvStockTransfer.q.IsComplete==False),orderBy=[model.InvStockTransfer.q.CreateTime])
		for item in stfromhere:
			pendingSTFromHere.append(dict(id=item.id, name=item.Name()))
		return dict(pendingSTFromHere=pendingSTFromHere, pendingSTToHere=pendingSTToHere, Name=Name,\
			FromStockLocationID=FromStockLocationID, FromStockLocationName=FromStockLocationName, \
			ToStockLocationID=ToStockLocationID, ToStockLocationName=ToStockLocationName, StockTransferRequestID=\
			StockTransferRequestID, StockTransferRequestName=StockTransferRequestName, Qty=Qty,Status=Status, \
			DateTransferred=DateTransferred, CompletedStatus=CompletedStatus, CanComplete=CanComplete,\
			StockTransferID=StockTransferID, FromLocationID=FromLocationID, StockItemID=StockItemID, StockItemName=\
			StockItemName, ToLocationID=ToLocationID, ToLocationName=ToLocationName, StockTransferRequestItemID=\
			StockTransferRequestItemID)
			
	@expose(format='json')
	@validate(validators={'QuickSearchText':validators.String()})
	@identity.require(identity.has_permission("stores_stocktransfer_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")		
	def StockTransfersEditorQuickSearch(self, QuickSearchText='', **kw):
		'''	Find stock transfers
		'''
		items = model.InvStockTransfer.select( OR (\
			AND (model.InvCatalogItem.q.Name.contains(str(QuickSearchText)),\
			model.InvCatalogItem.q.id==model.InvStockItem.q.CatalogItemID,\
			model.InvStockItem.q.id == model.InvStockLocation.q.StockItemID,\
			OR (model.InvStockLocation.q.id==model.InvStockTransfer.q.FromStockLocationID,\
			model.InvStockLocation.q.id==model.InvStockTransfer.q.ToStockLocationID)),\
			AND (model.InvStockItem.q.Name.contains(str(QuickSearchText)),\
			model.InvStockItem.q.id == model.InvStockLocation.q.StockItemID,\
			OR (model.InvStockLocation.q.id==model.InvStockTransfer.q.FromStockLocationID,\
			model.InvStockLocation.q.id==model.InvStockTransfer.q.ToStockLocationID))),\
			orderBy=[-model.InvStockTransfer.q.CreateTime],distinct=True)
		results = []
		for item in items:
			results.append(dict(id=item.id, text=item.Name()))
		return dict(results=results)

	@validate(validators={'StockTransferRequestItemID':validators.Int()})
	@expose(format='json')
	@identity.require(identity.has_permission("stores_stocktransfer_edit",))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")				
	def StockTransfersEditorStockItemSelect(self, SearchText='', StockTransferRequestItemID=None, **kw):
		'''	Load the Stock Item Options for this location
		'''
		SearchText = str(SearchText)
		items=[]
		if StockTransferRequestItemID == None and SearchText=='':
			items = model.InvStockLocation.select(AND (model.InvStockLocation.q.LocationID==int(self.LocationID),\
				model.InvStockLocation.q.IsConsumed==False, model.InvStockLocation.q.IsSold==False),\
				orderBy=[-model.InvStockLocation.q.Quantity])
		elif StockTransferRequestItemID == None and SearchText!='':
			items = model.InvStockLocation.select(AND (model.InvStockLocation.q.LocationID==int(self.LocationID),\
				model.InvStockLocation.q.IsConsumed==False, model.InvStockLocation.q.IsSold==False,\
				model.InvStockLocation.q.StockItemID==model.InvStockItem.q.id, \
				OR (model.InvStockItem.q.Name.contains(SearchText), AND (model.InvCatalogItem.q.id==\
				model.InvStockItem.q.CatalogItemID, model.InvCatalogItem.q.Name.contains(SearchText)))),\
				orderBy=[-model.InvStockLocation.q.Quantity],distinct=True)
		elif StockTransferRequestItemID != None and SearchText=='':
			STRitem = model.InvStockTransferRequestItem.get(StockTransferRequestItemID)
			items = model.InvStockLocation.select(AND (model.InvStockLocation.q.LocationID==int(self.LocationID),\
				model.InvStockLocation.q.IsConsumed==False, model.InvStockLocation.q.IsSold==False,\
				model.InvStockLocation.q.StockItemID==model.InvStockItem.q.id, STRitem.CatalogItemID==\
				model.InvStockItem.q.CatalogItemID),orderBy=[-model.InvStockLocation.q.Quantity],distinct=True)
		elif StockTransferRequestItemID != None and SearchText!='':
			STRitem = model.InvStockTransferRequestItem.get(StockTransferRequestItemID)
			items = model.InvStockLocation.select(AND (model.InvStockLocation.q.LocationID==int(self.LocationID),\
				model.InvStockLocation.q.IsConsumed==False, model.InvStockLocation.q.IsSold==False,\
				model.InvStockLocation.q.StockItemID==model.InvStockItem.q.id, STRitem.CatalogItemID==\
				model.InvStockItem.q.CatalogItemID, model.InvStockItem.q.Name.contains(SearchText)),\
				orderBy=[-model.InvStockLocation.q.Quantity],distinct=True)
		results = []
		for item in items:
			results.append(dict(id=item.StockItemID, text='%d of %s' % (item.Quantity, item.StockItem.Name), linkurl="StockItemsEditor?StockItemID=%d" % item.StockItemID))
		if StockTransferRequestItemID==None:
			function_name = 'StockTransfersEditorStockItemSelect'
		else:
			function_name = 'StockTransfersEditorStockItemSelect?StockTransferRequestItemID=%d' % StockTransferRequestItemID
		return dict(results=results, function_name=function_name)
		
	@expose(format='json')
	@identity.require(identity.has_permission("stores_stocktransfer_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")					
	def StockTransfersEditorToLocationSelect(self, SearchText='', **kw):
		'''	Load the City Options
		'''
		SearchText = str(SearchText)
		if SearchText=='':
			items = model.InvLocation.select(model.InvLocation.q.id!=int(self.LocationID),orderBy=[model.InvLocation.q.Name])
		else:
			items = model.InvLocation.select(AND (model.InvLocation.q.id!=int(self.LocationID), \
				model.InvLocation.q.Name.contains(SearchText)),orderBy=[model.InvLocation.q.Name])
		results = []
		for item in items:
				results.append(dict(id=item.id, text=item.Name))
		return dict(results=results, function_name='StockTransfersEditorToLocationSelect')

	@expose()
	@validate(validators={'StockTransferID':validators.Int(),'FromLocationID':validators.Int(),\
	'StockItemID':validators.Int(),'FromStockLocationID':validators.Int(),'ToLocationID':validators.Int(),\
	'ToStockLocationID':validators.Int(),'StockTransferRequestID':validators.Int(),\
	'StockTransferRequestItemID':validators.Int(),'Qty':validators.Number(),'DateTransferred':validators.String()})
	@identity.require(identity.has_permission("stores_stocktransfer_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")						
	def StockTransfersSave(self, StockTransferID=None, FromLocationID=None, StockItemID=None,\
		FromStockLocationID=None, Operation='', ToLocationID=None, ToStockLocationID=None, \
		StockTransferRequestID=None, StockTransferRequestItemID=None, Qty=None, DateTransferred='', **kw):
		'''	Delete or update (modify) a Stock Transfer 
		'''
		log.debug('StockTransfersSave')
		# Get our operation
		log.debug('....Operation: %s' % Operation)
		log.debug('....Variables: StockTransferID: %r, FromLocationID: %r, StockItemID: %r, FromStockLocationID: %r ToStockLocationID: %r, StockTransferRequestItemID: %r, ToLocationID: %r' % (StockTransferID, \
			FromLocationID, StockItemID, FromStockLocationID, ToStockLocationID, StockTransferRequestItemID, \
			ToLocationID))
		# Perform some validation on the date fields
		if DateTransferred != None and DateTransferred != '':
			DateTransferred = datetime.fromtimestamp(time.mktime(time.strptime(DateTransferred[0:10],DATE_FORMAT)))
		else:
			DateTransferred = None
		if Operation == 'Save' and StockTransferID != None: # Update a record
			ST = model.InvStockTransfer.get(StockTransferID)
			# Make sure that we're only editing transfers from our own originating location
			if ST.FromStockLocationID == int(self.LocationID):
				St.Qty = Qty
				St.DateTransferred = DateTransferred
				turbogears.flash('Record updated')
			else:
				turbogears.flash('Cannot update the record from this location')
		elif Operation == "Save" and StockTransferID==None: # Create a new record
			# There are at least 4/5 scenarios to work through when saving a new record, with many options
			ST = None
			if FromStockLocationID!=None and ToStockLocationID!=None:
				fromlocation = model.InvStockLocation.get(FromStockLocationID)
				tolocation = model.InvStockLocation.get(ToStockLocationID)
				if StockTransferRequestItemID != None: # If we have a stock ransfer request, we need to make sure we are filling it correctly
					request = model.InvStockTransferRequestItem.get(StockTransferRequestItemID)
				if StockTransferRequestItemID != None and (tolocation.LocationID != \
				   request.StockTransferRequest.ForLocationID or fromlocation.StockItem.CatalogItemID != \
				   request.CatalogItemID):
					turbogears.flash("Data entry error, the request isn't being filled properly")
				elif fromlocation.LocationID != int(self.LocationID):
					turbogears.flash('Cannot create a transfer originating from another location')
				elif tolocation.LocationID == int(self.LocationID):
					turbogears.flash('Cannot create a transfer going to this location')
				elif fromlocation.QtyAvailable() == 0.0:
					turbogears.flash('Upon closer inspection, we have no more stock to transfer.')
				elif fromlocation.IsSold or fromlocation.IsConsumed:
					turbogears.flash('Cannot transfer the selected stock because it is used')
				else:
					if fromlocation.QtyAvailable() > Qty:
						Quantity = Qty
					else:
						Quantity = fromlocation.QtyAvailable()
					ST = model.InvStockTransfer(FromStockLocationID=fromlocation.id, ToStockLocationID=\
						ToStockLocationID, Qty=Quantity, DateTransferred=DateTransferred, StockTransferRequestItemID=\
						StockTransferRequestItemID)
					if Quantity==Qty:
						QtyMsg = ''
					else:
						QtyMsg = ' (Note: the desired quantity could not be transferred)'
					turbogears.flash('New record created%s' % QtyMsg)
			elif FromStockLocationID!=None and ToLocationID!=None:
				fromlocation = model.InvStockLocation.get(FromStockLocationID)
				if StockTransferRequestItemID != None: # If we have a stock ransfer request, we need to make sure we are filling it correctly
					request = model.InvStockTransferRequestItem.get(StockTransferRequestItemID)
				if StockTransferRequestItemID != None and (ToLocationID != request.ForLocationID or \
				   fromlocation.StockItem.CatalogItemID != request.CatalogItemID):
					turbogears.flash("Data entry error, the request isn't being filled properly")
				elif fromlocation.LocationID != int(self.LocationID):
					turbogears.flash('Cannot create a transfer originating from another location')
				elif ToLocationID == int(self.LocationID):
					turbogears.flash('Cannot create a transfer going to this location')
				elif fromlocation.QtyAvailable() == 0.0:
					turbogears.flash('Upon closer inspection, we have no more stock to transfer.')
				elif fromlocation.IsSold or fromlocation.IsConsumed:
					turbogears.flash('Cannot transfer the selected stock because it is used')
				else:
					# Attempt to find a suitable destination stock location
					tolocations = model.InvStockLocation.select(AND (model.InvStockLocation.q.StockItemID==\
						fromlocation.StockItemID, model.InvStockLocation.q.LocationID==ToLocationID,\
						model.InvStockLocation.q.IsSold==False, model.InvStockLocation.q.IsConsumed==False))
					if tolocations.count() > 0:
						ToStockLocationID = tolocations[0].id
					else:
						newstocklocation = model.InvStockLocation(StockItemID=fromlocation.StockItemID,\
							LocationID=ToLocationID)
						ToStockLocationID = newstocklocation.id
					# Re-adjust the quantity just in case the stock changed
					if fromlocation.QtyAvailable() > Qty:
						Quantity = Qty
					else:
						Quantity = fromlocation.QtyAvailable()
					ST = model.InvStockTransfer(FromStockLocationID=fromlocation.id, ToStockLocationID=\
						ToStockLocationID, Qty=Quantity, DateTransferred=DateTransferred, StockTransferRequestItemID=\
						StockTransferRequestItemID)
					if Quantity==Qty:
						QtyMsg = ''
					else:
						QtyMsg = ' (Note: the desired quantity could not be transferred)'
					turbogears.flash('New record created%s' % QtyMsg)
			elif StockItemID!=None and ToLocationID!=None:
				# We need to find the appropriate stock from our location
				stockoptions = model.InvStockLocation.select(AND (model.InvStockLocation.q.StockItemID==StockItemID,\
					model.InvStockLocation.q.LocationID==int(self.LocationID),model.InvStockLocation.q.IsSold==False,\
					model.InvStockLocation.q.IsConsumed==False,model.InvStockLocation.q.Quantity>0))
				log.debug('....%d stock options found' % stockoptions.count())
				if stockoptions.count() > 0:
					fromlocation = model.InvStockLocation.get(stockoptions[0].id)
				else:
					fromlocation = None
				if StockTransferRequestItemID != None: # If we have a stock ransfer request, we need to make sure we are filling it correctly
					request = model.InvStockTransferRequestItem.get(StockTransferRequestItemID)
				if fromlocation==None:
					turbogears.flash('Upon closer inspection, we have no more stock to transfer.')
				elif StockTransferRequestItemID != None and (ToLocationID != request.ForLocationID or \
				   fromlocation.StockItem.CatalogItemID != request.CatalogItemID):
					turbogears.flash("Data entry error, the request isn't being filled properly")
				elif ToLocationID == int(self.LocationID):
					turbogears.flash('Cannot create a transfer going to this location')
				elif fromlocation.QtyAvailable() == 0.0:
					turbogears.flash('Upon closer inspection, we have no more stock to transfer.')
				else:
					# Attempt to find a suitable destination stock location
					tolocations = model.InvStockLocation.select(AND (model.InvStockLocation.q.StockItemID==\
						fromlocation.StockItemID, model.InvStockLocation.q.LocationID==ToLocationID,\
						model.InvStockLocation.q.IsSold==False, model.InvStockLocation.q.IsConsumed==False))
					if tolocations.count() > 0:
						ToStockLocationID = tolocations[0].id
					else:
						newstocklocation = model.InvStockLocation(StockItemID=fromlocation.StockItemID,\
							LocationID=ToLocationID)
						ToStockLocationID = newstocklocation.id
					# Re-adjust the quantity just in case the stock changed
					if fromlocation.QtyAvailable() > Qty:
						Quantity = Qty
					else:
						Quantity = fromlocation.QtyAvailable()
					ST = model.InvStockTransfer(FromStockLocationID=fromlocation.id, ToStockLocationID=\
						ToStockLocationID, Qty=Quantity, DateTransferred=DateTransferred, StockTransferRequestItemID=\
						StockTransferRequestItemID)
					if Quantity==Qty:
						QtyMsg = ''
					else:
						QtyMsg = ' (Note: the desired quantity could not be transferred)'
					turbogears.flash('New record created%s' % QtyMsg)
			if ST != None:
				StockTransferID = ST.id
			else:
				StockTransferID = None
		elif Operation == 'Delete' and StockTransferID!=None:
			ST = model.InvStockTransfer.get(StockTransferID)
			if ST.SafeToDelete(): # Check if the record is safe to delete
				ST.destroySelf()
				turbogears.flash('1 Record deleted')
				StockTransferID=None
			else:
				turbogears.flash('Cannot delete completed transaction')
		elif Operation == 'Un-Delete' and StockTransferID!=None:
			ST = model.InvStockTransfer.get(StockTransferID)
			ST.Status = ''
			turbogears.flash('Record un-deleted.')
		elif Operation == 'New':
			StockTransferID = None
		elif Operation == 'Complete' and StockTransferID!=None:
			ST = model.InvStockTransfer.get(StockTransferID)
			if ST.ToStockLocation.LocationID==int(self.LocationID):
				# Once the transfer completes, deduct the stock from the source location.  The stock already exists in
				# the destination.
				ST.ToStockLocation.Quantity += ST.Qty
				ST.FromStockLocation.Quantity -= ST.Qty
				ST.IsComplete = True
				turbogears.flash('Transfer completed, stock is exchanged.')
			else:
				turbogears.flash('Only the destination location can mark a transfer complete')
		else:
			turbogears.flash('Could not perform the operation (incomplete fields)')
		# Load the QuoteRequest
		if StockTransferID != None:
			raise cherrypy.HTTPRedirect('StockTransfersEditor?StockTransferID=%d' % StockTransferID)
		else:
			raise cherrypy.HTTPRedirect('StockTransfersEditor')
			
	
	@expose(html='turbocare.templates.store_stockmonitor')
	@validate(validators={'PurchaseOrderID':validators.Int()})
	@identity.require(identity.has_permission("stores_po_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")	
	def StockMonitor(self, Groups=[], SearchText='', **kw):
		'''	Displays a list of stock items for this location (only)
			Displays information on Stock Quantities (here and the hospital overall)
			The display is limited to 100 items
		'''
		log.debug('StockMonitor')
		# Prepare our catalog item groups for the list box
		CatalogItemGroups = [dict(id=x.id,name=x.Name,selected=None) for x in model.InvGrpStock.select(orderBy=[model.InvGrpStock.q.Name])]
		# Search for our items
		qArgs = ""
		qArgs+="model.InvStockItem.q.id==model.InvStockLocation.q.StockItemID,"
		qArgs+="model.InvStockLocation.q.LocationID==%s," % self.LocationID
		if SearchText!='' or len(Groups)>0:
			qArgs+="model.InvCatalogItem.q.id==model.InvStockItem.q.CatalogItemID,"
		if SearchText != '':
			qArgs+="OR ("
			qArgs+="model.InvCatalogItem.q.Name.contains('"+ SearchText + "'),"
			qArgs+="model.InvStockItem.q.Name.contains('"+ SearchText + "')),"
		# Process our groups
		if len(Groups) > 0:
			if isinstance(Groups,basestring):
				Groups = [Groups]
			# For our group list box on the web page, set the checked property
			for group in CatalogItemGroups:
				if str(group['id']) in Groups:
					group['selected'] = 'selected'
			# Create a filter for searching for the groups
			orArgs = ''
			for group in Groups:
				orArgs+="model.InvGrpStock.q.id == '"+group+"',"
			qArgs+= "OR ("+orArgs[0:len(orArgs)-1]+"),"
			qArgs+="model.InvGrpStock.q.id == model.InvViewJoinCatalogItemGrpStock.q.GrpStockId,"
			qArgs+="model.InvCatalogItem.q.id == model.InvViewJoinCatalogItemGrpStock.q.CatalogItemId,"
			#log.debug('....qArgs %s' % qArgs)
		if len(qArgs) > 0:
			stockitems = eval('model.InvStockItem.select(AND ('+qArgs[0:len(qArgs)-1]+'),\
				orderBy=[model.InvStockItem.q.Sort])')
		else:
			stockitems = model.InvStockItem.select(orderBy=[model.InvStockItem.q.Sort])
		result_count = stockitems.count()
		# Prepare our table presentation
		ColumnTitles = ['Stock Name','Item Master Name','Qty Available','Avg. Daily Consumption',
			'Qty Available Here','Qty Consumed','Qty Transferred Here', 'Qty Transferred Away',
			'Qty Transferring Here', 'Qty Transferring Away','Qty Created Here']
		results = []
		for item in stockitems[0:100]:
			row = {}
			row['StockItemID'] = item.id
			row['CatalogItemID'] = item.CatalogItemID
			row['StockItemName'] = item.Name
			if item.CatalogItemID == None:
				row['CatalogItemName'] = 'ERROR: Not linked to a Catalog Item'
			else:
				row['CatalogItemName'] = item.CatalogItem.Name
			row['QtyAvailable'] = "%.1f" % item.QtyAvailable()
			row['RateOfConsumption'] = "%.2f" % item.RateOfConsumption()
			row['QtyAvailableLocation'] = "%.1f" % item.QtyAvailableAtLocationID(self.LocationID)
			row['QtyConsumedLocation'] = "%d" % item.QtyConsumedAtLocationID(self.LocationID)
			row['QtyTransferredToLocation'] = "%d" % item.QtyTransferredToLocationID(self.LocationID)
			row['QtyTransferringToLocation'] = "%d" % item.QtyTransferringToLocationID(self.LocationID)
			row['QtyTransferredFromLocation'] = "%d" % item.QtyTransferredFromLocationID(self.LocationID)
			row['QtyTransferringFromLocation'] = "%d" % item.QtyTransferringFromLocationID(self.LocationID)
			row['QtyCreatedAtLocation'] = "%d" % item.QtyCreatedAtLocationID(self.LocationID)
			results.append(row)
		return dict(LocationName=self.LocationName, ColumnTitles=ColumnTitles, results=results, 
		SearchText=SearchText, Groups=Groups, CatalogItemGroups=CatalogItemGroups, ResultCount=result_count)