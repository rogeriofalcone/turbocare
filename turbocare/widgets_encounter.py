from turbogears import widgets, validators, expose, paginate
from sqlobject import *
from tgfklookup.widgets import AutoCompletingFKLookupField
from tgpaginate.widgets import AjaxPaginatedGrid
from model import DATE_FORMAT, Encounter, TypeEncounter, ClassEncounter, ClassFinancial, InsuranceFirm, ClassInsurance, Person, Personell
from model import DATETIME_FORMAT
import logging

log = logging.getLogger("turbocare.controllers")

class EncounterFormPage1(widgets.WidgetsList):
	''' General Information '''
	PersonID = widgets.HiddenField("PersonID")
	EncounterDate = widgets.CalendarDatePicker(name="EncounterDate", label="Date of visit", button_text="Date",
						field_class="calendardatepicker", format=DATE_FORMAT)
	IsDischarged = widgets.CheckBox(name="IsDischarged", label="Is Discharged", attrs=dict(checked=None))
	DischargeDateTime = widgets.CalendarDateTimePicker(name="DischargeDateTime", label="Discharge date/time", button_text="Time",
						field_class="calendardatepicker", format=DATETIME_FORMAT)
	EncounterClassNr = AutoCompletingFKLookupField(
			name = 'EncounterClassNr',
			label='Type (in/out patient)',  
			search_controller='EncounterClassSearch', 
			id_search_param='encounter_class_id',
			text_search_param='encounter_class_name',  
			var_name='encounter_classes')
	EncounterType = widgets.SingleSelectField(name='EncounterType', label="Visit type",   
					options=[x.Name for x in TypeEncounter.select(distinct=True)],
					default=1)
	EncounterStatus = widgets.TextField(label="Encounter Status")
	ExtraService = widgets.TextField(label="Extra service")

#class EncounterFormPage2(widgets.WidgetsList):
#	''' Insurance Information '''
	FinancialClassNr = AutoCompletingFKLookupField(
			name = 'FinancialClassNr',
			label='Financial classification (private/common)',  
			search_controller='FinancialClassSearch', 
			id_search_param='financial_class_id',
			text_search_param='financial_class_name',  
			var_name='financial_classes')
	InsuranceNr = widgets.TextField(label="Insurance Number")
	InsuranceFirmId = widgets.SingleSelectField(name='InsuranceFirmId', label="Insurance Firm",   
					options=['None']+[x.Name for x in InsuranceFirm.select()],
					default=1)
	InsuranceClassNr = AutoCompletingFKLookupField(
			name = 'InsuranceClassNr',
			label='Insurance class',  
			search_controller='InsuranceClassSearch', 
			id_search_param='insurance_class_id',
			text_search_param='insurance_class_name',  
			var_name='insurance_classes')
	Insurance2Nr = widgets.TextField(label="Insurance Number 2")
	Insurance2FirmId = widgets.SingleSelectField(name='Insurance2FirmId', label="Insurance Firm 2",   
					options=['None']+[x.Name for x in InsuranceFirm.select()],
					default=1)

#class EncounterFormPage3(widgets.WidgetsList):
#	''' Doctor Notes '''
	ReferrerDiagnosis = widgets.TextField(label="Referrer Diagnosis")
	ReferrerRecomTherapy = widgets.TextField(label="Referrer recommended therapy")
	ReferrerDr = widgets.TextField(label="Referrer Doctor")
	ReferrerDept = widgets.TextField(label="Referrer Department")
	ReferrerInstitution = widgets.TextField(label="Referrer Institution")
	ReferrerNotes = widgets.TextArea(label="Referrer Notes",cols=40,rows=3)
	CurrentAttDrNr = AutoCompletingFKLookupField(
			name = 'CurrentAttDrNr',
			label='Current attending Doctor',  
			search_controller='DoctorSearch', 
			id_search_param='personell_id',
			text_search_param='personell_name',  
			var_name='doctors')
	ConsultingDr = widgets.TextField(label="Consulting Doctor")
	FollowupDate = widgets.CalendarDatePicker(name="FollowupDate", label="Followup Date", button_text="Date",
						field_class="calendardatepicker", format=DATE_FORMAT)
	FollowupResponsibility = widgets.TextArea(label="Followup Responsibility",cols=40,rows=3)
	PostEncounterNotes = widgets.TextArea(label="Post Visit Notes",cols=40,rows=3)

Receipts = widgets.DataGrid(#name='Receipts',
				fields=[('ID', lambda row: row[0]),  
					('Description', lambda row: row[1]),
					('Total', lambda row: row[2])],  
			    default=[])
