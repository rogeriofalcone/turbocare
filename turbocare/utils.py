#
#	Care2x utility functions
#
from sqlobject import *
import model
import datetime, time
from model import DATE_FORMAT

class Temp:
	def tfunc(self):
		pass

def CopyAddressTable():
	'''	There are two address tables: InvAddressCitytown and AddressCityTown
		These two should be exactly the same in the context of this program
		so this routine is designed to make the InvAddressCitytown table match
		AddressCityTown
	'''
	ReadData = model.AddressCityTown.select(orderBy=[model.AddressCityTown.q.id])
	for address in ReadData:
		try:
			inv_address = model.InvAddressCitytown.get(address.id)
			inv_address.UneceModifier = address.UneceModifier
			inv_address.UneceLocode = address.UneceLocode
			inv_address.Name = address.Name
			inv_address.ZipCode = address.ZipCode
			inv_address.IsoCountryId = address.IsoCountryId
			inv_address.Block = address.Block
			inv_address.District = address.District
			inv_address.State = address.State
			inv_address.UneceLocodeType = address.UneceLocodeType
			inv_address.UneceCoordinates = address.UneceCoordinates
			inv_address.InfoUrl = address.InfoUrl
			inv_address.UseFrequency = address.UseFrequency
			inv_address.Status = address.Status
			inv_address.History = address.History
		except SQLObjectNotFound:
			inv_address = model.InvAddressCitytown(UneceModifier = address.UneceModifier, UneceLocode = address.UneceLocode,\
				Name = address.Name,ZipCode = address.ZipCode, IsoCountryId = address.IsoCountryId,\
				Block = address.Block,District = address.District,State = address.State,
				UneceLocodeType = address.UneceLocodeType,UneceCoordinates = address.UneceCoordinates,\
				InfoUrl = address.InfoUrl,UseFrequency = address.UseFrequency,Status = address.Status,\
				History = address.History,id=address.id)

def UpdateCatalogItemSort():
	'''	Go through all CatalogItem entries and recalculate their sort order
	'''
	catalogitems = model.InvCatalogItem.select()
	for item in catalogitems:
		item.Sort = item.CalcSort()
		
def UpdateStockLocationSort():
	'''	Go through all stock location entries and recalculate their sort order
	'''
	stocklocations = model.InvStockLocation.select()
	for item in stocklocations:
		item.Sort = item.CalcSort()

def UpdatePurchaseOrder(PurchaseOrderID):
	'''	Take a purchase order and update all the POItems
		based on the goods received.
	'''
	PurchaseOrderID = int(PurchaseOrderID) # in case we're given a string
	PO = model.InvPurchaseOrder.get(PurchaseOrderID)
	# Recalc by CatalogItemID
	for item in PO.Items:
		# Find the total quantity of stock received for this item and the Purchase price
		stockitems = model.InvStockItem.select(AND (model.InvStockItem.q.CatalogItemID==item.CatalogItemID, \
			model.InvStockItem.q.PurchaseOrderID==model.InvGoodsReceived.q.id, \
			model.InvGoodsReceived.q.PurchaseOrderID==PurchaseOrderID))
		total_quantity, actual_price = 0.0, 0.0
		for gritem in stockitems:
			actual_price = gritem.PurchasePrice
			total_quantity += gritem.Quantity
		item.QuantityReceived = total_quantity
		item.ActualPrice = actual_price

def FixVendorQuoteRequests():
	'''	Go through all the vendors and remove any QuoteRequests which were deleted
		but where the relationship was not deleted
	'''
	print "FixVendorQuoteRequests"
	vendors = model.InvVendor.select()
	for vendor in vendors:
		Errs = True
		print '====================='
		while Errs:
			print '->VendorID: %d' % vendor.id
			try:
				for qr in vendor.QuoteRequests:
					print '....QuoteRequest: %d' % qr.id
				else:
					Errs = False
			except SQLObjectNotFound, err:
				# Grab the faulty ID and fix it
				QRID = int(err.args[0][err.args[0].find('by the ID ')+10:err.args[0].find(' does not exist')])
				print "....Error on %d" % QRID
				vendor.removeInvQuoteRequest(QRID)

