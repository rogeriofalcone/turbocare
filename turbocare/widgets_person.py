from turbogears import widgets, validators, expose, paginate
from tgfklookup.widgets import AutoCompletingFKLookupField
from tgpaginate.widgets import AjaxPaginatedGrid
from model import Person, AddressCityTown, TypeEthnicOrig, dbReligion, DATE_FORMAT, InvCustomer, InvLocation
import logging

log = logging.getLogger("turbocare.controllers")

class PersonForm(widgets.WidgetsList):
	PersonID = widgets.HiddenField("PersonID")
	Title = widgets.TextField(label="Title")
	NameFirst = widgets.TextField(validator=validators.NotEmpty(), label="First Name")
	NameMiddle = widgets.TextField(label="Middle Name")
	NameLast = widgets.TextField(validator=validators.NotEmpty(), label="Last Name")
	DateBirth = widgets.CalendarDatePicker(name="DateBirth", label="Date of Birth", button_text="Date",
						field_class="calendardatepicker", format=DATE_FORMAT)
	AddrStr = widgets.TextField(label="Street Address")
	AddrZip = widgets.TextField(label="PIN Code")
	AddrCitytownNr = AutoCompletingFKLookupField(
			name = 'AddrCitytownNr',
			label='City (ID/Name)',  
			search_controller='CityFkSearch', 
			id_search_param='city_id',  
			text_search_param='city_name',
			#text_result_attr={'name':'AddrCitytownNr_text'},
			var_name='cities')
	Phone1Nr = widgets.TextField(label="Phone Number")
	Cellphone1Nr = widgets.TextField(label="Cell Number")
	Fax = widgets.TextField(label="Fax Number")
	Email = widgets.TextField(label="E-mail")

	Citizenship = widgets.TextField(label="Citizenship")
	SssNr = widgets.TextField(label="Social Security Number")
	NatIdNr = widgets.TextField(label="National ID")
	Citizenship = widgets.TextField(label="Citizenship")
	Occupation = widgets.TextField(label="Occupation")
	#Occupation = widgets.AutoCompleteField(name="Occupation",label="Occupation", search_controller="OccupationSearch",
	#                              search_param="occupation",result_name="occupations")
	Religion = widgets.SingleSelectField(name='Religion', label="Religion",   
					options=dbReligion,  
					default=1)
	CivilStatus = widgets.SingleSelectField(name='CivilStatus', label="Civil Status",   
					options=[('Unknown', "Unknown"),   
						('Single', "Single"),   
						('Married', "Married"),  
						('Divorced', "Divorced"),
						('Widow(er)',"Widow(er)")],  
					default=1)
	Sex = widgets.SingleSelectField(name="Sex", label="Gender",   
					options=[('U', "Unknown"),   
						('M', "Male"),   
						('F', "Female")],  
					default=1)
	EthnicOrig = AutoCompletingFKLookupField(
			name = 'EthnicOrig',
			label='Tribe (ID/Name)',  
			search_controller='EthnicOrigFkSearch', 
			id_search_param='tribe_id',  
			text_search_param='tribe_name',  
			var_name='tribes')

@expose(format='json')
def CityFkSearch(self, city_id = None, city_name = None, **kw):
	cities = []
	if city_name:
		search = AddressCityTown.select(AddressCityTown.q.Name.contains(str(city_name)))
		for city in search:
			cities.append((city.id, city.DisplayNameShort()))
	else:
		try:
			city = AddressCityTown.get(int(city_id))
			cities.append((city.id, city.DisplayNameShort()))
		except:
			pass
	return dict(cities=cities)

@expose(format='json')
def EthnicOrigFkSearch(self, tribe_id = None, tribe_name = None, **kw):
	tribes = []
	if tribe_name:
		search = TypeEthnicOrig.select(TypeEthnicOrig.q.Name.contains(str(tribe_name)))
		for tribe in search:
			tribes.append((tribe.id, tribe.Name))
	else:
		try:
			tribe = TypeEthnicOrig.get(int(tribe_id))
			tribes.append((tribe.id, tribe.Name))
		except:
			pass
	return dict(tribes=tribes)

	
@expose(format='json')
def OccupationSearch(self, occupation = None, **kw):
	occupations = []
	if occupation:
		search = Person.select(Person.q.Occupation.contains(str(occupation)),distinct=True)
		#log.debug("Occupation results %d" % search.count())
		for person in search:
			occupations.append(person.Occupation)
		# occupations = set(occupations)
	return dict(occupations=occupations)

class CustomerForm(widgets.WidgetsList):
	CustomerID = widgets.HiddenField()
	CreditAmount = widgets.TextField(label="Current Credit")
	Accounting = widgets.TextField(label="Accounting")
	InventoryLocation = AutoCompletingFKLookupField(
			name = 'InventoryLocation',
			label='Default Inventory Location',  
			search_controller='LocationSearch', 
			id_search_param='location_id',
			text_search_param='location_name',  
			var_name='locations')
	# Groups = RelatedJoin("InvGrpCustomer")
Receipts = widgets.DataGrid(#name='Receipts',
				fields=[('ID', lambda row: row[0]),  
					('Description', lambda row: row[1]),
					('Total', lambda row: row[2])],  
			    default=[])
Payments = widgets.DataGrid(#name='PaymentsGrid',
				fields=[('ID', lambda row: row[0]),  
					('Description', lambda row: row[1]),
					('Amount', lambda row: row[2])],  
				default = [])

