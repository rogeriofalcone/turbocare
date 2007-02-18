from datetime import datetime, date, timedelta
from __future__ import division
import time

from sqlobject import *

from turbogears import identity 
from turbogears.database import PackageHub

hub = PackageHub("care2x")
__connection__ = hub

#Default Vars:
default_sort = 1000
DATE_FORMAT = '%Y-%m-%d'
LATEST_GRS = 5 # In the Goods Received quick listing, how many will we list
LATEST_QRS = 5 # In quote requests quick listing, we limit the display of past quote requests
LATEST_QS = 5 # Quotes quick listing limit
LATEST_POS = 5 # Purchase order quick list limit
LATEST_STRS = 5 # Stock Transfer Requests quick list limit
# Default values for certain patient services... hard coded
DFLT_WARD = {'Referral':3,'Emergency':1,'Birth delivery':3,'Walk-in':2,'Accident':1}
#1=General Surgery, 2=General Surgery 3rd Floor, 3=Ob-Gyn
DFLT_CONSLT_COMMON = {'name':'Consultation Common', 'catalogid':34}
DFLT_CONSLT_PRIVCOM = {'name':'Consultation Common+Private', 'catalogid':37}
DFLT_CONSLT_PRIVATE = {'name':'Consultation Private', 'catalogid':38}
DFLT_CONSLT_VRYPRIV = {'name':'Consultation Very Private', 'catalogid':39}
DFLT_NURSE_COMMON = {'name':'Nursing Common', 'catalogid':41}
DFLT_NURSE_PRIVCOM = {'name':'Nursing Common+Private', 'catalogid':42}
DFLT_NURSE_PRIVATE = {'name':'Nursing Private', 'catalogid':43}
DFLT_NURSE_VRYPRIV = {'name':'Nursing Very Private', 'catalogid':44}
DFLT_ROOM_COMMON = {'name':'Room Common', 'catalogid':46}
DFLT_ROOM_PRIVCOM = {'name':'Room Common+Private', 'catalogid':47}
DFLT_ROOM_PRIVATE = {'name':'Room Private', 'catalogid':48}
DFLT_ROOM_VRYPRIV = {'name':'Room Very Private', 'catalogid':49}
# Room prefix to catalog id mapping
DFLT_ROOMPREFIX= {'COMM':DFLT_ROOM_COMMON['catalogid'],'CMPR':DFLT_ROOM_PRIVCOM['catalogid'],'PRIV':DFLT_ROOM_PRIVATE['catalogid']}
CATID_ROOMPREFIX= {DFLT_ROOM_COMMON['catalogid']:'COMM',DFLT_ROOM_PRIVCOM['catalogid']:'CMPR',DFLT_ROOM_PRIVATE['catalogid']:'PRIV'}
#Insurance classes
CLASS_INSR = {'self_pay':3, 'private':1, 'charity':4, 'hospital':5}
CLASS_ENCR = {'inpatient':1, 'outpatient':2}
CLASS_FIN = {'common':9,'private + common':10,'private':11,'private plus':12}
# types (in the future, load these values on startup)
TYPE_DISCHARGE = {'regular':1,'own':2,'emergeny':3,'change_ward':4,'change_room':5,'change_bed':6,'death':6,'change_dept':8}
TYPE_LOCATION = {'ward':2,'room':4,'bed':5,'clinic':6,'dept':1,'firm':3}	
# Common Functions

def concat_datetime(date_obj, time_string):
	'''	Care2x often has date fields and time fields separate
		I need to combine them.
		date: datetime object
		time: String object with HH:MM:SS format
		returns datetime
	'''
	t = time.strptime(time,'%H:%M:%S')
	return datetime(date_obj.year,date_obj.month,date_obj.day,t.tm_hour,t.tm_min,t.tm_sec)
	
	
def cur_date_time():
	return datetime.now()
	
def cur_user_id():
	try:
#		if (not identity.current.anonymous) and identity.was_login_attempted() and (not identity.get_identity_errors()):
#			return identity.current.user_name
		if (identity.current.user_name == '') or (identity.current.user_name == None):
			return 'unknown'
		else:
			return identity.current.user_name
	except identity.exceptions.RequestRequiredException:
		return 'unknown'
	except:
		return 'unknown:err'
		raise

def cur_user_name():
	try:
#		if (not identity.current.anonymous) and identity.was_login_attempted() and (not identity.get_identity_errors()):
#			return identity.current.user_name
		if (identity.current.user_name == None) or (identity.current.user_name == ''):
			return 'unknown'
		else:
			return identity.current.user.display_name
	except identity.exceptions.RequestRequiredException:
		return 'unknown'
	except:
		raise
		return 'unknown:err'
		

def related_join_search(records=[],keys=[],colName='',colNameAttr='Name'):
	result = []
	for record in records:
		my_keys = []
		for item in getattr(record,colName):
			my_keys.append(getattr(item,colNameAttr))
		if len(set(keys) & set(my_keys)) != 0:
			result.append(record)
	return result
	
def sql_related_join(my_table='', mid_table='', join_table='', keys=[], colName='name', **kw):
	"""	Construct the SQL Where clause just for the related join.  This is "AND"ed to
		whatever extra sql where clause that exists.  SQLBuilder's docs didn't work
		for me at this point (ie. I tried the examples in a console, and I wasn't getting
		the results that the example was getting)
	"""
	#SQL to join my table to the middle table and then from the middle table to the end join table
	if (my_table=='') or (mid_table=='') or (join_table=='') or (keys==[]):
		sql=''
		clauseTables=[]
	else:
		clauseTables=[mid_table, join_table]
		sql = my_table+".id = "+mid_table+"."+my_table+"_id AND "+join_table+".id = "+mid_table+"."+join_table+"_id AND ("
		for key in keys:
			sql += join_table+"."+colName+" = '"+key+"' OR "
		sql = sql[0:-4]+")"
	return dict(sql=sql, clauseTables=clauseTables)

def sql_filter(my_table='', colName='', var='', **kw):
	"""	Construct a simple LIKE statement """
	if (my_table=='') or (colName=='') or (var==''):
		return dict(sql='',clauseTables=[])
	else:
		sql = my_table+"."+colName+" LIKE '%"+var+"%'"
		return dict(sql=sql,clauseTables=[])

def sql_filter_bool(my_table='', colName='', var='', **kw):
	"""	Construct a simple equality statement """
	if (my_table=='') or (colName=='') or (var==''):
		return dict(sql='',clauseTables=[])
	else:
		sql = my_table+"."+colName+" == "+var
		return dict(sql=sql,clauseTables=[])
	
def sql_filter_foreignkey(my_table='', my_col='', join_table='', colName='', var='', **kw):
	"""	Construct a foreign key filter """
	if (my_table=='') or (join_table=='') or (colName=='') or (var=='') or (my_col==''):
		return dict(sql='',clauseTables=[])
	else:
		clauseTables=[join_table]
		sql = my_table+"."+my_col+" = "+join_table+".id AND "+join_table+"."+colName+" LIKE '%"+var+"%'"
		return dict(sql=sql, clauseTables=clauseTables)

def sql_filter_n_foreignkey(my_table='', my_col='', join_table=[], colName=[], var='', **kw):
	"""	Construct a nth level foreign key filter 
		my_table.my_col = join_table[0].id AND join_table[0].colName[0] = join_table[1].id AND ...
	"""
	if (my_table=='') or (join_table=='') or (colName=='') or (var=='') or (my_col=='') or (len(join_table)!=len(colName)) or len(join_table)<2:
		return dict(sql='',clauseTables=[])
	else:
		clauseTables=join_table
		sql = my_table+"."+my_col+" = "+join_table[0]+".id AND "
		i = 0
		for table in join_table:
			if i+1<len(join_table):
				sql += table+"."+colName[i]+" = "+join_table[i+1]+".id AND "
				i += 1
			else:
				sql += table+"."+colName[i]+" LIKE '%"+var+"%'"
		return dict(sql=sql, clauseTables=clauseTables)
		 #sql_merge(sqls=['sql1', 'sql2', 'sql4'], clauseTables=['one'])

def sql_merge(sqls=[],clauseTables=[]):
	"""	AND all the sql statments together
	"""
	sql = ''
	for statement in sqls:
		sql += statement + " AND "
	sql = sql[0:-5]
	tabs = set(clauseTables)
	return dict(sql=sql,clauseTables=tabs)