def DeleteStockLocation(StockLocationID):
	'''	Remove all stock transfers from a stock location
		Update all locations where we got stock from and cancel
		the transfers.  Then delete the StockLocation.
		
		If there are stock transfers FROM this location, or the items
		are already sold or consumed, then cancel the deletion.
	'''
	del_list = []
	record = model.InvStockLocation.get(StockLocationID)
	if record.IsSold or record.IsConsumed or len(record.TransfersFromHere) > 0:
		return (False, 'Cannot delete stock location (ID: %d) because of record usage state' % record.id)
	else:
		Msg = ''
		for transfer in record.TransfersToHere: # Undo the transfers
			Msg += ' Transfer %d items to %s (Transfer record deleted).' % (transfer.Qty, transfer.FromStockLocation.Location.Name)
			transfer.FromStockLocation.Quantity += transfer.Qty
			transfer.Status = 'deleted'
			del_list.append(transfer.id)
		for id in del_list: # Delete the transfers
			transfer = model.InvStockTransfer.get(id)
			transfer.destroySelf()
		# Delete the stock location
		Msg += ' Stock location (ID: %d) deleted' % record.id
		record.destroySelf()
		return (True, Msg)

def FixStockLocations():
	''' 	Go through all stock location entries and make sure they have a stock item.
		If the stock item entry deosn't exist, then delete them because there isn't too much
		we can do for it.
	'''
	Errs = True
	while Errs:
		stocklocations = model.InvStockLocation.select()
		try:
			for location in stocklocations:
				StockItemID = location.StockItemID
				name = location.StockItem.Name
			else:
				Errs = False
		except SQLObjectNotFound:
			location.destroySelf()