@expose(format='json')  
def ReceiptSearch(self, PersonID=None, **kw):
	receipts = []
	if PersonID:
		try:
			person = Person.get(int(PersonID))
			customer = person.Customer[0]
			for receipt in customer.Receipts:
				receipts.append((receipt.id, '%d Items purchased on %s (%s)' % (receipt.CountPurchasedItems(), receipt.ModifyTime.strftime(DATE_FORMAT), receipt.StatusText()), receipt.TotalPaymentCalc()))
		except:
			log.debug("No receipts for person")
	return dict(headers = ['id','Description','Total'], rows=receipts)

@expose(format='json')  
@paginate('payments')  
def PaymentSearch(self, PersonID=None, **kw):
	payments = []
	if PersonID:
		try:
			person = Person.get(int(PersonID))
			customer = person.Customer[0]
			log.debug("Payments count %d" % len(customer.Payments))
			for payment in customer.Payments:
				payments.append((payment.id, '%s on %s' % (payment.Type(), payment.DatePaid.strftime(DATE_FORMAT)), payment.Amount))
		except:
			log.debug("No payments for person")
	return dict(payments=payments)

@expose(format='json')
def LocationSearch(self, location_id = None, location_name = None, **kw):
	locations = []
	if location_name:
		search = InvLocation.select(InvLocation.q.Name.contains(str(location_name)))
		for location in search:
			locations.append((location.id, location.Name))
	else:
		try:
			location = InvLocation.get(int(location_id))
			locations.append((location.id, location.Name))
		except:
			pass
	return dict(locations=locations)

class PersonellForm(widgets.WidgetsList):
	PersonellID = widgets.HiddenField("PersonellID")
	JobFunctionTitle = widgets.TextField(label="Job Title")
	DateJoin = widgets.CalendarDatePicker(name="DateJoin", label="Date of Joining", button_text="Date",
						field_class="calendardatepicker", format=DATE_FORMAT, default="")
	DateExit = widgets.CalendarDatePicker(name="DateExit", label="Date of Exit", button_text="Date",
						field_class="calendardatepicker", format=DATE_FORMAT, default="")
	ContractClass = widgets.TextField(label="Contract Class")
	ContractStart = widgets.CalendarDatePicker(name="ContractStart", label="Contract Start", button_text="Date",
						field_class="calendardatepicker", format=DATE_FORMAT, default="")
	ContractEnd = widgets.CalendarDatePicker(name="ContractEnd", label="Contract End", button_text="Date",
						field_class="calendardatepicker", format=DATE_FORMAT, default="")
	IsDischarged = widgets.CheckBox(name="IsDischarged", label="Is Discharged", attrs=dict(checked=None))
	PayClass = widgets.TextField(label="Pay Class")
	PayClassSub = widgets.TextField(label="Pay Sub-class")
	LocalPremiumId = widgets.TextField(label="Local premium id")
	TaxAccountNr = widgets.TextField(label="Tax account #")
	IrCode = widgets.TextField(label="IR Code")
	NrWorkday = widgets.TextField(label="Working days/week",validator=validators.Number())
	NrWeekhour = widgets.TextField(label="Working hours/day",validator=validators.Number())
	NrVacationDay = widgets.TextField(label="Vacation days/year",validator=validators.Number())
	MultipleEmployer = widgets.CheckBox(name="MultipleEmployer", label="Has Multiple employers", attrs=dict(checked=None))
	NrDependent = widgets.TextField(label="Number of Dependents",validator=validators.Number())
	
EmployeeEncounters = widgets.DataGrid(fields=[('ID', lambda row: row[0]),  
					('Description', lambda row: row[1]),
					('Amount', lambda row: row[2])],  
				default = [])

#               DateReg = DateTimeCol(dbName='date_reg',default=cur_date_time())
#               Name2 = widgets.TextField(validator=validators.NotEmpty(), label="Name (2nd)")
#               Name3 = widgets.TextField(validator=validators.NotEmpty(), label="Name (3rd)")
#               NameMaiden = StringCol(length=60,dbName='name_maiden', default=None)
#               NameOthers = StringCol(length=255,dbName='name_others', default=None)
#               BloodGroup = StringCol(length=2,dbName='blood_group', default=None)
#               AddrStrNr = StringCol(length=10,dbName='addr_str_nr', default=None)
#               AddrZip = StringCol(length=15,dbName='addr_zip', default=None)
#               AddrIsValid = BoolCol(dbName='addr_is_valid', default=None)
#               Phone1Code = StringCol(length=15, dbName='phone_1_code', default=None)
#               Phone2Code = StringCol(length=15, dbName='phone_2_code', default=None)
#               Phone2Nr = StringCol(length=35, dbName='phone_2_nr', default=None)
#               Cellphone2Nr = StringCol(length=35, dbName='cellphone_2_nr', default=None)
#               Photo = BLOBCol(dbName='photo', default=None)
#               PhotoFilename = StringCol(length=60,dbName='photo_filename', default=None)
#               OrgId = StringCol(length=60,dbName='org_id', default=None)

#               MotherPid = ForeignKey("Person", dbName='mother_pid', default=None)
#               FatherPid = ForeignKey("Person", dbName='father_pid', default=None)
#               ContactPerson = StringCol(length=255,dbName='contact_person', default=None)
#               ContactPid = ForeignKey("Person",dbName='contact_pid', default=None)
#               ContactRelation = StringCol(length=25,dbName='contact_relation', default=None)
#               DeathDate = DateCol(dbName='death_date', default=None)
#               DeathEncounterNr = ForeignKey("Encounter", dbName='death_encounter_nr', default=None)
#               DeathCause = StringCol(length=255,dbName='death_cause', default=None)
#               DeathCauseCode = StringCol(length=15,dbName='death_cause_code', default=None) # foreign key?
#               DateUpdate = DateTimeCol(dbName='date_update',default=cur_date_time())
#                = StringCol(length=60,dbName='occupation',default=None)