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
from model import DATE_FORMAT
import widgets_person
from widgets_encounter import EncounterFormPage1
import widgets_encounter
from div_dialogs.widgets import DialogBoxLink

log = logging.getLogger("turbocare.controllers")

class HRef(widgets.Widget):
	params=['link_text','link_ref']
	#link_href = ''
	#link_text = ''

	def __init__(self, link_text='', link_ref='', *args, **kw):
		super(HRef,self).__init__(*args, **kw)
		self.link_ref = link_ref
		self.link_text = link_text
	
	template = '''
	<a xmlns:py="http://purl.org/kid/ns#" href="${link_href}">${link_text}</a>
	'''
def Checked(value):
	if value:
		return "checked"
	else:
		return None
def ConvertDate(value):
	if value not in [None, '']:
		tdate = time.strptime(str(value),DATE_FORMAT)
		return datetime.datetime(tdate.tm_year,tdate.tm_mon,tdate.tm_mday)
	else:
		return None
def ConvertInt(value):
	if value in ['', None]:
		return None
	else:
		try:
			return int(value)
		except ValueError:
			return None

class PersonManager(turbogears.controllers.Controller):
	@expose(html='turbocare.templates.programmingerror')
	def idFail(error):
		error= "Not Permited to do operation"
		log.debug(error)
		next_link = "/"
		return dict(error_message = error, next_link=next_link)
	
	@identity.require(identity.has_permission("person_manager_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	@expose(html='turbocare.templates.pm_Main')
	def index(self, PersonID=None, CustomerID=None, PersonellID=None, **kw):
		'''     The main page for the Person manager - which will also do patient management
			PersonID -  the id of the person we want to load (priority)
			CustomerID - if no PersonID is available, customer id will suffice
			PersonellID - final resort for an id to load
			If no Id's are given, then the user is re-directed to the Search Screen
		'''
		def DateConvert(value):
			if value:
				return value.strftime(DATE_FORMAT)
			else:
				return ""
		def CreateCustomer(Person):
			"""     Create a customer record based on the Person record """
			if Person.AddrCitytownNrID:
				citytown = model.AddressCityTown.get(Person.AddrCitytownNrID)
				AddressLabel = '%s\n%s\n%s, %s\n%s\n%s' % (Person.AddrStr, citytown.Name, citytown.Block, citytown.District, citytown.State, citytown.ZipCode)                  
			else:
				AddressLabel = Person.AddrStr
			PersonName = ('%s %s,%s,%s' % (Person.Title, Person.NameFirst, Person.NameMiddle, Person.NameLast)).replace(',,',',').replace(',', ' ').strip()
			customer = model.InvCustomer(Name=PersonName ,CityID=Person.AddrCitytownNrID , AddressLabel=AddressLabel, CreditAmount=0.0, \
				InventoryLocation=self.GetDefaultCustomerLocationID(), ExternalID=Person.id)
			return customer
		def GetCustomer(Person):
			"""     Look for a customer based on the person record.  If none is found, then create it """
			customers = model.InvCustomer.select(model.InvCustomer.q.ExternalID==Person.id)
			if customers.count() == 0:
				return CreateCustomer(Person)
			else:
				return customers[0]
		# Load any data
		# Set our defaults
		person = None
		customer = None
		personell = None
		if PersonID or CustomerID or PersonellID:
			try:
				if PersonID:
					person = model.Person.get(int(PersonID))
					customer = GetCustomer(person)
					if len(person.Personell) > 0:
						personell = person.Personell[0]
				elif CustomerID:
					customer = model.InvCustomer.get(int(CustomerID))
					person = customer.External
					if len(person.Personell) > 0:
						personell = person.Personell[0]
				else:
					personell = model.Personell.get(int(PersonellID))
					person = personell.Person
					customer = GetCustomer(person)
			except SQLObjectNotFound:
				turbogears.flash("Could not find the record you wanted")
		if not PersonID and person:
			PersonID = person.id
		# Person Information
		personvalues = None
		if person:
			personvalues = self.LoadPersonValues(person)
		# Customer Information
		customervalues = None
		receiptvalues = []
		paymentvalues = []
		if customer:
			customervalues = {}
			customervalues['CustomerID'] = customer.id
			customervalues['CreditAmount'] = customer.CreditAmount
			customervalues['Accounting'] = customer.Accounting
			customervalues['InventoryLocation'] = customer.InventoryLocationID
			# Get Receipt values
			for receipt in customer.Receipts:
				#receipt_link = '<a href="/billing/?receipt_id=%d">%d</a>' % (receipt.id, receipt.id)
				receipt_link = HRef()
				receiptvalues.append((receipt_link.display(link_href='/billing/?receipt_id=%d' % receipt.id, link_text=receipt.id), '%d Items purchased on %s (%s)' % (receipt.CountPurchasedItems(), receipt.ModifyTime.strftime(DATE_FORMAT), receipt.StatusText()), receipt.TotalPaymentCalc()))
			# Get Payment values
			for payment in customer.Payments:
				paymentvalues.append((payment.id, '%s on %s' % (payment.Type(), payment.DatePaid.strftime(DATE_FORMAT)), payment.Amount))
		# Employee Information
		personellvalues = {}
		if person:
			personellvalues['PersonellPersonID'] = person.id
		if personell:
			personellvalues['PersonellID'] = personell.id
			personellvalues['JobFunctionTitle'] = personell.JobFunctionTitle
			personellvalues['DateJoin'] = DateConvert(personell.DateJoin)
			personellvalues['DateExit'] = DateConvert(personell.DateExit)
			personellvalues['ContractClass'] = personell.ContractClass
			personellvalues['ContractStart'] = DateConvert(personell.ContractStart)
			personellvalues['ContractEnd'] = DateConvert(personell.ContractEnd)
			personellvalues['IsDischarged'] = Checked(personell.IsDischarged)
			personellvalues['PayClass'] = personell.PayClass
			personellvalues['PayClassSub'] = personell.PayClassSub
			personellvalues['LocalPremiumId'] = personell.LocalPremiumId
			personellvalues['TaxAccountNr'] = personell.TaxAccountNr
			personellvalues['IrCode'] = personell.IrCode
			personellvalues['NrWorkday'] = personell.NrWorkday
			personellvalues['NrWeekhour'] = personell.NrWeekhour
			personellvalues['NrVacationDay'] = personell.NrVacationDay
			personellvalues['MultipleEmployer'] = personell.MultipleEmployer
			personellvalues['NrDependent'] = personell.NrDependent
		# Patient Information
		encountervalues = []
		dialogboxes = []
		if person:
			for encounter in person.Encounters:
				encountervalues.append((HRef().display(link_href='Encounter?EncounterID=%d' % encounter.id, link_text=encounter.id), encounter.Description()))
				#encountervalues.append((DialogBoxLink(title=encounter.Description(),link_text="%d" % encounter.id,dom_id='encounter_dialogbox%d' % encounter.id).display(), encounter.Description()))
		# Attempt to load our objects
		person_form = widgets.TableForm(name="person_form", fields=widgets_person.PersonForm(), \
							submit_text="Save", action="PersonSave") #, validator=EmailFormSchema())
		customer_form = widgets.TableForm(name="customer_form", fields=widgets_person.CustomerForm(), \
							submit_text="Save", action="CustomerSave") #, validator=EmailFormSchema())
		personell_form = widgets.TableForm(name="personell_form", fields=widgets_person.PersonellForm(), \
							submit_text="Save", action="PersonellSave") #, validator=EmailFormSchema())
		tabber = widgets.Tabber()
		person_search = widgets.RemoteForm(update = 'search_results', fields = [widgets.TextField("searchtext",label="Search")],
							name="person_search",action = "PersonSearch")
		return dict(person_form=person_form,tabber=tabber,person_search=person_search, personvalues=personvalues,
			customer_form=customer_form, customervalues=customervalues,customer_payments=widgets_person.Payments,
			customer_receipts=widgets_person.Receipts, PersonID=PersonID, receiptvalues=receiptvalues,
			paymentvalues = paymentvalues, personellvalues=personellvalues, personell_form=personell_form,
			encountervalues=encountervalues, encounters=widgets_person.Encounters)
	
	def LoadPersonValues(self, person):
		''' Load the values of person into a dictionary for our form '''
		personvalues = {}
		personvalues['Citizenship'] = person.Citizenship
		personvalues['SssNr'] = person.SssNr
		personvalues['NatIdNr'] = person.NatIdNr
		personvalues['Occupation'] = person.Occupation
		personvalues['PersonID'] = person.id
		personvalues['Title'] = person.Title
		personvalues['NameFirst'] = person.NameFirst
		personvalues['NameMiddle'] = person.NameMiddle
		personvalues['NameLast'] = person.NameLast
		personvalues['DateBirth'] = person.DateBirth
		personvalues['AddrStr'] = person.AddrStr
		personvalues['AddrZip'] = person.AddrZip
		personvalues['AddrCitytownNr'] = person.AddrCitytownNrID
		personvalues['AddrCitytownNr_text'] = 'TEST'#person.AddrCitytownNrID
		personvalues['Phone1Nr'] = person.Phone1Nr
		personvalues['Cellphone1Nr'] = person.Cellphone1Nr
		personvalues['Religion'] = person.Religion
		personvalues['Fax'] = person.Fax
		personvalues['Email'] = person.Email
		personvalues['CivilStatus'] = person.CivilStatus
		personvalues['Sex'] = person.Sex
		personvalues['EthnicOrig'] = person.EthnicOrigID
		return personvalues

	# These lines include the search functions locally - a necessary step
	CityFkSearch = widgets_person.CityFkSearch
	EthnicOrigFkSearch = widgets_person.EthnicOrigFkSearch
	OccupationSearch = widgets_person.OccupationSearch
	LocationSearch = widgets_person.LocationSearch
	EncounterClassSearch = widgets_encounter.EncounterClassSearch
	FinancialClassSearch = widgets_encounter.FinancialClassSearch
	InsuranceClassSearch = widgets_encounter.InsuranceClassSearch
	DoctorSearch = widgets_encounter.DoctorSearch
	@expose()
	def PersonSearch(self, searchtext=None, **kw):
		""" Search for a person... currently, only a name search """
		html = "<ul><h4>Results:</h4>"
		if searchtext:
			search = model.Person.select(OR (model.Person.q.NameFirst.contains(str(searchtext)), 
							model.Person.q.NameLast.contains(str(searchtext))))
			if search.count() > 0:
				for person in search:
					html += '<li><a href="?PersonID=%s">%s</a></li>' % (str(person.id), person.DisplayName())
		#log.debug(html)
		html += "</ul>"
		return html
	
	@expose()
	def PersonSave(self, PersonID=None, Title='', NameFirst='', NameMiddle='', NameLast='', DateBirth=None, AddrStr='', AddrZip='',
			AddrCitytownNr=None, Phone1Nr='', Cellphone1Nr='', Fax='', Email='', CivilStatus='', Sex='', EthnicOrig=None, Religion='',
			Citizenship='', SssNr = '', NatIdNr = '', Occupation = ''):
		""" Save Person data Ajax style """
		# If PersonID is None, then we have a new entry
		if EthnicOrig in ['',None]:
			EthnicOrig = None
		else:
			EthnicOrig = int(EthnicOrig)
		if AddrCitytownNr not in [None, '']:
			AddrCitytownNr = int(AddrCitytownNr)
		else:
			AddrCitytownNr = None
		if DateBirth not in [None, '']:
			#log.debug(DateBirth)
			bday = time.strptime(str(DateBirth),DATE_FORMAT)
			bdate = datetime.datetime(bday.tm_year,bday.tm_mon,bday.tm_mday)
		else:
			bdate = None
		if PersonID not in [None, '']:
			try:
				person = model.Person.get(int(PersonID))
			except SQLObjectNotFound:
				person = none
				turbogears.flash("The person couldn't be found, so we're creating a new record")
		else:
			person = None
		if not person:
			# Create new person and customer record
			person = model.Person(NameFirst=NameFirst,NameLast=NameLast,NameMiddle=NameMiddle,\
				AddrStr=AddrStr,AddrCitytownNrID=AddrCitytownNr,Sex=Sex, Religion=Religion,\
				DateBirth=bdate, EthnicOrig=EthnicOrig,Citizenship = Citizenship,SssNr = SssNr,\
				NatIdNr = NatIdNr,Occupation = Occupation)
		else:
			# Update the person information
			person.Citizenship = Citizenship
			person.SssNr = SssNr
			person.NatIdNr = NatIdNr
			person.Occupation = Occupation
			person.Title = Title
			person.NameFirst = NameFirst
			person.NameMiddle = NameMiddle
			person.NameLast = NameLast
			person.DateBirth = bdate
			person.AddrStr = AddrStr
			person.AddrZip = AddrZip
			person.AddrCitytownNrID = AddrCitytownNr
			person.Phone1Nr = Phone1Nr
			person.Cellphone1Nr = Cellphone1Nr
			person.Fax = Fax
			person.Email = Email
			person.CivilStatus = CivilStatus
			person.Sex = Sex
			person.EthnicOrigID = EthnicOrig
		# Update/add customer information
		if AddrCitytownNr:
			citytown = model.AddressCityTown.get(AddrCitytownNr)
			AddressLabel = '%s\n%s\n%s, %s\n%s\n%s' % (AddrStr, citytown.Name, citytown.Block, citytown.District, citytown.State, citytown.ZipCode)
		else:
			AddressLabel = AddrStr
		PatientName = ('%s %s,%s,%s' % (Title, NameFirst, NameMiddle, NameLast)).replace(',,',',').replace(',', ' ').strip()
		if len(person.Customer)==0:
			customer = model.InvCustomer(Name=PatientName ,CityID=person.AddrCitytownNrID , AddressLabel=AddressLabel, CreditAmount=0.0, \
							InventoryLocation=self.GetDefaultCustomerLocationID(), ExternalID=person.id)
		else:
			customer = person.Customer[0]
			customer.AddressLabel = AddressLabel
			customer.Name = PatientName
		raise cherrypy.HTTPRedirect("?PersonID=%d" % person.id)
		return "OK"
	
	@expose()
	def CustomerSave(self, CustomerID = None, Accounting = None, InventoryLocation = None, **kw):
		''' Save customer specific information... which isn't much at this point '''
		if InventoryLocation in [None, '']:
			InventoryLocation = None
		else:
			InventoryLocation = int(InventoryLocation)
		if CustomerID:
			try:
				customer = model.InvCustomer.get(int(CustomerID))
				customer.Accounting = Accounting
				customer.InventoryLocation = InventoryLocation
			except SQLObjectNotFound:
				turbogears.flash("The customer record doesn't exist")
		if customer:
			person = customer.External
			raise cherrypy.HTTPRedirect("?PersonID=%d" % person.id)
		return "OK"
	
	@expose()
	def PersonellSave(self, PersonellID=None, JobFunctionTitle='',DateJoin='', DateExit='', ContractClass='', ContractStart='',
			  ContractEnd='', IsDischarged=None, PayClass='', PayClassSub='', LocalPremiumId='', TaxAccountNr='', 
			  IrCode='', NrWorkday=None, NrWeekhour=None, NrVacationDay=None, MultipleEmployer=None, NrDependent=None,
			  PersonellPersonID=None):
		''' Save personell specific information '''
		# Convert inputs to proper datatypes
		DateJoin = ConvertDate(DateJoin)
		DateExit = ConvertDate(DateExit)
		ContractStart = ConvertDate(ContractStart)
		ContractEnd = ConvertDate(ContractEnd)
		NrWorkday = ConvertInt(NrWorkday)
		NrWeekhour = ConvertInt(NrWeekhour)
		NrVacationDay = ConvertInt(NrVacationDay)
		NrDependent = ConvertInt(NrDependent)
		# Find/create a personell record.  Note: a person record must exist
		if PersonellID not in ['', None]:
			try:
				personell = model.Personell.get(int(PersonellID))
			except SQLObjectNotFound:
				log.debug("PersonellSave (Person Manager) cannot find PersonellID %s" % PersonellID)
				personell = None
		else:
			personell = None
		if not personell and PersonellPersonID not in ['', None]:
			# No personell record... yet.  If we have a person id, then we'll create a new record
			try:
				person = model.Person.get(int(PersonellPersonID))
				personell = model.Personell(JobFunctionTitle=JobFunctionTitle,DateJoin=DateJoin, DateExit=DateExit, 
							    ContractClass=ContractClass, ContractStart=ContractStart, ContractEnd=ContractEnd, 
							    IsDischarged=(IsDischarged!=None), PayClass=PayClass, PayClassSub=PayClassSub, 
							    LocalPremiumId=LocalPremiumId, TaxAccountNr=TaxAccountNr, IrCode=IrCode, 
							    NrWorkday=NrWorkday, NrWeekhour=NrWeekhour, NrVacationDay=NrVacationDay, 
							    MultipleEmployer=(MultipleEmployer!=None), NrDependent=NrDependent, PersonID=person.id)
			except SQLObjectNotFound:
				log.debug("Tried creating a personell record, but the person record could not be found (controllers_person_manager)")
		elif personell:
			personell.JobFunctionTitle=JobFunctionTitle
			personell.DateJoin=DateJoin
			personell.DateExit=DateExit 
			personell.ContractClass=ContractClass
			personell.ContractStart=ContractStart
			personell.ContractEnd=ContractEnd
			personell.IsDischarged=(IsDischarged!=None)
			personell.PayClass=PayClass
			personell.PayClassSub=PayClassSub
			personell.LocalPremiumId=LocalPremiumId
			personell.TaxAccountNr=TaxAccountNr
			personell.IrCode=IrCode
			personell.NrWorkday=NrWorkday
			personell.NrWeekhour=NrWeekhour
			personell.NrVacationDay=NrVacationDay
			personell.MultipleEmployer=(MultipleEmployer!=None)
			personell.NrDependent=NrDependent
		else:
			log.debug("Attempted to save the personell record, but there is insufficient information to do this (controllers_person_manager)")
		if personell or person:
			if not person:
				person = personell.Person
			raise cherrypy.HTTPRedirect("?PersonID=%d" % person.id)
		else:
			raise cherrypy.HTTPRedirect("index")
		return "OK"

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
	
	@identity.require(identity.has_permission("person_manager_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	@expose(html='turbocare.templates.pm_Encounter')
	def Encounter(self, EncounterID=None, **kw):
		''' Load and display Encounter (visit) information '''
		encountervalues = {}
		Name = 'Unknown Encounter'
		PersonLink = "index"
		if EncounterID:
			try:
				encounter = model.Encounter.get(int(EncounterID))
				person = encounter.P
			except SQLObjectNotFound:
				encounter = None
			if encounter:
				encountervalues['PersonID'] = person.id
				encountervalues['EncounterDate'] = encounter.EncounterDate
				encountervalues['IsDischarged'] = Checked(encounter.IsDischarged)
				# FIX THIS next line for date time, not just date
				encountervalues['DischargeDateTime'] = encounter.DischargeDate
				encountervalues['EncounterClassNr'] = encounter.EncounterClassNrID
				encountervalues['EncounterType'] = encounter.EncounterType
				encountervalues['EncounterStatus'] = encounter.EncounterStatus
				encountervalues['ExtraService'] = encounter.ExtraService				
				encountervalues['FinancialClassNr'] = encounter.FinancialClassNrID
				encountervalues['InsuranceNr'] = encounter.InsuranceNr
				encountervalues['InsuranceFirmId'] = encounter.InsuranceFirmId
				encountervalues['InsuranceClassNr'] = encounter.InsuranceClassNrID
				encountervalues['Insurance2Nr'] = encounter.Insurance2Nr
				encountervalues['Insurance2FirmId'] = encounter.Insurance2FirmId
				encountervalues['ReferrerDiagnosis'] = encounter.ReferrerDiagnosis
				encountervalues['ReferrerRecomTherapy'] = encounter.ReferrerRecomTherapy
				encountervalues['ReferrerDr'] = encounter.ReferrerDr
				encountervalues['ReferrerDept'] = encounter.ReferrerDept
				encountervalues['ReferrerInstitution'] = encounter.ReferrerInstitution
				encountervalues['ReferrerNotes'] = encounter.ReferrerNotes
				encountervalues['CurrentAttDrNr'] = encounter.CurrentAttDrNrID
				encountervalues['ConsultingDr'] = encounter.ConsultingDr
				encountervalues['FollowupDate'] = encounter.FollowupDate
				encountervalues['FollowupResponsibility'] = encounter.FollowupResponsibility
				encountervalues['PostEncounterNotes'] = encounter.PostEncounterNotes
				# Other page variables
				Name = person.DisplayNameAsContact()
				PersonLink = "index?PersonID=%d" % person.id
		encounter_form = widgets.TableForm(name="encounter_form%d" % encounter.id, fields=EncounterFormPage1(),
					submit_text="Save", action="EncounterSave?EncounterID=%d" % encounter.id)
		person_search = widgets.RemoteForm(update = 'search_results', fields = [widgets.TextField("searchtext",label="Search")],
							name="person_search",action = "PersonSearch")
		return dict(encounter_form=encounter_form, encountervalues=encountervalues,Name=Name,PersonLink=PersonLink,
			    person_search=person_search)
	
	
	@identity.require(identity.has_permission("person_manager_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	@expose()
	def EncounterSave(self, EncounterID=None, **kw):
		''' Update Encounter information
		Note, there are some issues with this: what if someone changes from insurance to self-pay?  what happens to current receipts?
		'''
		if EncounterID:
			try:
				encounter = model.Encounter.get(int(EncounterID))
			except SQLObjectNotFound:
				encounter = None
		if encounter:
			for key in kw.keys():
				if hasattr(encounter,key):
					if key in ['EncounterDate','DischargeDateTime','FollowupDate']:
						setattr(encounter,key,ConvertDate(kw[key]))
					elif key in ['IsDischarged']:
						setattr(encounter,key,True)
					elif key in ['EncounterClassNrID','FinancialClassNrID','InsuranceClassNrID','CurrentAttDrNrID']:
						setattr(encounter,key,ConvertInt(kw[key]))
					else:
						setattr(encounter,key,kw[key])
			if 'IsDischarged' not in kw.keys():
				encounter.IsDischarged = False
			raise cherrypy.HTTPRedirect("Encounter?EncounterID=%s" % encounter.id)
		else:
			raise cherrypy.HTTPRedirect("index")