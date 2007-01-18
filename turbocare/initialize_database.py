#
#	Initialize the TurboCare database with some required values
#
from sqlobject import *
import model
import datetime, time
from model import DATE_FORMAT

def AddDepartment(Loc):
	'''	Add a department entry for the location 
		Return the new department
	'''
	# First, search for a matching department
	departments = model.Department.select(model.Department.q.NameFormal==Loc.Name)
	if departments.count() == 0: # Create a new department
		Dept = model.Department(NameFormal=Loc.Name, Id=Loc.Name.replace(' ','_').lower(), 
			NameShort=Loc.Name, NameAlternate=Loc.Name, Description=Loc.Description)
		Loc.DepartmentID = Dept.id
	else: # Join the first entry (Normally, the formal name should be unique)
		Loc.DepartmentID = Dept.id
	return Dept

def InitCatalogItems():
	'''	TurboCare requires some types of rooms to be defined in the catalog for pricing purposes
		So I enter some default values for these... they can be changed later  though
	'''
	# 1. Look for InvGrpStock entries for services, patient
	Groups = model.InvGrpStock.select(model.InvGrpStock.q.Name=='Services')
	if Groups.count()==0:
		GrpService = model.InvGrpStock(Name='Services',Description='Services')
	else:
		GrpService = Groups[0]
	Groups = model.InvGrpStock.select(model.InvGrpStock.q.Name=='Patient')
	if Groups.count()==0:
		GrpPatient = model.InvGrpStock(Name='Patient',Description='Patient')
	else:
		GrpPatient = Groups[0]
	# 2. Look for a Services CatalogItem Header
	Items = model.InvCatalogItem.select(model.InvCatalogItem.q.Name=='Services')
	if Items.count() == 0:
		Service = model.CatalogItem(ParentItemID==None,Name='Services',Description='Hospital Services',IsService=True,IsSelectable=False,
			IsDispensable=False,IsFixedAsset=False, IsForSale=False, Tax=0.0,MinStockAmt=0.0, ReorderAmt=0.0)
		Service.addInvGrpStock(GrpService)
	else:
		Service = Items[0]
	# 3. Look for a Patient CatalogItem Header (under Services)
	Items = model.InvCatalogItem.select(AND (model.InvCatalogItem.q.Name=='Patient',model.InvCatalogItem.q.ParentItemID==Service.id))
	if Items.count() == 0:
		Patient = model.CatalogItem(ParentItemID==Service.id,Name='Patient',Description='Patient Services',IsService=True,IsSelectable=False,
			IsDispensable=False,IsFixedAsset=False, IsForSale=False, Tax=0.0,MinStockAmt=0.0, ReorderAmt=0.0)
		Patient.addInvGrpStock(GrpService)
		Patient.addInvGrpStock(GrpPatient)
	else:
		Patient = Items[0]
	# 4. Check for a 'MRD' Location
	Locations = model.InvLocation.select(model.InvLocation.q.Name=='MRD')
	if Locations.count() == 0:
		MRD = model.InvLocation(Name='MRD',Description='Medical Records Department', IsStore=False,CanReceive=False,CanSell=True,
			IsConsumed=False)
		AddDepartment(MRD)
	else:
		MRD = Locations[0]
	# 5. Look for Consultation Common, Consultation Common+Private, Consultation Private, Consultation Very Private, Nursing Common,
	# Nursing Common+Private, Nursing Private, Nursing Very Private, Room Common, Room Common+Private, Room Private, Room Very Private
	ItemNames = ['Consultation Common', 'Consultation Common+Private', 'Consultation Private', 'Consultation Very Private', 'Nursing Common',
		'Nursing Common+Private', 'Nursing Private', 'Nursing Very Private', 'Room Common', 'Room Common+Private', 'Room Private', 'Room Very Private']
	for item in ItemNames:
		Items = model.InvCatalogItem.select(AND (model.InvCatalogItem.q.Name==item,model.InvCatalogItem.q.ParentItemID==Patient.id))
		if Items.count() == 0:
			ServiceItem = model.CatalogItem(ParentItemID==Patient.id,Name=item,Description=item,IsService=True,IsSelectable=True,
				IsDispensable=False,IsFixedAsset=False, IsForSale=False, Tax=0.0,MinStockAmt=0.0, ReorderAmt=0.0)
			ServiceItem.addInvGrpStock(GrpService)
			ServiceItem.addInvGrpStock(GrpPatient)
		else:
			ServiceItem = Items[0]
		# Check for stock for the item
		if len(SercieItem.StockItems)==0:
			# Create some stock and place it in MRD
			ServiceStock = model.InvStockItem(Name=item,CatalogItemID=ServiceItem.id,PurchaseOrder=None,MRP=1.0,SalePrice=1.0,PurchasePrice=0.0,
				Quantity=1000)
			# Have stock all in the MRD department
			ServiceStockLocation = model.InvStockLocation(StockItemID=ServiceStock.id, LocationID=MRD.id,Quantity=1000,IsConsumed=False,IsSold=False)