class InvCatalogItem(SQLObject):
	"""	The catalog is a tree of items and which can be ordered.  
			They are not the specific stock, but a place holder for 
			specific stock items.
	"""
	#def _set_ParentItemID(self, value):
	#	try:
	#		if value==self.id:
	#			if self.ParentItemID==self.id:
	#				value = None
	#			else:
	#				value = self.ParentItemID
	#		value = self.ParentItemID
	#		self._SO_set_ParentItemID(value)
	#	except AttributeError:
	#		self._SO_set_ParentItemID(value)
			
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)
	
	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		if len(self.StockItems) == 0:
			value += 500
		if self.IsFixedAsset == True:
			value += 500
		if self.IsService == True:
			value += 100
		if self.IsForSale == False:
			value += 20
		if self.IsSelectable == False:
			value += 500
		if self.IsDispensable == False:
			value += 100
		value += self.DaysUntilReorder()
		self.Sort = value
		return value
		
	def VendorQuote(self, VendorID):
		'''	Go through the quote items for this catalog item
			and return the most recent quote from the specified
			vendor.  Returns the InvQuoteItems ID or None
		'''
		InvQuoteItemsID = None
		QuoteDate = None
		for item in self.Quotes:
			if item.Quote.VendorID == VendorID:
				if QuoteDate==None or item.Quote.ValidOn > QuoteDate:
					QuoteDate = item.Quote.ValidOn
					InvQuoteItemsID = item.id
		return InvQuoteItemsID
	
	def MostRecentQuotes(self):
		'''	Go through all vendors and find the most recent
			set of quotes for this catalog item.  Return an array
			of dictionairies with: VendorID, VendorName, QuotePrice,
			Ranking, QuoteItemID and ValidOn.  Results are sorted by Rank.
		'''
		Quotes = []
		Vendors = {}
		Rankings = {}
		for item in self.Quotes:
			VendorID = item.Quote.VendorID
			if Vendors.has_key(item.Quote.VendorID):
				if Vendors[VendorID]['ValidOn'] < item.Quote.ValidOn:
					Vendors[VendorID]['ValidOn'] = item.Quote.ValidOn
					Vendors[VendorID]['Price'] = item.Price
					Vendors[VendorID]['Ranking'] = item.Ranking
					Vendors[VendorID]['VendorName'] = item.Quote.Vendor.Name
					Vendors[VendorID]['QuoteItemID'] = item.id
			else:
				Vendors[VendorID] = {'ValidOn':item.Quote.ValidOn, 'Price':item.Price,'Ranking':item.Ranking,\
					'VendorName':item.Quote.Vendor.Name,'QuoteItemID':item.id}
				if Rankings.has_key(item.Ranking):
					Rankings[item.Ranking].append(VendorID)
				else:
					Rankings[item.Ranking] = [VendorID]
		for rank in Rankings.keys():
			for VendorID in Rankings[rank]:
				Quotes.append(dict(VendorID=VendorID, VendorName=Vendors[VendorID]['VendorName'],ValidOn=\
					Vendors[VendorID]['ValidOn'],Price=Vendors[VendorID]['Price'],Ranking=\
					Vendors[VendorID]['Ranking'],QuoteItemID=Vendors[VendorID]['QuoteItemID']))
		return Quotes
				
	def AvgCost(self):
		#Determine the current average cost for all items not consumed
		totalcost = 0.0
		totalitems = 0
		for item in self.StockItems:
			itemqty = 0
			itemtotalcost = 0.0
			if item.Quantity > 0:
				for item_location in item.Locations:
					if (not item_location.IsSold) and (not item_location.IsConsumed):
						itemqty += item_location.Quantity
						itemtotalcost += (item_location.Quantity)*item.PurchasePrice
			totalcost += itemtotalcost
			totalitems += itemqty
		if (totalcost == 0) or (totalitems == 0):
			value = 0.0
		else:
			value = totalcost/totalitems
		return value
		
	def QtyReceived(self):
		sum = 0.0
		for item in self.StockItems:
			sum += item.QtyReceived()
		return sum

	def QtyAvailable(self):
		Quantity = 0.0
		for item in self.StockItems:
			Quantity += item.QtyAvailable()
		return Quantity

	def QtySold(self):
		sum = 0.0
		for item in self.StockItems:
			sum += item.QtySold()
		return sum
	
	def ValueAvailablePurchase(self):
		''' Money value of items using purchase price
		'''
		value = 0.0
		for item in self.StockItems:
			value  += item.ValueAvailablePurchase()
		return value
	
	def DaysUntilZero(self):
		'''	Checks the rate of consumption based on recent history (if possible)
			If an item isn't being consumed recently, it will progressively look back
			30 consumption, 90 day consumption, ... until it finds some consumption
		'''
		if self.IsService or self.IsFixedAsset or (not self.IsSelectable) or (self.MinStockAmt <= 0):
			value = 10000 #Make it a large number
		else:
			#check last 30 days
			FromDate = datetime.now() - timedelta(days=30)
			qty = self.Consumption(FromDate)
			if qty == 0:
				#check last 90 days
				FromDate = datetime.now() - timedelta(days=90)
				qty = self.Consumption(FromDate)
				if qty == 0:
					#check last 365 days
					FromDate = datetime.now() - timedelta(days=365)
					qty = self.Consumption(FromDate)
					if qty == 0:
						#check all history.  Start date is the create date/time of the catalog item (for speed)
						FromDate = self.CreateTime
						qty = self.Consumption(FromDate)
			if qty == 0:
				value = 10000
			else:
				dayCount = float((datetime.now()-FromDate).days)
				value = int((self.QtyAvailable())/(qty/dayCount))
		return value
	
	def DaysUntilReorder(self):
		'''	Checks the rate of consumption based on recent history (if possible)
			If an item isn't being consumed recently, it will progressively look back
			30 consumption, 90 day consumption, ... until it finds some consumption
		'''
		if self.IsService or self.IsFixedAsset or (not self.IsSelectable) or (self.MinStockAmt == None) or (self.MinStockAmt == 0):
			value = 10000 #Make it a large number
		else:
			#check last 30 days
			FromDate = datetime.now() - timedelta(days=30)
			qty = self.Consumption(FromDate)
			if qty == 0.0:
				#check last 90 days
				FromDate = datetime.now() - timedelta(days=90)
				qty = self.Consumption(FromDate)
				if qty == 0.0:
					#check last 365 days
					FromDate = datetime.now() - timedelta(days=365)
					qty = self.Consumption(FromDate)
					if qty == 0.0:
						#check all history.  Start date is the create date/time of the catalog item (for speed)
						FromDate = self.CreateTime
						qty = self.Consumption(FromDate)
			if qty == 0.0:
				value = 20000
			else:
				dayCount = float((datetime.now()-FromDate).days)
				value = int((self.QtyAvailable()-self.MinStockAmt)/(qty/dayCount))
		return value

	def Consumption(self, FromDate=None):
		#Calculate The number of items consumed since the indicated date
		if FromDate == None:
			return self.QtyConsumed()
		else:
			sum = 0.0
			for item in self.StockItems:
				sum += item.Consumption(FromDate)
			return sum
			
	def QtyConsumed(self):
		sum = 0.0
		for item in self.StockItems:
			sum += item.QtyConsumed()
		return sum
		
	def TotalSold(self):
		sum = 0.0
		for item in self.StockItems:
			sum += item.TotalSold()
		return sum
		
	def LatestPO(self):
		'''	Return a dictionary of PurchaseOrderID, POSentOnDate, QuantityRequested for the latest
			PurchaseOrder involving this catalog item
		'''
		if len(self.POItems) > 0:
			PODate = self.POItems[0].PurchaseOrder.POSentOnDate
			PurchaseOrderID = self.POItems[0].PurchaseOrderID
			QuantityRequested = self.POItems[0].QuantityRequested
			QuantityReceived = self.POItems[0].QuantityReceived
			for item in self.POItems:
				if item.PurchaseOrder.POSentOnDate==None or item.PurchaseOrder.POSentOnDate > PODate:
					if item.PurchaseOrder.POSentOnDate == None:
						PODate = cur_date_time()
					else:
						PODate = item.PurchaseOrder.POSentOnDate
					PurchaseOrderID = item.PurchaseOrderID
					QuantityRequested = item.QuantityRequested
					QuantityReceived = item.QuantityReceived
			return {'id':PurchaseOrderID, 'POSentOnDate':PODate, 'QuantityRequested':QuantityRequested,'QuantityReceived':QuantityReceived}
		else:
			return {'id':None, 'POSentOnDate':None, 'QuantityRequested':0,'QuantityReceived':0}
		
	#Assists in choosing the next stock location item.  Especially useful when the stock in question has
	#an expire date.  Returns the stock id
	#If a quantity is specified, then it will search for a stock item with the correct quantity available
	def NextStockItemID(self, Quantity=0):
		ExpireDate = None
		StockItemID = None
		#Find the item closest to Expire
		for stock in self.StockItems:
			if stock.QtyAvailable() > Quantity:
				if (stock.ExpireDate != None) and (ExpireDate ==None):
					ExpireDate = stock.ExpireDate
					StockItemID = stock.id
				elif (stock.ExpireDate != None) and (stock.ExpireDate >= cur_date_time()) and \
						(ExpireDate > stock.ExpireDate):
					ExpireDate = stock.ExpireDate
					StockItemID = stock.id
		#Probably no expire dates, so find the first available item
		if StockItemID == None:
			for stock in self.StockItems:
				if stock.QtyAvailable() > Quantity:
					StockItemID = stock.id
					break
		return StockItemID
		
	def TypeDescription(self):
		'''	Based on the item properties, it describes what kind of catalog item entry it is '''
		if self.ParentItemID==None and self.IsSelectable==False:
			return "Top Level Item Category"
		elif not self.IsSelectable:
			return "Item Category"
		elif self.IsService and not self.IsDispensable:
			return "Intrinsic Service"
		elif self.IsService and self.IsDispensable:
			return "Hospital Service"
		elif self.IsFixedAsset:
			return "Fixed Asset"
		elif self.IsForSale:
			return "Item For Sale"
		else:
			return "Some system junk"
		
	def DisplayName(self):
		'''	Show the CatalogItem Name with some extra information related to stock
		'''
		return '%s: %d items in stock with %d days until re-order' % (self.Name,self.QtyAvailable(),self.DaysUntilReorder())

	CatalogGroups = RelatedJoin("InvGrpStock") #helps for searching and sorting
	ParentItem = ForeignKey("InvCatalogItem")
	ChildItems = MultipleJoin("InvCatalogItem", joinColumn="parent_item_id")
	StockItems = MultipleJoin("InvStockItem",joinColumn="catalog_item_id")
	Requests = MultipleJoin("InvStockTransferRequestItem",joinColumn="catalog_item_id")
	Quotes = MultipleJoin("InvQuoteItems",joinColumn="catalog_item_id")
	QuoteRequestItems = MultipleJoin("InvQuoteRequestItems",joinColumn="catalog_item_id")
	POItems = MultipleJoin("InvPOItems",joinColumn="catalog_item_id")
	CatalogCompoundQtys = MultipleJoin("InvCatalogCompoundQty",joinColumn="catalog_item_id")
	StockTransferRequestItems = MultipleJoin("InvStockTransferRequestItem",joinColumn="catalog_item_id")
	ReceiptItems = MultipleJoin("InvReceiptItems",joinColumn="catalog_item_id")
	Compound = ForeignKey("InvCatalogCompound",default=None) #Which catalog items are needed to make this item... if it is produced internally
	Packaging = ForeignKey("InvPackaging",default=None) #The type of packaging the item is delivered in.  The quantity number gets meaning from this.
	Name = StringCol(length=50)
	Description = StringCol(length=255,default=None)
	Accounting = StringCol(length=200,default=None)
	IsFixedAsset = BoolCol(default=False)
	IsService = BoolCol(default=False)
	IsForSale = BoolCol(default=False)
	IsSelectable = BoolCol(default=True) #If the catalog item is just a node in the tree, use "False", if stock are linked to it, then use "True"
	IsDispensable = BoolCol(default=False) #If the item is dispensed at a particular location, then this is true, false otherwise.  If false, and the item is sold, then the program will autmatically complete the full transaction when the bill is paid.
	Tax = FloatCol()
	MinStockAmt = FloatCol()
	ReorderAmt = FloatCol()
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvStockItem(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		if self.QtyAvailable() > 0:
			if self.ExpireDate == None:
				value += 500
			elif (self.ExpireDate + timedelta(days=7)) < cur_date_time():
				value -= 500
			else:
				value += (cur_date_time() - self.ExpireDate).days
		else:
			value += 1000
		self.Sort = value
		return value
					
	def RateOfConsumption(self):
		'''	The number of items consumed per day for the last 365 days '''
		return float(self.CatalogItem.Consumption(datetime.now()-timedelta(days=365))/float(365))
		
	def QtyReceived(self):
		sum = 0
		for item in self.Locations:
			sum += item.Quantity
		return sum
		
	def QtyAvailable(self):
		sum = 0.0
		for item in self.Locations:
			if not (item.IsConsumed or item.IsSold):
				if item.Quantity != None:
					sum += item.Quantity
		return sum
		
	def QtySold(self):
		sum = 0.0
		for item in self.Locations:
			if item.IsSold:
				sum += item.Quantity
		return sum
		
	def QtyAvailableAtLocationID(self,LocationID):
		'''	Calculate the amount of stock available at the specified location id'''
		sum = 0.0
		for item in self.Locations:
			if item.LocationID==int(LocationID):
				if not (item.IsConsumed or item.IsSold):
					sum += item.Quantity
		return sum
		
	def QtyConsumedAtLocationID(self,LocationID):
		'''	Calculate the amount of stock consumed at the specified location id'''
		sum = 0.0
		for item in self.Locations:
			if item.LocationID==int(LocationID) and item.IsConsumed:
				sum += item.Quantity
		return sum
	
	def QtyTransferredToLocationID(self,LocationID):
		'''	Calculate the amount of stock transferred to the specified location id'''
		sum = 0.0
		for item in self.Locations:
			if item.LocationID==int(LocationID):
				sum += item.QtyTransferredHere()
		return sum
		
	def QtyTransferringToLocationID(self,LocationID):
		'''	Calculate the amount of stock transferring (not complete) to the specified location id'''
		sum = 0.0
		for item in self.Locations:
			if item.LocationID==int(LocationID):
				sum += item.QtyTransferringHere()
		return sum
		
	def QtyTransferredFromLocationID(self,LocationID):
		'''	Calculate the amount of stock transferred from the specified location id'''
		sum = 0.0
		for item in self.Locations:
			if item.LocationID==int(LocationID):
				sum += item.QtyTransferredAway()
		return sum
	
	def QtyTransferringFromLocationID(self,LocationID):
		'''	Calculate the amount of stock transferring (not complete) from the specified location id'''
		sum = 0.0
		for item in self.Locations:
			if item.LocationID==int(LocationID):
				sum += item.QtyTransferringAway()
		return sum
	
	def QtyCreatedAtLocationID(self,LocationID):
		'''	Calculate the amount of stock created at the specified location id'''
		sum = 0.0
		for item in self.Locations:
			if item.LocationID==int(LocationID):
				sum += item.QtyStockCreatedHere()
		return sum
		
	def ValueAvailablePurchase(self):
		sum = 0.0
		for item in self.Locations:
			if not (item.IsConsumed or item.IsSold):
				try:
					sum += item.Quantity * self.PurchasePrice
				except:
					pass
		return sum
	
	def Consumption(self, FromDate=None):
		#Calculate The number of items consumed since the indicated date
		if FromDate == None:
			return self.QtyConsumed()
		else:
			sum = 0.0
			for item in self.Locations:
				item.UpdateDateConsumed() # Do this to make sure a DateConsumed is entered
				if (item.IsConsumed) and (item.DateConsumed != None) and (item.DateConsumed >= FromDate):
					sum += item.Quantity
			return sum

	def QtyConsumed(self):
		sum = 0.0
		for item in self.Locations:
			if item.IsConsumed:
				sum += item.Quantity
		return sum
		
	def TotalSold(self):
		sum = 0.0
		for item in self.Locations:
			if item.IsSold:
				sum += item.TotalPaid
		return sum
		
	def IsCompound(self):
		try:
			value = False
			if self.CatalogItemID != None:
				if self.CatalogItem.CompoundID != None:
					value = True
		except AttributeError:
			value = False
		return value
	
	def GRName(self):
		try:
			if (self.Name == '') or (self.PurchaseOrder.DateReceived.strftime(DATE_FORMAT) == ''):
				value = 'NEW ENTRY'
			elif self.Status == 'deleted':
				value = '***MARKED DELETED*** ' + str(self.QtyReceived()) + ' of ' + self.Name + ' received on ' + self.PurchaseOrder.DateReceived.strftime(DATE_FORMAT)
			else:
				value =  str(self.QtyReceived()) + ' of ' + self.Name + ' received on ' + self.PurchaseOrder.DateReceived.strftime(DATE_FORMAT)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	def DisplayName(self):
		try:
			if self.IsCompound():
				Compound = " (Compound)"
			else:
				Compound = ""
			if (self.Name == ''):
				Name = 'NEW ENTRY'
			else:
				Name = self.Name
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			value = '%s%d/%d of %s in stock%s' % (Deleted,self.QtyAvailable(),self.Quantity,Name,Compound)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value
		
	def CostDifference(self):
		try:
			if (self.MRP != None)  and (self.SalePrice != None):
				value = self.MRP - self.SalePrice
			else:
				value = None
		except AttributeError:
			value = None
		return value
		
	def VATAmount(self):
		try:
			if (self.MRP != None)  or (self.CatalogItemID != None):
				if (self.CatalogItemID != None) and (self.MRP != None) and (self.CatalogItem.Tax != None):
					value = self.MRP*self.CatalogItem.Tax
				else:
					value = None
			else:
				value = None
		except AttributeError:
			value = None
		return value
		
	def SafeToDelete(self):
		'''	Determines if it is safe to delete this stock item
		'''
		if self.TransferCount() > 0:
			return False
		if self.QtyConsumed() > 0.0:
			return False
		if self.TotalSold() > 0.0:
			return False
		return True
		
	def TransferCount(self):
		'''	Counts the number of transfers for this item
		'''
		tcount = 0
		for loc in self.Locations:
			tcount += len(loc.TransfersFromHere)
		return tcount
		
	def AvailableStockLocations(self):
		'''	A list of locations where we can move stock from (stores)
		'''
		Available = []
		for location in self.Locations:
			if location.Location.CanSell:
				Available.append(location)
		return Available
		
	def FindStockLocationIDs(self, Quantity):
		'''	A list of stock location ids which can fulfill the required amount
			First found, first used!
		'''
		SL = []
		CurrQuantity = 0
		for location in self.Locations:
			if location.Location.CanSell and location.QtyAvailable() > 0:
				SL.append(location.id)
			CurrQuantity += location.QtyAvailable()
			if CurrQuantity >= Quantity:
				break
		return SL
		
	Name = StringCol(length=40)
	CatalogItem = ForeignKey("InvCatalogItem")
	PurchaseOrder = ForeignKey("InvGoodsReceived",default=None) # Almost always exists, except when the item is produced locally
	CompoundQtys = MultipleJoin("InvStockCompoundQty",joinColumn='stock_compound_id') # Almost always None, except when produced locally
	Locations = MultipleJoin("InvStockLocation",joinColumn="stock_item_id") # How much is located where
	MRP = FloatCol(dbName='m_r_p') #Maximum Retail Price
	SalePrice = FloatCol()
	PurchasePrice = FloatCol()
	Quantity = FloatCol() # the quantity originally purchased
	BatchNumber = StringCol(length=150,default=None)
	ExpireDate = DateTimeCol(default=None)
	CompoundDateProduced = DateTimeCol(default=cur_date_time())
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvVendor(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		value += self.ItemPurchases()
		self.Sort = value
		return value
		
	def SafeToDelete(self):
		'''	Determines if the record is safe to delete
		'''
		if self.Status == 'deleted':
			return False
		if len(self.Quotes)>0 or len(self.QuoteRequests)>0 or len(self.PurchaseOrders)>0:
			return False
		return True
	
	def ItemPurchases(self):
		#Counts the number of different items ordered (not qty of items)
		count = 0
		for po in self.PurchaseOrders:
			count += len(po.items)
		return count

	Name = StringCol(length=50)
	Description = StringCol(length=200,default=None)
	DeliveryInstructions = StringCol(length=255,default=None)
	OrderDays = FloatCol(default=7.0)#The time from when the purchase order is sent to when the last goods received is entered (normally an average)
	Phone1 = StringCol(length=20,default=None)
	Phone2 = StringCol(length=20,default=None)
	Fax = StringCol(length=20,default=None)
	EMail1 = StringCol(length=20,default=None)
	EMail2 = StringCol(length=20,default=None,dbName='email2')
	City = ForeignKey("InvAddressCitytown",default=None) #to help in searching
	AddressLabel = StringCol(length=255,default=None) #The full address label, including city, state, etc...
	ContactName = StringCol(length=200,default=None)
	Quotes = MultipleJoin("InvQuote",joinColumn="vendor_id")
	QuoteRequests = RelatedJoin("InvQuoteRequest")
	PurchaseOrders = MultipleJoin("InvPurchaseOrder",joinColumn="vendor_id")
	Groups = RelatedJoin("InvGrpVendor")
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvCustomer(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		value += self.CreditAmount
		(last_purchase, id) = self.MostRecentReceipt()
		if last_purchase != None:
			value += (cur_date_time() - last_purchase).days
		else:
			value += 500
		self.Sort = value
		return value
		
	def CalcPaid(self):
		'''	From Receipts: Calculate how much has been paid
			This is all the receipts in the history of the customer
		'''
		Paid = 0.0
		for receipt in self.Receipts:
			Paid += receipt.TotalPaidCalc()
		return Paid
		
	def CalcPayment(self):
		'''	From Receipts: Calculate how much should be paid
			This is all receipts in the history of the customer
		'''
		Payment = 0.0
		for receipt in self.Receipts:
			Payment += receipt.TotalPaymentCalc()
		return Payment
		
	def CalcPaymentsMade(self):
		'''	From Customer Payments: This uses the payments table to track
			how much has actually been exchanged
		'''
		total = 0.0
		for item in self.Payments:
			total += item.Amount
		return total
		
	def CalcBalance(self, DoNotIncludReceiptID=None):
		'''	How much the customer owes us (if positive) or we owe (if negative)
			This is done by taking Sum(TotalSelfPay) - Sum(CustomerPayments)
		'''
		SumTotalSelfPay = 0.0
		if DoNotIncludReceiptID==None:
			for receipt in self.Receipts:
				SumTotalSelfPay += receipt.TotalPaymentCalc() # receipt.TotalSelfPay
		else:
			DoNotIncludReceiptID = int(DoNotIncludReceiptID)
			for receipt in self.Receipts:
				if receipt.id != DoNotIncludReceiptID:
					SumTotalSelfPay += receipt.TotalPaymentCalc() # receipt.TotalSelfPay
		SumCustomerPayments = 0.0
		for payment in self.Payments:
			SumCustomerPayments += payment.Amount
		return SumTotalSelfPay - SumCustomerPayments

	def MostRecentReceipt(self):
		last_purchase = None
		receipt_id = None
		for receipt in self.Receipts:
			if last_purchase == None:
				last_purchase = receipt.CreateTime
				receipt_id = receipt.id
			elif receipt.CreateTime > last_purchase:
				last_purchase = receipt.CreateTime
				receipt_id = receipt.id
		return (last_purchase, receipt_id)

#	def UpdateCreditAmount(self):
#		pass

	Name = StringCol(length=200)
	Phone1 = StringCol(length=20,default=None)
	Phone2 = StringCol(length=20,default=None)
	Fax = StringCol(length=20,default=None)
	EMail1 = StringCol(length=20,default=None)
	Email2 = StringCol(length=20,default=None)
	City = ForeignKey("InvAddressCitytown",default=None)
	AddressLabel = StringCol(length=255,default=None)
	CreditAmount = FloatCol(default=None) #How much money they have given us (can be negative if they owe)
	Accounting = StringCol(length=200,default=None)
	Receipts = MultipleJoin("InvReceipt",joinColumn="customer_id")
	Payments = MultipleJoin("InvCustomerPayment",joinColumn="customer_id")
	InventoryLocation = ForeignKey("InvLocation",default=None) #Where purchased items get moved to in the Inventory location table
	Groups = RelatedJoin("InvGrpCustomer")
	Sort = IntCol(default=1000)
	# ExternalID = IntCol(default=None)
	ExternalID = ForeignKey("Person",default=None, dbName="external_id")
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvCustomerPayment(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		value += self.CreditAmount
		(last_purchase, id) = self.MostRecentReceipt()
		if last_purchase != None:
			value += (cur_date_time() - last_purchase).days
		else:
			value += 500
		self.Sort = value
		return value
		
	def Name(self):
		if self.DatePaid == None or self.CustomerID == None or self.Amount == None:
			return "New Payment Entry"
		else:
			if self.Status == 'deleted':
				return "%s paid Rs. %d on %s: ***MARKED DELETED***" % (self.Customer.Name, self.Amount, self.DatePaid.strftime(DATE_FORMAT))
			else:
				return "%s paid Rs. %d on %s" % (self.Customer.Name, self.Amount, self.DatePaid.strftime(DATE_FORMAT))


	Customer = ForeignKey("InvCustomer")
	Amount = FloatCol(default=0.0) #How much money they have given us (can be negative if they were refunded)
	DatePaid = DateTimeCol(default=cur_date_time())
	Notes = StringCol(length=100,default=None)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvLocation(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		if self.CanReceive:
			value += 100
		if self.CanSell:
			value += 100
		if self.IsConsumed:
			value -= 500
		else:
			value += len(self.StockItems)
		self.Sort = value
		return value

	Name = StringCol(length=25)
	Description = StringCol(length=200)
	StockItems = MultipleJoin("InvStockLocation",joinColumn="location_id")
	Groups = RelatedJoin("InvGrpLocation")
	IsStore = BoolCol(default=False)
	CanReceive = BoolCol(default=False) #If True, then PO's can be delivered here
	CanSell = BoolCol(default=False) #If True, then Items can be sold to customers here
	IsConsumed = BoolCol(default=False) #If True, then Items stored at this location are considered consumed (like Customer)
	Department = ForeignKey("Department",default=None)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvStockLocation(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		if self.QtyAvailable() > 0:
			if self.StockItem.ExpireDate == None:
				value += 500
			elif (self.StockItem.ExpireDate + timedelta(days=7)) < cur_date_time():
				value -= 500
			else:
				value += (cur_date_time() - self.ExpireDate).days
		else:
			value += 1000
		self.Sort = value
		return value
		
	def QtyTransferredHere(self):
		'''	Calculate the total of stock transferred to this location (completed)'''
		sum = 0.0
		for transfer in self.TransfersToHere:
			if transfer.IsComplete:
				sum+=transfer.Qty
		return sum
	
	def QtyTransferredAway(self):
		'''	Calculate the total of stock transferred from this location (completed)'''
		sum = 0.0
		for transfer in self.TransfersFromHere:
			if transfer.IsComplete:
				sum+=transfer.Qty
		return sum
	
	def QtyTransferringHere(self):
		'''	Calculate the total of stock transferred to this location but not completed'''
		sum = 0.0
		for transfer in self.TransfersToHere:
			if not transfer.IsComplete:
				sum+=transfer.Qty
		return sum
		
	def QtyTransferringAway(self):
		'''	Calculate the total of stock transferred from this location but not completed'''
		sum = 0.0
		for transfer in self.TransfersFromHere:
			if not transfer.IsComplete:
				sum+=transfer.Qty
		return sum
		
	def QtyStockCreatedHere(self):
		'''	This is stock that was created at this location, either received here or a stock adjustment '''
		return self.Quantity - self.QtyTransferredHere() + self.QtyTransferredAway()
		
	def RateOfConsumption(self):
		'''	The number of items consumed per day for the last 365 days '''
		return float(self.StockItem.CatalogItem.Consumption(datetime.now()-timedelta(days=365))/float(365))

#	def _set_IsConsumed(self, value):
#		try:
#			if (self.IsConsumed == False) and (value == True):
#				self.DateConsumed = cur_date_time()
#			elif value == False:
#				self.DateConsumed = None
#		except AttributeError:
#			self.DateConsumed = None
#			raise
#		self._SO_set_IsConsumed(value)
	
	def QtyAvailable(self):
		''' This is: [Quantity] - [Quantity transferred from here, but not completed] = qty available
		# When an item is transferred the stock isn't adjusted until the transfer is marked completed
		# QtyAvailable will show the real available amount
		#if the items are sold or consumed, zero is the default '''
		FromQty = 0
		for item in self.TransfersFromHere:
			if (not item.IsComplete):
				FromQty -= item.Qty
		#FromQty = 0
		#for item in self.TransfersFromHere:
		#	if (not item.IsComplete):
		#		FromQty += item.Qty
		Qty = self.Quantity - FromQty #- FromQty
		return Qty
		
	def QtyAfterTransfers(self):
		''' Quantity after all transfers are complete '''
		Qty = self.Quantity
		for item in self.TransfersFromHere:
			if (not item.IsComplete):
				Qty -= item.Qty
		for item in self.TransfersToHere:
			if (not item.IsComplete):
				Qty += item.Qty
		return Qty
		
	def IsService(self):
		'''	Returns true if the stock item is a service item, otherwise false
		'''
		if self.StockItem.CatalogItem.IsService:
			return True
		else:
			return False
			
	def NoPendingTransfers(self):
		'''	Looks to see if there are any pending transfers
		'''
		pending_count = 0
		for t in self.TransfersFromHere:
			if not t.IsComplete:
				pending_count += 1
		for t in self.TransfersToHere:
			if not t.IsComplete:
				pending_count += 1		
		return pending_count == 0

	def FromName(self):
		'''	The names of the locations where the stock was transferred from
		'''
		if self.NoPendingTransfers():
			Status = ' (complete)'
		else:
			Status = ''
		if len(self.TransfersToHere) == 0:
			return "No transfers"
		elif len(self.TransfersToHere) == 1:
			return self.TransfersToHere[0].FromStockLocation.Name() + Status
		else:
			return reduce(lambda x, y: x+'`, `'+y, [x.FromStockLocation.Name() for x in self.TransferToHere]) + Status
				
	def FromLocationID(self):
		'''	The LocationIDs (in a list) where the stock is transferred from
		'''
		return [x.FromStockLocationID for x in self.TransfersToHere]

	def NameItemLoc(self):
		try:
			if (self.StockItem.Name == '') or (self.Location.Name == ''):
				value = 'NEW ENTRY'
			elif self.Status == 'deleted':
				value = self.StockItem.Name + ' ***MARKED DELETED*** stored at ' + self.Location.Name
			else:
				value = self.StockItem.Name + ' stored at ' + self.Location.Name
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value
		
	def UpdateDateConsumed(self):
		'''	If the entry should have a DateConsumed entered (and there isn't), this function
			should try to figure it out and set it right.
		'''
		LatestDate = None
		if self.IsConsumed and self.DateConsumed==None and self.Quantity>0:
			if self.NoPendingTransfers():

				for transfer in self.TransfersToHere:
					if LatestDate == None or LatestDate<transfer.DateTransferred:
						LatestDate = transfer.DateTransferred
				self.DateConsumed = LatestDate
		return LatestDate
		
	def Description(self):
		'''	Description of the status of the stuff stored at the location, minus the stock item name
		'''
		try:
			if self.ReceiptID != None and self.IsSold and self.IsConsumed: #This is a purchased item
				value = '%d items purchased by %s on %s for Rs. %d' % (self.Quantity,self.Receipt.Receipt.Customer.Name,\
					self.Receipt.CreateTime.strftime(DATE_FORMAT), self.TotalPaid)
			elif self.IsConsumed and not self.IsSold:
				if self.DateConsumed != None:
					Date = self.DateConsumed.strftime(DATE_FORMAT)
				else:
					Date = 'Unknown Date'
				value = '%d items were used on %s' % (self.Quantity, Date)
			elif not self.IsSold and not self.IsConsumed:
				value = '%d items available for use' % self.QtyAvailable()
			elif self.IsSold and not self.IsConsumed:
				value = 'The items are sold but not consumed!  Is this an error?'
			else:
				value = 'The items are in purgatory (purchase of indulgences required!)'
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			value = '%s%s' % (Deleted, value)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value
			
	
	def Name(self):
		try:
			if self.StockItemID == None:
				StockName = 'New Item'
			else:
				StockName = self.StockItem.Name
			if self.LocationID == None:
				LocationName = 'New Location'
			else:
				LocationName = self.Location.Name
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			value = '%s%d of %s stored at %s' % (Deleted, self.QtyAvailable(), StockName, LocationName)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value
		
	StockItem = ForeignKey("InvStockItem")
	Location = ForeignKey("InvLocation")
	Receipt = ForeignKey("InvReceiptItems",default=None) #RECEIPTITEMID!!!! link the item back to the purchase, then to the customer
	TotalPaid = FloatCol(default=0.0)
	Quantity = FloatCol(default=0.0)
	IsConsumed = BoolCol(default=False,dbName='is_consumed')
	IsSold = BoolCol(default=False)
	TransfersFromHere = MultipleJoin("InvStockTransfer",joinColumn="from_stock_location_id")
	TransfersToHere = MultipleJoin("InvStockTransfer",joinColumn="to_stock_location_id")
	Compounds = MultipleJoin("InvStockCompoundQty",joinColumn="stock_location_id") # how much of this stock item was used in a compounded item
	Sort = IntCol(default=1000)
	DateConsumed = DateTimeCol(default=None)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvQuote(SQLObject):
	"""	Vendors send back a list of items they supply and their price
			Stock managers can then rank the vendors listing on a priority
			basis for making Purchase orders.
	"""
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	def Name(self):
		try:
			if self.VendorID == None:
				Vendor = 'NEW ENTRY'
			else:
				Vendor = 'Quote from %s' % self.Vendor.Name
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED***'
			else:
				Deleted = ''
			if self.ValidOn in ['',None]:
				Date = 'no valid date'
			else:
				Date = 'on %s' % self.ValidOn.strftime(DATE_FORMAT)
			value = '%s%s %s' % (Deleted, Vendor, Date)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	Vendor = ForeignKey("InvVendor")
	QuoteRequest = ForeignKey("InvQuoteRequest")
	Items = MultipleJoin("InvQuoteItems",joinColumn="quote_id")
	ValidOn = DateCol(default=cur_date_time())
	Notes = StringCol(length=100,default=None)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvQuoteItems(SQLObject):
	"""	This is the details of a vendor quote
	"""
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	def ShortName(self):
		try:
			if self.CatalogItemID == None:
				Name = 'NEW ENTRY'
			else:
				Name = self.CatalogItem.Name
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			value = '%s%s' % (Deleted, Name)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	def Name(self):
		try:
			if self.CatalogItemID == None:
				Name = 'NEW ENTRY'
			else:
				if self.Product in ['', None]:
					Name = self.CatalogItem.Name
				else:
					Name = '%s (%s)' % (self.CatalogItem.Name, self.Product)
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			value = '%s%s' % (Deleted, Name)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	Quote = ForeignKey("InvQuote")
	CatalogItem = ForeignKey("InvCatalogItem")
	Product = StringCol(length=100,default=None)
	Price = FloatCol(default=None)
	Ranking = IntCol(default=None)
	Notes = StringCol(length=100,default=None)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvReceipt(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		value += (self.TotalPaid - self.TotalPayment)*10
		self.Sort = value
		return value
		
	def ContainsCatalogItemID(self, CatalogItemID):
		'''	Return the first ReceiptItemsID for the record matching the catalog item id
			Otherwise return None
		'''
		for item in CatalogItems:
			if item.CatalogItemID == CatalogItemID:
				return item.id
		return None
	
	def ContainsStockLocationID(self, StockLocationID):
		'''	Returns the first ReceiptItemsID with a matching StockLocationID
			Otherwise it returns None
		'''
		for item in CatalogItems:
			for stocklocation in item.StockItems:
				if stocklocation.id == StockLocationID:
					return item.id
		return None
		
	def CountPurchasedItems(self):
		if len(self.CatalogItems) == 0:
			return 0
		else:
			Count=0.0
			for item in self.CatalogItems:
				Count += item.PercentComplete()
			return Count
			
	def IsDispensed(self):
		'''	True if all items are dispensed, false otherwise
		'''
		for item in self.CatalogItems:
			if not item.IsDispensed():
				return False
		return True
			
	def FromLocationList(self):
		'''	List of locations where the items were originally from
		'''
		list = []
		for item in self.CatalogItems:
			list += item.FromLocationList()
		return [x for x in set(list)]
		
	def LocationList(self):
		'''	Returns a list of locations where the items are assigned to
		'''
		list = []
		for item in self.CatalogItems:
			list += item.LocationList()
		return [x for x in set(list)]
			
	def StatusText(self):
		'''	Report on what stage the receipt is at
			Empty, Un-Paid, Paid (not dispensed), Completed (paid and dispensed)
		'''
		self.TotalPayment = self.TotalPaymentCalc()
		if self.TotalPaid == self.TotalPayment and self.IsSatisfied():
			text = 'Paid for'
		else:
			text = 'Un-paid for'
		if self.IsDispensed():
			text += ', and dispensed'
		else:
			text += ', and not dispensed'
		return text
		
	def TotalPaymentCalc(self):
		#Go through the catalog items and figure out what the total payment should be
		TotalPay = 0.0
		for item in self.CatalogItems:
			TotalPay += item.Quantity*item.UnitCost - item.Discount
		TotalPay = float(round(TotalPay))
		
		return TotalPay
	
	def TotalPaidCalc(self):
		# Go through the stock locations and figure out how much was paid total
		TotalPaid = 0.0
		for item in self.CatalogItems:
			for stock in item.StockItems:
				TotalPaid += stock.TotalPaid
		return TotalPaid
		
	def IsSatisfied(self):
		for item in self.CatalogItems:
			if not item.IsSatisfied():
				return False
		return True

	def Name(self):
		try:
			#Fix the create and modify time to current time if it is currently None -- might be a bad idea
			if self.ModifyTime == None:
				self.ModifyTime = cur_date_time()
			if self.CreateTime == None:
				self.CreateTime = cur_date_time()
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			if (self.CustomerID == None):
				value = '%sNEW ENTRY created on %s' % (Deleted,self.CreateTime.strftime('%Y-%m-%d %H:%M:%S'))
			else:
				value = '%s%s purchased %s of %s items for Rs %s and has paid Rs %s (last updated on %s)' % \
					(Deleted,self.Customer.Name, str(self.CountPurchasedItems()), str(len(self.CatalogItems)), \
					str(self.TotalPayment), str(self.TotalPaid), self.ModifyTime.strftime(DATE_FORMAT))
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
			raise
		return value

	Customer = ForeignKey("InvCustomer")
	CatalogItems = MultipleJoin("InvReceiptItems",joinColumn="receipt_id")
	TotalPayment = FloatCol(default=None)
	TotalPaid = FloatCol(default=None)
	TotalSelfPay = FloatCol(default=None) #Credit card, cash, chickens, etc...
	SelfPayNotes = StringCol(length=200,default=None) #any notable details of the payment
	TotalInsurance = FloatCol(default=None) #Company insurance
	InsuranceNotes = StringCol(length=200,default=None) #any notable details about insurance
	# ExternalId = IntCol(default=None) #Connect the receipt to an external record, in this case, a particular encounter
	ExternalId = ForeignKey("Encounter",default=None, dbName="external_id") #Connect the receipt to an external record, in this case, a particular encounter
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvReceiptItems(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value
			
	def PercentComplete(self):
		if len(self.StockItems) == 0:
			return 0
		elif self.Quantity == 0:
			return 0.0
		else:
			QtyPurchased = 0.0
			for item in self.StockItems:
				QtyPurchased += item.Quantity
			return (QtyPurchased/self.Quantity)
			
	def IsDispensed(self):
		'''	If all the items are dispensed true, otherwise false
		'''
		if len(self.StockItems) == 0:
			return False
		for item in self.StockItems:
			if not item.NoPendingTransfers():
				return False
		return True
		
	def FromLocationList(self):
		'''	List of locations where the items were originally from
		'''
		list = []
		for location in self.StockItems:
			if len(location.TransfersToHere) > 0:
				list.append(location.TransfersToHere[0].FromStockLocation.Location.Name)
		return [x for x in set(list)]

	def FromLocationIDList(self):
		'''	List of location ids where the items were originally from
		'''
		list = []
		for location in self.StockItems:
			if len(location.TransfersToHere) > 0:
				list.append(location.TransfersToHere[0].FromStockLocation.LocationID)
		return [x for x in set(list)]

	def LocationList(self):
		'''	Returns a list of locations where the
			receipt item is located
		'''
		list = []
		for location in self.StockItems:
			list.append(location.Location.Name)
		return [x for x in set(list)]
		
	def IsSatisfied(self):
		QtyPurchased = 0
		for item in self.StockItems:
			QtyPurchased += item.QtyAfterTransfers()
		if QtyPurchased >= self.Quantity:
			value = True
		else:
			value = False
		return value
	
	def TotalPayment(self):
		'''	Calculate how much is owed for this receipt item
		'''
		return self.UnitCost * self.Quantity - self.Discount
		
	def TotalPaid(self):
		'''	Go through the stock items and see how much has been
			paid for already
		'''
		Paid = 0.0
		for item in self.StockItems:
			if item.Status == '':
				Paid += item.TotalPaid
		return Paid
			
	def IsPaid(self):
		'''	Determine if the expected payment amount
			has been paid
		'''
		return (self.TotalPayment() == self.TotalPaid())
		
	def IsExcessive(self):
		QtyPurchased = 0
		for item in self.StockItems:
			QtyPurchased += item.Quantity
		if QtyPurchased > self.Quantity:
			value = True
		else:
			value = False
		return value
				
	def IsFinished(self):
		'''	A receipt item is considered finished if it IsSatisfied
			and for non-services, the item is marked as transferred
		'''
		if self.IsSatisfied() and self.IsPaid():
			for stock in self.StockItems:
				if not stock.IsService():
					if not stock.NoPendingTransfers():
						return False
			return True
		else:
			return False
			
	def StockLocationIDs(self):
		'''	Returns a list of StockLocationID
		'''
		return [x.id for x in self.StockItems]

	def ShortName(self):
		try:
			if (self.ReceiptID == None) and (self.CatalogItemID == None):
				value = 'NEW ENTRY'
			elif self.Status == 'deleted':
				value = '***MARKED DELETED*** %s of %s' % (str(self.Quantity), self.CatalogItem.Name)
			elif (len(self.StockItems) == 1):
				value = '%s of %s' % (str(self.Quantity), self.StockItems[0].StockItem.Name)
			else:
				value = '%s of %s' % (str(self.Quantity), self.CatalogItem.Name)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	def Name(self):
		try:
			if (self.ReceiptID == None) and (self.CatalogItemID == None):
				value = 'NEW ENTRY created on ' + self.CreateTime.strftime('%Y-%m-%d %H:%M:%S')
			elif self.Status == 'deleted':
				value = '***MARKED DELETED*** %s of %s for Rs %s per item (total including any discount: %s)' % \
					(str(self.Quantity), self.CatalogItem.Name, str(self.UnitCost), str((self.UnitCost*self.Quantity)-self.Discount))
			elif (len(self.StockItems) == 1):
				value = '%s of %s for Rs %s per item (total including any discount: %s)' % \
					(str(self.Quantity), self.StockItems[0].StockItem.Name, str(self.UnitCost), str((self.UnitCost*self.Quantity)-self.Discount))				
			else:
				value = '%s of %s for Rs %s per item (total including any discount: %s)' % \
					(str(self.Quantity), self.CatalogItem.Name, str(self.UnitCost), str((self.UnitCost*self.Quantity)-self.Discount))
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	Receipt = ForeignKey("InvReceipt")
	CatalogItem = ForeignKey("InvCatalogItem")
	StockItems = MultipleJoin("InvStockLocation",joinColumn="receipt_id") # The stock items used to fulfill this request
	UnitCost = FloatCol(default=0.0)
	Discount = FloatCol(default=0.0)
	Quantity = FloatCol(default=0.0)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvQuoteRequest(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	def Name(self):
		try:
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			if self.RequestDate == None:
				Date = 'New Quote Request'
			else:
				Date = 'Quote Requested on %s' % self.RequestDate.strftime(DATE_FORMAT)
			if len(self.RequestItems) == 0:
				Items = 'having no items selected'
			else:
				Items = 'having %d items selected' % len(self.RequestItems)
			if len(self.Quotes) == 0:
				Response = "with no responses"
			else:
				Response = "with %d responses" % len(self.Quotes)
			value = '%s%s %s %s' % (Deleted,Date,Items, Response)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value
		
	Vendors = RelatedJoin("InvVendor")
	RequestDate = DateCol(default=cur_date_time())
	RequestItems = MultipleJoin("InvQuoteRequestItems",joinColumn="quote_request_id")
	Notes = StringCol(length=100,default=None)
	Quotes = MultipleJoin("InvQuote",joinColumn="quote_request_id")
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvQuoteRequestItems(SQLObject):
	"""	This is the details of a vendor quote
	"""
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	def Name(self):
		try:
			if self.CatalogItemID == None:
				Name = 'NEW ENTRY'
			else:
				Name = self.CatalogItem.Name
				if self.Qty == None or self.Qty == 0:
					Quantity = 'no items'
				else:
					Quantity = '%d items' % self.Qty
				Name = '%s of %s requested' % (Quantity, Name)
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			value = '%s%s' % (Deleted, Name)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	QuoteRequest = ForeignKey("InvQuoteRequest")
	CatalogItem = ForeignKey("InvCatalogItem")
	Qty = FloatCol(default=None)
	Notes = StringCol(length=100,default=None)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")
	
class InvPurchaseOrder(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		
		self.Sort = value
		return value

	def PercentComplete(self):
		#1=all done; between 0 and 1, not complete; -1=Undefined (nothing requested)
		received = 0.0
		requested = 0.0
		for item in self.Items:
			requested += item.QuantityRequested
			received += item.QuantityReceived
		if (requested == 0) or (received == 0):
			return -1.0
		elif requested == received:
			return 1.0
		else:
			return float(received)/float(requested)

	def StatusText(self):
		status = self.PercentComplete()
		if status==-1.0:
			text = ''
		elif status == 1.0:
			text = ' [Completed]'
		else:
			text = ' [%d Percent Complete]' % int(status*100)
		return text

	def Name(self):
		try:
			if self.Vendor.Name == None or self.Vendor.Name == '':
				Name = 'NEW ENTRY'
			else:
				Name = 'PO to %s' % self.Vendor.Name
			if (self.POSentOnDate == None) or (self.POSentOnDate.strftime(DATE_FORMAT) == ''):
				Date = 'not sent'
			else:
				Date = 'sent on %s' % self.POSentOnDate.strftime(DATE_FORMAT)
			if self.Status == 'deleted':
				StatusMsg = '***MARKED DELETED*** '
			else:
				StatusMsg = ''
			value =  '%s%s %s %s with %d items' % (StatusMsg, Name, Date, self.StatusText(), len(self.Items))
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	Vendor = ForeignKey("InvVendor")
	Items = MultipleJoin("InvPOItems",joinColumn="purchase_order_id")
	GoodsReceived = MultipleJoin("InvGoodsReceived",joinColumn="purchase_order_id")
	POSentOnDate = DateTimeCol(default=None)
	ExpectedDeliveryDate = DateTimeCol(default=None)
	Notes = StringCol(length=255,default=None)
	TransferRequests = MultipleJoin("InvStockTransferRequestItem",joinColumn="purchase_order_id")
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvPOItems(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value
		
	def GetQuoteItemName(self):
		'''	Look for the latest Quote Item Name for this item '''
		ItemNames = []
		for quote in self.PurchaseOrder.Vendor.Quotes:
			for item in quote.Items:
				if item.CatalogItemID == self.CatalogItemID:
					ItemNames.append((quote.ValidOn,item.Product))
		if len(ItemNames) == 0:
			return self.CatalogItem.Name
		else:
			ItemNames.sort()
			return ItemNames[-1][1]

	def Name(self):
		try:
			if self.CatalogItemID==None:
				Item = 'Nothing'
			else:
				Item = self.CatalogItem.Name
			if self.QuantityRequested > 0:
				if self.QuantityReceived > 0:
					if self.ActualPrice > 0:
						State = '%d of %d items received for Rs. %d each (Quoted at Rs. %d)' % (self.QuantityReceived,\
							self.QuantityRequested, self.ActualPrice, self.QuotePrice)
					else:
						State = '%d of %d items received for free (Quoted at Rs. %d)' % (self.QuantityReceived,\
							self.QuantityRequested, self.QuotePrice)
				else:
					State = '%d items ordered (Quoted at Rs. %d)' % (self.QuantityRequested,self.QuotePrice)
			else:
				State = 'no items ordered (Quoted at Rs. %d)' % self.QuotePrice
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			value = '%s%s: %s' % (Deleted,Item,State)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	PurchaseOrder = ForeignKey("InvPurchaseOrder")
	CatalogItem = ForeignKey("InvCatalogItem")
	QuantityRequested = FloatCol(default=0.0)
	QuantityReceived = FloatCol(default=0.0)
	QuotePrice = FloatCol(default=0.0)
	ActualPrice = FloatCol(default=0.0)
	Notes = StringCol(length=100,default='')
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")
	
class InvGoodsReceived(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		value += (cur_date_time() - self.DateReceived()).days
		self.Sort = value
		return value
	
	def SafeToDelete(self):
		'''	Determines if the record is safe to delete
		'''
		# check all the stock items, if they are delete-able (no transfers, only one location with all the stock)
		if self.Status == 'deleted':
			return False
		for stockitem in self.StockItems:
			if  len(stockitem.Locations) > 1 or (stockitem.TransferCount() > 0):
				return False
		return True

	def Name(self):
		try:
			if self.Status == 'deleted':
				Del = '***MARKED DELETED*** '
			else:
				Del = ''
			if self.DateReceived == None:
				Received = 'Not Received'
			else:
				Received = 'Received on %s' % self.DateReceived.strftime(DATE_FORMAT)
			if self.PurchaseOrderID == None:
				PO = 'no PurchaseOrder'
			else:
				if self.PurchaseOrder.POSentOnDate == None:
					SentDate = 'Not sent'
				else:
					SentDate = 'sent on %s' % self.PurchaseOrder.POSentOnDate.strftime(DATE_FORMAT)
				PO = 'from %s %s' % (self.PurchaseOrder.Vendor.Name, SentDate)
			value = '%sGR %s %s' % (Del, Received, PO)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	PurchaseOrder = ForeignKey("InvPurchaseOrder")
	DateReceived = DateTimeCol(default=cur_date_time())
	StockItems = MultipleJoin("InvStockItem",joinColumn="purchase_order_id")
	# InvoiceNumber = StringCol(length=100,default=None) # NOT YET IMPLEMENTED, but I'll probably need it
	Notes = StringCol(length=255,default=None)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvStockCompoundQty(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	def Name(self):
		try:
			if self.StockLocationID==None:
				Location = 'No Location'
				StockItem = 'No Stock Item'
			else:
				Location = self.StockLocation.Location.Name
				StockItem = self.StockLocation.StockItem.Name
			if self.StockCompoundID==None:
				Compound = 'No Compound'
			else:
				Compound = self.StockCompound.CatalogItem.Compound.Name
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			value = '%s%d of %s from %s for making %s' % (Deleted,self.Qty,StockItem,Location,Compound)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	StockLocation = ForeignKey("InvStockLocation") #this is an igredient
	StockCompound = ForeignKey("InvStockItem") #this is the final product
	Qty = FloatCol() #This is the amount of the igredient
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvCatalogCompound(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	Name = StringCol(length=25)
	Description = StringCol(length=200,default=None)
	ResultQty = FloatCol(default=1.0)
	ConsumedLocation = ForeignKey("InvLocation") #When stock is used to produce a stock item of this compound, which location, by default, to send the quantity
	Groups = RelatedJoin("InvGrpCompound")
	ItemQtys = MultipleJoin("InvCatalogCompoundQty",joinColumn='catalog_compound_id')
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvCatalogCompoundQty(SQLObject):
	"""	Gives an inventory item a quantity, which is then linked back to a compound
	"""
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	def Name(self):
		try:
			if (self.CatalogCompound.Name == '') or (self.CatalogItem.Name == ''):
				value = 'NEW ENTRY'
			elif self.Status == 'deleted':
				value = '***MARKED DELETED*** ' + str(self.Qty) + ' of ' + self.CatalogItem.Name + ' in ' + self.CatalogCompound.Name
			else:
				value =  str(self.Qty) + ' of ' + self.CatalogItem.Name + ' in ' + self.CatalogCompound.Name
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	CatalogCompound = ForeignKey("InvCatalogCompound")
	CatalogItem = ForeignKey("InvCatalogItem")
	Qty = FloatCol()
	Description = StringCol(length=50,default=None)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvPackaging(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		value -= len(self.CatalogItems)
		self.Sort = value
		return value

	Name = StringCol(length=25)
	Description = StringCol(length=200,default=None)
	Groups = RelatedJoin("InvGrpPackaging")
	CatalogItems = MultipleJoin("InvCatalogItem", joinColumn="packaging_id")
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvStockTransfer(SQLObject):
	"""	Tracks movement of Stock Items between locations
			This includes ALL locations: Vendor (via PO), Customer,
			Stores, Pharmacy, Departments.
	"""
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		if self.IsComplete:
			value += 10000
		else:
			value -= (datetime.now() - self.DateTransferred).days
		self.Sort = value
		return value
		
	def SafeToDelete(self):
		'''	If the record is safe to remove, then this will return True
			Note that Stock transfer Undo operations do not use this
		'''
		return not self.IsComplete
	
	def SafeToUndo(self):
		'''	If the record is safe to perform an undo operation, then return True
		'''
		if (not self.IsComplete) or ((not self.ToStockLocation.IsConsumed) and (not self.ToStockLocation.IsSold) and\
		   (self.ToStockLocation.QtyAvailable() > self.Qty)):
			return True
		else:
			return False

	def CheckCompleted(self):
		if self.StockTransferRequestItemID != None:
			if self.StockTransferRequestItem.IsTransferred:
				self.IsComplete = True
		return self.IsComplete

	def Name(self):
		try:
			note = ""
			if not self.IsComplete:
				note = "[NOT COMPLETE!]"
			else:
				note = "[completed]"
			if self.Status=='deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			if self.FromStockLocationID == None:
				FromLocation = 'unknown'
			else:
				FromLocation = self.FromStockLocation.Location.Name
			if self.ToStockLocationID == None:
				ToLocation = 'unknown'
			else:
				ToLocation = self.ToStockLocation.Location.Name
			if self.ToStockLocationID == None and self.FromStockLocationID == None:
				StockName = 'unknown'
			elif self.ToStockLocationID != None:
				StockName = self.ToStockLocation.StockItem.Name
			else:
				StockName = self.FromStockLocation.StockItem.Name
			if self.DateTransferred in ['', None]:
				DateTransferred = '(no date selected)'
			else:
				DateTransferred = self.DateTransferred.strftime(DATE_FORMAT)
			value = '%s%d of %s moved from %s to %s on %s %s' % (Deleted, self.Qty, StockName, FromLocation,\
				ToLocation, DateTransferred, note)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	FromStockLocation = ForeignKey("InvStockLocation")
	ToStockLocation = ForeignKey("InvStockLocation")
	StockTransferRequestItem = ForeignKey("InvStockTransferRequestItem",default=None)
	Qty = FloatCol(default=0)
	DateTransferred = DateTimeCol(default=cur_date_time())
	IsComplete = BoolCol(default=False)
	#Requests = MultipleJoin("InvStockTransferRequestItem",joinColumn="stock_transfer_id")
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvStockTransferRequest(SQLObject):
	"""	A request to transfer stock from one location to another
	"""
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		elif self.Status != '':
			value += 200
		if self.CompletionStatus():
			value += 10000
		else:
			diff_require = self.RequiredBy - cur_date_time()
			diff_request = self.RequestedOn - cur_date_time()
			value += diff_require.days + diff_request.days
		self.Sort = value
		return value
		
	def Sort(self):
		sum = 500.0
		if self.CompletionStatus():
			sum += 10000
		elif self.Status == 'deleted':
			sum += 10000
		else:
			if self.Status != '':
				sum += 500
			diff_require = self.RequiredBy - cur_date_time()
			diff_request = self.RequestedOn - cur_date_time()
			sum += diff_require.days + diff_request.days
		return sum
		
	def SafeToDelete(self):
		'''	Returns true if the record is safe to delete, false otherwise '''
		for item in self.Items:
			if item.IsTransferred or len(item.StockTransfers) > 0:
				return False
		return True
		
	def CompletionStatus(self):
		requested = 0.0
		received = 0.0
		IsAllReceived = True
		for item in self.Items:
			data = item.CompletionStatus()
			requested += data['requested']
			received += data['received']
			if not item.IsTransferred:
				IsAllReceived = False
		if (requested == 0.0) or (received == 0.0):
			result = False
		elif (requested == received):
			if IsAllReceived:
				result = True
			else:
				result = False
		else:
			result = False
		return result
		
	def CompletionStatusText(self):
		requested = 0.0
		received = 0.0
		IsAllReceived = True
		for item in self.Items:
			data = item.CompletionStatus()
			requested += data['requested']
			received += data['received']
			if not item.IsTransferred:
				IsAllReceived = False
		if (requested == 0.0) or (received == 0.0):
			text = ''
		elif (requested == received):
			if IsAllReceived:
				text = ' [Completed]'
			else:
				text = ' [Transfers in progress]'
		else:
			text = ' [%s Percent completed]' % str(int(received/requested*100))
		return text

	def Name(self):
		try:
			if self.RequestedBy=='':
				RequestedBy='no one'
			else:
				RequestedBy=self.RequestedBy
			if self.ForLocationID==None:
				ForLocation = 'un-known'
			else:
				ForLocation = self.ForLocation.Name
			if self.RequiredBy == '':
				ByTime = 'whenever'
			else:
				ByTime = self.RequiredBy.strftime(DATE_FORMAT)
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			value = '%s%d items requested by %s for %s by %s %s' % (Deleted,len(self.Items),RequestedBy,\
				ForLocation,ByTime,self.CompletionStatusText())
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
			#raise
		return value

	RequestedBy = StringCol(length=35,default = cur_user_id())
	RequestedOn = DateTimeCol(default=cur_date_time())
	RequiredBy = DateTimeCol(default=cur_date_time())
	ForLocation = ForeignKey("InvLocation")
	Items = MultipleJoin("InvStockTransferRequestItem",joinColumn="stock_transfer_request_id")
	Notes = StringCol(length=200,default=None)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")
	
class InvStockTransferRequestItem(SQLObject):
	"""	Specific items requested
	"""
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value
	
	def CheckAllComplete(self):
		#Returns true and sets "IsTransferred" to true if all linked transfers are marked complete
		#Or, if the Transfer is marked completed, then make sure all linked transfers are also marked complete
		if self.IsTransferred:
			linked_transfers = self.StockTransfers
			for transfer in linked_transfers:
				if transfer.IsComplete == False:
					transfer.IsComplete = True
			result = True
		else:
			linked_transfers = self.StockTransfers
			result = True
			for transfer in linked_transfers:
				if (transfer.IsComplete == False) or (transfer.Status == 'deleted'):
					result = False
			self.IsTransferred = result
		return result
		
	def IsSatisfied(self):
		''' 	True if the quantity in stock transfers satisfies or more than satisfies the request, false otherwise
			This includes in-complete Stock Transfers
		'''
		sum = 0.0
		for item in self.StockTransfers:
			if item.Status == '':
				sum += item.Qty
		if sum >= self.Qty:
			return True
		else:
			return False
			
	def CompletionStatus(self):
		'''	How close to completion is the Stock Transfer. NOTE: this only includes finished transfers'''
		sum = 0.0
		for item in self.StockTransfers:
			if item.IsComplete:
				sum += item.Qty
		return dict(requested=self.Qty, received=sum)
		
	def IsExcessive(self):
		#True if more than what is requested is transferred, otherwise, false
		sum = 0.0
		for item in self.StockTransfers:
			sum += item.Qty
		if sum <= self.Qty:
			return True
		else:
			return False
			

	def Name(self):
		try:
			if self.CatalogItemID==None:
				Item = 'No Item'
			else:
				Item = self.CatalogItem.Name
			if self.Qty == 0:
				Percent = 'nothing requested'
			else:
				cmplt = self.CompletionStatus()
				Percent = '%d%% of %d items received' % (int(cmplt['received']/cmplt['requested']*100),self.Qty)
			if self.Status == 'deleted':
				Deleted = '***MARKED DELETED*** '
			else:
				Deleted = ''
			if self.IsTransferred:
				State = '[Completed]'
			elif self.IsOnOrder:
				if self.PurchaseOrderID == None:
					StatePO = 'On Order, but no PO assigned!'
				else:
					complete = self.PurchaseOrder.PercentComplete()
					if complete < 0:
						StatePO = 'On Order (PO has quantity errors)'
					else:
						StatePO = 'On Order (PO is %d%% complete)' % int(complete*100)
				State = '[%s]' % StatePO
			else:
				State = '[Please respond!]'
			value = '%s%s of %s %s' % (Deleted,Percent,Item, State)
		except AttributeError:
			value = 'NEW ENTRY (ERR)'
		return value

	StockTransferRequest = ForeignKey("InvStockTransferRequest")
	PurchaseOrder = ForeignKey("InvPurchaseOrder",default=None)
	CatalogItem = ForeignKey("InvCatalogItem")
	#StockTransfer = ForeignKey("InvStockTransfer",default=None)
	StockTransfers = MultipleJoin("InvStockTransfer",joinColumn="stock_transfer_request_item_id")
	IsTransferred = BoolCol(default=False)
	IsOnOrder = BoolCol(default=False)
	Qty = FloatCol(default=0.0)
	Notes = StringCol(length=200,default=None)
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvGrpStock(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	Name = StringCol(length=25)
	Description = StringCol(length=200,default=None)
	CatalogItems = RelatedJoin('InvCatalogItem')
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvGrpLocation(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	Name = StringCol(length=25)
	Description = StringCol(length=200,default=None)
	Locations = RelatedJoin('InvLocation')
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvGrpCompound(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	Name = StringCol(length=25)
	Description = StringCol(length=200,default=None)
	Compounds = RelatedJoin('InvCatalogCompound')
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvGrpVendor(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	Name = StringCol(length=25)
	Description = StringCol(length=200,default=None)
	Vendors = RelatedJoin('InvVendor')
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvGrpCustomer(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	Name = StringCol(length=25)
	Description = StringCol(length=200,default=None)
	Customers = RelatedJoin('InvCustomer')
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvGrpPackaging(SQLObject):
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	
	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)
	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)
	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value

	Name = StringCol(length=25)
	Description = StringCol(length=200,default=None)
	Packagings = RelatedJoin('InvPackaging')
	Sort = IntCol(default=1000)
	Status = StringCol(length=25,dbName="status",default="")
	ModifyId = StringCol(length=35,dbName="modify_id",default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id",default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class InvAddressCitytown(SQLObject):
	class sqlmeta:
		idName = 'nr'

	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	

	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)

	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)

	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

	def CalcSort(self):
		value = default_sort
		if self.Status == 'deleted':
			value += 1000
		if self.Status != '':
			value += 200
		self.Sort = value
		return value
	
	def MultiLineName(self,html=False):
		'''	Display the name over multiple lines '''
		try:
			if html:
				br = '<br />'
			else:
				br = '\n'
			if self.Status == 'deleted':
				value = '***MARKED DELETED***'+br
			else:
				value = ''
			if (self.Name == ''):
				value += 'NEW ENTRY'
			else:
				value += '%s' % self.Name
			if self.Block != '':
				Block = self.Block+", "
			else:
				Block = ''
			if self.District !='':
				District = self.District+", "
			else:
				District = ''
			line2 = "%s%s%s" % (Block, District, self.State)
			if len(line2) > 0:
				value += br+line2
			if self.ZipCode != '':
				value += br+self.ZipCode
		except AttributeError:
			value = 'Error in Entry (ERR)'
		return value
		
	def DisplayName(self):
		try:
			if (self.Name == ''):
				value = 'NEW ENTRY'
			elif self.Status == 'deleted':
				value = "***MARKED DELETED*** %s Blck: %s  Dstrct: %s  State: %s" % (self.Name, self.Block, self.District, self.State)
			else:
				value = "%s Blck: %s  Dstrct: %s  State: %s" % (self.Name, self.Block, self.District, self.State)
		except AttributeError:
			value = 'Error in Entry (ERR)'
		return value
		
	def DisplayNameAlt(self):
		try:
			if (self.Name == ''):
				value = 'NEW ENTRY'
			elif self.Status == 'deleted':
				value = "***MARKED DELETED*** %s (%s) <%s> [%s] {%d}" % (self.Name, self.Block, self.District, self.State, self.id)
			else:
				value = " %s (%s) <%s> [%s] {%d}" % (self.Name, self.Block, self.District, self.State, self.id)
		except AttributeError:
			value = 'Error in Entry (ERR)'
		return value
		
	UneceModifier = StringCol(length=2, default=None) #char 2 
	UneceLocode = StringCol(length=15, default=None)#char 15
	Name = StringCol(length=100)#char 100
	ZipCode = StringCol(length=25, default=None)#char 25
	IsoCountryId = StringCol(length=3, default='IND')#char 3
	Block = StringCol(length=60,default=None)#char 60
	District = StringCol(length=60,default=None)#char 60
	State = StringCol(length=60, default='Nagaland')#char 60
	Vendors = MultipleJoin("InvVendor", joinColumn="city_id")
	Customers = MultipleJoin("InvCustomer", joinColumn="city_id")
	UneceLocodeType = IntCol(default=None)#int 3
	UneceCoordinates = StringCol(length=25, default=None)#char 25
	InfoUrl = StringCol(length=255, default=None)#char 255
	UseFrequency = IntCol(default=1)#int
	Sort = IntCol(default=1000)
	Status = StringCol(length=25, default=None)#char 25
	History = StringCol(default=None)#text
	ModifyId = StringCol(length=35,default=None)#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=None)#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class InvViewJoinCatalogItemGrpStock(SQLObject):
	CatalogItemId = IntCol()
	GrpStockId = IntCol()

	@classmethod
	def createTable(cls, ifNotExists=False, createJoinTables=True,
			createIndexes=True, applyConstraints=True,
			connection=None):
		conn = connection or cls._connection
		if ifNotExists and conn.tableExists(cls.sqlmeta.table):
			return
		sql, constraints = cls.createTableSQL()
		# Treat the view like a constraint, only create it
		# after all the other tables have been created.
		return [sql]

	@classmethod
	def createTableSQL(cls, createJoinTables=True, createIndexes=True,
		       connection=None):
		return """CREATE OR REPLACE VIEW %s as (
		SELECT inv_catalog_item_id*1000000000 + inv_grp_stock_id as id,
			inv_catalog_item_id as catalog_item_id,
			inv_grp_stock_id as grp_stock_id
		FROM 
			inv_catalog_item_inv_grp_stock
		) """ % (cls.sqlmeta.table,), []