def TableList():
	'''	Produce a dictionary of tables which the user can query '''
	# This is a manual listing
	tables = {'AddressCityTown':'Address information in the patient database',
		'Appointment':'CURRENTLY NOT USED - Patient appointment schedule',
		'CategoryDiagnosis':'CURRENTLY NOT USED - Categories table - Diagnosis categories',
		'CategoryDisease':'CURRENTLY NOT USED - Categories table - Disease categories (use ICD10 codes instead?)',
		'CategoryProcedure':'CURRENTLY NOT USED - Categories table - Procedure categories',
		'ClassEncounter':'Classification table - the class of the encounter (Inpatient/outpatient)',
		'ClassEthnicOrig':'Classification table - Ethnic origin (Race/Country)',
		'ClassFinancial':'Classification table - Financial (private, semi-private, common, etc...)',
		'ClassInsurance':'Classification table - Insurance (self-pay, private, etc...)',
		'ClassTherapy':'CURRENTLY NOT USED - Classification table - Therapy',
		'ClassifNeonatal':'CURRENTLY NOT USED - Classification table - Neonatal',
		'Complication':'CURRENTLY NOT USED - Complications in pregnancy',
		'Department':'Department data',
		'DiagnosisLocalcode':'CURRENTLY NOT USED - Locally developed codes for diagnoses (use ICD10 tables instead)',
		'DrgIntern':'CURRENTLY NOT USED - Locally developed codes for DRG groups (use ICD10 tables instead)',
		'DrgQuicklist':'CURRENTLY NOT USED - DRG quick use table',
		'DrgRelatedCodes':'CURRENTLY NOT USED - Link table for related DRG codes',
		'DutyplanOncall':'CURRENTLY NOT USED - On-call duty plan/schedule',
		'EffectiveDay':'CURRENTLY NOT USED - Effective admission day',
		'Encounter':'Patient visits and admissions',
		'EncounterDiagnosis':'CURRENTLY NOT USED - Standard ICD codes of an encounter',
		'EncounterDiagnosticsReport':'CURRENTLY NOT USED - List of diagnostic reports e.g. radiology, pathology,etc.',
		'EncounterDrgIntern':'CURRENTLY NOT USED - DRG groups codes of an encounter',
		'EncounterEventSignaller':'CURRENTLY NOT USED - Stores event flags to signal events',
		'EncounterFinancialClass':'Stores financial (payment) class of an encounter',
		'EncounterImage':'CURRENTLY NOT USED - Store images data of an encounter',
		'EncounterImmunization':'CURRENTLY NOT USED - Immunization data of an encounter',
		'EncounterLocation':'Admission locations, wards, rooms, beds, transfers',
		'EncounterMeasurement':'CURRENTLY NOT USED - Measurement data of an encounter',
		'EncounterNotes':'CURRENTLY NOT USED - Reports, records, medocs, notes of an encounter',
		'EncounterObstetric':'CURRENTLY NOT USED - Pregnancy, child birth data',
		'EncounterOp':'CURRENTLY NOT USED - OR surgical operation data',
		'EncounterPrescription':'CURRENTLY NOT USED - Prescriptions data of an encounter (use inventory instead)',
		'EncounterPrescriptionNotes':'CURRENTLY NOT USED - Notes and remarks for prescriptions of an encounter',
		'EncounterProcedure':'CURRENTLY NOT USED - Standard procedure codes of an encounter',
		'EncounterSickconfirm':'CURRENTLY NOT USED - Sickness confirmation data of an encounter',
		'Group':'System table - Groups',
		'Icd10En':'CURRENTLY NOT USED - English ICD10 codes',
		'ImgDiagnostic':'CURRENTLY NOT USED - Dicom images data',
		'InsuranceFirm':'Insurance firms data',
		'InvAddressCitytown':'Inventory/Billing - Inventory address information table (a copy of the patient table)',
		'InvCatalogCompound':'Inventory/Billing - Item compounding header table',
		'InvCatalogCompoundQty':'Inventory/Billing - Item compounding details (ingredients)',
		'InvCatalogItem':'Inventory/Billing - Item Catalog (Item Master) listing',
		'InvCustomer':'Inventory/Billing - Customer information (linked to patient records)',
		'InvCustomerPayment':'Inventory/Billing - Cash payments made by customers',
		'InvGoodsReceived':'Inventory/Billing - Goods received from a purchase order',
		'InvGrpCompound':'Inventory/Billing - Grouping table - Item Compounds',
		'InvGrpCustomer':'Inventory/Billing - Grouping table - Customer',
		'InvGrpLocation':'Inventory/Billing - Grouping table - Location',
		'InvGrpPackaging':'Inventory/Billing - Grouping table - Packaging',
		'InvGrpStock':'Inventory/Billing - Grouping table - Item Catalog (Item Master)',
		'InvGrpVendor':'Inventory/Billing - Grouping table - Vendors',
		'InvLocation':'Inventory/Billing - Locations (should be similar to Departments in the care2x db)',
		'InvPOItems':'Inventory/Billing - Purchase order items',
		'InvPackaging':'Inventory/Billing - Types of item packages (bottle, 250mg pill, 500mg pill, etc...)',
		'InvPurchaseOrder':'Inventory/Billing - Purchase order header',
		'InvQuote':'Inventory/Billing - Quote header (received from a vendor)',
		'InvQuoteItems':'Inventory/Billing - Quote details (the items which are quoted)',
		'InvQuoteRequest':'Inventory/Billing - Quote request header (date/to whom)',
		'InvQuoteRequestItems':'Inventory/Billing - Quote request details (which items)',
		'InvReceipt':'Inventory/Billing - Receipt header (for a customer purchase)',
		'InvReceiptItems':'Inventory/Billing - Receipt details (which items)',
		'InvStockCompoundQty':'Inventory/Billing - For physical stock items which are a compound, the details of the composition',
		'InvStockItem':'Inventory/Billing - Stock Item header',
		'InvStockLocation':'Inventory/Billing - Stock item details (quantities stored at which locations)',
		'InvStockTransfer':'Inventory/Billing - Stock transfer details (how much, from where to where)',
		'InvStockTransferRequest':'Inventory/Billing - Stock transfer request header',
		'InvStockTransferRequestItem':'Inventory/Billing - Stock transfer request details',
		'InvVendor':'Inventory/Billing - Vendor information',
		'InvViewJoinCatalogItemGrpStock':'Inventory/Billing - Link table - catalog items to groups',
		'MethodInduction':'CURRENTLY NOT USED - Birth delivery induction methods',
		'ModeDelivery':'CURRENTLY NOT USED - Birth delivery modes',
		'Neonatal':'CURRENTLY NOT USED - Birth data',
		'OpMedDoc':'CURRENTLY NOT USED - Surgical operation medical report (textual)',
		'Permission':'System table - ',
		'Person':'Person information (for both patients and personell)',
		'PersonInsurance':'Person insurance data',
		'PersonOtherNumber':'CURRENTLY NOT USED - Person\'s other numbers (other PIDs) ',
		'Personell':'Personnel data',
		'PersonellAssignment':'Personnel assignment data',
		'Phone':'CURRENTLY NOT USED - Telephone, beeper directory',
		'Pregnancy':'CURRENTLY NOT USED - Pregnancy data',
		'RolePerson':'CURRENTLY NOT USED - Person roles',
		'Room':'Rooms data',
		'StandbyDutyReport':'CURRENTLY NOT USED - Reports of work done during standy by duty',
		'SteriProductsMain':'CURRENTLY NOT USED - Main products/materials list of sterilization department',
		'TechQuestions':'CURRENTLY NOT USED - Questions to the technical department',
		'TechRepairDone':'CURRENTLY NOT USED - Reports on technical work done',
		'TechRepairJob':'CURRENTLY NOT USED - Requests for technical repairs',
		'TestFindingsBaclabor':'CURRENTLY NOT USED - Test findings and reports for bacteriological tests',
		'TestFindingsChemlab':'CURRENTLY NOT USED - Test findings and reports for chemical/serological tests',
		'TestFindingsPatho':'CURRENTLY NOT USED - Test findings and reports for pathological tests',
		'TestFindingsRadio':'CURRENTLY NOT USED - Test findings and reports for radiological tests, xrays, ultrasound',
		'TestGroup':'CURRENTLY NOT USED - Test groups for chemical/serological laboratory tests',
		'TestParam':'CURRENTLY NOT USED - test parameters for chemical/serological laboratory tests',
		'TestRequestBaclabor':'CURRENTLY NOT USED - Requests for bacteriological tests',
		'TestRequestBlood':'CURRENTLY NOT USED - Requests for blood tests and products',
		'TestRequestChemlabor':'CURRENTLY NOT USED - Requests for chemical/serological tests',
		'TestRequestGeneric':'CURRENTLY NOT USED - Generic test requests',
		'TestRequestPatho':'CURRENTLY NOT USED - Requests for pathological tests',
		'TestRequestRadio':'CURRENTLY NOT USED - Requests for radiological tests, imagery',
		'TypeAnaesthesia':'CURRENTLY NOT USED - Type definition table - Anaesthesia (general, spinal, epidural,...)',
		'TypeApplication':'CURRENTLY NOT USED - Type definition table - Application (oral, mask, intravenous,...)',
		'TypeAssignment':'CURRENTLY NOT USED - Type definition table - Assignment (ward, dept., firm, clinic)',
		'TypeCauseOpdelay':'CURRENTLY NOT USED - Type definition table - OP delay cause (patient, nurse, cleaning,...)',
		'TypeColor':'CURRENTLY NOT USED - Type definition table - Colour (yellow, black, blue,...)',
		'TypeDepartment':'Type definition table - department (medical, support, news)',
		'TypeDischarge':'Type definition table - discharge (regular, emergency, change ward, death,...)',
		'TypeDuty':'CURRENTLY NOT USED - Type definition table - duty (regular, standby, afternoon,...)',
		'TypeEncounter':'Type definition table - Encounter (referral, walk-in, accident,...)',
		'TypeEthnicOrig':'Type definition table - Ethnic Origin (asian, caucasian, black,...)',
		'TypeFeeding':'CURRENTLY NOT USED - Type definition table - Feeding for children (breast, formula, never,...)',
		'TypeImmunization':'CURRENTLY NOT USED - Type definition table - Immunization',
		'TypeInsurance':'CURRENTLY NOT USED - Type definition table - Insurance (disability, dental, liability,...)',
		'TypeLocalization':'CURRENTLY NOT USED - Type definition table - Localization (left, right, both sides)',
		'TypeLocation':'CURRENTLY NOT USED - Type definition table - Location (dept, ward, room,...)',
		'TypeMeasurement':'CURRENTLY NOT USED - Type definition table - Measurement (temp, height, bp systolic,...)',
		'TypeNotes':'CURRENTLY NOT USED - Type definition table - Notes (consult, discharge, daily ward,...)',
		'TypeOutcome':'CURRENTLY NOT USED - Type definition table - Outcome for child delivery (alive, stillborn, late,...)',
		'TypePerineum':'CURRENTLY NOT USED - Type definition table - Perineum for pregnancy, child delivery (intact, 2nd degree tear, episiotomy,...)',
		'TypePrescription':'CURRENTLY NOT USED - Type definition table - Perscription (anticoagulant, hemolytic,...)',
		'TypeRoom':'Type definition table - Room (ward, op)',
		'TypeTest':'CURRENTLY NOT USED - Type definition table - Test (Pathological, Blood & product, radiological,...)',
		'TypeTime':'CURRENTLY NOT USED - Type definition table - OR OP times (Patient entry/exit, reposition, bandage,...)',
		'TypeUnitMeasurement':'CURRENTLY NOT USED - Type definition table - Unit of measure (volume, weight, length,...)',
		'UnitMeasurement':'CURRENTLY NOT USED - again, unit of measure',
		'User':'System table - Users',
		'Visit':'System table - User session visit',
		'VisitIdentity':'System table - User session identity',
		'Ward':'Ward data'}
	return tables

