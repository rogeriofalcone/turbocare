import logging
import os
import sys
import stat
import string
import getopt
import os.path
import time
import cherrypy
import simplejson
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model
import model_inventory
import report_CatalogItems
import ReportDefinition
from datetime import datetime, timedelta
import time
from mytable_sqlite import MyTable
import pprint
import inspect

log = logging.getLogger("turbocare.controllers")	

class Temp:
	def tfunc(self):
		pass

MAX_LEVELS = 1 # The maximum depth that we search for sub-tables
# The following definitions are used to save on space in the code below
RD = ReportDefinition.ReportDefinition
CS = 'ColumnSort'
CD = 'ColumnDefinitions'
ReportBaseDir = 'turbocare/static/user_reports/'

class UserDefinedReport(controllers.RootController):
	'''	User defined reports.  This gives the greatest amount of flexibility to the user for reporting.
		A simplified user interface to perform simple ad-hoc queries against the database which
		produces data formatted in a generic fashion.  Future ideas: export to csv...
	'''
	RecordCount = 0
	TotalRecords = 1	
	iteration = 0
	
	def TableList(self):
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

	def Cols(self, tablename):
		'''	Return a listing of columns.  This is all db columns except foreign keys '''
		Listing = []
		# Make sure we're working with a string representation of the table name
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		# Go through all the columns in the table
		for col in eval("model.%s.sqlmeta.columns" % tablename):
			if eval("model.%s.sqlmeta.columns['%s'].__class__.__name__" % (tablename,col)) in \
				['SOStringCol','SODateTimeCol','SODateCol','SOTimeCol','SOBoolCol','SOFloatCol','SOIntCol']:
				Listing.append(col)
		return Listing
		
	def ColsString(self, tablename):
		'''	Return a listing of String columns'''
		Listing = []
		# Make sure we're working with a string representation of the table name
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		# Go through all the columns in the table
		for col in eval("model.%s.sqlmeta.columns" % tablename):
			if eval("model.%s.sqlmeta.columns['%s'].__class__.__name__" % (tablename,col)) == 'SOStringCol':
				Listing.append(col)
		return Listing
		
	def ColsDateTime(self, tablename):
		'''	Return a listing of DateTime columns '''
		Listing = []
		# Make sure we're working with a string representation of the table name
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		# Go through all the columns in the table
		for col in eval("model.%s.sqlmeta.columns" % tablename):
			if eval("model.%s.sqlmeta.columns['%s'].__class__.__name__" % (tablename,col)) in ['SODateTimeCol','SODateCol','SOTimeCol']:
				Listing.append(col)
		return Listing
		
	def ColsForeignKey(self, tablename):
		'''	Return a Dictionary of ForeignKey columns	'''
		Listing = {}
		# Make sure we're working with a string representation of the table name
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		# Go through all the columns in the table
		for col in eval("model.%s.sqlmeta.columns" % tablename):
			if eval("model.%s.sqlmeta.columns['%s'].__class__.__name__" % (tablename,col)) == 'SOForeignKey':
				Listing[col] = eval("model.%s.sqlmeta.columns['%s'].foreignKey" % (tablename,col))
		return Listing
		
	def ColsBool(self, tablename):
		'''	Return a listing of Boolean columns	'''
		Listing = []
		# Make sure we're working with a string representation of the table name
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		# Go through all the columns in the table
		for col in eval("model.%s.sqlmeta.columns" % tablename):
			if eval("model.%s.sqlmeta.columns['%s'].__class__.__name__" % (tablename,col)) == 'SOBoolCol':
				Listing.append(col)
		return Listing
		
	def ColsFloat(self, tablename):
		'''	Return a listing of float columns	'''
		Listing = []
		# Make sure we're working with a string representation of the table name
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		# Go through all the columns in the table
		for col in eval("model.%s.sqlmeta.columns" % tablename):
			if eval("model.%s.sqlmeta.columns['%s'].__class__.__name__" % (tablename,col)) == 'SOFloatCol':
				Listing.append(col)
		return Listing
		
	def ColsInt(self, tablename):
		'''	Return a listing of Integer columns	'''
		Listing = []
		# Make sure we're working with a string representation of the table name
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		# Go through all the columns in the table
		for col in eval("model.%s.sqlmeta.columns" % tablename):
			if eval("model.%s.sqlmeta.columns['%s'].__class__.__name__" % (tablename,col)) == 'SOIntCol':
				Listing.append(col)
		return Listing
		
	def ColsFunction(self, tablename):
		'''	Return a list of the functions for the table (only custom functions) '''
		Listing = []
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		for col in dir(eval('model.%s' % tablename)):
			try:
				if isinstance(eval("model.%s.%s" % (tablename,col)), type(Temp.tfunc)) and (col[0]!='_') and (not col[0].islower()):
					# Examine the function for variables that need to be passed to it.  Count the non "self" paramters and count
					# the number of parameters which have defaults, and see if they match
					parms = inspect.getargspec("model.%s.%s" % (tablename,col))
					log.debug('Inspect model.%s.%s: %r' % (tablename,col,parms))
					if (len(parms[0]) - 1== 0) or (parms[-1]!=None and (len(parms[0])-1==len(parms[-1]))):
						Listing.append(col)
			except:
				raise
		return Listing
	
	def GetLinkColumn(self, tablename, dbName):
		'''	find the class column name for table name
			with the db column name dbName
		'''
		for col in eval("model.%s.sqlmeta.columnList" % tablename):
			if col.dbName == dbName:
				return col.name
		return None
		
	def ColsMultipleJoin(self, tablename):
		'''	Returns a dictionary of columns and their multi joined tablename '''
		Listing = {}
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		for join in eval("model.%s.sqlmeta.joins" % tablename):
			if join.joinDef.__class__.__name__ == 'MultipleJoin':
				Listing[join.joinMethodName] = dict(Table=join.otherClass.__name__, LinkColumn=self.GetLinkColumn(join.otherClass.__name__,join.joinColumn))
		return Listing
		
	def ColsRelatedJoin(self, tablename):
		'''	Returns a dictionary of columns and their related join tablename '''
		Listing = {}
		if not isinstance(tablename, str):
			tablename = tablename.__name__
		for join in eval("model.%s.sqlmeta.joins" % tablename):
			if join.joinDef.__class__.__name__ == 'RelatedJoin':
				Listing[join.joinMethodName] = dict(Table=join.otherClass.__name__, LinkColumn=self.GetLinkColumn(join.otherClass.__name__,join.joinColumn))
		return Listing
		
	def ColDataType(self, tablename, col):
		'''	Return the column simplified data type and tablename (in case of foreign keys) '''
		try:
			SOType = eval("model.%s.sqlmeta.columns['%s'].__class__.__name__" % (tablename,col))
			if SOType in ['SOIntCol', 'SOFloatCol']:
				return "Numeric", None
			elif SOType == 'SOBoolCol':
				return "Boolean", None
			elif SOType == 'SOForeignKey':
				return "ForeignKey", eval("model.%s.sqlmeta.columns['%s'].foreignKey" % (tablename,col))
			elif SOType in ['SODateTimeCol','SODateCol','SOTimeCol']:
				return "DateTime", None
			elif SOType == 'SOStringCol':
				return "Text", None
		except KeyError: # The key error will occur because function names don't exist in the column listing of a table, or it's the id field
			if col == 'id':
				return "Numeric", None
			else:
				return "Function", None
			
	@expose(format='json')
	@identity.require(identity.not_anonymous())
	def LoadTables(self):
		return self.TableList()
	
	def GetFKColumns(self, tablename, colname):
		'''	Return a list of column dictionaries (type and name)
			This is for ForeignKeys only and is based on the ReportDefinition
		'''
		Cols = []
		for col in RD[tablename][CS]:
			if RD[tablename][CD][col]['FKShow']:
				# NOTE: I'm using the colname[:-2] to remove the "ID" from the end of the foreign key column
				# This will assist in getting the value in the future
				# Also Note: We need to check if the foreign key column is a function
				type, fktable = self.ColDataType(tablename, col)
				if type == 'Function':
					# Examine the function for variables that need to be passed to it.  
					# Count the non "self" paramters and count the number of parameters 
					# which have defaults, and see if they match
					try:
						parms = inspect.getargspec(eval("model.%s.%s" % (tablename,col)))
						if (len(parms[0]) - 1== 0) or (parms[-1]!=None and (len(parms[0])-1==len(parms[-1]))):
							Cols.append(dict(Name='%s.%s()' % (colname[:-2],col), Type='Function'))
					except TypeError: # The value we tried to add really isn't a function
						log.debug('Inspect model.%s.%s' % (tablename,col))
				else:
					Cols.append(dict(Name='%s.%s' % (colname[:-2],col), Type='ForeignKey'))
		return Cols
		
	def GetColDefinitionsOld(self, tablename):
		'''	Return a list of column dictionaries (type and name)
			This is only for non related joins or multiple joins
		'''
		Cols = []
		for col in self.ColsInt(tablename):
			Cols.append(dict(Name=col, Type='Numeric'))
		for col in self.ColsFloat(tablename):
			Cols.append(dict(Name=col, Type='Numeric'))
		for col in self.ColsBool(tablename):
			Cols.append(dict(Name=col, Type='Boolean'))
		for col in self.ColsString(tablename):
			Cols.append(dict(Name=col, Type='Text'))
		for col in self.ColsDateTime(tablename):
			Cols.append(dict(Name=col, Type='DateTime'))
		for col in self.ColsFunction(tablename):
			Cols.append(dict(Name=col, Type='Function'))
		FKs = self.ColsForeignKey(tablename)
		for col in FKs:
			Cols += self.GetFKColumns(FKs[col], col)
		return Cols
	
	def GetColDefinitions(self, tablename, isSubTable=False):
		'''	Return a list of column dictionaries (type and name)
			This is only for non related joins or multiple joins
			It is based on the ReportDefinition.  If the isSubTable
			is true, then it filters the columns based on the 
			sub table view definition
		'''
		Cols = []
		if isSubTable:
			View = 'SubTableShow'
		else:
			View = 'Show'
		for col in RD[tablename][CS]:
			if RD[tablename][CD][col][View]:
				Type, FKTable = self.ColDataType(tablename,col)
				if Type == 'ForeignKey':
					Cols += self.GetFKColumns(FKTable, col)
				elif Type == 'Function': # add the () to the function name
					# Examine the function for variables that need to be passed to it.  
					# Count the non "self" paramters and count the number of parameters 
					# which have defaults, and see if they match
					try:
						parms = inspect.getargspec(eval("model.%s.%s" % (tablename,col)))
						# log.debug('Inspect model.%s.%s: %r' % (tablename,col,parms))
						if (len(parms[0]) - 1== 0) or (parms[-1]!=None and (len(parms[0])-1==len(parms[-1]))):
							Cols.append(dict(Name=col+'()', Type=Type))
					except TypeError: # The value we tried to add really isn't a function
						log.debug('Inspect model.%s.%s' % (tablename,col))
				else:
					Cols.append(dict(Name=col, Type=Type))
		return Cols
		
	def GetSubTableDefinition(self, tablename, linkcolumn=None, parenttable=None, jointype=None, joinname=None):
		'''	Look at Related Joins and MultipleJoins and return
			The table definitions for each, nesting any sub-
			tables for each as a seperate table definition at
			another sub-level - Instead of using recursion, I'm 
			doing a looping procedure (less intuitive, but less
			error prone)
		'''
		def AssignTD(tablename, linkcolumn=None, parenttable=None,jointype=None, joinname=None):			
			TD = {}
			if tablename==None or not (tablename in RD.keys()):
				return dict(TableDef=None, SubTables=None)
			else:
				TD['TableName'] = tablename
				TD['ParentTable'] = parenttable
				TD['JoinType'] = jointype
				TD['LinkColumn'] = linkcolumn
				TD['JoinName'] = joinname
				try:
					TD['AltName'] = RD[parenttable][CD][joinname]['AltName']
				except KeyError:
					TD['AltName'] = joinname
				TD['Cols'] = self.GetColDefinitions(tablename,isSubTable=True)
			return TD
		#
		level = 1 # We start counting with the second level
		TD = AssignTD(tablename, linkcolumn, parenttable,jointype,joinname)
		Tdict = dict(TableDef=TD, SubTables=[])
		# Add Sub tables
		# NOTE: if the ReportDefinition has no columns to show for the sub-table, then the sub
		# table will be omitted from the list of sub-tables, and any sub-sub tables will also be
		# skipped
		LevelList = [[Tdict]]
		ParentST = None
		while level < MAX_LEVELS:
			LevelList.append([]) # Create a listing for the next level
			for td in LevelList[level-1]:
				# Create the table definitions with empty sub-tables for the next level
				currtable = td['TableDef']['TableName']
				MJs = self.ColsMultipleJoin(currtable)
				for col in MJs:
					#log.debug('JoinMethodName (col): %r' % col)
					nTdict = dict(TableDef=AssignTD(tablename=MJs[col]['Table'],linkcolumn=MJs[col]['LinkColumn'],
						parenttable=currtable,jointype="MultipleJoin",joinname=col),SubTables=[])
					td['SubTables'].append(nTdict)
					LevelList[level].append(nTdict)
				RJs = self.ColsRelatedJoin(currtable)
				for col in RJs:
					#log.debug('JoinMethodName (col): %r' % col)
					nTdict = dict(TableDef=AssignTD(tablename=RJs[col]['Table'],linkcolumn=col,parenttable=currtable,
						jointype="RelatedJoin",joinname=col),SubTables=[])
					td['SubTables'].append(nTdict)
					LevelList[level].append(nTdict)
			level += 1
		#log.debug('%r' % Tdict)
		return Tdict
		
	@expose(format='json')
	@identity.require(identity.not_anonymous())
	def GetSubTables(self, tablename=None, **kw):
		'''	Return a formatted list of sub-tables '''
		ST = []
		if tablename!=None:
			tablename = str(tablename)
		if tablename==None or not (tablename in self.TableList().keys()):
			return dict(SubTables=ST)
		else:
			MJs = self.ColsMultipleJoin(tablename)
			RJs = self.ColsRelatedJoin(tablename)
			for col in MJs:
				sTD = self.GetSubTableDefinition(MJs[col]['Table'],MJs[col]['LinkColumn'],tablename,"MultipleJoin",col)
				if sTD!=None and (sTD['TableDef']!=None) and len(sTD['TableDef']['Cols']) > 0:
					ST.append(sTD)
			for col in RJs:
				sTD = self.GetSubTableDefinition(RJs[col]['Table'],col,tablename,"RelatedJoin",col)
				if sTD!=None and (sTD['TableDef']!=None) and len(sTD['TableDef']['Cols']) > 0:
					ST.append(sTD)
			return dict(SubTables=ST)
		
	@expose(format='json')
	@identity.require(identity.not_anonymous())
	def GetTableDefinition(self, tablename=None, **kw):
		'''	Return a formatted table definition, including all sub tables (and their sub tables)
		'''
		TD = {}
		ST = []
		if tablename!=None:
			tablename = str(tablename)
		if tablename==None or not (tablename in self.TableList().keys()):
			return dict(TableDef=TD, SubTables=ST)
		else:
			TD['TableName'] = tablename
			TD['ParentTable'] = None
			TD['LinkColumn'] = None
			TD['JoinName'] = None
			TD['Cols'] = self.GetColDefinitions(tablename)
			# Add Sub tables
			MJs = self.ColsMultipleJoin(tablename)
			RJs = self.ColsRelatedJoin(tablename)
			for col in MJs:
				sTD = self.GetSubTableDefinition(MJs[col]['Table'],MJs[col]['LinkColumn'],tablename,"MultipleJoin",col)
				if sTD!=None and (sTD['TableDef']!=None) and len(sTD['TableDef']['Cols']) > 0:
					ST.append(sTD)
			for col in RJs:
				sTD = self.GetSubTableDefinition(RJs[col]['Table'],col,tablename,"RelatedJoin",col)
				if sTD!=None and (sTD['TableDef']!=None) and len(sTD['TableDef']['Cols']) > 0:
					ST.append(sTD)
			return dict(TableDef=TD, SubTables=ST)
	
	def GetMasterTable(self, QD):
		'''	Look for the Master table definition from within the QueryDefinition '''
		for table in QD['Tables']:
			if not table.has_key('ParentTable'):
				return table
		else:
			return None
	
	def GetDetailTables(self, QD, TableID):
		''' 	Find the listing of Table Definitions which are detail
			sections for the table called tablename
		'''
		DTs = []
		for table in QD['Tables']:
			if (table.has_key('ParentTableID') and table['ParentTableID'] == TableID):
				DTs.append(table)
		return DTs
	
	def ConvertDateTime(self, DT):
		'''	Convert the date time string into a date
			We sometimes have relative dates to
			convert to an actual date time value
		'''
		def DayMultiply(st):
			if st.lower == 'days':
				return 1
			elif st.lower == 'weeks':
				return 7
			elif st.lower == 'months':
				return 30
			elif st.lower == 'years':
				return 365
		sDT = DT.split(' ')
		if DT in ['', None]: # Empty
			return None
		elif DT[0].isdigit(): # Probably ISO date
			if len(DT) == 19:
				return datetime.fromtimestamp(time.mktime(time.strptime(DT,'%Y-%m-%d %H:%M:%S')))
			else:
				return datetime.fromtimestamp(time.mktime(time.strptime(DT[0:10],'%Y-%m-%d')))
		elif len(sDT) != 3: # Unknown format
			return None
		elif sDT[0].lower() in ['next','last']: # Process the relative date
			try:
				days = float(sDT[1]) * DayMultiply(sDT[2]) # calculate the number of days relative to today
				delta = timedelta(days=days)
			except:
				return None
			if sDT[0].lower() =='next':
				return datetime.now() + delta
			else:
				return datetime.now() - delta
		else: # Process the ISO date format
			try:
				return datetime.fromtimestamp(time.mktime(time.strptime(DT[0:10],'%Y-%m-%d')))
			except:
				return None
				
	def GetFilteredData(self, TD, IDs=[]):
		'''	Parse, construct, then execute the query returning a SQLObject
			select results.
			TD: Table definition (if it's a sub table, it is the detail section)
			IDs: Are the primary keys from the parent table which we need to link.  
				One or more.  Only required if we're processing a detail section.
		'''
		if (TD == None) or (not TD.has_key('TableName')): # If our table definition is empty
			return []
		table = TD['TableName']
		qVars = '' # Query statements to be ANDed together
		orVars = '' # Query statements to be ORed together
		for col in TD['Columns']:
			# Foreign keys and functions don't have filters. NOTE:  hidden columns can be used in filters
			if (not col['ColType'] in ['ForeignKey','Function']):
				if col['ColType'] == 'DateTime':
					qVars += self.DateTimeFilter(col)
				elif col['ColType'] == 'Numeric':
					qVars += self.NumericFilter(col)
				elif col['ColType'] == 'Text':
					qVars += self.TextFilter(col)
				elif col['ColType'] == 'Boolean':
					qVars += self.BooleanFilter(col)
		if TD.has_key('ParentTable'): # we're a sub table, we need to filter with the parent object
			if TD['JoinType'] == "MultipleJoin":
				qVars += "model.%s.q.%s==model.%s.q.id," % (table,TD['LinkColumn'],TD['ParentTable'])
				orVars = "OR ("
				log.debug('IDs: %r' % IDs)
				for id in IDs:
					orVars += "model.%s.q.id==%d," % (TD['ParentTable'],id)
				orVars = orVars[:-1] + "),"
				qVars += orVars
				#log.debug('Query Args: %s' % qVars)
			else: # RelatedJoin - it's tricky to get the id's in a related join situation because of the middle table problem
				# Create a list of IDs for the current table
				# First, select the rows from the parent table (often, just one)
				subIDs = []
				for id in IDs:
					# log.debug(' Table name: %s, Parent Table: %s, Join: %s, id: %d' % 
					#	(TD['TableName'],TD['ParentTable'],TD['LinkColumn'],id))
					row = eval("model.%s.get(%d)" % (TD['ParentTable'],id))
					# NOTE: LinkColumn for RelatedJoins refers to the Parent table's column
					for joinrow in eval('row.%s' % TD['LinkColumn']): 
						subIDs.append(joinrow.id)
				subIDs = set(subIDs) # remove duplicates
				orVars = ''
				if len(subIDs) > 0:
					orVars = "OR ("
					for id in subIDs:
						orVars += "model.%s.q.id==%d," % (table,id)
					orVars = orVars[:-1] + "),"
				if len(qVars) > 0:
					qVars += orVars
		# All filters are now applied, now run the select
		if len(qVars) > 0:
			log.debug("Query: model.%s.select(AND (%s))" % (table, qVars[:-1]))
			res = eval("model.%s.select(AND (%s))" % (table, qVars[:-1]))
		elif len(orVars) > 0:
			log.debug("Query: model.%s.select(%s)" % (table, orVars[:-1]))
			res = eval("model.%s.select(%s)" % (table, orVars[:-1])) # RelatedJoins with no other filters
		else:
			log.debug("Query: model.%s.select()" % table)
			res = eval("model.%s.select()" % table)
		list(res)
		return res
		
	def DateTimeFilter(self, CD):
		'''	Parse the date time column and return a filter if applicable '''
		FromDate = self.ConvertDateTime(CD['FromDate'])
		ToDate = self.ConvertDateTime(CD['ToDate'])
		neg = CD['NotFilter']
		empty = CD['NullFilter']
		table = CD['TableName']
		col = CD['ColName']
		# log.debug('FILTER: from date=%r, to date=%r' % (FromDate,ToDate))
		txt = ''
		argCount = 0 # This is used for the NOT operator, which only takes 1 argument at a time. if we have multiple argurements, then we need to do an  AND operation before the NOT
		if empty:
			txt = "model.%s.q.%s == None," % (table,col)
			argCount = 1
		elif FromDate == None and ToDate == None: # No filter
			return ''
		elif FromDate != None and ToDate != None: # Date between (inclusive)
			txt = "model.%s.q.%s >= '%s', model.%s.q.%s <= '%s'," % (table, col, FromDate.strftime('%Y-%m-%d'),table, col,ToDate.strftime('%Y-%m-%d'))
			argCount = 2
		elif FromDate != None: # Date greater than from date
			txt = "model.%s.q.%s >= '%s'," % (table, col, FromDate.strftime('%Y-%m-%d'))
			argCount = 1
		elif ToDate != None: # Date greater than from date
			txt = "model.%s.q.%s <= '%s'," % (table, col, ToDate.strftime('%Y-%m-%d'))
			argCount = 1
		if neg and len(txt)>0:
			if argCount == 1:
				return "NOT (%s)," % txt[:-1]
			else:
				return "NOT (AND (%s))," % txt[:-1]
		else:
			return txt
		
	def NumericFilter(self, CD):
		'''	Parse the Numeric column and return a filter if applicable '''
		try:
			neg = CD['NotFilter']
			empty = CD['NullFilter']
			if CD['GreaterThan'] != '':
				GT = float(CD['GreaterThan'])
			else:
				GT = None
			if CD['LessThan'] != '':
				LT = float(CD['LessThan'])
			else:
				LT = None
			table = CD['TableName']
			col = CD['ColName']
			txt = ''
			argCount = 0 # This is used for the NOT operator, which only takes 1 argument at a time. if we have multiple argurements, then we need to do an  AND operation before the NOT
			if empty:
				txt = "model.%s.q.%s == None," % (table,col)
				argCount = 1
			elif GT == None and LT == None: # No filter
				return ''
			elif GT != None and LT != None: # Date between (inclusive)
				txt = "model.%s.q.%s >= %d, model.%s.q.%s <= %d," % (table, col, GT, table, col,LT)
				argCount = 2
			elif GT != None: # Date greater than from date
				txt = "model.%s.q.%s >= %d," % (table, col, GT)
				argCount = 1
			elif LT != None: # Date greater than from date
				txt = "model.%s.q.%s <= %d," % (table, col,LT)
				argCount = 1
			if neg and len(txt)>0:
				if argCount == 1:
					return "NOT (%s)," % txt[:-1]
				else:
					return "NOT (AND (%s))," % txt[:-1]
			else:
				return txt
		except:
			return ''
	
	def TextFilter(self, CD):
		'''	Parse the Text column and return a filter if applicable '''
		try:
			neg = CD['NotFilter']
			empty = CD['NullFilter']
			if CD['TextFilter'] != '':
				text = str(CD['TextFilter'])
			else:
				text = None
			table = CD['TableName']
			col = CD['ColName']
			txt = ''
			if empty:
				txt = "OR (model.%s.q.%s == None, model.%s.q.%s == '')," % (table,col,table,col)
			elif text == None: # No filter
				return ''
			else: # filter data
				arText = text.split(',') # split the text by the comma and see if we have multiple filters (OR'd together)
				if len(arText) > 1:
					txt = 'OR ('
					for line in arText:
						txt += "model.%s.q.%s.contains('%s')," % (table,col,text)
					txt = txt[:-1] + '),'
				else:
					txt = "model.%s.q.%s.contains('%s')," % (table,col,text)
			if neg and len(txt)>0:
				return "NOT (%s)," % txt[:-1]
			else:
				return txt
		except:
			return ''
			
	def BooleanFilter(self, CD):
		'''	Parse the Numeric column and return a filter if applicable '''
		try:
			filter = CD['BoolFilter']
			table = CD['TableName']
			col = CD['ColName']
			neg = CD['NotFilter']
			empty = CD['NullFilter']
			txt = ''
			if empty:
				txt = "model.%s.q.%s == None," % (table,col)
			elif filter == 'No Filter': # No filter
				return ''
			else: # filter data
				txt = "model.%s.q.%s == %s," % (table,col,filter)
			if neg and len(txt)>0:
				return "NOT (%s)," % txt[:-1]
			else:
				return txt
		except:
			return ''
				
	def DataProcess(self, Results, TD):
		'''	Based on the Table definition, group, aggregate, total, sort
			the query results for the report.  NOTE:  if the table is marked
			hidden, then group all the data into one row automatically.
		'''
		if (TD == None) or (not TD.has_key('TableName')): # If our table definition is empty
			return None
		if Results.count() == 0:
			return []
		tablename = TD['TableName']
		ShowCols = []
		GroupingCols = []
		TypeCols = []
		SortingCols = []
		if Results.count() > 0:
			row1 = Results[0] # Get a sneak peak at the data.  Needed so we can determine the type of Functions and Foriegn keys
		else:
			row1 = None
		for col in TD['Columns']:
			if col['colvisible'] and not (col['ColType'] in ['RowDisplay','LoadSubTables','RemoveTable']):
				ShowCols.append(col)
				GroupingCols.append(col['Aggregate'])
				SortingCols.append(col['Sorting'])
				if col['ColType'] in ['ForeignKey','Function'] and (row1!=None):
					# We need to inspect the data to see the type, either numeric or text
					# NOTE: we have to be careful with foreign keys and make sure the value is not 'None'
					try:
						#log.debug('row1.%s' % col['ColName'])
						tempdata = eval('row1.%s' % col['ColName'])
					except AttributeError: # This error comes when we have a NoneType variable
						tempdata = None
					if isinstance(tempdata, (float, int)):
						TypeCols.append('Numeric')
					else:
						TypeCols.append('Text')
				elif col['ColType'] in ['ForeignKey','Function'] and (row1==None):
					TypeCols.append('Text')
				else:
					TypeCols.append(col['ColType'])
		# Add a definition column for the primary key (last column)
		GroupingCols.append('Normal')
		SortingCols.append('No Sorting')
		TypeCols.append('Integer')
		#log.debug('GroupingCols: %r' % GroupingCols)
		#log.debug('SortingCols: %r' % SortingCols)
		#log.debug('TypeCols: %r' % TypeCols)
		# Create our table data
		mtbl = MyTable(TypeCols=TypeCols, GroupingCols=GroupingCols, SortingCols=SortingCols, pkcol=-1,hidden=(not TD['rowvisible']))
		for row in Results:
			#Format our row of data
			frow = []
			for col,num in zip(ShowCols,range(len(ShowCols))):
				if ((col['ColType'] in ['ForeignKey','Function']) and TypeCols[num] == 'Text'):
					try:
						#log.debug('Convert (%s): row.%s' % (tablename, col['ColName']))
						frow.append('%r' % eval('row.%s' % col['ColName']))
					except AttributeError: # If our foreign key is "None"
						frow.append(None)
					except TypeError: #Some tuple type results won't convert... Arghh
						frow.append('Error in converting')
				elif col['ColType'] == 'DateTime':
					try:
						frow.append(eval('row.%s' % col['ColName']).strftime('%Y-%m-%d %H:%M:%S'))
					except AttributeError:
						frow.append(None)
				else:
					try:
						frow.append(eval('row.%s' % col['ColName']))
					except AttributeError:
						frow.append(None)
			frow.append(row.id) # add the id column to the end
			mtbl.AddRow(frow)
		mtbl.Compute()
		# Create our formatted table: a list of lists.  Like:
		# [ [tablename=t1, parenttable=None, 'Data', col1, col2, col3],
		#   [tablename=t2, parenttable=t1, 'Data', col1, col2,col3, col4, col5],
		#   [tablename=t3, parenttable=t2, 'Data', col1, col2, col3, col4],
		#   [tablename=t4, parenttable=t1, 'Data', col1],
		#   [tablename=t1, parenttable=None, 'Data', col1, col2, col3],
		#   [tablename=t3, parenttable=t2, 'Data', col1, col2, col3, col4],
		#   [tablename=t4, parenttable=t1, 'Data', col1],
		 #  [tablename=t1, parenttable=None, 'Total', col1, col2, col3],
		#   [tablename=t5, parenttable=None, 'Data', col1, col2,col3, col4, col5, col6],
		#   etc....
		# ]
		# Produce our formatted table, convert datetime types to datetime objects... in the next version
		Data = []
        #f.write('==================%s============================\n' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		for row in mtbl.data:
			if TD.has_key('ParentTableID'):
				Data.append([TD['TableID'],TD['ParentTableID'],'Data']+list(row))
			else:
				Data.append([TD['TableID'],None,'Data']+list(row))
		#	f.write('%r\n' % Data[-1])
		# Append the totals row
		if TD.has_key('ParentTable'):
			Data.append([TD['TableID'],TD['ParentTableID'],'Total']+mtbl.Totals)
		else:
			Data.append([TD['TableID'],None,'Total']+list(mtbl.Totals))
		#f.write('%r\n' % Data[-1])
		mtbl.Close()
		del(mtbl) # try to pursuade python to collect this garbage
		#f.close()
		return Data
		
	def GetDetailSection(self, QD, TD, IDs=[],depth=1):
		'''	Get the detail section for the current table definition (TD)
		'''
		# log.debug('%d of %d: %d' % (self.RecordCount, self.TotalRecords, self.iteration))
		SubData = self.DataProcess(self.GetFilteredData(TD,IDs), TD)
		sDetailTables = self.GetDetailTables(QD, TD['TableID'])
		self.TotalRecords += len(SubData)
		# Loop through the data of the master results, and inserting detail sections
		NewSubData = []
		for row in SubData:
			self.RecordCount += 1
			if row[2] == 'Data':
				ids = row[-1] # id's for filtering the detail sections
				NewSubData.append(row)
				for td in sDetailTables:
					sub_data = self.GetDetailSection(QD, td, ids,depth+1)
					if len(sub_data) > 0:
						NewSubData += sub_data
			if row[2] == 'Total':
				NewSubData.append(row)
		self.iteration += 1
		return NewSubData
	
	@expose(format='json')
	@identity.require(identity.not_anonymous())
	def ExecuteQuery(self, Query=None, **kw):
		'''	Parse and then execute the query, returning the results.
			Query: a serialized JSON object which we need to convert
		'''
		# self.iteration = 0
		QD = simplejson.loads(Query)
		# For Debugging purposes:
		#f = open('data.py','w')
		#p = pprint.PrettyPrinter(stream=f)
		#p.pprint(QD)
		#f.close()
		if str(Query) in ['{"Tables":[]}', "{'Tables':[]}"]:
			return dict(Data=None, Dfn=QD)
		# End of debugging file
		MT = self.GetMasterTable(QD)
		# log.debug('Execute Query: table: %s' % MT['TableName'])
		# Get the results for the Master table
		ReportData = self.DataProcess(self.GetFilteredData(MT), MT)
		self.TotalRecords = len(ReportData)
		# Make a list of reports recursively
		sDetailTables = self.GetDetailTables(QD, MT['TableID'])
		# f = open('datareport.py','w')
		# p = pprint.PrettyPrinter(stream=f)
		# p.pprint(ReportData)
		# f.close()
		# Loop through the data of the master results, and inserting detail sections
		NewReportData = []
		for row in ReportData:
			self.RecordCount += 1
			if row[2] == 'Data':
				ids = row[-1] # id's for filtering the detail sections
				NewReportData.append(list(row))
				for td in sDetailTables:
					sub_data = self.GetDetailSection(QD, td, ids,1)
					if len(sub_data) > 0:
						NewReportData += sub_data
			elif row[2] == 'Total':
				NewReportData.append(row)
		#log.debug('.....SAVING DATA')
		#f = open('datareport.py','w')
		#p = pprint.PrettyPrinter(stream=f)
		#p.pprint(NewReportData)
		#f.close()
		#log.debug('.....DATA SAVED')
		return dict(Data=NewReportData, Dfn=QD)
		
	@expose(format='json')
	@identity.require(identity.has_permission("report_editor"))
	def SaveQuery(self, Query=None, ReportName='', **kw):
		'''	Save the query definition (already serialized) to a file
		'''
		if str(Query) in ['{"Tables":[]}', "{'Tables':[]}"]:
			return dict(message="Error: No Query Definition to save")
		elif ReportName in ['', None]:
			return dict(message="Error: No Report Name for the definition")
		FileName = str(ReportName.replace(' ','_') + datetime.now().strftime('%Y%m%d%H%M%S.qry'))
		f = open('%snew/%s' % (ReportBaseDir, FileName),'w')
		f.write(Query)
		f.close()
		return dict(message="Report %s saved as %s in %s" % (ReportName, FileName, ReportBaseDir+'new/'))
	
	@expose(format='json')
	@identity.require(identity.has_permission("report_editor"))
	def DebugData(self, data):
		''' 	Used to debug the data the web browser is sending me.
			format the data and save it to a temporary file
		'''
		#QD = simplejson.loads(data)
		#f = open('data.py','w')
		#p = pprint.PrettyPrinter(stream=f)
		#p.pprint(QD)
		#f.close()
		return dict(success=True)
			
		
	@expose(template="turbocare.templates.UDReportBuilder")
	@identity.require(identity.has_permission("report_editor"))
	def Builder(self):
		tables = self.TableList()
		tablenames = tables.keys()
		tablenames.sort()
		return dict(title='User Defined Reports', tablenames=tablenames, tables=tables)

	@expose(template="turbocare.templates.UDReportEditor")
	@identity.require(identity.has_permission("report_editor"))
	def Editor(self):
		usersDir = self.getDirectories(ReportBaseDir)
		usersFiles= {}
		for direc in usersDir:
			log.debug("Directory name " +direc)
			usersFiles[direc]=self.getReport(ReportBaseDir,direc)
		log.debug(usersFiles)
		return dict(groups=usersDir,reports=[], title="Saved Reports")
	
	@expose(html='turbocare.templates.UDReportViewer')
	@identity.require(identity.not_anonymous())
	def index(self, **kw):
		usersDir = self.getDirectories(ReportBaseDir)
		usersFiles= {}
		for direc in usersDir:
			log.debug("Directory name " +direc)
			usersFiles[direc]=self.getReport(ReportBaseDir,direc)
		log.debug(usersFiles)
		return dict(groups=usersDir,reports=[], title="Saved Reports")
	
	def getDirectories(self,my_dir):
		try:
			file_list = os.listdir(my_dir)
		except:
			log.debug("No such directory "+ ReportBaseDir)
			return []
		#print file_list
		new_list=[]
		log.debug("Your Permissions are " + str(turbogears.identity.current.permissions))
		for name in file_list:
			if os.path.isdir(my_dir + "/" +name):