#Insurance classes
CLASS_INSR = {'self_pay':3, 'private':1, 'charity':4, 'hospital':5}
CLASS_FIN = {'common':9,'private + common':10,'private':11,'private plus':12}
# types (in the future, load these values on startup)
TYPE_DISCHARGE = {'regular':1,'own':2,'emergeny':3,'change_ward':4,'change_room':5,'change_bed':6,'death':6,'change_dept':8}
TYPE_LOCATION = {'ward':2,'room':4,'bed':5,'clinic':6,'dept':1,'firm':3}	

def InitCareClasses():
	# Initialize ClassEncounter
	Classes = model.ClassEncounter.select(model.ClassEncounter.q.ClassId=='inpatient')
	if Classes.count()==0:
		NewClass = model.ClassEncounter(ClassId='inpatient',Name='Inpatient',LdVar='LDStationary',Description='Inpatient admission - stays at least in a ward and assigned bed')
	Classes = model.ClassEncounter.select(model.ClassEncounter.q.ClassId=='outpatient')
	if Classes.count()==0:
		NewClass = model.ClassEncounter(ClassId='outpatient',Name='Outpatient',LdVar='LDStationary',Description='Outpatient admission - does not stay in a ward nor assigned a bed')
	data = [('care_c','care','c','common','LDcommon',"Common nursing care services. (Non-private)","Patient with common health fund insurance policy."),
		('care_pc','care','p/c',"private + common",'LDprivatecommon',"Private services added to common services","Patient with common health fund insurance policy with additional private insurance policyOR self paying components."),
		('care_p','care','p','private','LDprivate',"Private nursing care services","Patient with private insurance policy OR self paying."),
		('care_pp','care','pp',"private plus",'LDprivateplus',"Very private nursing care services","Patient with private health insurance policy AND self paying components."),
		('room_c','room','c','common','LDcommon',"Common room services (non-private)","Patient with common health fund insurance policy."),
		('room_pc','room','p/c',"private + common",'',"Private services added to common services","Patient with common health fund insurance policy with additional private insurance policy OR self paying components."),
		('room_p','room','p','private','',"Private room services","Patient with private insurance policy OR self paying."),
		('room_pp','room','pp',"private plus",'',"Very private room services","Patient with private health insurance policy AND self paying components."),
		('att_dr_c','att_dr','c','common','',"Common clinician services","Patient with common health fund insurance policy."),
		('att_dr_pc','att_dr','p/c',"private + common",'',"Private services added to common clinician services","Patient with common health fund insurance policy with additional private insurance policy OR self paying components."),
		('att_dr_p','att_dr','p','private','',"Private clinician services","Patient with private insurance policy OR self paying."),
		('att_dr_pp','att_dr','pp',"private plus",'',"Very private clinician services","Patient with private health insurance policy AND self paying components.")]
	for FinClass in data:
		Classes = model.ClassFinancial.select(model.ClassFinancial.q.ClassId==FinClass[0])
		if Classes.count()==0:
			NewClass = model.ClassFinancial(ClassId='outpatient',Name='Outpatient',LdVar='LDStationary',Description='Outpatient admission - does not stay in a ward nor assigned a bed')
