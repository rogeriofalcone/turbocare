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
from turbogears.toolbox.catwalk import CatWalk 
import model
import datetime, time
from model import DATE_FORMAT
import model_inventory
import inventory_catalogitem
from printer_inventory import *

log = logging.getLogger("turbocare.controllers")
conn = model.hub.getConnection()

class Registration(turbogears.controllers.Controller):
#===== Inventory App Stuff ====================================================
	@expose(html='turbocare.templates.registration_search')
	def index(self, **kw):
		return dict(title="Registration Search")

	@expose(html='turbocare.templates.programmingerror')
	def idFail(error):
		error= "Not Permited to do operation"
		log.debug(error)
		next_link = "/billing/"
		return dict(error_message = error, next_link=next_link)

	@expose(html='turbocare.templates.programmingerror')
	def ProgrammingError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		if next_link == '':
			next_link = "/billing/"
		return dict(error_message = error, next_link=next_link)

	@expose(html='turbocare.templates.dataentryerror')
	def DataEntryError(self, error='', next_link = '', **kw):
		if error == '':
			error = "Unknown Error"
		if next_link == '':
			next_link = "/billing/"
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

	@expose(format='json')
	def RegistrationCityTownSearch(self, CityTownName='', PostOffice='', Block='', District='', State='', Country='',  **kw):
		'''	Search for Addresses (by Block, City/Town, District, State)
		'''
		qArgs = ''
		if CityTownName != '':
			qArgs+="model.AddressCityTown.q.Name.contains('"+ CityTownName + "'),"
		if PostOffice != '':
			qArgs+="model.AddressCityTown.q.ZipCode.contains('"+ PostOffice + "'),"
		if District != '':
			qArgs+="model.AddressCityTown.q.District.contains('"+ District + "'),"
		if State != '':
			qArgs+="model.AddressCityTown.q.State.contains('"+ State + "'),"
		if Country != '':
			qArgs+="model.AddressCityTown.q.IsoCountryId.contains('"+ Country + "'),"
		if Block != '':
			qArgs+="model.AddressCityTown.q.Block.contains('"+ Block + "'),"
		if len(qArgs) > 0:
			log.debug('Query String [Args]: model.AddressCityTown.select(AND (%s))' % qArgs[:-1])
			items = eval('model.AddressCityTown.select(AND (%s))' % qArgs[:-1])
		else:
			items = []
		Results = []
		for item in items:
			Text = '(id:%d) %s' % (item.id, item.DisplayName())
			Results.append(dict(id=item.id,text=Text,city_town_name=item.Name, post_office=item.ZipCode, \
				district=item.District, state=item.State, country=item.IsoCountryId, block=item.Block))
		return dict(result_count=len(Results), results=Results, city_town_name=CityTownName, post_office=PostOffice,\
			block=Block, district=District, state=State, country=Country)
		
	
	@expose(format='json')
	def RegistrationSearch(self, SearchText='', SearchAddress='', **kw):
		'''	Search for patients which match the criteria specified
			SearchText searches First, Middle and Last name fields
				if a SearchText value is a number, it is assumed to be a customer id
				An "OR" operation is done on all
		'''
		TextWords = SearchText.replace(',','').split()
		AddressWords = SearchAddress.replace(',','').split()
		qArgs = ""
		qAddr = ''
		IsDigit = False
		if not (SearchText in [None, '']):
			# Look for a number, which we'll use for an id search
			for word in TextWords:
				if word.isdigit():
					if len(word) == 18:#then it's a patient id
						return dict(url_var="PatientID=%d" % int(word))
					else: #It's a customer id
						return dict(url_var="CustomerID=%d" % int(word))
					IsDigit = True
					break;
			# Look for First, middle last name
			if not IsDigit:
				if len(TextWords) == 3: #Try a first, middle, last name search
					qArgs+="AND ("
					qArgs+="model.Person.q.NameFirst.contains('"+ TextWords[0] + "'),"
					qArgs+="model.Person.q.NameMiddle.contains('"+ TextWords[1] + "'),"
					qArgs+="model.Person.q.NameLast.contains('"+ TextWords[2] + "')"
					qArgs+="),"
				if len(TextWords) == 2: #Try a first, last name search and vice versa
					qArgs+="OR (AND ("
					qArgs+="model.Person.q.NameFirst.contains('"+ TextWords[0] + "'),"
					qArgs+="model.Person.q.NameLast.contains('"+ TextWords[1] + "')"
					qArgs+="), AND ("
					qArgs+="model.Person.q.NameFirst.contains('"+ TextWords[1] + "'),"
					qArgs+="model.Person.q.NameLast.contains('"+ TextWords[0] + "')"
					qArgs+=")),"
				if len(TextWords) == 1: #Try a first or last name search
					qArgs+="OR ("
					qArgs+="model.Person.q.NameFirst.contains('"+ TextWords[0] + "'),"
					qArgs+="model.Person.q.NameLast.contains('"+ TextWords[0] + "')"
					qArgs+="),"
		if not (SearchAddress in [None, '']) and not IsDigit:
			if len(AddressWords) > 0:
				qAddr = "model.Person.q.AddrCitytownNrID == model.AddressCityTown.q.id,"
				qAddr += "OR ("
				for word in AddressWords:
					qAddr+="model.AddressCityTown.q.Name.contains('"+ word + "'),"
					qAddr+="model.AddressCityTown.q.Block.contains('"+ word + "'),"
					qAddr+="model.AddressCityTown.q.District.contains('"+ word + "')"
				qAddr += '),'
		if len(qArgs) > 0 and len(qAddr) > 0:
			log.debug('Query String [Addr, Args]: model.Person.select(AND (%s %s))' % (qArgs, qAddr[:-1]))
			items = eval('model.Person.select(AND (%s %s))' % (qArgs, qAddr[:-1]))
		elif len(qArgs) > 0:
			log.debug('Query String [Args]: model.Person.select(%s)' % qArgs[:-1])
			items = eval('model.Person.select(%s)' % qArgs[:-1])
		elif len(qAddr) > 0:
			log.debug('Query String [Addr]: model.Person.select(AND (%s))' % qAddr[:-1])
			items = eval('model.Person.select(AND (%s))' % qAddr[:-1])
		else:
			log.debug('Query String: NONE')
			items = []
		results = []
		try:
			log.debug('%d items found' % items.count())
		except:
			log.debug('0 items found')
		for item in items:
			results.append(dict(id=item.id, text=item.DisplayName()))		
		return dict(results=results, result_count=len(results))
	
	def GetDefaultCustomerLocationID(self):
		'''	When moving inventory to a location where it's sold, we need to mark the new location as the customer
			location.  Most customers should have a location already defined, but we need
			a default just in case
		'''
		items = model.InvLocation.select(model.InvLocation.q.Name.contains('Customer'))
		if items.count() > 0:
			return items[0].id
		else:
			return None
	
	
	def RegistrationPatientLoad(self, PatientID='', CustomerID=''):
		'''	Either load patient data, or create a blank form for data entry
			to add new patient to the system
		'''
		# Attempt to load patient information, customerid will take precedence
		log.debug('RegistrationPatientLoad, PatientID: %s, CustomerID: %s' % (PatientID, CustomerID))
		patient = None
		customer = None
		if CustomerID != '':
			try:
				customer = model.InvCustomer.get(int(CustomerID))
				patient = model.Person.get(customer.ExternalID)
				CustomerID = customer.id
			except:
				raise
		elif PatientID != '':
			try:
				patient = model.Person.get(int(PatientID))
				#Search for the customer record for the patient (to get financial information)
				customers = model.InvCustomer.select(AND (model.InvCustomer.q.ExternalID == patient.id, \
					model.InvCustomer.q.Status != 'deleted'))
				if customers.count() == 0:
					#if the patient doesn't have a customer record, create one
					log.debug('....Creating customer record')
					if patient.AddrCitytownNrID == 0:
						patient.AddrCitytownNrID = None
					if patient.AddrCitytownNrID == None:
						AddressLabel = 'No Address Provided'
					else:
						AddressLabel = '%s\n%s\n%s, %s\n%s\n%s' % (patient.AddrStr, patient.AddrCitytownNr.Name, patient.AddrCitytownNr.Block, \
							patient.AddrCitytownNr.District, patient.AddrCitytownNr.State, patient.AddrCityTownNr.ZipCode)
					PatientName = ('%s %s,%s,%s' % (patient.Title, patient.NameFirst, patient.NameMiddle, patient.NameLast)).replace(',,',',').replace(',', ' ').strip()
					customer = model.InvCustomer(Name=PatientName ,Phone1=patient.Phone1Nr , Phone2=patient.Phone2Nr , Fax=patient.Fax , \
						EMail1=patient.Email , CityID=patient.AddrCitytownNrID , AddressLabel=AddressLabel, CreditAmount=0.0, \
						InventoryLocation=self.GetDefaultCustomerLocationID(), ExternalID=patient.id)
					CustomerID = customer.id
				else:
					#Attach to the first matching customer record
					log.debug('....loading customer record')
					customer = customers[0]
					CustomerID = customer.id
			except:
				raise
		if patient == None:
			NameFirst = ''
			NameMiddle = ''
			NameLast = ''
			AddressStreet = ''
			AddrCitytownNrID = ''
			CityTownName = ''
			PostOffice = ''
			Block = ''
			District = ''
			State = ''
			Country = ''
			PatientID=''
			Age=''
			DateBirth=''
			SelectedCity = 'No City Selected'
		else:
			NameFirst = patient.NameFirst
			NameMiddle = patient.NameMiddle
			NameLast = patient.NameLast
			AddressStreet = patient.AddrStr
			if patient.AddrCitytownNrID == 0:
				patient.AddrCitytownNrID = None
			AddrCitytownNrID = patient.AddrCitytownNrID
			if AddrCitytownNrID == None:
				CityTownName = ''
				PostOffice = ''
				Block = ''
				District = ''
				State = ''
				Country = ''
			else:
				CityTownName = patient.AddrCitytownNr.Name
				PostOffice = patient.AddrCitytownNr.ZipCode
				Block = patient.AddrCitytownNr.Block
				District = patient.AddrCitytownNr.District
				State = patient.AddrCitytownNr.State
				Country = patient.AddrCitytownNr.IsoCountryId
			DateBirth = patient.DateBirth.strftime(DATE_FORMAT)
			if AddrCitytownNrID == None:
				SelectedCity = 'No city selected'
			else:
				SelectedCity = '(id:%d) %s in %s, %s (%s)' % (AddrCitytownNrID, Block, CityTownName, \
					District, PostOffice)
			PatientID = patient.id
		# Load the latest encounter information (this contains patient type information)
		if patient == None:
			encounter = None
		else:
			try:
				encounter = model.Encounter.get(patient.GetLatestEncounter())
			except AssertionError:
				#AssertionError when patient.GetLatestEncounter() returns "None"
				encounter = None
			except:
				raise
				encounter = None
		if encounter == None:
			InsuranceNumber = ''
		else:
			InsuranceNumber = encounter.InsuranceNr
		# Load our patient types: similar to titles
		PatientType = ''
		if encounter != None:
			PatientType = encounter.InsuranceClassNrID
		else:
			PatientType = 3 # 3=self_pay
		patienttypes = []
		items = model.ClassInsurance.select()
		for patienttype in items:
			if patienttype.id == PatientType:
				patienttypes.append(dict(id=patienttype.id, name=patienttype.Name, selected='selected'))
			else:
				patienttypes.append(dict(id=patienttype.id, name=patienttype.Name, selected=None))
		# Load our firm names: similar to titles
		FirmID = ''
		if encounter != None:
			FirmID = encounter.InsuranceFirmId
		firms=[]
		items = model.InsuranceFirm.select()
		for firm in items:
			if firm.FirmId == FirmID:
				firms.append(dict(id=firm.FirmId, name=firm.Name, selected='selected'))
			else:
				firms.append(dict(id=firm.FirmId, name=firm.Name, selected=None))
		# Load our titles: we need title.name and title.selected (where title.selected = 'selected' for the patient's title)
		Title = ''
		if patient != None:
			Title = patient.Title
		items=['Ms.', 'Mrs.', 'Mr.', 'Dr.']
		titles=[]
		for title in items:
			if title == Title:
				titles.append(dict(id=title, name=title, selected='selected'))
			else:
				titles.append(dict(id=title, name=title, selected=None))
		# Load our genders: similar to titles
		Gender = ''
		#Care2x wants lower case variables -- sheesh.
		if patient != None:
			patient.Sex = patient.Sex.lower()
			Gender = patient.Sex
		else:
			Gender = 'u'
		items=['U','F','M']
		genders=[]
		for gender in items:
			if gender == Gender.upper():
				genders.append(dict(id=gender, name=gender, selected='selected'))
			else:
				genders.append(dict(id=gender, name=gender, selected=None))		
		# Load our religions: similar to titles
		Religion = ''
		if patient != None:
			Religion = patient.Religion
		else:
			Religion = 'Unknown'
		items=['Christian', 'Hindu', 'Muslim', 'Scientology', 'Unknown']
		religions=[]
		for religion in items:
			if religion == Religion:
				religions.append(dict(id=religion, name=religion, selected='selected'))
			else:
				religions.append(dict(id=religion, name=religion, selected=None))
		# Load our tribes: similar to titles *****************************************************STILL UNFINISHED
		Tribe = ''
		items=['option1', 'option2', 'option3']
		tribes=[]
		for tribe in items:
			if tribe == Tribe:
				tribes.append(dict(id=tribe, name=tribe, selected='selected'))
			else:
				tribes.append(dict(id=tribe, name=tribe, selected=None))
		# Load previous registration information
		History = []
		if customer != None:
			History.append('Name: %s' % customer.Name)
			PastDues = customer.CalcPayment() - customer.CalcPaid()
			if PastDues > 0:
				History.append('Past dues: %d' % PastDues)
			elif PastDues == 0:
				History.append('Past dues: None')
			else:
				History.append('Credit: %d' % abs(PastDues))
			if encounter != None:
				History.append('Last visit: %s' % encounter.EncounterDate.strftime(DATE_FORMAT))
				History.append('Visit count: %d' % len(patient.Encounters))
				if encounter.EncounterDate.strftime(DATE_FORMAT) == datetime.datetime.now().strftime(DATE_FORMAT):
					History.append('Already registered today')
				elif (encounter.EncounterClassNr.Name == 'Inpatient') and (not encounter.IsDischarged):
					History.append('Currently admitted')
		else:
			History.append('NEW PATIENT')
		# Calculate the age in years (using the days between, plus 1/2 a day)
		if DateBirth != '':
			Age = int(((datetime.datetime.now().date() - patient.DateBirth).days+0.5)/365.25)
		else:
			Age = ''
		return dict(tribes=tribes, titles=titles,genders=genders,religions=religions,firms=firms, patienttypes=patienttypes,\
			InsuranceNumber=InsuranceNumber,NameFirst=NameFirst,NameMiddle=NameMiddle,NameLast=NameLast,\
			AddressStreet=AddressStreet,AddrCitytownNrID=AddrCitytownNrID,CityTownName=CityTownName,PostOffice=PostOffice,\
			Block=Block,District=District,State=State,Country=Country, history=History, SelectedCity=SelectedCity,\
			PatientID=PatientID, CustomerID=CustomerID, DateBirth=DateBirth, Age=Age)			
	
	@expose(html='turbocare.templates.registration_patient_page1')
	@identity.require(identity.has_permission("reg_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def RegistrationPage1Reload(self, Tribe='', Title='', Gender='', Religion='', Firm='', PatientType='', \
			InsuranceNumber='', NameFirst='', NameMiddle='', NameLast='', AddressStreet='',\
			AddrCitytownNrID='',PatientID='', CustomerID='', DateBirth='', **kw):
		'''	Normally called if we get an error and we want to re-do the page.
			Majority of errors should be missing a required entry
		'''
		'''	Either load patient data, or create a blank form for data entry
			to add new patient to the system
		'''
		# Attempt to load patient information, customerid will take precedence
		log.debug('RegistrationPage1Reload')
		patient = None
		customer = None

		if AddrCitytownNrID == '':
			AddrCitytownNrID = ''
			CityTownName = ''
			PostOffice = ''
			Block = ''
			District = ''
			State = ''
			Country = ''
			PatientID=''
			SelectedCity = 'No City Selected'
		else:
			address = model.AddressCityTown.get(AddrCitytownNrID)
			CityTownName = address.Name
			PostOffice = address.ZipCode
			Block = address.Block
			District = address.District
			State = address.State
			Country = address.IsoCountryId
			SelectedCity = '(id:%s) %s in %s, %s (%s)' % (AddrCitytownNrID, Block, CityTownName, \
				District, PostOffice)
		# Figure out the age
		if DateBirth=='':
			Age = None
		else:
			Age = int(((datetime.datetime.now().date() - patient.DateBirth).days+0.5)/365.25)
		# Load our patient types: similar to titles
		log.debug(PatientType)
		if PatientType == '':
			PatientType = 3 #3=self_pay
		patienttypes = []
		items = model.ClassInsurance.select()
		for patienttype in items:
			if patienttype.id == PatientType:
				patienttypes.append(dict(id=patienttype.id, name=patienttype.Name, selected='selected'))
			else:
				patienttypes.append(dict(id=patienttype.id, name=patienttype.Name, selected=None))
		# Load our firm names: similar to titles
		firms=[]
		items = model.InsuranceFirm.select()
		for firm in items:
			if firm.FirmId == Firm:
				firms.append(dict(id=firm.FirmId, name=firm.Name, selected='selected'))
			else:
				firms.append(dict(id=firm.FirmId, name=firm.Name, selected=None))
		# Load our titles: we need title.name and title.selected (where title.selected = 'selected' for the patient's title)
		items=['Ms.', 'Mrs.', 'Mr.', 'Dr.']
		titles=[]
		for title in items:
			if title == Title:
				titles.append(dict(id=title, name=title, selected='selected'))
			else:
				titles.append(dict(id=title, name=title, selected=None))
		# Load our genders: similar to titles
		if Gender == '':
			Gender = 'U'
		items=['U','F','M']
		genders=[]
		for gender in items:
			if gender == Gender:
				genders.append(dict(id=gender, name=gender, selected='selected'))
			else:
				genders.append(dict(id=gender, name=gender, selected=None))		
		# Load our religions: similar to titles
		if Religion == '':
			Religion = 'Unknown'
		items=['Christian', 'Hindu', 'Muslim', 'Scientology', 'Unknown']
		religions=[]
		for religion in items:
			if religion == Religion:
				religions.append(dict(id=religion, name=religion, selected='selected'))
			else:
				religions.append(dict(id=religion, name=religion, selected=None))
		# Load our tribes: similar to titles *****************************************************STILL UNFINISHED
		items=['option1', 'option2', 'option3']
		tribes=[]
		for tribe in items:
			if tribe == Tribe:
				tribes.append(dict(id=tribe, name=tribe, selected='selected'))
			else:
				tribes.append(dict(id=tribe, name=tribe, selected=None))
		# Load previous registration information
		History = []
		History.append('NEW PATIENT')		
		return dict(tribes=tribes, titles=titles,genders=genders,religions=religions,firms=firms, patienttypes=patienttypes,\
			InsuranceNumber=InsuranceNumber,NameFirst=NameFirst,NameMiddle=NameMiddle,NameLast=NameLast,\
			AddressStreet=AddressStreet,AddrCitytownNrID=AddrCitytownNrID,CityTownName=CityTownName,PostOffice=PostOffice,\
			Block=Block,District=District,State=State,Country=Country, history=History, SelectedCity=SelectedCity,\
			PatientID=PatientID, CustomerID=CustomerID, DateBirth=DateBirth, Age=Age)			

	#	Step 1: Enter/Update Primary patient information
	@expose(html='turbocare.templates.registration_patient_page1')
	
	def RegistrationPage1(self, PatientID='', CustomerID='', **kw):
		'''	When loading the patient from a link or redirection, then this function is called
		'''
		return self.RegistrationPatientLoad(PatientID, CustomerID)
		
	@expose(format='json')
	def RegistrationPage1Ajson(self, PatientID='', CustomerID='', **kw):
		'''	When loading a patient using a barcode scanner within the page,
			this function is called.
		'''
		return self.RegistrationPatientLoad(PatientID, CustomerID)

	#	Step 2: Save (create/update) information from page 1, and prepare page 2
	@validate(validators={'Tribe':validators.String(),'Title':validators.String(), 'Gender':validators.String(), \
	'Religion':validators.String(),'Firm':validators.String(), 'PatientType':validators.String(), \
	'InsuranceNumber':validators.String(),'NameFirst':validators.String(), 'NameMiddle':validators.String(), \
	'NameLast':validators.String(),'AddressStreet':validators.String(), 'AddrCitytownNrID':validators.Int(), \
	'PatientID':validators.String(),'CustomerID':validators.String(), 'CityTownName':validators.String(), \
	'PostOffice':validators.String(),'Block':validators.String(), 'District':validators.String(), \
	'State':validators.String(),'Country':validators.String(), 'DateBirth':validators.String(), \
	'Age':validators.String()})
	@expose(html='turbocare.templates.registration_patient_page2')
	@identity.require(identity.has_permission("reg_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def RegistrationPage1Save(self, Tribe='', Title='', Gender='', Religion='', Firm='', PatientType='', \
			InsuranceNumber='', NameFirst='', NameMiddle='', NameLast='', AddressStreet='',\
			AddrCitytownNrID=None,PatientID='', CustomerID='', CityTownName='', PostOffice='',\
			Block='', District='', State='', Country='', DateBirth='', Age='', **kw):
		'''	Update or Add new patient (and customer) record.  Load the information for the next screen
			in the series for new patient data entry.
			1. Create/update a patient and customer record
			2. Check for a current encounter, either the patient registered that day or they are an inpatient
				otherwise, create a new encounter
			3. Create a new receipt
		'''
		# Check if all required inputs have been entered, if not, then redirect
		try:
			if Title=='':
				turbogears.flash('You need to enter a Title')
				raise ValueError
			if PatientType=='1' and Firm=='':
				turbogears.flash('You need to enter an Insurance Firm')
				raise ValueError
			if PatientType=='1' and InsuranceNumber=='':
				turbogears.flash('You need to enter an Insurance number')
				raise ValueError
			log.debug(NameFirst)
			if NameFirst=='':
				log.debug('Raising a value error')
				turbogears.flash('You need to enter a first name')
				raise ValueError
			if NameLast=='':
				turbogears.flash('You need to enter a last name')
				raise ValueError
			if AddrCitytownNrID==None:
				turbogears.flash('You need to select a city/town/area')
				raise ValueError
			if Age=='' or (int(Age)<0):
				turbogears.flash('The age cannot be empty or negative')
				raise ValueError
		except ValueError:
			log.debug('ValueError successfully raised')
			if PatientID != '':
				log.debug('redirecting to Registration page 1 using the patient id')
				raise cherrypy.HTTPRedirect('RegistrationPage1?PatientID=%s' % PatientID)
			elif CustomerID != '':
				log.debug('redirecting to Registration page 1 using the customer id')
				raise cherrypy.HTTPRedirect('RegistrationPage1?CustomerID=%s' % CustomerID)
			else:#NameMiddle=NameMiddle
				if AddrCitytownNrID==None:
					raise cherrypy.HTTPRedirect('RegistrationPage1Reload?Tribe=%s&Title=%s&Gender=%s&Religion=%s&Firm=%s&PatientType=%s&InsuranceNumber=%s&NameFirst=%s&NameLast=%s&AddressStreet=%s&DateBirth=%s&Age=%s' \
						% (Tribe, Title,Gender,Religion,Firm, PatientType,InsuranceNumber,NameFirst,NameLast,AddressStreet,DateBirth,Age) )
				else:
					raise cherrypy.HTTPRedirect('RegistrationPage1Reload?Tribe=%s&Title=%s&Gender=%s&Religion=%s&Firm=%s&PatientType=%s&InsuranceNumber=%s&NameFirst=%s&NameLast=%s&AddressStreet=%s&AddrCitytownNrID=%d&DateBirth=%s&Age=%s' \
						% (Tribe, Title,Gender,Religion,Firm, PatientType,InsuranceNumber,NameFirst,NameLast,AddressStreet,AddrCitytownNrID,DateBirth,Age) )
		# Create new/update entry [Patient and Customer record]
		if PatientID != '': #We're updating
			patient = model.Person.get(PatientID)
			customer = model.InvCustomer.get(CustomerID)
			#Update name
			patient.Title = Title
			patient.NameFirst = NameFirst
			patient.NameMiddle = NameMiddle
			patient.NameLast = NameLast
			customer.Name = ('%s %s,%s,%s' % (Title, NameFirst, NameMiddle, NameLast)).replace(',,',',').replace(',', ' ').strip()
			#Update address
			patient.AddrStr = AddressStreet
			patient.AddrCitytownNrID = AddrCitytownNrID
			citytown = model.AddressCityTown.get(AddrCitytownNrID)
			customer.CityID = citytown.id
			AddressLabel = '%s\n%s\n%s, %s\n%s\n%s' % (AddressStreet, citytown.Name, citytown.Block, citytown.District, citytown.State, citytown.ZipCode)
			customer.AddressLabel = AddressLabel
			# Other info
			patient.Sex = Gender
			patient.Religion = Religion
			bday = time.strptime(str(DateBirth),DATE_FORMAT)
			patient.DateBirth = datetime.datetime(bday.tm_year,bday.tm_mon,bday.tm_mday)
			# patient.XXXXXXX = Tribe  ******************Need to add this sometime
		else:
			bday = time.strptime(str(DateBirth),DATE_FORMAT)
			bdate = datetime.datetime(bday.tm_year,bday.tm_mon,bday.tm_mday)
			patient = model.Person(NameFirst=NameFirst,NameLast=NameLast,NameMiddle=NameMiddle,\
				AddrStr=AddressStreet,AddrCitytownNrID=AddrCitytownNrID,Sex=Gender,Religion=Religion,\
				DateBirth=bdate)
			citytown = model.AddressCityTown.get(AddrCitytownNrID)
			AddressLabel = '%s\n%s\n%s, %s\n%s\n%s' % (AddressStreet, citytown.Name, citytown.Block, citytown.District, citytown.State, citytown.ZipCode)			
			PatientName = ('%s %s,%s,%s' % (Title, NameFirst, NameMiddle, NameLast)).replace(',,',',').replace(',', ' ').strip()
			customer = model.InvCustomer(Name=PatientName ,CityID=patient.AddrCitytownNrID , AddressLabel=AddressLabel, CreditAmount=0.0, \
				InventoryLocation=self.GetDefaultCustomerLocationID(), ExternalID=patient.id)
		# Check that the latest encounter (is the patient still admitted?)
		try:
			EncounterMessage = 'A new encounter entered'
			encounter = model.Encounter.get(patient.GetLatestEncounter())
			if encounter.EncounterDate.strftime(DATE_FORMAT) == datetime.datetime.now().strftime(DATE_FORMAT):
				EncounterMessage = 'Using today\'s encounter'
			elif (encounter.EncounterClassNr.Name == 'Inpatient') and (not encounter.IsDischarged):
				EncounterMessage = 'Patient currently admitted'
			else:
				#Mark our record as discharged.
				if not encounter.IsDischarged:
					encounter.IsDischarged = True
					encounter.DischargeDate = model.cur_date_time()
					encounter.DischargeTime = str(model.cur_date_time()).rjust(8)
				encounter = None
		except AssertionError:
			#AssertionError when patient.GetLatestEncounter() returns "None"
			encounter = None
		except:
			raise
			encounter = None
		if encounter == None:
			#Add a new encounter, NOTE CLASS_ENCR is defined in model_inventory.py
			if int(PatientType) != model.CLASS_INSR['private']:
				InsuranceNumber = None
				Firm = None
			encounter = model.Encounter(Pid=patient.id, EncounterType='Outpatient', \
				EncounterClassNrID=model.CLASS_ENCR['outpatient'], InsuranceClassNr=int(PatientType),\
				InsuranceNr=InsuranceNumber, InsuranceFirmId=Firm, FinancialClassNrID=model.CLASS_FIN['common'])
		else:
			#Update our Encounter with new information for patient type and insurance number
			encounter.InsuranceClassNrID = int(PatientType)
			#CLASS_INSR is defined in "model_inventory.py"
			if int(PatientType) == model.CLASS_INSR['private']:
				encounter.InsuranceNr = InsuranceNumber
				encounter.InsuranceFirmId = Firm
		# Create/Update a new bill/receipt
		# First check if we have a receipt for this encounter with an un-paid registration.  Assume the unpaid registration
		# IS the current registration (back button was pressed)
		receipts = model.InvReceipt.select(AND (model.InvReceipt.q.ExternalId == encounter.id, model.InvReceipt.q.CreateTime >= \
			encounter.EncounterDate))
		if receipts.count() > 0:
			receipt = receipts[0]
			log.debug('....Found a matching receipt to use')
		else:
			receipt = model.InvReceipt(CustomerID=customer.id, TotalPayment=0.0, TotalPaid=0.0, TotalSelfPay=0.0,\
				TotalInsurance=0.0, ExternalId=encounter.id)
		#bill for registration
		registration = model.InvCatalogItem.select(model.InvCatalogItem.q.Name == "Registration")[0]
		# Look in the receipt for a receipt item for registration
		receipt_item = None
		for item in receipt.CatalogItems:
			if item.CatalogItemID == registration.id:
				receipt_item = item
				break;
		if receipt_item == None:
			receipt_item = model.InvReceiptItems(ReceiptID=receipt.id, CatalogItemID=registration.id, Quantity=1)
		#
		#	NOTE: Stock transfer will happen on the billing screen
		# if len(receipt_item.StockItems) == 0:
			#transfer the registration
		#	from_location = registration.StockItems[0].Locations[0]
		#	to_location = model.InvStockLocation(StockItemID=from_location.StockItemID,LocationID=\
		#		customer.InventoryLocationID,ReceiptID=receipt_item.id,IsConsumed=True,IsSold=True,
		#		TotalPaid=0.0, Quantity=1)
		#	transfer = model.InvStockTransfer(FromStockLocationID=from_location.id,ToStockLocationID=to_location.id,\
		#		Qty=1,DateTransferred=datetime.datetime.now())
		# PREPARE our variables for the next screen
		ContactPerson = patient.ContactPerson
		ContactRelation = patient.ContactRelation
		CRLTextField = widgets.TextField("Relation", attrs={'size':'40'})
		ContactRelationLookup = widgets.AutoCompleteField(name="ContactRelation", search_controller="RegistrationSearchRelationship",\
			search_param="Relationship", result_name="relationships", default=ContactRelation, text_field=CRLTextField)
		Phone1Nr = patient.Phone1Nr
		Cellphone1Nr = patient.Cellphone1Nr
		Email = patient.Email
		#Get our occupation
		Occupation = ''
		if patient != None:
			Occupation = patient.Occupation
		OLTextField = widgets.TextField("Occupation", attrs={'size':'40'})
		OccupationLookup = widgets.AutoCompleteField(name="Occupation", search_controller="RegistrationSearchOccupation",\
			search_param="Occupation", result_name="occupations", default=Occupation, text_field=OLTextField)
		#Get our Financial class options
		FinancialClassNr = 'common'
		if encounter != None:
			FinancialClassNr = patient.GetLatestEncounterVar(VarName='FinancialClassNrID')
		items=[x[0] for x in conn.queryAll('select distinct name from care_class_financial')]
		financialclassnrs=[]
		for financialclassnr in items:
			if financialclassnr == Occupation:
				#NOTE: CLASS_FIN is defined in model_inventory.py
				financialclassnrs.append(dict(id=model.CLASS_FIN[financialclassnr], name=financialclassnr, selected='selected'))
			else:
				financialclassnrs.append(dict(id=model.CLASS_FIN[financialclassnr], name=financialclassnr, selected=None))
		#EncounterType Configuration
		EncounterType = 'Walk-in'
		items=[x[0] for x in conn.queryAll('select distinct name from care_type_encounter')]
		encountertypes=[]
		for encountertype in items:
			if encountertype == EncounterType:
				#NOTE: CLASS_FIN is defined in model_inventory.py
				encountertypes.append(dict(id=encountertype, name=encountertype, selected='checked'))
			else:
				encountertypes.append(dict(id=encountertype, name=encountertype, selected=None))
		#Fill up the history information
		History = []
		if customer != None:
			History.append('Name: %s' % customer.Name)
			PastDues = customer.CalcPayment() - customer.CalcPaid()
			if PastDues > 0:
				History.append('Past dues: %d' % PastDues)
			elif PastDues == 0:
				History.append('Past dues: None')
			else:
				History.append('Credit: %d' % abs(PastDues))
			if encounter != None:
				History.append('Last visit: %s' % encounter.EncounterDate.strftime(DATE_FORMAT))
				History.append('Visit count: %d' % len(patient.Encounters))
				if encounter.EncounterDate.strftime(DATE_FORMAT) == datetime.datetime.now().strftime(DATE_FORMAT):
					History.append('Already registered today')
				elif (encounter.EncounterClassNr.Name == 'Inpatient') and (not encounter.IsDischarged):
					History.append('Currently admitted')
		return dict(PatientID=patient.id, CustomerID=customer.id, ReceiptID=receipt.id, EncounterID=encounter.id, \
			ContactPerson=ContactPerson, ContactRelationLookup=ContactRelationLookup, \
			OccupationLookup=OccupationLookup, Phone1Nr=Phone1Nr, history=History,\
			Cellphone1Nr=Cellphone1Nr, Email=Email, financialclassnrs=financialclassnrs, encountertypes=encountertypes)

	@expose(format='json')
	def RegistrationSearchOccupation(self, Occupation):
		'''	Type ahead lookup for occupations
		'''
		Occupation = Occupation.lower()
		items=[x[0] for x in conn.queryAll('select distinct occupation from care_person')]
		if len(items)>0:
			return dict(occupations=filter(lambda item: item != None and Occupation in item.lower(), items))
		else:
			return dict(occupations=[])

	@expose(format='json')
	def RegistrationSearchRelationship(self, Relationship):
		'''	Type ahead lookup for relationships
		'''
		Relationship = Relationship.lower()
		items=[x[0] for x in conn.queryAll('select distinct contact_relation from care_person')]
		if len(items) > 0:
			return dict(relationships=filter(lambda item: item != None and Relationship in item.lower(), items))
		else:
			return dict(relationships=[])
			
	#	Step 3: Update Patient/Encounter information and choose between in/out patient
	@validate(validators={'Cellphone1Nr':validators.String(),'Phone1Nr':validators.String(), 'ContactPerson':validators.String(), \
	'PatientID':validators.Int(),'CustomerID':validators.Int(), 'EncounterID':validators.Int(), \
	'ReceiptID':validators.Int(),'btnNext':validators.String(), 'FinancialClassNr':validators.Int(), \
	'Email':validators.String(),'EncounterType':validators.String()})
	@expose(html='turbocare.templates.registration_patient_page3')
	@identity.require(identity.has_permission("reg_edit"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	def RegistrationPage2Save(self, PatientID=None, CustomerID=None, EncounterID=None, ReceiptID=None, btnNext='', 
			FinancialClassNr='', Email='', Cellphone1Nr='', Phone1Nr='', Occupation={}, ContactRelation={},\
			ContactPerson='', EncounterType='', **kw):
		'''	Update Patient/Encounter information and choose between in/out patient
		'''
		log.debug('RegistrationPage2Save')
		try:
			if (PatientID==None) or (CustomerID==None) or (EncounterID==None) or (ReceiptID==None):
				turbogears.flash('There is a registration flow error, try from the start again')
				raise ValueError
		except ValueError:
			log.debug('RegistrationPage2Save: tried to save without id values')
			raise cherrypy.HTTPRedirect('/registration')
		# Update the patient record
		patient = model.Person.get(PatientID)
		patient.ContactPerson = ContactPerson
		patient.ContactRelation = ContactRelation['Relation']
		patient.Occupation = Occupation['Occupation']
		patient.Email = Email
		patient.Cellphone1Nr = Cellphone1Nr
		patient.Phone1Nr = Phone1Nr
		# Figure out what kind of encounter we have Inpatient or Outpatient
		encounter = model.Encounter.get(int(EncounterID))
		encounter.EncounterType = EncounterType
		# Set the financial classification
		encounter.FinancialClassNrID = FinancialClassNr
		# Define blank entries for our variables now
		rooms=[]
		beds = []
		wards=[]
		DoctorLookup = None
		queues = []
		# If we selected Inpatient, or if the current encounter has been inpatient for more than a day, then we do an 
		#  Inpatient record.
		if (btnNext == "Inpatient") or (encounter.EncounterClassNrID == model.CLASS_ENCR['inpatient'] and \
				((model.cur_date_time() - encounter.EncounterDate).seconds > 86400)):
			PatientClass = 'Inpatient'
			#Prepare for the inpatient admission
			encounter.EncounterClassNrID = model.CLASS_ENCR['inpatient']
			# Bed assignment
			# Get the Ward
			Ward = model.DFLT_WARD[EncounterType] #Default wards are defined in model_inventory.py
			if encounter.CurrentWardNrID != None:
				Ward = encounter.CurrentWardNrID
			items=[{'id':x.id,'name':x.Name} for x in model.Ward.select(AND (model.Ward.q.IsTempClosed == False,\
					model.Ward.q.Status!='deleted'))]
			wards=[]
			for ward in items:
				if ward['id'] == Ward:
					#NOTE: CLASS_FIN is defined in model_inventory.py
					wards.append(dict(id=ward['id'] , name=ward['name'], selected='selected'))
				else:
					wards.append(dict(id=ward['id'] , name=ward['name'], selected=None))
			# Get the room, and possibly the bed too
			items=[{'id':x.id,'name':x.RoomNr, 'beds':x.NrOfBeds} for x in model.Room.select(AND (model.Room.q.IsTempClosed == False,\
					model.Room.q.Status!='deleted',model.Room.q.DateClose==None, \
					model.Room.q.WardNrID == Ward),distinct=True, orderBy=[model.Room.q.RoomNr])]
			Room = None
			rooms=[]
			bed_items=[]
			beds = []
			Bed = None
			if encounter.CurrentRoomNr != None:
				Room = encounter.CurrentRoomNr
				Bed = encounter.CurrentBedNumber()
				#Get the room ID
				wardrooms = model.Room.select(AND (model.Room.q.WardNrID==Ward,model.Room.q.RoomNr==Room,),\
					distinct=True)
				#Use the first room from the ward that matches
				try:
					bed_items = self.RegistrationBeds(wardrooms[0].id)
				except:
					raise
					bed_items = []
			if Bed != None: #We have a bed, so we should add this to the beds list already
				beds.append(dict(id=Bed, name=Bed, selected='selected'))
			SelectedWard = model.Ward.get(Ward)
			RoomPrefix = SelectedWard.Roomprefix
			for room in items:
				if Room == None: #If we don't have a room, then find the first room with an available bed
					bed_items = self.RegistrationBeds(room['id'])
					if len(beds) > 0:
						Room = room['id']
						Bed = bed_items[0] #First available bed
				if room['name'] == Room:
					#NOTE: CLASS_FIN is defined in model_inventory.py
					Text = '%s%d (%d of %d available)' % (RoomPrefix, room['name'], len(self.RegistrationBeds(room['id'])), room['beds'])
					rooms.append(dict(id=room['name'], name=Text, selected='selected'))
				else:
					Text = '%s%d (%d of %d available)' % (RoomPrefix, room['name'], len(self.RegistrationBeds(room['id'])), room['beds'])
					rooms.append(dict(id=room['name'], name=Text, selected=None))
			#Configure our bed options
			for bed in bed_items:
				if bed == Bed:
					beds.append(dict(id=bed, name=bed, selected='selected'))
				else:
					beds.append(dict(id=bed, name=bed, selected=None))					
		else:
			PatientClass = 'Outpatient'
			#Prepare for outpatient consulation. 
			encounter.EncounterClassNrID = model.CLASS_ENCR['outpatient']
			# Setup the Doctor Queue options (Financial classification plays a role in this choice)
			#{'common':9,'private + common':10,'private':11,'private plus':12}
			items = ['General', 'Priority', 'Specialist']
			if FinancialClassNr in [9, 10]:
				Queue = 'General'
			else:
				Queue = 'Priority'
			queues = []
			for queue in items:
				if queue == Queue:
					queues.append(dict(id=queue, name=queue, selected='selected'))
				else:
					queues.append(dict(id=queue, name=queue, selected=None))				
			# Select a doctor - This is only needed if "Specialist" is selected from above
			if encounter.ConsultingDr != None:
				Doctor = encounter.ConsultingDr
			else:
				Doctor = ''
			DoctorName = widgets.TextField("DoctorName", attrs={'size':'40'})
			DoctorLookup = widgets.AutoCompleteField(name="DoctorName", search_controller="RegistrationSearchDoctor",\
				search_param="DoctorName", result_name="doctors", default=Doctor, text_field=DoctorName)
		# Collect referral information
		ReferrerInstitution = ''
		ReferrerDr = ''
		ReferrerDept = ''
		ReferrerDiagnosis = ''
		ReferrerRecomTherapy = ''
		ReferrerNotes = ''
		if EncounterType == 'Referral':
			Referrer = True
			if encounter != None:
				ReferrerInstitution = encounter.ReferrerInstitution
				ReferrerDr = encounter.ReferrerDr
				ReferrerDept = encounter.ReferrerDept
				ReferrerDiagnosis = encounter.ReferrerDiagnosis
				ReferrerRecomTherapy = encounter.ReferrerRecomTherapy
				ReferrerNotes = encounter.ReferrerNotes
		else:
			Referrer = False			
		#Fill up the history information
		History = []
		customer = model.InvCustomer.get(CustomerID)
		if customer != None:
			History.append('Name: %s' % customer.Name)
			PastDues = customer.CalcPayment() - customer.CalcPaid()
			if PastDues > 0:
				History.append('Past dues: %d' % PastDues)
			elif PastDues == 0:
				History.append('Past dues: None')
			else:
				History.append('Credit: %d' % abs(PastDues))
			if encounter != None:
				History.append('Last visit: %s' % encounter.EncounterDate.strftime(DATE_FORMAT))
				History.append('Visit count: %d' % len(patient.Encounters))
				if encounter.EncounterDate.strftime(DATE_FORMAT) == datetime.datetime.now().strftime(DATE_FORMAT):
					History.append('Registered today')
				elif (encounter.EncounterClassNr.Name == 'Inpatient') and (not encounter.IsDischarged):
					History.append('Currently admitted')
		# Booklet printing 
		if len(patient.Encounters) == 1:
			BookletPrinting = 'CHECKED'
		else:
			BookletPrinting = None
		return dict(PatientID=PatientID, CustomerID=CustomerID, ReceiptID=ReceiptID, EncounterID=EncounterID, \
			history=History, wards=wards, rooms=rooms, beds=beds, queues=queues, DoctorLookup=DoctorLookup,\
			ReferrerInstitution = ReferrerInstitution,	ReferrerDr = ReferrerDr,	ReferrerDept = ReferrerDept,\
			ReferrerDiagnosis=ReferrerDiagnosis,ReferrerRecomTherapy=ReferrerRecomTherapy,\
			ReferrerNotes=ReferrerNotes, Referrer = Referrer, PatientClass = PatientClass, BookletPrinting=BookletPrinting)
			
	@expose(format='json')
	def RegistrationRooms(self, WardID):
		'''	Produces a listing of Rooms for a particular ward
		'''
		log.debug("RegistrationRooms")
		rooms = model.Room.select(model.Room.q.WardNrID == int(WardID))
		ward = model.Ward.get(int(WardID))
		RoomPrefix = ward.Roomprefix
		result = []
		for room in rooms:
			Text = '%s%d (%d of %d available)' % (RoomPrefix,room.RoomNr, len(self.RegistrationBeds(room.id)), room.NrOfBeds)
			#log.debug("....%s" % Text)
			result.append(dict(id=room.RoomNr, name=Text))
		return dict(result=result)
		
	@expose(format='json')
	@validate(validators={'WardID':validators.Int(),'RoomNr':validators.Int(), 'EncounterID':validators.Int()})
	def RegistrationBedsInRoom(self, WardID, RoomNr, EncounterID):
		'''	Given a ward id and a room number, return a list
			of available beds.  Using the EncounterID If a bed is
			assigned to the patient, then include this in the list
			and try to make it selected
		'''
		log.debug("RegistrationBedsInRoom")
		log.debug("....RoomNr: %d, WardID: %d" % (RoomNr, WardID))
		# Find the first room with the number belonging to the Ward
		RoomID = model.Room.select(AND (model.Room.q.WardNrID==int(WardID),model.Room.q.RoomNr==int(RoomNr)))[0].id
		log.debug('....RoomID: %d' % RoomID)
		# Check to see if there is a bed assigned to the patient in the current room
		AssignedBed = None
		Room = model.EncounterLocation.select(AND ((OR (model.EncounterLocation.q.DischargeTypeNrID == 0,\
			model.EncounterLocation.q.DischargeTypeNrID == None)), model.EncounterLocation.q.GroupNr==WardID,\
			model.EncounterLocation.q.TypeNrID==model.TYPE_LOCATION['room'],model.EncounterLocation.q.EncounterNrID\
			==EncounterID, model.EncounterLocation.q.LocationNr==RoomNr))
		# We're looking for a bed, but we need to make sure that the bed is in the same room.  The query above checks that we
		# have an entry with a matching room.  The bottom checks for the bed number.  Both have to return results greater than 0
		Bed = model.EncounterLocation.select(AND ((OR (model.EncounterLocation.q.DischargeTypeNrID == 0,\
			model.EncounterLocation.q.DischargeTypeNrID == None)), model.EncounterLocation.q.GroupNr==WardID,\
			model.EncounterLocation.q.TypeNrID==model.TYPE_LOCATION['bed'],model.EncounterLocation.q.EncounterNrID\
			==EncounterID))
		log.debug('....bed count: %d, room count: %d' % (Bed.count(), Room.count()))
		if (Bed.count() > 0) and (Room.count() > 0): 
			AssignedBed = Bed[0].LocationNr
		if AssignedBed != None:
			result = [AssignedBed]+self.RegistrationBeds(RoomID)
		else:
			result = self.RegistrationBeds(RoomID)
		# Return the list of available beds
		return dict(result=result)
	
	def RegistrationBeds(self, RoomID):
		'''	Produces a listing of available beds for a particular
			room
		'''
		room = model.Room.get(int(RoomID))
		#Get the bed numbers
		BedNumbers = set(range(1,room.NrOfBeds+1))
		# Get locked/closed beds
		ClosedBeds = set(int(x) for x in room.ClosedBeds.rsplit('/')[:-1])
		#Compile the bed usage information for our room
		Beds = model.EncounterLocation.select(AND (OR (model.EncounterLocation.q.DischargeTypeNrID == 0,\
			model.EncounterLocation.q.DischargeTypeNrID == None), \
			model.EncounterLocation.q.GroupNr == room.WardNrID, OR (model.EncounterLocation.q.TypeNrID == 4,\
			model.EncounterLocation.q.TypeNrID==5)),orderBy=[model.EncounterLocation.q.EncounterNrID,\
			model.EncounterLocation.q.TypeNrID])
		Encounters = {}
		for row in Beds:
			if (not Encounters.has_key(row.EncounterNrID)) and (row.TypeNrID == 4) and (row.LocationNr == room.RoomNr):
				Encounters[row.EncounterNrID] = 0
			elif Encounters.has_key(row.EncounterNrID) and (row.TypeNrID == 5):
				Encounters[row.EncounterNrID] = row.LocationNr
		FreeBeds = [x for x in (BedNumbers - set(Encounters.values()))-ClosedBeds]
		return FreeBeds
	
	@expose(format='json')
	def RegistrationSearchDoctor(self, DoctorName):
		'''	Type ahead lookup for Doctors
		'''
		DoctorName = DoctorName.lower()
		items=model.Personell.select(AND (model.Personell.q.JobFunctionTitle == 'Doctor',\
			model.Personell.q.Status != 'deleted', model.Personell.q.IsDischarged == False))
		doctors = [x.DisplayName() for x in items]
		if len(doctors) > 0:
			return dict(doctors=filter(lambda doctor: DoctorName in doctor.lower(), doctors))
		else:
			return dict(doctors=[])

	# Room assignment change
	def RegistrationBedRoomChange(self, EncounterID, Ward, Room, Bed):
		'''	Make a room assignment change.  If the change happens withing 4 hours of the initial
			assignment, then don't make a transfer, just update the record.  Otherwise, do a 
			Transfer.
			Return the catalog id used for billing of the current room assignment
		'''
		# Get our current EncounterLocation rows
		log.debug('RegistrationBedRoomChange')
		curward = model.EncounterLocation.select(AND (model.EncounterLocation.q.EncounterNrID==EncounterID,\
			(OR (model.EncounterLocation.q.DischargeTypeNrID == 0,model.EncounterLocation.q.DischargeTypeNrID\
			== None)), model.EncounterLocation.q.TypeNrID==2))[0]
		GroupNr = curward.GroupNr
		curroom = model.EncounterLocation.select(AND (model.EncounterLocation.q.EncounterNrID==EncounterID,\
			(OR (model.EncounterLocation.q.DischargeTypeNrID == 0,model.EncounterLocation.q.DischargeTypeNrID\
			== None)), model.EncounterLocation.q.TypeNrID==4,model.EncounterLocation.q.GroupNr==GroupNr))[0]
		curbed = model.EncounterLocation.select(AND (model.EncounterLocation.q.EncounterNrID==EncounterID,\
			(OR (model.EncounterLocation.q.DischargeTypeNrID == 0,model.EncounterLocation.q.DischargeTypeNrID\
			== None)), model.EncounterLocation.q.TypeNrID==5,model.EncounterLocation.q.GroupNr==GroupNr))[0]
		# Make sure we're editing the right data, return null if there's nothing to change here
		if (curward.LocationNr == Ward) and (curroom.LocationNr == Room) and (curbed.LocationNr == Bed):
			# HEY, NOTHING TO CHANGE, so we'll exit now
			return None
		# See if the time difference between edits is less than 4 hours!
		d = curward.DateFrom
		t = time.strptime(str(curward.TimeFrom),'%H:%M:%S')
		DateTimeFrom = datetime.datetime(d.year,d.month,d.day,t.tm_hour,t.tm_min,t.tm_sec)
		diff = DateTimeFrom - model.cur_date_time() 
		if (diff.seconds/60/60) < 4 and diff.days == 0:
			#Update the current entries only
			curward.LocationNr = Ward
			curroom.LocationNr = Room
			curbed.LocationNr = Bed
		else:
			encounter = model.Encounter.get(EncounterID)
			# Close the current ward/room/bed assignment and create a new one
			newward = None
			newroom = None
			newbed = None
			if curward.LocationNr != Ward:
				curward.DateTo = model.cur_date_time()
				curward.TimeTo = model.cur_date_time().strftime('%H:%M:%S')
				curward.DischargeTypeNr = model.TYPE_DISCHARGE['change_ward']
				curroom.DateTo = model.cur_date_time()
				curroom.TimeTo = model.cur_date_time().strftime('%H:%M:%S')
				curroom.DischargeTypeNr = model.TYPE_DISCHARGE['change_ward']
				curbed.DateTo = model.cur_date_time()
				curbed.TimeTo = model.cur_date_time().strftime('%H:%M:%S')
				curbed.DischargeTypeNr = model.TYPE_DISCHARGE['change_ward']
				#Create all new records (NOTE, the GroupNr is the Ward id... i think)
				newward = model.EncounterLocation(EncounterNr=EncounterID,TypeNr=model.TYPE_LOCATION['ward'],\
					LocationNr=Ward,GroupNr=Ward,DischargeTypeNrID=0) #defaults take care of the rest
				newroom = model.EncounterLocation(EncounterNr=EncounterID,TypeNr=model.TYPE_LOCATION['room'],\
					LocationNr=Room,GroupNr=Ward,DischargeTypeNrID=0) #defaults take care of the rest
				newbed = model.EncounterLocation(EncounterNr=EncounterID,TypeNr=model.TYPE_LOCATION['bed'],\
					LocationNr=Bed,GroupNr=Ward,DischargeTypeNrID=0) #defaults take care of the rest
				# Update the encounter
				encounter.CurrentWardNrID = Ward
				encounter.CurrentRoomNr = Room
			elif curroom.LocationNr != Room:
				curroom.DateTo = model.cur_date_time()
				curroom.TimeTo = model.cur_date_time().strftime('%H:%M:%S')
				curroom.DischargeTypeNr = model.TYPE_DISCHARGE['change_room']
				curbed.DateTo = model.cur_date_time()
				curbed.TimeTo = model.cur_date_time().strftime('%H:%M:%S')
				curbed.DischargeTypeNr = model.TYPE_DISCHARGE['change_room']
				#Create all new records (NOTE, the GroupNr is the Ward id... i think)
				newroom = model.EncounterLocation(EncounterNr=EncounterID,TypeNr=model.TYPE_LOCATION['room'],\
					LocationNr=Room,GroupNr=Ward,DischargeTypeNrID=0) #defaults take care of the rest
				newbed = model.EncounterLocation(EncounterNr=EncounterID,TypeNr=model.TYPE_LOCATION['bed'],\
					LocationNr=Bed,GroupNr=Ward,DischargeTypeNrID=0) #defaults take care of the rest
				# Update the encounter
				encounter.CurrentRoomNr = Room
			elif curbed.LocationNr != Bed:
				curbed.DateTo = model.cur_date_time()
				curbed.TimeTo = model.cur_date_time().strftime('%H:%M:%S')
				curbed.DischargeTypeNr = model.TYPE_DISCHARGE['change_bed']
				# Create new record
				newbed = model.EncounterLocation(EncounterNr=EncounterID,TypeNr=model.TYPE_LOCATION['bed'],\
					LocationNr=Bed,GroupNr=Ward,DischargeTypeNrID=0) #defaults take care of the rest
		# Get the Catalog id for this room (for billing purposes)
		if newward != None:
			return model.DFLT_ROOMPREFIX[newward.WardNr.Roomprefix]
		else:
			return model.DFLT_ROOMPREFIX[curward.WardNr.Roomprefix]
				
	# Bed assignment receipt item
	def RegistrationBedReceipt(self, EncounterID, ReceiptID):
		'''	Make sure there are Receipt entries for all current
			Bed assignment entries.  Any un-accounted entries
			will be added to the ReceiptID indicated with a min
			of 1 days assigned
		'''
		log.debug('RegistrationBedReceipt')
		encounter = model.Encounter.get(EncounterID)
		RoomDays = encounter.GetRoomDays()
		log.debug('....%d RoomDays' % len(RoomDays))
		# Room charges are based on the Ward Prefix
		PrefixDays = {'COMM':0, 'CMPR':0, 'PRIV':0} #Count the number of days spent in each financial category
		for room in RoomDays:
			ward = model.Ward.get(room['WardID'])
			PrefixDays[ward.Roomprefix] += room['Days']
		# Subtract any paid days from what we have
		for receipt in encounter.Receipts:
			for item in receipt.CatalogItems:
				if model.CATID_ROOMPREFIX.has_key(item.CatalogItemID):
					PrefixDays[model.CATID_ROOMPREFIX[item.CatalogItemID]] -= item.Quantity
		# Update any un-paid Receipt entries with what's left
		for receipt in encounter.Receipts:
			for item in receipt.CatalogItems:
				if model.CATID_ROOMPREFIX.has_key(item.CatalogItemID) and PrefixDays[model.CATID_ROOMPREFIX[item.CatalogItemID]] != 0:
					log.debug('...item name:%s, is paid:%s' % (item.Name(), item.IsPaid()))
					if not item.IsPaid(): #Unpaid items will absorb the un-accounted quantity
						item.Quantity += round(PrefixDays[model.CATID_ROOMPREFIX[item.CatalogItemID]],1)
						PrefixDays[model.CATID_ROOMPREFIX[item.CatalogItemID]] = 0
		# Create any un-accounted entries for bed assignment
		# NOTE, the stock transfer doesn't have to happen here since billing will do this automatically for us
		if PrefixDays['COMM'] != 0:
			receipt_item = model.InvReceiptItems(Quantity=round(PrefixDays['COMM'],1),ReceiptID=ReceiptID,CatalogItemID=model.DFLT_ROOMPREFIX['COMM'])
		if PrefixDays['CMPR'] != 0:
			receipt_item = model.InvReceiptItems(Quantity=round(PrefixDays['CMPR'],1),ReceiptID=ReceiptID,CatalogItemID=model.DFLT_ROOMPREFIX['CMPR'])
		if PrefixDays['PRIV'] != 0:
			receipt_item = model.InvReceiptItems(Quantity=round(PrefixDays['PRIV'],1),ReceiptID=ReceiptID,CatalogItemID=model.DFLT_ROOMPREFIX['PRIV'])

	def GetBookletPrintingID(self):
		'''	Get the CatalogItemID for booklet printing
		'''
		booklet = model.InvCatalogItem.select(model.InvCatalogItem.q.Name == 'Booklet printing')[0]
		return booklet.id
		
	#	Step 3: Update Patient/Encounter information and choose between in/out patient
	@validate(validators={'PatientID':validators.Int(),'CustomerID':validators.Int(), 'EncounterID':validators.Int(), \
	'ReceiptID':validators.Int(),'BookletPrinting':validators.String(), 'Ward':validators.Int(), 'Room':validators.Int(),\
	'Bed':validators.Int(),'ReferrerInstitution':validators.String(),'ReferrerDr':validators.String(),\
	'ReferrerDept':validators.String(),'ReferrerDiagnosis':validators.String(),'ReferrerRecomTherapy':validators.String(),\
	'ReferrerNotes':validators.String(),'Queue':validators.String(),'PatientClass':validators.String()})
	@expose()
	def RegistrationPage3Save(self, PatientID=None, CustomerID=None, EncounterID=None, ReceiptID=None, \
		BookletPrinting='', Ward=None, Room=None, Bed=None, ReferrerInstitution='', ReferrerDr='', ReferrerDept='',\
		ReferrerDiagnosis='', ReferrerRecomTherapy='',ReferrerNotes='',Queue='',DoctorName={},\
		PatientClass='', **kw):
		'''	Assign/Update bed/referral/booklet/consultant information for in/out patients
			Update billing information
			After saving the patient and customer information redirect the screen to billing
		'''
		log.debug('RegistrationPage3Save')
		if Room != None and Ward !=None and Bed !=None:
			log.debug('....Room: %d, Ward: %d, Bed: %d' % (Room, Ward, Bed))
		if Room != None:
			room = model.Room.select(AND (model.Room.q.RoomNr==Room, model.Room.q.WardNrID==Ward))[0]
			#room = model.Room.get(Room)
		try:
			if (PatientID==None) or (CustomerID==None) or (EncounterID==None) or (ReceiptID==None):
				turbogears.flash('There is a registration flow error, try from the start again')
				raise ValueError
		except ValueError:
			log.debug('RegistrationPage2Save: tried to save without id values')
			raise cherrypy.HTTPRedirect('/registration')
		#Get our encounter
		encounter = model.Encounter.get(EncounterID)
		# Get our receipt
		receipt = model.InvReceipt.get(ReceiptID)
		# Update referral information
		encounter.ReferrerInstitution=ReferrerInstitution
		encounter.ReferrerDr=ReferrerDr
		encounter.ReferrerDept=ReferrerDept
		encounter.ReferrerDiagnosis=ReferrerDiagnosis
		encounter.ReferrerRecomTherapy=ReferrerRecomTherapy
		encounter.ReferrerNotes=ReferrerNotes
		# Booklet label printing check
		if BookletPrinting.lower() == 'on':
			log.debug('....Booklet printing')
			BookletID = self.GetBookletPrintingID()
			AlreadyExists = False
			# Look for an existing booklet printing on the receipt
			for item in receipt.CatalogItems:
				if item.CatalogItemID == BookletID:
					AlreadyExists = True
			if not AlreadyExists:
				# Add a booklet printing receipt item
				receipt_item = model.InvReceiptItems(CatalogItemID=BookletID,Quantity=1,ReceiptID=ReceiptID)
		if PatientClass == 'Inpatient':
			# Update/Create bed assignment
			# Look for the current bed assignment
			if encounter.CurrentWardNrID != None and encounter.CurrentRoomNr != None:
				CurrentBed = encounter.CurrentBedNumber()
				#log.debug('....Current bed=%d, New bed=%d' % (CurrentBed, Bed))
				#log.debug('....Current ward=%d, New ward=%d' % (encounter.CurrentWardNrID, Ward))
				#log.debug('....Current room=%d, New room=%d' % (encounter.CurrentRoomNr, Room))
				if (Ward != encounter.CurrentWardNrID) or (encounter.CurrentRoomNr != Room) or (CurrentBed != Bed):
					# Change the room assignment.  If the room assignment change happens within 4 hours, then
					# I'll update the current values without showing a transfer, otherwise, I'll show a transfer record
					RoomCatalogID = self.RegistrationBedRoomChange(EncounterID, Ward, Room, Bed)
				else:
					curward = model.Ward.get(Ward)
					RoomCatalogID = model.DFLT_ROOMPREFIX[curward.Roomprefix]
			else: # Add new room entries
				#Create all new records (NOTE, the GroupNr is the Ward id... i think)
				newward = model.EncounterLocation(EncounterNr=EncounterID,TypeNr=model.TYPE_LOCATION['ward'],\
					LocationNr=Ward,GroupNr=Ward,DischargeTypeNrID=0) #defaults take care of the rest
				newroom = model.EncounterLocation(EncounterNr=EncounterID,TypeNr=model.TYPE_LOCATION['room'],\
					LocationNr=Room,GroupNr=Ward,DischargeTypeNrID=0) #defaults take care of the rest
				newbed = model.EncounterLocation(EncounterNr=EncounterID,TypeNr=model.TYPE_LOCATION['bed'],\
					LocationNr=Bed,GroupNr=Ward,DischargeTypeNrID=0) #defaults take care of the rest
				# Update the encounter
				encounter.CurrentWardNrID = Ward
				encounter.CurrentRoomNr = Room
			# Go through all bed assignments for this encounter and add any un-accounted entries to our receipt
			self.RegistrationBedReceipt(EncounterID, ReceiptID)
		else: #PatientClass == 'Outpatient'
			# Doctor name:   ['General', 'Priority', 'Specialist'] 
			# General and Priority are different queues which are put into the Doctor name
			# If the Queue is "Specialist" then there needs to be a real doctor name which we use.  Specialist is by
			# referral only.  If Priority is selected, then if there is a Doctor name, we'll use the Doctor name
			log.debug('....%s' % Queue)
			if Queue == 'General':
				encounter.ConsultingDr = 'General'
				ConsultationID = model.DFLT_CONSLT_COMMON['catalogid']
			elif Queue == 'Priority':
				if DoctorName['DoctorName'] == '':
					encounter.ConsultingDr = 'Priority'
				else:
					encounter.ConsultingDr = DoctorName['DoctorName']
				ConsultationID = model.DFLT_CONSLT_PRIVATE['catalogid']
			elif Queue == 'Specialist':
				encounter.ConsultingDr = DoctorName['DoctorName']
				ConsultationID = model.DFLT_CONSLT_COMMON['catalogid']
			# See if we have a consultation of any sort on the receipt
			ConsultIDs = [model.DFLT_CONSLT_COMMON['catalogid'], model.DFLT_CONSLT_PRIVCOM['catalogid'],\
				model.DFLT_CONSLT_PRIVATE['catalogid'], model.DFLT_CONSLT_VRYPRIV['catalogid']]
			AlreadyAssigned = False
			for item in receipt.CatalogItems:
				if item.CatalogItemID in ConsultIDs:
					log.debug('....Found an existing consultation')
					AlreadyAssigned = True
					item.CatalogItemID = ConsultationID
					item.Quantity = 1
					break #Stop looking now that we've found an entry
			if not AlreadyAssigned:
				# Create a new entry
				log.debug('....Assigning a new consultation')
				receipt_item = model.InvReceiptItems(CatalogItemID=ConsultationID,ReceiptID=ReceiptID,Quantity=1)
		raise cherrypy.HTTPRedirect('/billing/?receipt_id=%d' % ReceiptID)

		