def TblCols(tablename):
	'''	Return a listing of columns.  This is all db columns '''
	Listing = []
	# Make sure we're working with a string representation of the table name
	if not isinstance(tablename, str):
		tablename = tablename.__name__
	# Every table has an "id" column.  Add that column to the list
	Listing.append('id')
	# If the table has Name or description, append those at the start
	if eval("model.%s.sqlmeta.columns.has_key('%s')" % (tablename,'Name')):
		Listing.append('Name')
	if eval("model.%s.sqlmeta.columns.has_key('%s')" % (tablename,'Description')):
		Listing.append('Description')
	# Go through all the (rest of the) columns in the table
	for col in eval("model.%s.sqlmeta.columns" % tablename):
		# Append the following columns (if they exist) at the end of the list
		if not (col in ['Sort','Status','ModifyId','ModifyTime','CreateId','CreateTime','Name','id','Description']):
			# append items of known datatypes only
			if eval("model.%s.sqlmeta.columns['%s'].__class__.__name__" % (tablename,col)) in ['SOStringCol','SODateTimeCol','SODateCol','SOTimeCol','SOBoolCol','SOFloatCol','SOIntCol','SOForeignKey']:
				Listing.append(col)
	else:
		if eval("model.%s.sqlmeta.columns.has_key('%s')" % (tablename,'Sort')):
			Listing.append('Sort')
		if eval("model.%s.sqlmeta.columns.has_key('%s')" % (tablename,'Status')):
			Listing.append('Status')
		if eval("model.%s.sqlmeta.columns.has_key('%s')" % (tablename,'ModifyId')):
			Listing.append('ModifyId')
		if eval("model.%s.sqlmeta.columns.has_key('%s')" % (tablename,'ModifyTime')):
			Listing.append('ModifyTime')
		if eval("model.%s.sqlmeta.columns.has_key('%s')" % (tablename,'CreateId')):
			Listing.append('CreateId')
		if eval("model.%s.sqlmeta.columns.has_key('%s')" % (tablename,'CreateTime')):
			Listing.append('CreateTime')
	return Listing
	
