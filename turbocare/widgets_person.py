from turbogears import widgets, validators, expose
from tgfklookup.widgets import AutoCompletingFKLookupField
from model import Person, AddressCityTown, TypeEthnicOrig

class PersonForm(widgets.WidgetsList):
	
	PersonID = widgets.HiddenField("PersonID")
	Title = widgets.TextField(label="Title")
	NameFirst = widgets.TextField(validator=validators.NotEmpty(), label="First Name")
	NameMiddle = widgets.TextField(label="Middle Name")
	NameLast = widgets.TextField(validator=validators.NotEmpty(), label="Last Name")
	DateBirth = widgets.CalendarDatePicker("date_of_birth", label="Date of Birth", button_text="Date",field_class="calendardatepicker")
	AddrStr = widgets.TextField(label="Street Address")
	AddrZip = widgets.TextField(label="PIN Code")
	AddrCitytownNr = AutoCompletingFKLookupField(
		 name = 'AddrCitytownNr',
                 label='City (ID/Name)',  
                 search_controller='CityFkSearch', 
                 id_search_param='city_id',  
                 text_search_param='city_name',  
                 var_name='cities')
	Phone1Nr = widgets.TextField(label="Phone Number")
	Cellphone1Nr = widgets.TextField(label="Cell Number")
	Fax = widgets.TextField(label="Fax Number")
	Email = widgets.TextField(label="E-mail")
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

	
#		DateReg = DateTimeCol(dbName='date_reg',default=cur_date_time())
#	        Name2 = widgets.TextField(validator=validators.NotEmpty(), label="Name (2nd)")
#	        Name3 = widgets.TextField(validator=validators.NotEmpty(), label="Name (3rd)")
#		NameMaiden = StringCol(length=60,dbName='name_maiden', default=None)
#		NameOthers = StringCol(length=255,dbName='name_others', default=None)
#		BloodGroup = StringCol(length=2,dbName='blood_group', default=None)
#		AddrStrNr = StringCol(length=10,dbName='addr_str_nr', default=None)
#		AddrZip = StringCol(length=15,dbName='addr_zip', default=None)
#		AddrIsValid = BoolCol(dbName='addr_is_valid', default=None)
#		Citizenship = StringCol(length=35,dbName='citizenship', default=None)
#		Phone1Code = StringCol(length=15, dbName='phone_1_code', default=None)
#		Phone2Code = StringCol(length=15, dbName='phone_2_code', default=None)
#		Phone2Nr = StringCol(length=35, dbName='phone_2_nr', default=None)
#		Cellphone2Nr = StringCol(length=35, dbName='cellphone_2_nr', default=None)
#		Photo = BLOBCol(dbName='photo', default=None)
#		PhotoFilename = StringCol(length=60,dbName='photo_filename', default=None)
#		OrgId = StringCol(length=60,dbName='org_id', default=None)

#		SssNr = StringCol(length=60,dbName='sss_nr', default=None)
#		NatIdNr = StringCol(length=60,dbName='nat_id_nr', default=None)
#		Religion = StringCol(length=125,  default=None,dbName='religion')
#		MotherPid = ForeignKey("Person", dbName='mother_pid', default=None)
#		FatherPid = ForeignKey("Person", dbName='father_pid', default=None)
#		ContactPerson = StringCol(length=255,dbName='contact_person', default=None)
#		ContactPid = ForeignKey("Person",dbName='contact_pid', default=None)
#		ContactRelation = StringCol(length=25,dbName='contact_relation', default=None)
#		DeathDate = DateCol(dbName='death_date', default=None)
#		DeathEncounterNr = ForeignKey("Encounter", dbName='death_encounter_nr', default=None)
#		DeathCause = StringCol(length=255,dbName='death_cause', default=None)
#		DeathCauseCode = StringCol(length=15,dbName='death_cause_code', default=None) # foreign key?
#		DateUpdate = DateTimeCol(dbName='date_update',default=cur_date_time())
#		Occupation = StringCol(length=60,dbName='occupation',default=None)