#				log.debug('Dir name is ' + name)
				#Check is user is in write group. 
				if name in turbogears.identity.current.permissions:
					new_list.append(name)
					log.debug('You are allowed ' + name)
		return new_list
		
	@expose(format='json')
	@identity.require(identity.not_anonymous())
	def LoadReportList(self, Group='', **kw):
		'''	Load the list of reports for a particular group '''
		return dict(reports=self.getReport(ReportBaseDir,Group))

	def getReport(self,basedir,direcory_name):
		log.debug("In "+direcory_name)
		new_list=[]
		file_list = os.listdir(basedir+"/" + direcory_name)
		for name in file_list:
			if name[0] != '.':
				new_list.append(name)
		return new_list
		
	@expose(format='json')
	@identity.require(identity.has_permission("report_editor"))
	def LoadSavedQuery(self, Group='', ReportFile='', **kw):
		'''	Load the specified report file, for editing.
		'''
		f = open(ReportBaseDir+Group+'/'+ReportFile,'r')
		Query = f.read()
		QD = simplejson.loads(Query)
		f.close()
		return dict(QD=QD)
		
	@expose(format='json')
	@identity.require(identity.not_anonymous())
	def ExecuteSavedQuery(self, Group='', ReportFile='', **kw):
		'''	Load the specified report file, then run the query.
		'''
		f = open(ReportBaseDir+Group+'/'+ReportFile,'r')
		Query = f.read()
		QD = simplejson.loads(Query)
		f.close()
		if str(Query) in ['{"Tables":[]}', "{'Tables':[]}"]:
			return dict(Data=None, Dfn=QD)
		# End of debugging file
		MT = self.GetMasterTable(QD)
		# Get the results for the Master table
		ReportData = self.DataProcess(self.GetFilteredData(MT), MT)
		self.TotalRecords = len(ReportData)
		# Make a list of reports recursively
		sDetailTables = self.GetDetailTables(QD, MT['TableID'])
		# Loop through the data of the master results, and inserting detail sections
		NewReportData = []
		for row in ReportData:
			self.RecordCount += 1
			if row[2] == 'Data':
				ids = row[-1] # id's for filtering the detail sections
				NewReportData.append(list(row))
				for td in sDetailTables:
					sub_data = self.GetDetailSection(QD, td, ids,1)
					if len(sub_data) > 0:
						NewReportData += sub_data
			elif row[2] == 'Total':
				NewReportData.append(row)
		return dict(Data=NewReportData, Dfn=QD)