def TblFunction(tablename):
	'''	Return a list of the functions for the table (only custom functions) '''
	Listing = []
	if not isinstance(tablename, str):
		tablename = tablename.__name__
	for col in dir(eval('model.%s' % tablename)):
		try:
			if isinstance(eval("model.%s.%s" % (tablename,col)), type(Temp.tfunc)) and (col[0]!='_') and (not col[0].islower()):
				Listing.append(col)
		except:
			raise
	Listing.sort()
	return Listing

def GenerateReportDefinitions():
	'''	Read the model and create a file
		where we can read the report
		fields definitions (which fields to 
		show and hide)
	'''
	tables = TableList()
	ReportDefinition = {}
	for table in tables.keys():
		Cols = TblCols(table)
		Funcs = TblFunction(table)
		ColDef = {}
		for col in Cols:
			if col in ['Sort','Status','ModifyId','ModifyTime','CreateId','CreateTime']:
				ColDef[col] = dict(Show=False, FKShow=False, SubTableShow=False, AltName=col)
			elif col in ['Name','id','Description']:
				ColDef[col] = dict(Show=True, FKShow=True, SubTableShow=True, AltName=col)
			else:
				ColDef[col] = dict(Show=True, FKShow=False, SubTableShow=True, AltName=col)
		for col in Funcs:
			if col in ['CalcSort']:
				ColDef[col] = dict(Show=False, FKShow=False, SubTableShow=False, AltName=col)
			elif col in ['DisplayName', 'Name']:
				ColDef[col] = dict(Show=True, FKShow=True, SubTableShow=True, AltName=col)
			else:
				ColDef[col] = dict(Show=True, FKShow=False, SubTableShow=True, AltName=col)
		# Put the column and function list together.  Try to put the functions before the last 6 columns (Sort column)
		try:
			i = Cols.index('Sort')
		except ValueError:
			try:
				i = Cols.index('Status')
			except ValueError:
				try:
					i = Cols.index('ModifyId')
				except ValueError:
					i = len(Cols)
		ColSort = Cols[:i] + Funcs + Cols[i:]
		ReportDefinition[table] = dict(ColumnSort=ColSort, ColumnDefinitions=ColDef)
	f = open('ReportDefinition.py','w')
	f.write("ReportDefinition = {")
	for table in ReportDefinition:
		f.write("'%s': \n" % table)
		if len(ReportDefinition[table]['ColumnSort']) == 0: # If there are no columns
			f.write("    {'ColumnSort': [],\n")
			f.write("    'ColumnDefinitions': {}\n")
			f.write("    },\n")
		else: # If there are columns in the table
			f.write("    {'ColumnSort': %r,\n" % ReportDefinition[table]['ColumnSort'])
			f.write("    'ColumnDefinitions': {\n")
			for col in ReportDefinition[table]['ColumnDefinitions']:
				f.write("        '%s': %r,\n" % (col,ReportDefinition[table]['ColumnDefinitions'][col]))
			else:
				f.seek(-2,1) # remove the comma and carriage return
				f.write('\n') # add the return back in
			f.write("        }\n")
			f.write("    },\n")
	else:
		f.seek(-2,1) # remove the last return and comma
		f.write('\n') # add the return back in
	f.write("}")
	f.close()
	