EncounterLocations = widgets.DataGrid(#name='PaymentsGrid',
				fields=[('ID', lambda row: row[0]),  
					('Description', lambda row: row[1]),
					('Amount', lambda row: row[2])],  
				default = [])

		#GuarantorPid = ForeignKey("Person", dbName='guarantor_pid',default=None) - Not used
		#ContactPid = ForeignKey("Person", dbName='contact_pid',default=None) - We use the record on the Person table
		#ContactRelation = StringCol(length=35,dbName='contact_relation',default=None) - We use the field on the Person table
		#CurrentWardNr = ForeignKey('Ward',dbName='current_ward_nr',default=None) # care_encounter_location -> location_nr
		#CurrentRoomNr = IntCol(dbName='current_room_nr',default=None) # care_encounter_location -> location_nr
		#InWard = BoolCol(default=None,dbName='in_ward')
		#CurrentDeptNr = ForeignKey('Department',dbName='current_dept_nr',default=None) # care_encounter_location -> location_nr
		#InDept = BoolCol(default=False,dbName='in_dept')
		#CurrentFirmNr = IntCol(dbName='current_firm_nr',default=None) # Not Used

@expose(format='json')
def EncounterClassSearch(self, encounter_class_id = None, encounter_class_name = None, **kw):
	encounter_classes = []
	if encounter_class_name:
		search = ClassEncounter.select(ClassEncounter.q.Name.contains(str(encounter_class_name)))
		for encounter_class in search:
			encounter_classes.append((encounter_class.id, encounter_class.Name))
	else:
		try:
			encounter_class = ClassEncounter.get(int(encounter_class_id))
			encounter_classes.append((encounter_class.id, encounter_class.Name))
		except:
			pass
	return dict(encounter_classes=encounter_classes)

@expose(format='json')
def FinancialClassSearch(self, financial_class_id = None, financial_class_name = None, **kw):
	financial_classes = []
	if financial_class_name:
		search = ClassFinancial.select(AND (ClassFinancial.q.Name.contains(str(financial_class_name)), ClassFinancial.q.id > 8))
		for financial_class in search:
			financial_classes.append((financial_class.id, financial_class.Name))
	else:
		try:
			financial_class = ClassFinancial.get(int(financial_class_id))
			financial_classes.append((financial_class.id, financial_class.Name))
		except:
			pass
	return dict(financial_classes=financial_classes)

@expose(format='json')
def InsuranceFirmSearch(self, insurance_firm_id = None, insurance_firm_name = None, **kw):
	insurance_firms = []
	if insurance_firm_name:
		search = InsuranceFirm.select(InsuranceFirm.q.Name.contains(str(insurance_firm_name)))
		for insurance_firm in search:
			insurance_firms.append((insurance_firm.id, insurance_firm.Name))
	else:
		try:
			insurance_firm = InsuranceFirm.get(int(insurance_firm_id))
			insurance_firms.append((insurance_firm.id, insurance_firm.Name))
		except:
			pass
	return dict(insurance_firms=insurance_firms)

@expose(format='json')
def InsuranceClassSearch(self, insurance_class_id = None, insurance_class_name = None, **kw):
	insurance_classes = []
	if insurance_class_name:
		search = ClassInsurance.select(ClassInsurance.q.Name.contains(str(insurance_class_name)))
		for insurance_class in search:
			insurance_classes.append((insurance_class.id, insurance_class.Name))
	else:
		try:
			insurance_class = ClassInsurance.get(int(insurance_class_id))
			insurance_classes.append((insurance_class.id, insurance_class.Name))
		except:
			pass
	return dict(insurance_classes=insurance_classes)

@expose(format='json')
def DoctorSearch(self, personell_id = None, personell_name = None, **kw):
	doctors = []
	if personell_name:
		TextWords = personell_name.replace(',','').split()
		qArgs = ''
		if len(TextWords) == 3: #Try a first, middle, last name search
			qArgs+="AND ("
			qArgs+="Person.q.NameFirst.contains('"+ TextWords[0] + "'),"
			qArgs+="Person.q.NameMiddle.contains('"+ TextWords[1] + "'),"
			qArgs+="Person.q.NameLast.contains('"+ TextWords[2] + "')"
			qArgs+=")"
		if len(TextWords) == 2: #Try a first, last name search and vice versa
			qArgs+="OR (AND ("
			qArgs+=".Person.q.NameFirst.contains('"+ TextWords[0] + "'),"
			qArgs+="Person.q.NameLast.contains('"+ TextWords[1] + "')"
			qArgs+="), AND ("
			qArgs+="Person.q.NameFirst.contains('"+ TextWords[1] + "'),"
			qArgs+="Person.q.NameLast.contains('"+ TextWords[0] + "')"
			qArgs+="))"
		if len(TextWords) == 1: #Try a first or last name search
			qArgs+="OR ("
			qArgs+="Person.q.NameFirst.contains('"+ TextWords[0] + "'),"
			qArgs+="Person.q.NameLast.contains('"+ TextWords[0] + "')"
			qArgs+=")"
		search = eval('Personell.select(AND (Personell.q.JobFunctionTitle == "Doctor", Personell.q.PersonID == Person.q.id, %s))' % qArgs)
		for doctor in search:
			doctors.append((doctor.id, doctor.Person.DisplayNameAsContact()))
	else:
		try:
			doctor = Personell.get(int(personell_id))
			doctors.append((doctor.id, doctor.Person.DisplayNameAsContact()))
		except:
			pass
	return dict(doctors=doctors)