DFLT_PERMISSIONS = {'bill_create': 'Create Bill',
	       'bill_edit': 'Edit Bill',
	       'bill_pay': 'Pay Bills',
	       'bill_view': 'View Bills',
	       'bill_delete': 'Delete Bills',
	       'billing_report': 'Report Billing',
	       'dispensing_view': 'View Dispensing',
	       'dispensing_dispense': 'Dispensing',
	       'reg_view': 'Registration view',
	       'reg_create': 'Registration create',
	       'reg_edit': 'Registration Edit',
	       'stores_catalog_view': 'Stores Catalog view',
	       'stores_catalog_edit': 'Stores Catalog edit',
	       'stores_gr_view': 'Goods received view',
	       'stores_gr_edit': 'Goods received edit',
	       'stores_quote_view': 'Store quote view',
	       'stores_quote_edit': 'Store quote edit',
	       'stores_quoterequest_view': 'Quote Request View',
	       'stores_vendor_view': 'Vendor view',
	       'stores_quoterequest_edit': 'Quote request edit',
	       'stores_vendor_edit': 'Vendor edit',
	       'stores_stock_view': 'Stock view',
	       'stores_stock_edit': 'Stock edit',
	       'stores_stocktransferrequest_view': 'Stock transfer request view',
	       'stores_stocktransferrequest_edit': 'Stock transfer request edit',
	       'stores_stocktransfer_view': 'Stock transfer view',
	       'stores_stocktransfer_edit': 'Stock transfer edit',
	       'admin_controllers_inventory': 'Inventory controller admin',
	       'admin_catwalk': 'User Administration (with Catwalk)',
	       'stores_po_view': 'Purchase order view',
	       'stores_po_edit': 'Purchase order edit',
	       'report_editor': 'Report Editor',
	       'admin_users': 'Administer Users',
	       'bill_refund': 'Perform billing refunds',
	       'admin_controllers_configuration': 'Configuration controller access',
	       'person_manager_view':'Person Manager View'}
	
def InitAdmin(name='admin', password=None):
	''' Initialize an administrative account with a login id and password (name and password) '''
	# Step 1: make sure all the default permissions exist in the tg_permissions table (model.Permission)
	for perm in DFLT_PERMISSIONS.keys():
		permission = model.Permission.select(model.Permission.q.permission_name == perm)
		if permission.count() == 0:
			NewPermission = model.Permission(permission_name = perm, description = DFLT_PERMISSIONS[perm])
	# Step 2: Create/check for a group called 'superuser'
	supergroup_list = model.Group.select(model.Group.q.group_name == 'superuser')
	if supergroup_list.count() == 0:
		supergroup = model.Group(group_name = 'superuser', display_name = 'Super User')
	else:
		supergroup = supergroup_list[0]
	# Step 3: Make sure all permissions are assigned to this group
	permission_id_list = [x.id for x in supergroup.permissions]
	for permission in model.Permission.select():
		if permission.id not in permission_id_list:
			supergroup.addPermission(permission)
	# Step 4: Check for or Create the admin user
	users = model.User.select(model.User.q.user_name == name)
	if users.count() == 0:
		admin_user = model.User(user_name = name, email_address = name, display_name = name, password = password)
	else:
		admin_user = users[0]
		# Reset the password to what the user supplied
		admin_user.password = password
	# Step 5: Make sure the supergroup is included in the admin_user
	if supergroup.id not in [x.id for x in admin_user.groups]:
		admin_user.addGroup(supergroup)
	# DONE!!
	

