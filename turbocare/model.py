from datetime import datetime

from sqlobject import *

from turbogears import identity 
from turbogears.database import PackageHub
from model_inventory import *

hub = PackageHub("care2x")
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass
dbReligion = ['Christian', 'Hindu', 'Muslim', 'Scientology', 'Unknown']
dbGender = ['U','F','M']
dbTitles = ['Ms.', 'Mrs.', 'Mr.', 'Dr.']

class Visit(SQLObject):
    class sqlmeta:
        table = "visit"

    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName="by_visit_key")
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()

    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)

    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    def _set_password(self, cleartext_password):
        "Runs cleartext_password through the hash algorithm before saving."
        hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(hash)

    def set_password_raw(self, password):
        "Saves the password as-is to the database."
        self._SO_set_password(password)


class VisitIdentity(SQLObject):
    visit_key = StringCol( length=40, alternateID=True,
                          alternateMethodName="by_visit_key" )
    user_id = IntCol()


class Group(SQLObject):
    """
    An ultra-simple group definition.
    """
    
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table="tg_group"
    
    group_name = UnicodeCol( length=35, alternateID=True,
                            alternateMethodName="by_group_name" )
    display_name = UnicodeCol( length=255 )
    created = DateTimeCol( default=cur_date_time() )

    # collection of all users belonging to this group
    users = RelatedJoin( "User", intermediateTable="user_group",
                        joinColumn="group_id", otherColumn="id" )

    # collection of all permissions for this group
    permissions = RelatedJoin( "Permission", joinColumn="group_id", 
                              intermediateTable="group_permission",
                              otherColumn="permission_id" )


class User(SQLObject):
    """
    Reasonably basic User definition. Probably would lbwant additional attributes.
    """
    import md5 #Because care2x uses md5
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table="care_users"
        idName='id'

    user_name = UnicodeCol( length=35, alternateID=True,
                           alternateMethodName="by_user_name", dbName='login_id' )
    email_address = UnicodeCol( length=255, alternateID=True, dbName='history',
                               alternateMethodName="by_email_address" )
    display_name = UnicodeCol( length=60, dbName='name' )
    password = UnicodeCol( length=255, dbName='password' )
    created = DateTimeCol( default=cur_date_time(), dbName = 'create_time' )

    # groups this user belongs to
    #modified from original
    groups = RelatedJoin( "Group", intermediateTable="user_group",
                         joinColumn="id", otherColumn="group_id" )

    def _get_permissions( self ):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms
        
    def _set_password( self, cleartext_password ):
        "Runs cleartext_password through the hash algorithm before saving."
        hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(hash)
        
    def set_password_raw( self, password ):
        "Saves the password as-is to the database."
        self._SO_set_password(password)



class Permission(SQLObject):
    class sqlmeta:
        table="tg_permissions"

    permission_name = UnicodeCol( length=35, alternateID=True,
                                 alternateMethodName="by_permission_name" )
    description = UnicodeCol( length=255 )
    
    groups = RelatedJoin( "Group",
                        intermediateTable="group_permission",
                         joinColumn="permission_id", 
                         otherColumn="group_id" )

#
#	My database classes
#

class AddressCityTown(SQLObject):
	'''	Address information '''
	class sqlmeta:
		table = "care_address_citytown"
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
		
	def AddressBlock(self):
		'''	Text formatted as an address block
		'''
		return  '%s\n%s, %s\n%s\n%s' % (self.Name, self.Block, self.District, self.State, self.ZipCode)
	
	def DisplayName(self):
		'''	Address formatted as a one line entry
		'''
		Text = '%s in %s: %s, %s, %s [%s]' % (self.Block, self.Name, self.District, self.State, self.ZipCode, self.IsoCountryId)
		Text = Text.replace('unknown','?').replace('Unknown','?')
		return  Text
				
	#care_address_citytown
#	nr #int primary key
	UneceModifier = StringCol(length=2, default='') #char 2 
	UneceLocode = StringCol(length=15, default='')#char 15
	Name = StringCol(length=100)#char 100
	ZipCode = StringCol(length=25, default='Unknown')#char 25
	IsoCountryId = StringCol(length=3, default='IND')#char 3
	Block = StringCol(length=60)#char 60
	District = StringCol(length=60)#char 60
	State = StringCol(length=60, default='Nagaland')#char 60
	UneceLocodeType = IntCol(default=0)#int 3
	UneceCoordinates = StringCol(length=25, default='')#char 25
	InfoUrl = StringCol(length=255, default='')#char 255
	Persons = MultipleJoin("Person",joinColumn="addr_citytown_nr")
	UseFrequency = IntCol(default=1)#int
	Status = StringCol(length=25, default='')#char 25
	History = StringCol(default='')#text
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class ClassEthnicOrig(SQLObject):
	class sqlmeta:
		table = "care_class_ethnic_orig"
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
				
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var',default='')
	Status = StringCol(length=25,dbName='status',default='')
	Types = MultipleJoin("TypeEthnicOrig",joinColumn='class_nr')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Person(SQLObject):
	class sqlmeta:
		table = "care_person"
		idName = 'pid'
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

	def _set_DateReg(self, value):
		try:
			if self.DateReg == '':
				value = cur_date_time()
			else:
				value = self.DateReg
		except AttributeError:
			value = cur_date_time()
		self._SO_set_DateReg(value)
		
	def DisplayName(self):
		Name = ''
		if self.Title !=None and self.Title.isalnum():
			Name = self.Title
		if self.NameFirst != None and self.NameFirst.isalnum():
			Name+=' '+self.NameFirst
			Name = Name.strip()
		if self.NameMiddle != None and self.NameMiddle.isalnum():
			Name+=' '+self.NameMiddle
			Name = Name.strip()
		if self.NameLast != None and self.NameLast.isalnum():
			Name+=' '+self.NameLast
			Name = Name.strip()
		LastVisit = self.GetLatestEncounterDate()
		if LastVisit > datetime(1900,1,1):
			Visits = ' (last visit on %s)' % LastVisit.strftime(DATE_FORMAT)
		else:
			Visits = ''
		return Name + Visits
	
	def DisplayNameAsContact(self):
		Name = ''
		if self.Title !=None and self.Title.isalnum():
			Name = self.Title
		if self.NameFirst != None and self.NameFirst.isalnum():
			Name+=' '+self.NameFirst
			Name = Name.strip()
		if self.NameMiddle != None and self.NameMiddle.isalnum():
			Name+=' '+self.NameMiddle
			Name = Name.strip()
		if self.NameLast != None and self.NameLast.isalnum():
			Name+=' '+self.NameLast
			Name = Name.strip()
		return Name

	def GetLatestEncounter(self, MaxEncounterDate=datetime(2100,1,1)):
		EncounterID = None
		EncounterDate = datetime(1900,1,1)
		for Encounter in self.Encounters:
			if (Encounter.EncounterDate > EncounterDate) and (Encounter.EncounterDate <=MaxEncounterDate):
				EncounterDate = Encounter.EncounterDate
				EncounterID = Encounter.id
		return EncounterID
		
	def GetLatestEncounterVar(self, MaxEncounterDate=datetime(2100,1,1), VarName='DateReg'):
		'''	Return the latest value for a specific variable.  This is not always from the latest encounter.
			If the latest encounter has a 'None' value.  The latest non-None value will be returned.
			If there is no previous value, None will be returned.
		'''
		EncounterDate = datetime(1900,1,1)
		EncounterID = None
		Value = None
		for Encounter in self.Encounters:
			if (Encounter.EncounterDate > EncounterDate) and (Encounter.EncounterDate <=MaxEncounterDate) and (getattr(Encounter,VarName,None)!=None):
				EncounterDate = Encounter.EncounterDate
				EncounterID = Encounter.id
				Value = getattr(Encounter,VarName,None)
		return Value

	def GetLatestEncounterDate(self, MaxEncounterDate=datetime(2100,1,1)):
		EncounterID = None
		EncounterDate = datetime(1900,1,1)
		for Encounter in self.Encounters:
			if (Encounter.EncounterDate > EncounterDate) and (Encounter.EncounterDate <=MaxEncounterDate):
				EncounterDate = Encounter.EncounterDate
				break;
		return EncounterDate

	DateReg = DateTimeCol(dbName='date_reg',default=cur_date_time())
	NameFirst = StringCol(length=60, dbName='name_first')
	Name2 = StringCol(length=60, dbName='name_2', default=None)
	Name3 = StringCol(length=60, dbName='name_3', default=None)
	NameMiddle = StringCol(length=60,dbName='name_middle', default=None)
	NameLast = StringCol(length=60,dbName='name_last')
	NameMaiden = StringCol(length=60,dbName='name_maiden', default=None)
	NameOthers = StringCol(length=255,dbName='name_others', default=None)
	DateBirth = DateTimeCol(dbName='date_birth')
	BloodGroup = StringCol(length=2,dbName='blood_group', default=None)
	AddrStr = StringCol(length=60,dbName='addr_str')
	AddrStrNr = StringCol(length=10,dbName='addr_str_nr', default=None)
	AddrZip = StringCol(length=15,dbName='addr_zip', default=None)
	AddrCitytownNr = ForeignKey("AddressCityTown", dbName='addr_citytown_nr')
	AddrIsValid = BoolCol(dbName='addr_is_valid', default=None)
	Citizenship = StringCol(length=35,dbName='citizenship', default=None)
	Phone1Code = StringCol(length=15, dbName='phone_1_code', default=None)
	Phone1Nr = StringCol(length=35, dbName='phone_1_nr', default=None)
	Phone2Code = StringCol(length=15, dbName='phone_2_code', default=None)
	Phone2Nr = StringCol(length=35, dbName='phone_2_nr', default=None)
	Cellphone1Nr = StringCol(length=35, dbName='cellphone_1_nr', default=None)
	Cellphone2Nr = StringCol(length=35, dbName='cellphone_2_nr', default=None)
	Fax = StringCol(length=35,dbName='fax', default=None)
	Email = StringCol(length=60,dbName='email', default=None)
	CivilStatus = StringCol(length=35,dbName='civil_status', default=None)
	Sex = StringCol(length=1,dbName='sex')
	Title = StringCol(length=25,dbName='title', default=None)
	Photo = BLOBCol(dbName='photo', default=None)
	PhotoFilename = StringCol(length=60,dbName='photo_filename', default=None)
	EthnicOrig = ForeignKey("TypeEthnicOrig", dbName='ethnic_orig', default=None)
	OrgId = StringCol(length=60,dbName='org_id', default=None)
	SssNr = StringCol(length=60,dbName='sss_nr', default=None)
	NatIdNr = StringCol(length=60,dbName='nat_id_nr', default=None)
	Religion = StringCol(length=125,  default=None,dbName='religion')
	MotherPid = ForeignKey("Person", dbName='mother_pid', default=None)
	FatherPid = ForeignKey("Person", dbName='father_pid', default=None)
	ContactPerson = StringCol(length=255,dbName='contact_person', default=None)
	ContactPid = ForeignKey("Person",dbName='contact_pid', default=None)
	ContactRelation = StringCol(length=25,dbName='contact_relation', default=None)
	DeathDate = DateCol(dbName='death_date', default=None)
	DeathEncounterNr = ForeignKey("Encounter", dbName='death_encounter_nr', default=None)
	DeathCause = StringCol(length=255,dbName='death_cause', default=None)
	DeathCauseCode = StringCol(length=15,dbName='death_cause_code', default=None) # foreign key?
	DateUpdate = DateTimeCol(dbName='date_update',default=cur_date_time())
	Occupation = StringCol(length=60,dbName='occupation',default=None)
	Encounters = MultipleJoin("Encounter",joinColumn="pid")
	Customer = MultipleJoin("InvCustomer", joinColumn="external_id")
	Status = StringCol(length=20, default='',dbName='status')
	History = StringCol(length=255, default='',dbName='history')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class ClassInsurance(SQLObject):
	class sqlmeta:
		table = "care_class_insurance"
		idName = 'class_nr'
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
		
	ClassId = StringCol(length=35,dbName='class_id')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=25,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class ClassFinancial(SQLObject):
	class sqlmeta:
		table = "care_class_financial"
		idName = 'class_nr'
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

	ClassId = StringCol(length=15,dbName='class_id')
	Type = StringCol(length=25,dbName='type')
	Code = StringCol(length=5,dbName='code')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=25,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Policy = StringCol(length=255,dbName='policy')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeDischarge(SQLObject):
	class sqlmeta:
		table = "care_type_discharge"
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

	Type = StringCol(length=35)
	Name = StringCol(length=100)
	LdVar = StringCol(length=25)
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',
	
class TypeLocation(SQLObject):
	class sqlmeta:
		table = "care_type_location"
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

	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	Description = StringCol(length=255,dbName='description')
	LdVar = StringCol(length=25,dbName='LD_var')
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Personell(SQLObject):
	class sqlmeta:
		table = "care_personell"
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
		
	def DisplayName(self):
		Name = ''
		if self.Person.Title !=None and self.Person.Title.isalnum():
			Name = self.Person.Title
		if self.Person.NameFirst != None and self.Person.NameFirst.isalnum():
			Name+=' '+self.Person.NameFirst
			Name = Name.strip()
		if self.Person.NameMiddle != None and self.Person.NameMiddle.isalnum():
			Name+=' '+self.Person.NameMiddle
			Name = Name.strip()
		if self.Person.NameLast != None and self.Person.NameLast.isalnum():
			Name+=' '+self.Person.NameLast
			Name = Name.strip()
		return Name

	ShortId = StringCol(length=10, dbName='short_id', default=None)
	Person = ForeignKey("Person", dbName='pid')
	JobTypeNr = IntCol(dbName='job_type_nr',default=None)
	JobFunctionTitle = StringCol(length=60,dbName='job_function_title')
	DateJoin = DateCol(default=cur_date_time(),dbName='date_join')
	DateExit = DateCol(dbName='date_exit', default=None)
	ContractClass = StringCol(length=35,dbName='contract_class',default=None)
	ContractStart = DateCol(default=cur_date_time(),dbName='contract_start')
	ContractEnd = DateCol(dbName='contract_end',default=None)
	IsDischarged = BoolCol(dbName='is_discharged',default=False)
	PayClass = StringCol(length=25,dbName='pay_class',default=None)
	PayClassSub = StringCol(length=25,dbName='pay_class_sub',default=None)
	LocalPremiumId = StringCol(length=5,dbName='local_premium_id',default=None)
	TaxAccountNr = StringCol(length=60,dbName='tax_account_nr',default=None)
	IrCode = StringCol(length=25,dbName='ir_code',default=None)
	NrWorkday = IntCol(dbName='nr_workday',default=5)
	NrWeekhour = FloatCol(dbName='nr_weekhour',default=40)
	NrVacationDay = IntCol(dbName='nr_vacation_day',default=20)
	MultipleEmployer = BoolCol(dbName='multiple_employer',default=False)
	NrDependent = IntCol(dbName='nr_dependent',default=0)
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_date_time())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_date_time())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterLocation(SQLObject):
	class sqlmeta:
		table = "care_encounter_location"
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

	EncounterNr = ForeignKey("Encounter", dbName='encounter_nr')
	TypeNr = ForeignKey("TypeLocation", dbName='type_nr') # care_type_location -> nr: Room, Ward, Department...
	LocationNr = IntCol(dbName='location_nr')
	GroupNr = IntCol(dbName='group_nr',default=None)
	DateFrom = DateCol(default=cur_date_time(),dbName='date_from')
	DateTo = DateCol(dbName='date_to', default=None)
	TimeFrom = StringCol(default=str(cur_date_time()).rjust(8),dbName='time_from')
	TimeTo = StringCol(dbName='time_to',default=None)
	DischargeTypeNr = ForeignKey("TypeDischarge", dbName='discharge_type_nr',default=None) # care_type_discharge -> nr
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class ClassEncounter(SQLObject):
	class sqlmeta:
		table = "care_class_encounter"
		idName = 'class_nr'
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

	ClassId = StringCol(length=35,dbName='class_id')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=25,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	HideFrom = IntCol(dbName='hide_from')
	ModifyId = StringCol(length=35,default=cur_user_id())
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())
	CreateTime = DateTimeCol(default=cur_date_time())

class Encounter(SQLObject):
	class sqlmeta:
		table = "care_encounter"
		idName = 'encounter_nr'
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
		
	def GetRoomDays(self):
		'''	Return a list of dictionaries which contain
			EncounterLocationID, WardID, Days
		'''
		RoomDays = []
		# Get all our encounter locations
		for location in self.EncounterLocations:
			if (location.TypeNrID == TYPE_LOCATION['bed']) and ((location.DateTo != None) or (location.DischargeTypeNrID>0)):
				df = location.DateFrom
				tf = time.strptime(str(location.TimeFrom),'%H:%M:%S')
				DateTimeFrom = datetime(df.year,df.month,df.day,tf.tm_hour,tf.tm_min,tf.tm_sec)
				dt = location.DateTo
				tt = time.strptime(str(location.TimeTo),'%H:%M:%S')
				DateTimeTo = datetime(dt.year,dt.month,dt.day,tt.tm_hour,tt.tm_min,tt.tm_sec)
				diff = DateTimeTo - DateTimeFrom
				days = float(diff.days) + diff.seconds/60.0/60.0/24
				RoomDays.append(dict(EncounterLocationID=location.id,WardID=location.GroupNr,Days=days))
			elif location.TypeNrID == TYPE_LOCATION['bed'] and (location.DateTo == None):
				df = location.DateFrom
				tf = time.strptime(str(location.TimeFrom),'%H:%M:%S')
				DateTimeFrom = datetime(df.year,df.month,df.day,tf.tm_hour,tf.tm_min,tf.tm_sec)
				DateTimeTo = datetime.now()
				diff = DateTimeTo - DateTimeFrom
				days = float(diff.days )+ diff.seconds/60.0/60.0/24
				if days < 1.0: #Minimum day assignment is 1 day!!
					days = 1.0
				RoomDays.append(dict(EncounterLocationID=location.id,WardID=location.GroupNr,Days=days))				
		return RoomDays
				
	def CurrentBedNumber(self):
		for location in self.EncounterLocations:
			if (location.DischargeTypeNrID == None or location.DischargeTypeNrID == 0) and location.TypeNr.Type == 'bed':
				return location.LocationNr
		return None

	Pid = ForeignKey("Person", dbName='pid')
	EncounterDate = DateTimeCol(default=cur_date_time(), dbName='encounter_date')
	EncounterClassNr = ForeignKey("ClassEncounter", dbName='encounter_class_nr',default=None) #Inpatient/Outpatient
	EncounterType = StringCol(length=35,dbName='encounter_type',default=None) #TypeEncounter
	EncounterStatus = StringCol(length=35,dbName='encounter_status',default='')
	ReferrerDiagnosis = StringCol(length=255,dbName='referrer_diagnosis',default=None)
	ReferrerRecomTherapy = StringCol(length=255,dbName='referrer_recom_therapy',default=None)
	ReferrerDr = StringCol(length=60,dbName='referrer_dr',default=None)
	ReferrerDept = StringCol(length=255,dbName='referrer_dept',default=None)
	ReferrerInstitution = StringCol(length=255,dbName='referrer_institution',default=None)
	ReferrerNotes = StringCol(length=255,dbName='referrer_notes',default=None)
	FinancialClassNr = ForeignKey("ClassFinancial", dbName='financial_class_nr') # Not patient type: this is if the room/nurse/dr are private or common or private plus
	InsuranceNr = StringCol(length=25,dbName='insurance_nr',default=None)#IMPORTANT
	InsuranceFirmId = StringCol(length=25,dbName='insurance_firm_id',default=None) #care_insurance_firm -> firm_id ******IMPORTANT
	InsuranceClassNr = ForeignKey("ClassInsurance", dbName='insurance_class_nr') #IMPORTANT - self pay, private, etc
	Insurance2Nr = StringCol(length=25, dbName='insurance_2_nr',default=None)
	Insurance2FirmId = StringCol(length=25, dbName='insurance_2_firm_id',default=None) #care_insurance_firm -> firm_id
	GuarantorPid = ForeignKey("Person", dbName='guarantor_pid',default=None)
	ContactPid = ForeignKey("Person", dbName='contact_pid',default=None)
	ContactRelation = StringCol(length=35,dbName='contact_relation',default=None)
	CurrentWardNr = ForeignKey('Ward',dbName='current_ward_nr',default=None) # care_encounter_location -> location_nr
	CurrentRoomNr = IntCol(dbName='current_room_nr',default=None) # care_encounter_location -> location_nr
	InWard = BoolCol(default=None,dbName='in_ward')
	CurrentDeptNr = ForeignKey('Department',dbName='current_dept_nr',default=None) # care_encounter_location -> location_nr
	InDept = BoolCol(default=False,dbName='in_dept')
	CurrentFirmNr = IntCol(dbName='current_firm_nr',default=None)
	CurrentAttDrNr = ForeignKey("Personell", dbName='current_att_dr_nr',default=None) # care_personell -> nr
	ConsultingDr = StringCol(length=60,dbName='consulting_dr',default=None)
	ExtraService = StringCol(length=25,dbName='extra_service',default=None)
	IsDischarged = BoolCol(default=False,dbName='is_discharged')
	DischargeDate = DateTimeCol(default=None,dbName='discharge_date') 
	DischargeTime = StringCol(default=None,dbName='discharge_time') #str(cur_date_time()).rjust(8)
	FollowupDate = DateCol(default=None,dbName='followup_date')
	FollowupResponsibility = StringCol(length=255,dbName='followup_responsibility',default=None)
	PostEncounterNotes = StringCol(length=255,dbName='post_encounter_notes',default=None)
	#Multijoins
	EncounterLocations = MultipleJoin("EncounterLocation",joinColumn="encounter_nr")
	Receipts = MultipleJoin("InvReceipt",joinColumn="external_id")
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',
	
class BillingItem(SQLObject):
	class sqlmeta:
		table = "care_billing_item"
		idName = 'item_id'
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

	ItemUnitCost = FloatCol(dbName='item_unit_cost') #float(10,2) default '0.00',
	ItemCode = StringCol(alternateID='true', length=5,dbName='item_code')#varchar(5) NOT NULL,
	ItemDescription = StringCol(length=100,dbName='item_description')#varchar(100) default NULL,
	ItemType = StringCol(length=255,dbName='item_type')#tinytext,
	ItemDiscountMaxAllowed = BoolCol(dbName='item_discount_max_allowed')#tinyint(4) unsigned default '0',
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',	
	ItemStatus = StringCol(length=25,default='')#varchar(25) default '',

class BillingBill(SQLObject):
	class sqlmeta:
		table = "care_billing_bill"
		idName = 'bill_bill_no'
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

	BillEncounterNr = ForeignKey("Encounter", dbName='bill_encounter_nr')
	BillDateTime = DateTimeCol(default = cur_date_time(), dbName='bill_date_time')
	BillAmount = FloatCol(dbName='bill_amount')
	BillOutstanding = FloatCol(dbName='bill_outstanding')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class BillingBillItem(SQLObject):
	class sqlmeta:
		table = "care_billing_bill_item"
		idName = 'bill_item_id'
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

	BillItemEncounterNr = ForeignKey("Encounter", dbName='bill_item_encounter_nr')
	BillItemCode = StringCol(length=5,dbName='bill_item_code') # BillingItem -> ItemCode
	BillItemUnitCost = FloatCol(dbName='bill_item_unit_cost')
	BillItemUnits = IntCol(dbName='bill_item_units')
	BillItemAmount = FloatCol(dbName='bill_item_amount')
	BillItemDate = DateTimeCol(default=cur_date_time(),dbName='bill_item_date')
	BillItemStatus = EnumCol(enumValues = ['0','1'],dbName='bill_item_status')
	BillItemBillNo = ForeignKey("BillingBill", dbName='bill_item_bill_no')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class BillingFinal(SQLObject):
	class sqlmeta:
		table = "care_billing_final"
		idName = 'final_id'
	FinalEncounterNr = ForeignKey("Encounter", dbName='final_encounter_nr')
	FinalBillNo = ForeignKey("BillingBill", dbName='final_bill_no')
	FinalDate = DateCol(default = cur_date_time())
	FinalTotalBillAmount = FloatCol(dbName='final_total_bill_amount')
	FinalDiscount = IntCol(dbName='final_discount')
	FinalTotalReceiptAmount = FloatCol(dbName='final_total_receipt_amount')
	FinalAmountDue = FloatCol(dbName='final_amount_due')
	FinalAmountReceived = FloatCol(dbName='final_amount_recieved')

class BillingPayment(SQLObject):
	class sqlmeta:
		table = "care_billing_payment"
		idName = 'payment_id'
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

	PaymentEncounterNr = ForeignKey("Encounter", dbName='payment_encounter_nr')
	PaymentBillNo = ForeignKey("BillingBill", dbName='payment_bill_no')
	PaymentDate = DateTimeCol( default = cur_date_time(), dbName='payment_date' )
	PaymentCashAmount = FloatCol(dbName='payment_cash_amount')
	PaymentChequeNo = IntCol(dbName='payment_cheque_no')
	PaymentChequeAmount = FloatCol(dbName='payment_cheque_amount')
	PaymentCreditcardNo = StringCol(length=40,dbName='payment_creditcard_no')
	PaymentCreditcardAmount = FloatCol(dbName='payment_creditcard_amount')
	PaymentInsrFirmId = StringCol(length=40,dbName='payment_insr_Firm_id') # Insurance firm id
	PaymentInsrAmount = FloatCol(dbName='payment_insr_amount')
	PaymentAmountTotal = FloatCol(dbName='payment_amount_total')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default = cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default = cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',
	

class EncounterDiagnosticsReport(SQLObject):
	class sqlmeta:
		table = "care_encounter_diagnostics_report"
		idName = 'item_nr'
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

	ReportNr = IntCol(dbName='report_nr')
	ReportingDeptNr = ForeignKey('Department', dbName='reporting_dept_nr') #care_department -> nr
	ReportingDept = StringCol(length=100, dbName='reporting_dept')
	ReportDate = DateTimeCol(default=cur_date_time(),dbName='report_date')
	ReportTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='report_time')
	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	ScriptCall = StringCol(length=255,dbName='script_call')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TestFindingsBaclabor(SQLObject):
	class sqlmeta:
		table = "care_test_findings_baclabor"
		idName = 'batch_nr'
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

	def _set_DoctorId(self, value):
		try:
			if self.DoctorId == '':
				value = cur_user_id()
			else:
				value = self.DoctorId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_DoctorId(value)

	EncounterNr = ForeignKey('Encounter', dbName='encounter_nr')
	RoomNr = ForeignKey('Room',dbName='room_nr') # care_room -> nr
	DeptNr = ForeignKey('Department',dbName='dept_nr') # care_department -> nr
	Notes = StringCol(length=255,dbName='notes')
	FindingsInit = BoolCol(dbName='findings_init')
	FindingsCurrent = BoolCol(dbName='findings_current')
	FindingsFinal = BoolCol(dbName='findings_final')
	EntryNr = StringCol(length=10,dbName='entry_nr')
	RecDate = DateTimeCol(default=cur_date_time(),dbName='rec_date')
	TypeGeneral = StringCol(length=255,dbName='type_general')
	ResistAnaerob  = StringCol(length=255,dbName='resist_anaerob')
	ResistAerob = StringCol(length=255,dbName='resist_aerob')
	Findings = StringCol(length=255,dbName='findings')
	DoctorId = StringCol(length=35,dbName='doctor_id')
	FindingsDate = DateTimeCol(default=cur_date_time(),dbName='findings_date')
	FindingsTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='findings_time')
	Status = StringCol(length=10)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TestRequestBaclabor(SQLObject):
	class sqlmeta:
		table = "care_test_request_baclabor"
		idName = 'batch_nr'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
#	DeptNr = ForeignKey('',dbName='dept_nr')
	Material = StringCol(length=255,dbName='material')
	TestType = StringCol(length=255,dbName='test_type')
	MaterialNote = StringCol(length=255,dbName='material_note')
	DiagnosisNote = StringCol(length=255,dbName='diagnosis_note')
	ImmuneSupp = StringCol(length=255,dbName='immune_supp')
	SendDate = DateTimeCol(default=cur_date_time(),dbName='send_date')
	SampleDate = DateTimeCol(default=cur_date_time(),dbName='sample_date')
	Status = StringCol(length=10)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Department(SQLObject):
	class sqlmeta:
		table = "care_department"
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
	
	Id = StringCol(length=60,alternateID=True,dbName='id')
	Type = ForeignKey("TypeDepartment",dbName='type',default=None)
	NameFormal = StringCol(length=60,dbName='name_formal')
	NameShort = StringCol(length=35,dbName='name_short',default='')
	NameAlternate = StringCol(length=255,dbName='name_alternate',default='')
	LdVar = StringCol(length=35,dbName='LD_var',default='')
	Description = StringCol(length=255,dbName='description',default='')
	AdmitInpatient = BoolCol(dbName='admit_inpatient',default=False)
	AdmitOutpatient = BoolCol(dbName='admit_outpatient',default=False)
	HasOncallDoc = BoolCol(dbName='has_oncall_doc',default=False)
	HasOncallNurse = BoolCol(dbName='has_oncall_nurse',default=False)
	DoesSurgery = BoolCol(dbName='does_surgery',default=False)
	ThisInstitution = BoolCol(default=True,dbName='this_institution')
	IsSubDept = BoolCol(dbName='is_sub_dept',default=False)
	ParentDeptNr = ForeignKey('Department',dbName='parent_dept_nr',default=None)
	WorkHours = StringCol(length=100,dbName='work_hours',default='')
	ConsultHours = StringCol(length=100,dbName='consult_hours',default='')
	IsInactive = BoolCol(dbName='is_inactive',default=False)
	SortOrder = IntCol(dbName='sort_order',default=1)
	Address = StringCol(length=255,dbName='address',default='')
	SigLine = StringCol(length=60,dbName='sig_line',default='')
	SigStamp = StringCol(length=255,dbName='sig_stamp',default='')
	LogoMimeType = StringCol(length=5,dbName='logo_mime_type',default='')
	Locations = MultipleJoin("InvLocation",joinColumn="department_id")
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',


class TestRequestBlood(SQLObject):
	class sqlmeta:
		table = "care_test_request_blood"
		idName = 'batch_nr'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	BloodGroup = StringCol(length=10,dbName='blood_group')
	RhFactor = StringCol(length=10,dbName='rh_factor')
	Kell = StringCol(length=10,dbName='kell')
	DateProtocNr = StringCol(length=45,dbName='date_protoc_nr')
	PureBlood = StringCol(length=15,dbName='pure_blood')
	RedBlood =  StringCol(length=15,dbName='red_blood')
	LeukolessBlood = StringCol(length=15,dbName='leukoless_blood')
	WashedBlood = StringCol(length=15,dbName='washed_blood')
	PrpBlood = StringCol(length=15,dbName='prp_blood')
	ThromboCon = StringCol(length=15,dbName='thrombo_con')
	FfpPlasma = StringCol(length=15,dbName='ffp_plasma')
	TransfusionDev = StringCol(length=15,dbName='transfusion_dev')
	MatchSample = IntCol(dbName='match_sample')
	TransfusionDate = DateTimeCol(default=cur_date_time(),dbName='transfusion_date')
	Diagnosis = StringCol(length=255,dbName='diagnosis')
	Notes = StringCol(length=255,dbName='notes')
	SendDate = DateTimeCol(default=cur_date_time(),dbName='send_date')
	Doctor = StringCol(length=35,dbName='doctor')
	PhoneNr = StringCol(length=40,dbName='phone_nr')
	BloodPb = StringCol(length=255,dbName='blood_pb')
	BloodRb = StringCol(length=255,dbName='blood_rb')
	BloodLlrb = StringCol(length=255,dbName='blood_llrb')
	BloodWrb = StringCol(length=255,dbName='blood_wrb')
	BloodPrp = BLOBCol(default='empty',dbName='blood_prp')
	BloodTc = StringCol(length=255,dbName='blood_tc')
	BloodFfp = StringCol(length=255,dbName='blood_ffp')
	BGroupCount = IntCol(dbName='b_group_count')
	BGroupPrice = FloatCol(dbName='b_group_price')
	ASubgroupCount = IntCol(dbName='a_subgroup_count')
	ASubgroupPrice = FloatCol(dbName='a_subgroup_price')
	ExtraFactorsCount = IntCol(dbName='extra_factors_count')
	ExtraFactorsPrice = FloatCol(dbName='extra_factors_price')
	CoombsCount = IntCol(dbName='coombs_count')
	CoombsPrice = FloatCol(dbName='coombs_price')
	AbTestCount = IntCol(dbName='ab_test_count')
	AbTestPrice = FloatCol(dbName='ab_test_price')
	CrosstestCount = IntCol(dbName='crosstest_count')
	CrosstestPrice = FloatCol(dbName='crosstest_price')
	AbDiffCount = IntCol(dbName='ab_diff_count')
	AbDiffPrice = FloatCol(dbName='ab_diff_price')
	XTest1Code = IntCol(dbName='x_test_1_code')
	XTest1Name = StringCol(length=35,dbName='x_test_1_name')
	XTest1Count = IntCol(dbName='x_test_1_count')
	XTest1Price = FloatCol(dbName='x_test_1_price')
	XTest2Code = IntCol(dbName='x_test_2_code')
	XTest2Name = StringCol(length=35,dbName='x_test_2_name')
	XTest2Count = IntCol(dbName='x_test_2_count')
	XTest2Price = FloatCol(dbName='x_test_2_price')
	XTest3Code = IntCol(dbName='x_test_3_code')
	XTest3Name = StringCol(length=35,dbName='x_test_3_name')
	XTest3Count = IntCol(dbName='x_test_3_count')
	XTest3Price = FloatCol(dbName='x_test_3_price')
	LabStamp = DateTimeCol(default=cur_date_time(),dbName='lab_stamp')
	ReleaseVia = StringCol(length=20,dbName='release_via')
	ReceiptAck = StringCol(length=20,dbName='receipt_ack')
	MainlogNr = StringCol(length=7,dbName='mainlog_nr')
	LabNr = StringCol(length=7,dbName='lab_nr')
	MainlogDate = DateTimeCol(default=cur_date_time(),dbName='mainlog_date')
	LabDate = DateTimeCol(default=cur_date_time(),dbName='lab_date')
	MainlogSign = StringCol(length=20,dbName='mainlog_sign')
	LabSign = StringCol(length=20,dbName='lab_sign')
	Status = StringCol(length=10)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TestRequestGeneric(SQLObject):
	class sqlmeta:
		table = "care_test_request_generic"
		idName = 'batch_nr'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	TestingDept = StringCol(length=35,dbName='testing_dept')
	Visit = BoolCol(dbName='visit')
	OrderPatient = BoolCol(dbName='order_patient')
	DiagnosisQuiry = StringCol(length=255,dbName='diagnosis_quiry')
	SendDate = DateTimeCol(default=cur_date_time(),dbName='send_date')
	SendDoctor = StringCol(length=35,dbName='send_doctor')
	Result = StringCol(length=255,dbName='result')
	ResultDate = DateTimeCol(default=cur_date_time(),dbName='result_date')
	ResultDoctor = StringCol(length=35,dbName='result_doctor')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TestFindingsChemlab(SQLObject):
	class sqlmeta:
		table = "care_test_findings_chemlab"
		idName = 'batch_nr'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	JobId = ForeignKey('TestRequestChemlabor',dbName='job_id')  # care_test_request_chemlabor
	TestDate = DateTimeCol(default=cur_date_time(),dbName='test_date')
	TestTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='test_time')
	GroupId = StringCol(length=30,dbName='group_id')
	SerialValue = StringCol(length=255,dbName='serial_value')
	Validator = StringCol(length=15,dbName='validator')
	ValidateDt = DateTimeCol(dbName='validate_dt')
	Status = StringCol(length=20)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TestRequestChemlabor(SQLObject):
	class sqlmeta:
		table = "care_test_request_chemlabor"
		idName = 'batch_nr'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	RoomNr = ForeignKey('Room',dbName='room_nr')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	Parameters = StringCol(length=255,dbName='parameters')
	DoctorSign = StringCol(length=35,dbName='doctor_sign')
	Highrisk = BoolCol(dbName='highrisk')
	Notes = StringCol(length=255,dbName='notes')
	SendDate = DateTimeCol(default=cur_date_time(),dbName='send_date')
	SampleTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='sample_time')
	SampleWeekday = IntCol(dbName='sample_weekday')
	Status = StringCol(length=15)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TestFindingsPatho(SQLObject):
	class sqlmeta:
		table = "care_test_findings_patho"
		idName = 'batch_nr'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	RoomNr = ForeignKey('Room',dbName='room_nr')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	Material = StringCol(length=255,dbName='material')
	Macro = StringCol(length=255,dbName='macro')
	Micro = StringCol(length=255,dbName='Micro')
	Findings = StringCol(length=255,dbName='findings')
	Diagnosis = StringCol(length=255,dbName='diagnosis')
	DoctorId = StringCol(length=35,dbName='doctor_id')
	FindingsDate = DateTimeCol(default=cur_date_time(),dbName='findings_date')
	FindingsTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='findings_time')
	Status = StringCol(length=10)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TestRequestPatho(SQLObject):
	class sqlmeta:
		table = "care_test_request_patho"
		idName = 'batch_nr'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	QuickCut = BoolCol(dbName='quick_cut')
	QcPhone = StringCol(length=40,dbName='qc_phone')
	QuickDiagnosis = BoolCol(dbName='quick_diagnosis')
	QdPhone = StringCol(length=40,dbName='qd_phone')
	MaterialType = StringCol(length=25,dbName='material_type')
	MaterialDesc = StringCol(length=255,dbName='material_desc')
	Localization = StringCol(length=255,dbName='localization')
	ClinicalNote = StringCol(length=255,dbName='clinical_note')
	ExtraNote = StringCol(length=255,dbName='extra_note')
	RepeatNote = StringCol(length=255,dbName='repeat_note')
	GynLastPeriod = StringCol(length=25,dbName='gyn_last_period')
	GynPeriodType = StringCol(length=25,dbName='gyn_period_type')
	GynGravida = StringCol(length=25,dbName='gyn_gravida')
	GynMenopauseSince = StringCol(length=25,dbName='gyn_menopause_since')
	GynHysterectomy = StringCol(length=25,dbName='gyn_hysterectomy')
	GynContraceptive = StringCol(length=25,dbName='gyn_contraceptive')
	GynIud = StringCol(length=25,dbName='gyn_iud')
	GynHormoneTherapy = StringCol(length=25,dbName='gyn_hormone_therapy')
	DoctorSign = StringCol(length=35,dbName='doctor_sign')
	OpDate = DateTimeCol(default=cur_date_time(),dbName='op_date')
	SendDate = DateTimeCol(default=cur_date_time(),dbName='send_date')
	EntryDate = DateTimeCol(default=cur_date_time(),dbName='entry_date')
	JournalNr = StringCol(length=15,dbName='journal_nr')
	BlocksNr = IntCol(dbName='blocks_nr')
	DeepCuts = IntCol(dbName='deep_cuts')
	SpecialDye = StringCol(length=35,dbName='special_dye')
	ImmuneHistochem = StringCol(length=35,dbName='immune_histochem')
	HormoneReceptors = StringCol(length=35,dbName='hormone_receptors')
	Specials = StringCol(length=35,dbName='specials')
	Status = StringCol(length=10)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class CategoryDiagnosis(SQLObject):
	class sqlmeta:
		table = "care_category_diagnosis"
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

	Category = StringCol(length=35,dbName='category')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	ShortCode = StringCol(length=1,dbName='short_code')
	LdVarShortCode = StringCol(length=25,dbName='LD_var_short_code')
	Description = StringCol(length=255,dbName='description')
	HideFrom = StringCol(length=255,dbName='hide_from')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class CategoryProcedure(SQLObject):
	class sqlmeta:
		table = "care_category_procedure"
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

	Category = StringCol(length=35,dbName='category')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	ShortCode = StringCol(length=1,dbName='short_code')
	LdVarShortCode = StringCol(length=25,dbName='LD_var_short_code')
	Description = StringCol(length=255,dbName='description')
	HideFrom = StringCol(length=255,dbName='hide_from')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class DiagnosisLocalcode(SQLObject):
	class sqlmeta:
		table = "care_diagnosis_localcode"
		idName = 'id'
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

	Localcode = StringCol(length=12,dbName='localcode',alternateID=True)
	Description = StringCol(length=255,dbName='description')
	ClassSub = StringCol(length=5,dbName='class_sub')
	Type = StringCol(length=5,dbName='type')
	Inclusive = StringCol(length=255,dbName='inclusive')
	Exclusive = StringCol(length=255,dbName='exclusive')
	Notes = StringCol(length=255,dbName='notes')
	StdCode = StringCol(length=1,dbName='std_code')
	SubLevel = BoolCol(dbName='sub_level')
	Remarks = StringCol(length=255,dbName='remarks')
	ExtraCodes = StringCol(length=255,dbName='extra_codes')
	ExtraSubclass = StringCol(length=255,dbName='extra_subclass')
	SearchKeys = StringCol(length=255,dbName='search_keys')
	UseFrequency = IntCol(dbName='use_frequency')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class DrgIntern(SQLObject):
	class sqlmeta:
		table = "care_drg_intern"
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

	Code = StringCol(length=12,dbName='code',alternateID=True)
	Description = StringCol(length=255,dbName='description')
	Synonyms = StringCol(length=255,dbName='synonyms')
	Notes = StringCol(length=255,dbName='notes')
	StdCode = StringCol(length=1,dbName='std_code')
	SubLevel = BoolCol(dbName='sub_level')
	ParentCode = StringCol(length=12,dbName='parent_code') # a link back to this object on the code field
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',


class DrgRelatedCodes(SQLObject):
	class sqlmeta:
		table = "care_drg_related_codes"
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

	GroupNr = IntCol(dbName='group_nr')
	Code = StringCol(length=15,dbName='code')
	CodeParent = StringCol(length=15,dbName='code_parent') # links back to this object
	CodeType = StringCol(length=15,dbName='code_type')
	Rank = IntCol(dbName='rank')
	Status = StringCol(length=15)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',


class EncounterDiagnosis(SQLObject):
	class sqlmeta:
		table = "care_encounter_diagnosis"
		idName = 'diagnosis_nr'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	OpNr = ForeignKey('EncounterOp',dbName='op_nr')
	Date = DateTimeCol(default=cur_date_time(),dbName='date')
	Code = StringCol(length=25,dbName='code')
	CodeParent = StringCol(length=25,dbName='code_parent') #links back to itself on the code field
	GroupNr = ForeignKey('DrgIntern',dbName='group_nr')
	CodeVersion = IntCol(dbName='code_version')
	Localcode = StringCol(length=35, dbName='localcode') # care_diagnostics_localcode -> localcode
	LocalcodeNr = ForeignKey('DiagnosisLocalcode',dbName='localcode_nr')
	CategoryNr = ForeignKey('CategoryDiagnosis',dbName='category_nr')
	Type = StringCol(length=35, dbName='type')
	Localization = StringCol(length=35,dbName='localization') 
	LocalizationNr = ForeignKey('TypeLocalization',dbName='localization_nr')
	DiagnosingClinician = StringCol(length=60, dbName='diagnosing_clinician')
	DiagnosingDeptNr = ForeignKey('Department',dbName='diagnosing_dept_nr')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterProcedure(SQLObject):
	class sqlmeta:
		table = "care_encounter_procedure"
		idName = 'procedure_nr'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	OpNr = ForeignKey('EncounterOp',dbName='op_nr')
	Date = DateTimeCol(default=cur_date_time(),dbName='date')
	Code = StringCol(length=25,dbName='code')
	CodeParent = StringCol(length=25,dbName='code_parent') #links back to itself on the code field
	GroupNr = ForeignKey('DrgIntern',dbName='group_nr')
	CodeVersion = IntCol(dbName='code_version')
	Localcode = StringCol(length=35, dbName='localcode') # care_diagnostics_localcode -> localcode
	LocalcodeNr = ForeignKey('DiagnosisLocalcode',dbName='localcode_nr')
	CategoryNr = ForeignKey('CategoryDiagnosis',dbName='category_nr')
	Localization = StringCol(length=35,dbName='localization') 
	LocalizationNr = ForeignKey('TypeLocalization',dbName='localization_nr')
	ResponsibleClinician = StringCol(length=60,dbName='responsible_clinician')
	ResponsibleDeptNr = ForeignKey('Department',dbName='responsible_dept_nr')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeLocalization(SQLObject):
	class sqlmeta:
		table = "care_type_localization"
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

	Category = StringCol(length=35,dbName='category')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	ShortCode = StringCol(length=1,dbName='short_code')
	LdVarShortCode = StringCol(length=25,dbName='LD_var_short_code')
	Description = StringCol(length=255,dbName='description')
	HideFrom = StringCol(length=255,dbName='hide_from')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterMeasurement(SQLObject):
	class sqlmeta:
		table = "care_encounter_measurement"
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

	MsrDate = DateTimeCol(default=cur_date_time(),dbName='msr_date')
	MsrTime = FloatCol(dbName='msr_time')
	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	MsrTypeNr = ForeignKey('TypeMeasurement',dbName='msr_type_nr')
	Value = StringCol(length=255,dbName='value')
	UnitNr = ForeignKey('UnitMeasurement',dbName='unit_nr')
	UnitTypeNr = ForeignKey('TypeUnitMeasurement',dbName='unit_type_nr')
	Notes = StringCol(length=255,dbName='notes')
	MeasuredBy = StringCol(length=35,default=cur_user_id())
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterNotes(SQLObject):
	class sqlmeta:
		table = "care_encounter_notes"
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	TypeNr = ForeignKey('TypeNotes',dbName='type_nr')
	Notes = StringCol(length=255,dbName='notes')
	ShortNotes = StringCol(length=25,dbName='short_notes')
	AuxNotes = StringCol(length=255,dbName='aux_notes')
	RefNotesNr = ForeignKey('EncounterNotes',dbName='ref_notes_nr')
	PersonellNr = ForeignKey('Personell',dbName='personell_nr')
	PersonellName = StringCol(length=60,dbName='personell_name')
	SendToPid = ForeignKey('Person',dbName='send_to_pid')
	SendToName = StringCol(length=60,dbName='send_to_name')
	Date = DateTimeCol(default=cur_date_time(),dbName='date')
	Time = StringCol(default=str(cur_date_time()).rjust(8),dbName='time')
	LocationType = StringCol(length=35,dbName='location_type')
	LocationTypeNr = ForeignKey('TypeLocation',dbName='location_type_nr')
	LocationNr = IntCol(dbName='location_nr')
	LocationId = StringCol(length=60,dbName='location_id')
	AckShortId = StringCol(length=10,dbName='ack_short_id')
	DateAck = DateTimeCol(default=cur_date_time(),dbName='date_ack')
	DateChecked = DateTimeCol(default=cur_date_time(),dbName='date_checked')
	DatePrinted = DateTimeCol(default=cur_date_time(),dbName='date_printed')
	SendByMail = BoolCol(dbName='send_by_mail')
	SendByEmail = BoolCol(dbName='send_by_email')
	SendByFax = BoolCol(dbName='send_by_fax')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeMeasurement(SQLObject):
	class sqlmeta:
		table = "care_type_measurement"
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

	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeNotes(SQLObject):
	class sqlmeta:
		table = "care_type_notes"
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

	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	SortNr = IntCol(dbName='sort_nr')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeUnitMeasurement(SQLObject):
	class sqlmeta:
		table = "care_type_unit_measurement"
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

	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=35,dbName='description')
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class UnitMeasurement(SQLObject):
	class sqlmeta:
		table = "care_unit_measurement"
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

	UnitTypeNr = ForeignKey('TypeUnitMeasurement',dbName='unit_type_nr')
	Id = StringCol(length=25,dbName='id')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	System = StringCol(length=35,dbName='sytem')
	UseFrequency = IntCol(dbName='use_frequency')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterDrgIntern(SQLObject):
	class sqlmeta:
		table = "care_encounter_drg_intern"
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	Date = DateTimeCol(default=cur_date_time(),dbName='date')
	GroupNr = ForeignKey('DrgIntern',dbName='group_nr')
	Clinician = StringCol(length=60,dbName='clinician')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterFinancialClass(SQLObject):
	class sqlmeta:
		table = "care_encounter_financial_class"
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	ClassNr = ForeignKey('ClassFinancial',dbName='class_nr')
	DateStart = DateTimeCol(default=cur_date_time(),dbName='date_start')
	DateEnd = DateTimeCol(dbName='date_end')
	DateCreate = DateTimeCol(default=cur_date_time(),dbName='date_create')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterImage(SQLObject):
	class sqlmeta:
		table = "care_encounter_image"
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	ShotDate = DateTimeCol(default=cur_date_time(),dbName='shot_date')
	ShotNr = IntCol(dbName='shot_nr')
	MimeType = StringCol(length=10,dbName='mime_type')
	UploadDate = DateTimeCol(default=cur_date_time(),dbName='upload_date')
	Notes = StringCol(length=255,dbName='notes')
	GraphicScript = StringCol(length=255,dbName='graphic_script')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())#datetime default '0000-00-00 00:00:00',
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterImmunization(SQLObject):
	class sqlmeta:
		table = "care_encounter_immunization"
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	Date = DateTimeCol(default=cur_date_time(),dbName='date')
	Type = StringCol(length=60,dbName='type')
	Medicine = StringCol(length=60,dbName='medicine')
	Dosage = StringCol(length=60,dbName='dosage')
	ApplicationTypeNr = ForeignKey('TypeApplication',dbName='application_type_nr')
	ApplicationBy = StringCol(length=60,dbName='application_by')
	Titer = StringCol(length=15,dbName='titer')
	RefreshDate = DateTimeCol(dbName='refresh_date')
	Notes = StringCol(length=255,dbName='notes')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Icd10En(SQLObject):
	class sqlmeta:
		table = "care_icd10_en"
		idName = 'id'
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

	DiagnosisCode = StringCol(length=12,dbName='diagnosis_code',alternateID=True) #care_ncounter_diagnosis -> diagnosis_nr
	Description = StringCol(length=255,dbName='description')
	ClassSub = StringCol(length=5,dbName='class_sub')
	Type = StringCol(length=10,dbName='type')
	Inclusive = StringCol(length=255,dbName='inclusive')
	Exclusive = StringCol(length=255,dbName='exclusive')
	Notes = StringCol(length=255,dbName='notes')
	StdCode = StringCol(length=1,dbName='std_code')
	SubLevel = IntCol(dbName='sub_level')
	Remarks = StringCol(length=255,dbName='remarks')
	ExtraCodes = StringCol(length=255,dbName='extra_codes')
	ExtraSubclass = StringCol(length=255,dbName='extra_subclass')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeApplication(SQLObject):
	class sqlmeta:
		table = "care_type_application"
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

	GroupNr = IntCol(dbName='group_nr')
	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class InsuranceFirm(SQLObject):
	class sqlmeta:
		table = "care_insurance_firm"
		idName = 'id'
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

	FirmId = StringCol(length=40,dbName='firm_id',alternateID=True)
	Name = StringCol(length=60,dbName='name')
	IsoCountryId = StringCol(length=3,dbName='iso_country_id')
	SubArea = StringCol(length=60,dbName='sub_area')
	TypeNr = ForeignKey('TypeInsurance',dbName='type_nr')
	Addr = StringCol(length=255,dbName='addr')
	AddrMail = StringCol(length=200,dbName='addr_mail')
	AddrBilling = StringCol(length=200,dbName='addr_billing')
	AddrEmail = StringCol(length=60,dbName='addr_email')
	PhoneMain = StringCol(length=35,dbName='phone_main')
	PhoneAux = StringCol(length=35,dbName='phone_aux')
	FaxMain = StringCol(length=35,dbName='fax_main')
	FaxAux = StringCol(length=35,dbName='fax_aux')
	ContactPerson = StringCol(length=60,dbName='contact_person')
	ContactPhone = StringCol(length=35,dbName='contact_phone')
	ContactFax = StringCol(length=35,dbName='contact_fax')
	ContactEmail = StringCol(length=35,dbName='contact_email')
	UseFrequency = IntCol(dbName='use_frequency')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeInsurance(SQLObject):
	class sqlmeta:
		table = "care_type_insurance"
		idName = 'type_nr'
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

	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=60,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterSickconfirm(SQLObject):
	class sqlmeta:
		table = "care_encounter_sickconfirm"
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	DateConfirm = DateTimeCol(default=cur_date_time(),dbName='date_confirm')
	DateStart = DateTimeCol(default=cur_date_time(),dbName='date_start')
	DateEnd = DateTimeCol(dbName='date_end')
	DateCreate = DateTimeCol(default=cur_date_time(),dbName='date_create')
	Diagnosis = StringCol(length=255,dbName='diagnosis')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class CGroup(SQLObject):
	class sqlmeta:
		table = "care_group"
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

	Id = StringCol(length=35,dbName='id')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Room(SQLObject):
	class sqlmeta:
		table = "care_room"
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
				
	def IsConsultationRoom(self):
		if self.TypeNr.type == 'consultation':
			return True
		else:
			return False
	
	def IsWardRoom(self):
		if self.TypeNr.type == 'ward':
			return True
		else:
			return False

	def IsOperatingRoom(self):
		if self.TypeNr.type == 'op':
			return True
		else:
			return False

	TypeNr = ForeignKey('TypeRoom',dbName='type_nr')
	DateCreate = DateTimeCol(default=cur_date_time(),dbName='date_create')
	DateClose = DateTimeCol(dbName='date_close', default=None)
	IsTempClosed = BoolCol(dbName='is_temp_closed', default=False)
	RoomNr = IntCol(dbName='room_nr',default=None)
	WardNr = ForeignKey('Ward',dbName='ward_nr',default=None)
	DeptNr = ForeignKey('Department',dbName='dept_nr',default=None)
	NrOfBeds = IntCol(dbName='nr_of_beds',default=0)
	ClosedBeds = StringCol(length=255,dbName='closed_beds',default='')
	Info = StringCol(length='60',dbName='info',default='')
	#Multi-Joins
	# Bookings for rooms on this column needs an additional filter on "type_nr" or TypeNr=
	#EncounterLocations = MultipleJoin("EncounterLocation",joinColumn="location_nr")
	#Regular
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeDepartment(SQLObject):
	class sqlmeta:
		table = "care_type_department"
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

	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeRoom(SQLObject):
	class sqlmeta:
		table = "care_type_room"
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

	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Ward(SQLObject):
	class sqlmeta:
		table = "care_ward"
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

	WardId = StringCol(length=35,dbName='ward_id')
	Name = StringCol(length=35,dbName='name')
	DateCreate = DateTimeCol(default=cur_date_time(),dbName='date_create')
	DateClose = DateTimeCol(dbName='date_close',default=None)
	IsTempClosed = BoolCol(dbName='is_temp_closed',default=False)
	Description = StringCol(length=255,dbName='description',default='')
	Info = StringCol(length=255,dbName='info',default='')
	DeptNr = ForeignKey('Department',dbName='dept_nr',default=None)
	RoomNrStart = IntCol(dbName='room_nr_start',default=None)
	RoomNrEnd = IntCol(dbName='room_nr_end',default=None)
	Roomprefix = StringCol(length=4,dbName='roomprefix',default='')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Complication(SQLObject):
	class sqlmeta:
		table = "care_complication"
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

	GroupNr = IntCol(dbName='group_nr')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Code = StringCol(length=25,dbName='code')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterObstetric(SQLObject):
	class sqlmeta:
		table = "care_encounter_obstetric"
		idName = 'id'
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	PregnancyNr = ForeignKey('Pregnancy',dbName='pregnancy_nr')
	HospitalAdmNr = IntCol(dbName='hospital_adm_nr')
	PatientClass = StringCol(length=60,dbName='patient_class')
	IsDischargedNotInLabour = BoolCol(dbName='is_discharged_not_in_labour')
	IsReAdmission = BoolCol(dbName='is_re_admission')
	ReferralStatus = StringCol(length=60,dbName='referral_status')
	ReferralReason = StringCol(length=255,dbName='referral_reason')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class MethodInduction(SQLObject):
	class sqlmeta:
		table = "care_method_induction"
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

	GroupNr = IntCol(dbName='group_nr')
	Method = StringCol(length=35,dbName='method')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class ModeDelivery(SQLObject):
	class sqlmeta:
		table = "care_mode_delivery"
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

	GroupNr = IntCol(dbName='group_nr')
	Mode = StringCol(length=35,dbName='mode')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Pregnancy(SQLObject):
	class sqlmeta:
		table = "care_pregnancy"
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	ThisPregnancyNr = IntCol(dbName='this_pregnancy_nr')
	DeliveryDate = DateTimeCol(default=cur_date_time(),dbName='delivery_date')
	DeliveryTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='delivery_time')
	Gravida = IntCol(dbName='gravida')
	Para = IntCol(dbName='para')
	PregnancyGestationalAge = IntCol(dbName='pregnancy_gestational_age')
	NrOfFetuses = IntCol(dbName='nr_of_fetuses')
	ChildEncounterNr = StringCol(length=255,dbName='child_encounter_nr')
	IsBooked = BoolCol(dbName='is_booked')
	Vdrl = StringCol(length=1,dbName='vdrl')
	Rh = IntCol(dbName='rh')
	DeliveryMode = ForeignKey('ModeDelivery',dbName='delivery_mode')
	DeliveryBy = StringCol(length=60,dbName='delivery_by')
	BpSystolicHigh = IntCol(dbName='bp_systolic_high')
	BpDiastolicHigh = IntCol(dbName='bp_diastolic_high')
	Proteinuria = BoolCol(dbName='proteinuria')
	LabourDuration = IntCol(dbName='labour_duration')
	InductionMethod = ForeignKey('MethodInduction',dbName='induction_method')
	InductionIndication = StringCol(length=125,dbName='induction_indication')
	AnaesthTypeNr = ForeignKey('TypeAnaesthesia',dbName='anaesth_type_nr')
	IsEpidural = StringCol(length=1,dbName='is_epidural')
	Complications = StringCol(length=255,dbName='complications')
	Perineum = IntCol(dbName='perineum')
	BloodLoss = FloatCol(dbName='blood_loss')
	IsRetainedPlacenta = StringCol(length=1,dbName='is_retained_placenta') #Yes/No??
	PostLabourCondition = StringCol(length=35,dbName='post_labour_condition')
	Outcome = StringCol(length=35,dbName='outcome')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeAnaesthesia(SQLObject):
	class sqlmeta:
		table = "care_type_anaesthesia"
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

	Id = StringCol(length=35,dbName='id')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeOutcome(SQLObject):
	class sqlmeta:
		table = "care_type_outcome"
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

	GroupNr = IntCol(dbName='group_nr')
	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypePerineum(SQLObject):
	class sqlmeta:
		table = "care_type_perineum"
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

	Id = StringCol(length=35,dbName='id')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterPrescription(SQLObject):
	class sqlmeta:
		table = "care_encounter_prescription"
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

	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	PrescriptionTypeNr = ForeignKey('TypePrescription',dbName='prescription_type_nr')
	Article = StringCol(length=100,dbName='article')
	DrugClass = StringCol(length=60,dbName='drug_class')
	OrderNr = ForeignKey('PharmaProductsMain',dbName='order_nr')
	Dosage = StringCol(length=255,dbName='dosage')
	ApplicationTypeNr = ForeignKey('TypeApplication',dbName='application_type_nr')
	Notes = StringCol(length=255,dbName='notes')
	PrescribeDate = DateTimeCol(default=cur_date_time(),dbName='prescribe_date')
	Prescriber = StringCol(length=60,dbName='prescriber')
	ColorMarker = StringCol(length=10,dbName='color_marker')
	IsStopped = BoolCol(dbName='is_stopped')
	StopDate = DateTimeCol(dbName='stop_date')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterPrescriptionNotes(SQLObject):
	class sqlmeta:
		table = "care_encounter_prescription_notes"
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

	Date = DateTimeCol(default=cur_date_time(),dbName='date')
	PrescriptionNr = ForeignKey('EncounterPrescription',dbName='prescription_nr')
	Notes = StringCol(length=35,dbName='Notes')
	ShortNotes = StringCol(length=25,dbName='short_notes')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class PharmaProductsMain(SQLObject):
	class sqlmeta:
		table = "care_pharma_products_main"
		idName = 'id'
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

	Bestellnum = StringCol(length=25,dbName='bestellnum')
	Artikelnum = StringCol(length=255,dbName='artikelnum')
	Industrynum = StringCol(length=255,dbName='industrynum')
	Artikelname = StringCol(length=255,dbName='artikelname')
	Generic = StringCol(length=255,dbName='generic')
	Description = StringCol(length=255,dbName='description')
	Packing = StringCol(length=255,dbName='packing')
	Minorder = IntCol(dbName='minorder')
	Maxorder = IntCol(dbName='maxorder')
	Proorder = StringCol(length=255,dbName='proorder')
	Picfile = StringCol(length=255,dbName='picfile')
	Encoder = StringCol(length=255,dbName='encoder')
	EncDate = StringCol(length=255,dbName='enc_date')
	EndTime = StringCol(length=255,dbName='enc_time')
	LockFlag = BoolCol(dbName='lock_flag')
	Medgroup = StringCol(length=255,dbName='medgroup')
	Cave = StringCol(length=255,dbName='cave')
	Status = StringCol(length=20)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypePrescription(SQLObject):
	class sqlmeta:
		table = "care_type_prescription"
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

	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class MedOrdercatalog(SQLObject):
	class sqlmeta:
		table = "care_med_ordercatalog"
		idName = 'item_no'
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

	DeptNr = ForeignKey('Department',dbName='dept_nr')
	Hit = IntCol(dbName='hit')
	Artikelname = StringCol(length=255,dbName='artikelname')
	Bestellnum = StringCol(length=20,dbName='bestellnum')
	Minorder = IntCol(dbName='minorder')
	Maxorder = IntCol(dbName='maxorder')
	Proorder = StringCol(length=255,dbName='proorder')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class MedOrderlist(SQLObject):
	class sqlmeta:
		table = "care_med_orderlist"
		idName = 'order_nr'
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

	DeptNr = ForeignKey('Department',dbName='dept_nr')
	OrderDate = DateTimeCol(default=cur_date_time(),dbName='order_date')
	OrderTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='order_time')
	Articles = StringCol(length=255,dbName='articles')
	Extra1 = StringCol(length=255,dbName='extra1')
	Extra2 = StringCol(length=255,dbName='extra2')
	Validator = StringCol(length=255,dbName='validator')
	IpAddr = StringCol(length=255,dbName='ip_addr')
	Priority = StringCol(length=255,dbName='priority')
	SentDatetime = DateTimeCol(default=cur_date_time(),dbName='sent_datetime')
	ProcessDatetime =DateTimeCol(default=cur_date_time(),dbName='process_datetime')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class MedProductsMain(SQLObject):
	class sqlmeta:
		table = "care_med_products_main"
		idName = 'id'
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

	Bestellnum = StringCol(length=25,dbName='bestellnum')
	Artikelnum = StringCol(length=255,dbName='artikelnum')
	Industrynum = StringCol(length=255,dbName='industrynum')
	Artikelname = StringCol(length=255,dbName='artikelname')
	Generic = StringCol(length=255,dbName='generic')
	Description = StringCol(length=255,dbName='description')
	Packing = StringCol(length=255,dbName='packing')
	Minorder = IntCol(dbName='minorder')
	Maxorder = IntCol(dbName='maxorder')
	Proorder = StringCol(length=255,dbName='proorder')
	Picfile = StringCol(length=255,dbName='picfile')
	Encoder = StringCol(length=255,dbName='encoder')
	EncDate = StringCol(length=255,dbName='enc_date')
	EndTime = StringCol(length=255,dbName='enc_time')
	LockFlag = BoolCol(dbName='lock_flag')
	Medgroup = StringCol(length=255,dbName='medgroup')
	Cave = StringCol(length=255,dbName='cave')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class MedReport(SQLObject):
	class sqlmeta:
		table = "care_med_report"
		idName = 'report_nr'
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

	Dept = ForeignKey('Department',dbName='dept')
	Report = StringCol(length=255,dbName='report')
	Reporter = StringCol(length=25,dbName='reporter')
	IdNr = StringCol(length=15,dbName='id_nr')
	ReportDate = DateTimeCol(default=cur_date_time(),dbName='report_date')
	ReportTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='report_time')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class CategoryDisease(SQLObject):
	class sqlmeta:
		table = "care_category_disease"
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

	GroupNr = IntCol(dbName='group_nr')
	Category = StringCol(length=35,dbName='category')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class ClassifNeonatal(SQLObject):
	class sqlmeta:
		table = "care_classif_neonatal"
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

	Id = StringCol(length=35,dbName='id')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Neonatal(SQLObject):
	class sqlmeta:
		table = "care_neonatal"
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

	Pid = ForeignKey('Person',dbName='pid')
	DeliveryDate = DateTimeCol(default=cur_date_time(),dbName='delivery_date')
	ParentEncounterNr = ForeignKey('Encounter',dbName='parent_encounter_nr')
	DeliveryNr = IntCol(default=1,dbName='delivery_nr')
	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	DeliveryPlace = StringCol(length=60,dbName='delivery_place')
	DeliveryMode = ForeignKey('ModeDelivery',dbName='delivery_mode')
	CSReason = StringCol(length=255,dbName='c_s_reason')
	BornBeforeArrival = BoolCol(dbName='born_before_arrival')
	FacePresentation = BoolCol(dbName='face_presentation')
	PosterioOccipitalPosition = BoolCol(dbName='posterio_occipital_position')
	DeliveryRank = IntCol(default=1,dbName='delivery_rank')
	Apgar1Min = IntCol(default=0,dbName='apgar_1_min')
	Apgar5Min = IntCol(default=0,dbName='apgar_5_min')
	Apgar10Min = IntCol(default=0,dbName='apgar_10_min')
	TimeToSpontResp = IntCol(default=1,dbName='time_to_spont_resp')
#	Condition = StringCol(length=60,dbName='condition')
# Condition is a MySQL 5 keyword.
	Weight = FloatCol(default=1.0,dbName='weight')
	Length = FloatCol(default=1.0,dbName='length')
	HeadCircumference = FloatCol(default=1.0,dbName='head_circumference')
	ScoredGestationalAge = FloatCol(default=1.0,dbName='scored_gestational_age')
	Feeding = ForeignKey('TypeFeeding',dbName='feeding')
	CongenitalAbnormality = StringCol(length=125,dbName='congenital_abnormality')
	Classification = StringCol(length=255,dbName='classification') #ClassifNeonatal -> Name
	DiseaseCategory = ForeignKey('CategoryDisease',dbName='disease_category')
	Outcome = ForeignKey('TypeOutcome',dbName='outcome')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeFeeding(SQLObject):
	class sqlmeta:
		table = "care_type_feeding"
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

	GroupNr = IntCol(dbName='group_nr')
	Type = StringCol(length=35,dbName='type')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Description = StringCol(length=255,dbName='description')
	Status = StringCol(length=25,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class EncounterOp(SQLObject):
	class sqlmeta:
		table = "care_encounter_op"
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

	Year = StringCol(length=4,dbName='year')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	OpRoom = ForeignKey('Room',dbName='op_room')
	OpNr = IntCol(dbName='op_nr')
	OpDate = DateTimeCol(default=cur_date_time(),dbName='op_date')
	OpSrcDate = StringCol(length=8,dbName='op_src_date')
	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	Diagnosis = StringCol(length=255,dbName='diagnosis')
	Operator = StringCol(length=255,dbName='operator')
	Assistant = StringCol(length=255,dbName='assistant')
	ScurbNurse = StringCol(length=255,dbName='scrub_nurse')
	RotatingNurse = StringCol(length=255,dbName='rotating_nurse')
	Anesthesia = StringCol(length=30,dbName='anesthesia')
	AnDoctor = StringCol(length=255,dbName='an_doctor')
	OpTherapy = StringCol(length=255,dbName='op_therapy')
	ResultInfo = StringCol(length=255,dbName='result_info')
	EntryTime = StringCol(length=5,dbName='entry_time')
	CutTime = StringCol(length=5,dbName='cut_time')
	CloseTime = StringCol(length=5,dbName='close_time')
	ExitTime = StringCol(length=5,dbName='exit_time')
	EntryOut = StringCol(length=255,dbName='entry_out')
	CutClose = StringCol(length=255,dbName='cut_close')
	WaitTime = StringCol(length=255,dbName='wait_time')
	BandageTime = StringCol(length=255,dbName='bandage_time')
	ReposTime = StringCol(length=255,dbName='repos_time')
	Encoding = StringCol(length=255,dbName='encoding')
	DocDate = StringCol(length=10,dbName='doc_date')
	DocTime = StringCol(length=5,dbName='doc_time')
	DutyType = StringCol(length=15,dbName='duty_type')
	MaterialCodedlist = StringCol(length=255,dbName='material_codedlist') # PharmaProductsMain
	ContainerCodedlist = StringCol(length=255,dbName='container_codedlist') # SteriProductsMain
	IcdCode = StringCol(length=255,dbName='icd_code')
	OpsCode = StringCol(length=255,dbName='ops_code')
	OpsInternCode = StringCol(length=255,dbName='ops_intern_code')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TypeEthnicOrig(SQLObject):
	class sqlmeta:
		table = "care_type_ethnic_orig"
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

	ClassNr = ForeignKey('ClassEthnicOrig',dbName='class_nr')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var',default='')
	Persons = MultipleJoin("Person",joinColumn='ethnic_orig')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',
	
class PersonellAssignment(SQLObject):
	class sqlmeta:
		table = "care_personell_assignment"
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

	PersonellNr = ForeignKey('Personell',dbName='personell_nr')
	RoleNr = ForeignKey('RolePerson',dbName='role_nr')
	LocationTypeNr = ForeignKey('TypeLocation',dbName='location_type_nr')
	LocationNr = ForeignKey('Department',dbName='location_nr')
	DateStart = DateTimeCol(default=cur_date_time(),dbName='date_start')
	DateEnd = DateTimeCol(dbName='date_end')
	IsTemporary = BoolCol(dbName='is_temporary')
	ListFrequency = IntCol(dbName='list_frequency')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class Phone(SQLObject):
	class sqlmeta:
		table = "care_phone"
		idName = 'item_nr'
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

	Title = StringCol(length=25,dbName='title')
	Name = StringCol(length=45,dbName='name')
	Vorname = StringCol(length=45,dbName='vorname')
	Pid = ForeignKey('Person',dbName='pid')
	PersonellNr = ForeignKey('Personell',dbName='personell_nr')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	Beruf = StringCol(length=25,dbName='beruf')
	Bereich1 = StringCol(length=25,dbName='bereich1')
	Bereich2 = StringCol(length=25,dbName='bereich2')
	Inphone1 = StringCol(length=15,dbName='inphone1')
	Inphone2 = StringCol(length=15,dbName='inphone2')
	Inphone3 = StringCol(length=15,dbName='inphone3')
	Exphone1 = StringCol(length=25,dbName='exphone1')
	Exphone2 = StringCol(length=25,dbName='exphone2')
	Funk1 = StringCol(length=15,dbName='funk1')
	Funk2 = StringCol(length=15,dbName='funk2')
	Roomnr = StringCol(length=10,dbName='roomnr')
	Date = DateTimeCol(default=cur_date_time(),dbName='date')
	Time = StringCol(default=str(cur_date_time()).rjust(8),dbName='time')
	Status = StringCol(length=15)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class RolePerson(SQLObject):
	class sqlmeta:
		table = "care_role_person"
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

	GroupNr = IntCol(dbName='group_nr')
	Role = StringCol(length=35,dbName='role')
	Name = StringCol(length=35,dbName='name')
	LdVar = StringCol(length=35,dbName='LD_var')
	Status = StringCol(length=25,default='')
#	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class PharmaOrdercatalog(SQLObject):
	class sqlmeta:
		table = "care_pharma_ordercatalog"
		idName = 'item_no'
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	Hit = IntCol(dbName='hit')
	Artikelname = StringCol(length=255,dbName='artikelname')
	Bestellnum = StringCol(length=20,dbName='bestellnum')#PharamProductsMain -> Bestellnum
	Minorder = IntCol(dbName='minorder')
	MaxOrder = IntCol(dbName='maxorder')
	Proorder = StringCol(length=255,dbName='proorder')

class PharmaOrderlist(SQLObject):
	class sqlmeta:
		table = "care_pharma_orderlist"
		idName = 'order_nr'
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

	DeptNr = ForeignKey('Department',dbName='dept_nr')
	OrderDate = DateTimeCol(default=cur_date_time(),dbName='order_date')
	OrderTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='order_time')
	Articles = StringCol(length=255,dbName='articles')
	Extra1 = StringCol(length=255,dbName='extra1')
	Extra2 = StringCol(length=255,dbName='extra2')
	Validator = StringCol(length=255,dbName='validator')
	IpAddr = StringCol(length=255,dbName='ip_addr')
	Priority = StringCol(length=255,dbName='priority')
	SentDatetime = DateTimeCol(default=cur_date_time(),dbName='sent_datetime')
	ProcessDatetime =DateTimeCol(default=cur_date_time(),dbName='process_datetime')
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TestFindingsRadio(SQLObject):
	class sqlmeta:
		table = "care_test_findings_radio"
		idName = 'id'
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

	BatchNr = ForeignKey('EncounterDiagnosticsReport',dbName='batch_nr')
	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	RoomNr = ForeignKey('Room',dbName='room_nr')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	Findings = StringCol(length=255,dbName='findings')
	Diagnosis = StringCol(length=255,dbName='diagnosis')
	DoctorId = StringCol(length=35,dbName='doctor_id')
	FindingsDate = DateTimeCol(default=cur_date_time(),dbName='findings_date')
	FindingsTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='findings_time')
	Status = StringCol(length=10)
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

class TestRequestRadio(SQLObject):
	class sqlmeta:
		table = "care_test_request_radio"
		idName = 'id'
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

	BatchNr = ForeignKey('EncounterDiagnosticsReport',dbName='batch_nr')
	EncounterNr = ForeignKey('Encounter',dbName='encounter_nr')
	DeptNr = ForeignKey('Department',dbName='dept_nr')
	Xray = BoolCol(dbName='xray')
	Ct = BoolCol(dbName='ct')
	Sono = BoolCol(dbName='sono')
	Mammograph = BoolCol(dbName='mammograph')
	Mrt = BoolCol(dbName='mrt')
	Nuclear = BoolCol(dbName='nuclear')
	IfPatmobile = BoolCol(dbName='if_patmobile')
	IfAllergy = BoolCol(dbName='if_allergy')
	IfHyperten = BoolCol(dbName='if_hyperten')
	IfPregnant = BoolCol(dbName='if_pregnant')
	ClinicalInfo = StringCol(length=255,dbName='clinical_info')
	TestRequest = StringCol(length=255,dbName='test_request')
	SendDate = DateTimeCol(default=cur_date_time(),dbName='send_date')
	SendDoctor = StringCol(length=35,dbName='send_doctor')
	XrayNr = StringCol(length=9,dbName='xray_nr')
	RCm2 = StringCol(length=15,dbName='r_cm_2')
	Mtr = StringCol(length=35,dbName='mtr')
	XrayDate = DateTimeCol(default=cur_date_time(),dbName='xray_date')
	XrayTime = StringCol(default=str(cur_date_time()).rjust(8),dbName='xray_time')
	Results = StringCol(length=255,dbName='results')
	ResultsDate = DateTimeCol(default=cur_date_time(),dbName='results_date')
	ResultsDoctor = StringCol(length=35,dbName='results_doctor')
	ProcessId = StringCol(length=35,dbName='process_id')
	ProcessTime = DateTimeCol(default=cur_date_time())
	Status = StringCol(length=25,default='')
	History = StringCol(length=255,default='')
	ModifyId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	ModifyTime = DateTimeCol(default=cur_date_time())
	CreateId = StringCol(length=35,default=cur_user_id())#varchar(35) NOT NULL default '',
	CreateTime = DateTimeCol(default=cur_date_time())#timestamp NOT NULL default '0000-00-00 00:00:00',

##=====Automatically Generated Code Pasted Here ==========

class TypeCauseOpdelay(SQLObject):
	class sqlmeta:
		table = 'care_type_cause_opdelay'
		idName = 'type_nr'

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

	Type = StringCol(length=35,dbName="type")
	Cause = StringCol(length=255,dbName="cause")
	LdVar = StringCol(length=35,dbName="LD_var")
	Status = StringCol(length=25,dbName="status")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class PersonInsurance(SQLObject):
	class sqlmeta:
		table = 'care_person_insurance'
		idName = 'item_nr'

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

	Pid = ForeignKey("Person",dbName="pid")
	Type = StringCol(length=60,dbName="type")
	InsuranceNr = StringCol(length=50,dbName="insurance_nr")
	FirmId = StringCol(length=60,dbName="firm_id")
	ClassNr = ForeignKey("ClassInsurance",dbName="class_nr")
	IsVoid = BoolCol(dbName="is_void")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class StandbyDutyReport(SQLObject):
	class sqlmeta:
		table = 'care_standby_duty_report'
		idName = 'report_nr'

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

	Dept = StringCol(length=15,dbName="dept")
	Date = DateTimeCol(default=cur_date_time(),dbName="date")
	StandbyName = StringCol(length=35,dbName="standby_name")
	StandbyStart = StringCol(default=str(cur_date_time()).rjust(8),length=8,dbName="standby_start")
	StandbyEnd = StringCol(default=str(cur_date_time()).rjust(8),length=8,dbName="standby_end")
	OncallName = StringCol(length=35,dbName="oncall_name")
	OncallStart = StringCol(default=str(cur_date_time()).rjust(8),length=8,dbName="oncall_start")
	OncallEnd = StringCol(default=str(cur_date_time()).rjust(8),length=8,dbName="oncall_end")
	OpRoom = StringCol(length=2,dbName="op_room")
	DiagnosisTherapy = StringCol(length=255,dbName="diagnosis_therapy")
	Encoding = StringCol(length=255,dbName="encoding")
	Status = StringCol(length=20,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TypeImmunization(SQLObject):
	class sqlmeta:
		table = 'care_type_immunization'
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

	Type = StringCol(length=20,dbName="type")
	Name = StringCol(length=20,dbName="name")
	LdVar = StringCol(length=35,dbName="LD_var")
	Period = IntCol(dbName="period")
	Tolerance = IntCol(dbName="tolerance")
	Dosage = StringCol(length=255,dbName="dosage")
	Medicine = StringCol(length=255,dbName="medicine")
	Titer = StringCol(length=255,dbName="titer")
	Note = StringCol(length=255,dbName="note")
	Application = IntCol(dbName="application")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class ImgDiagnostic(SQLObject):
	class sqlmeta:
		table = 'care_img_diagnostic'
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

	Pid = ForeignKey("Person",dbName="pid")
	EncounterNr = ForeignKey("Encounter",dbName="encounter_nr")
	DocRefIds = StringCol(length=255,dbName="doc_ref_ids")
	ImgType = StringCol(length=10,dbName="img_type")
	MaxNr = IntCol(dbName="max_nr")
	UploadDate = DateTimeCol(default=cur_date_time(),dbName="upload_date")
	CancelDate = DateTimeCol(default=cur_date_time(),dbName="cancel_date")
	CancelBy = StringCol(length=35,dbName="cancel_by")
	Notes = StringCol(length=255,dbName="notes")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TypeColor(SQLObject):
	class sqlmeta:
		table = 'care_type_color'
		idName = 'id'

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

	ColorId = StringCol(length=25,alternateID=True,dbName='color_id')
	Name = StringCol(length=35,dbName="name")
	LdVar = StringCol(length=35,dbName="LD_var")
	Status = StringCol(length=25,dbName="status")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")

class TypeAssignment(SQLObject):
	class sqlmeta:
		table = 'care_type_assignment'
		idName = 'type_nr'

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

	Type = StringCol(length=35,alternateID=True,dbName="type")
	Name = StringCol(length=35,dbName="name")
	LdVar = StringCol(length=25,dbName="LD_var")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class EncounterEventSignaller(SQLObject):
	class sqlmeta:
		table = 'care_encounter_event_signaller'
		idName = 'id'

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

	EncounterNr = ForeignKey("Encounter",dbName='encounter_nr')
	Yellow = BoolCol(dbName="yellow")
	Black = BoolCol(dbName="black")
	BluePale = BoolCol(dbName="blue_pale")
	Brown = BoolCol(dbName="brown")
	Pink = BoolCol(dbName="pink")
	YellowPale = BoolCol(dbName="yellow_pale")
	Red = BoolCol(dbName="red")
	GreenPale = BoolCol(dbName="green_pale")
	Violet = BoolCol(dbName="violet")
	Blue = BoolCol(dbName="blue")
	Biege = BoolCol(dbName="biege")
	Orange = BoolCol(dbName="orange")
	Green1 = BoolCol(dbName="green_1")
	Green2 = BoolCol(dbName="green_2")
	Green3 = BoolCol(dbName="green_3")
	Green4 = BoolCol(dbName="green_4")
	Green5 = BoolCol(dbName="green_5")
	Green6 = BoolCol(dbName="green_6")
	Green7 = BoolCol(dbName="green_7")
	Rose1 = BoolCol(dbName="rose_1")
	Rose2 = BoolCol(dbName="rose_2")
	Rose3 = BoolCol(dbName="rose_3")
	Rose4 = BoolCol(dbName="rose_4")
	Rose5 = BoolCol(dbName="rose_5")
	Rose6 = BoolCol(dbName="rose_6")
	Rose7 = BoolCol(dbName="rose_7")
	Rose8 = BoolCol(dbName="rose_8")
	Rose9 = BoolCol(dbName="rose_9")
	Rose10 = BoolCol(dbName="rose_10")
	Rose11 = BoolCol(dbName="rose_11")
	Rose12 = BoolCol(dbName="rose_12")
	Rose13 = BoolCol(dbName="rose_13")
	Rose14 = BoolCol(dbName="rose_14")
	Rose15 = BoolCol(dbName="rose_15")
	Rose16 = BoolCol(dbName="rose_16")
	Rose17 = BoolCol(dbName="rose_17")
	Rose18 = BoolCol(dbName="rose_18")
	Rose19 = BoolCol(dbName="rose_19")
	Rose20 = BoolCol(dbName="rose_20")
	Rose21 = BoolCol(dbName="rose_21")
	Rose22 = BoolCol(dbName="rose_22")
	Rose23 = BoolCol(dbName="rose_23")
	Rose24 = BoolCol(dbName="rose_24")

class TestParam(SQLObject):
	class sqlmeta:
		table = 'care_test_param'
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

	GroupId = StringCol(length=35,dbName="group_id")
	Name = StringCol(length=35,dbName="name")
	Id = StringCol(length=10,dbName="id")
	MsrUnit = StringCol(length=15,dbName="msr_unit")
	Median = StringCol(length=20,dbName="median")
	HiBound = StringCol(length=20,dbName="hi_bound")
	LoBound = StringCol(length=20,dbName="lo_bound")
	HiCritical = StringCol(length=20,dbName="hi_critical")
	LoCritical = StringCol(length=20,dbName="lo_critical")
	HiToxic = StringCol(length=20,dbName="hi_toxic")
	LoToxic = StringCol(length=20,dbName="lo_toxic")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TypeEncounter(SQLObject):
	class sqlmeta:
		table = 'care_type_encounter'
		idName = 'type_nr'

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

	Type = StringCol(length=35,dbName="type")
	Name = StringCol(length=35,dbName="name")
	LdVar = StringCol(length=25,dbName="LD_var")
	Description = StringCol(length=255,dbName="description")
	HideFrom = IntCol(dbName="hide_from")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class CafePrices(SQLObject):
	class sqlmeta:
		table = 'care_cafe_prices'
		idName = 'item'

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

	Lang = StringCol(length=10,dbName="lang")
	Productgroup = StringCol(length=255,dbName="productgroup")
	Article = StringCol(length=255,dbName="article")
	Description = StringCol(length=255,dbName="description")
	Price = StringCol(length=10,dbName="price")
	Unit = StringCol(length=255,dbName="unit")
	PicFilename = StringCol(length=255,dbName="pic_filename")
	ModifyId = StringCol(length=25,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=25,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class SteriProductsMain(SQLObject):
	class sqlmeta:
		table = 'care_steri_products_main'
		idName = 'bestellnum'

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

	Containernum = StringCol(length=15,dbName="containernum")
	Industrynum = StringCol(length=255,dbName="industrynum")
	Containername = StringCol(length=40,dbName="containername")
	Description = StringCol(length=255,dbName="description")
	Packing = StringCol(length=255,dbName="packing")
	Minorder = IntCol(dbName="minorder")
	Maxorder = IntCol(dbName="maxorder")
	Proorder = StringCol(length=255,dbName="proorder")
	Picfile = StringCol(length=255,dbName="picfile")
	Encoder = StringCol(length=255,dbName="encoder")
	EncDate = StringCol(length=255,dbName="enc_date")
	EncTime = StringCol(length=255,dbName="enc_time")
	LockFlag = BoolCol(dbName="lock_flag")
	Medgroup = StringCol(length=255,dbName="medgroup")
	Cave = StringCol(length=255,dbName="cave")

class MenuMain(SQLObject):
	class sqlmeta:
		table = 'care_menu_main'
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

	SortNr = IntCol(dbName="sort_nr")
	Name = StringCol(length=35,dbName="name")
	LdVar = StringCol(length=35,dbName="LD_var")
	Url = StringCol(length=255,dbName="url")
	IsVisible = BoolCol(dbName="is_visible")
	HideBy = StringCol(length=255,dbName="hide_by")
	Status = StringCol(length=25,dbName="status")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")

class NewsArticle(SQLObject):
	class sqlmeta:
		table = 'care_news_article'
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

	Lang = StringCol(length=10,dbName="lang")
	DeptNr = IntCol(dbName="dept_nr")
	Category = StringCol(length=255,dbName="category")
	Status = StringCol(length=10,dbName="status")
	Title = StringCol(length=255,dbName="title")
	Preface = StringCol(length=255,dbName="preface")
	Body = StringCol(length=255,dbName="body")
	Pic = BLOBCol(default="",dbName="pic")
	PicMime = StringCol(length=4,dbName="pic_mime")
	ArtNum = BoolCol(dbName="art_num")
	HeadFile = StringCol(length=255,dbName="head_file")
	MainFile = StringCol(length=255,dbName="main_file")
	PicFile = StringCol(length=255,dbName="pic_file")
	Author = StringCol(length=30,dbName="author")
	SubmitDate = DateTimeCol(default=cur_date_time(),dbName="submit_date")
	EncodeDate = DateTimeCol(default=cur_date_time(),dbName="encode_date")
	PublishDate = DateTimeCol(default=cur_date_time(),dbName="publish_date")
	ModifyId = StringCol(length=30,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=30,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TechQuestions(SQLObject):
	class sqlmeta:
		table = 'care_tech_questions'
		idName = 'batch_nr'

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

	Dept = StringCol(length=60,dbName="dept")
	Query = StringCol(length=255,dbName="query")
	Inquirer = StringCol(length=25,dbName="inquirer")
	Tphone = StringCol(length=30,dbName="tphone")
	Tdate = DateTimeCol(default=cur_date_time(),dbName="tdate")
	Ttime = StringCol(default=str(cur_date_time()).rjust(8),length=8,dbName="ttime")
	Tid = DateTimeCol(default=cur_date_time(),dbName="tid")
	Reply = StringCol(length=255,dbName="reply")
	Answered = BoolCol(dbName="answered")
	Ansby = StringCol(length=25,dbName="ansby")
	Astamp = StringCol(length=16,dbName="astamp")
	Archive = BoolCol(dbName="archive")
	Status = StringCol(length=15,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class DutyplanOncall(SQLObject):
	class sqlmeta:
		table = 'care_dutyplan_oncall'
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

	DeptNr = ForeignKey("Department", dbName="dept_nr")
	RoleNr = ForeignKey("RolePerson",dbName="role_nr")
	Year = StringCol(default=str(cur_date_time()).ljust(4),length=4,dbName="year")
	Month = StringCol(length=2,dbName="month")
	Duty1Txt = StringCol(length=255,dbName="duty_1_txt")
	Duty2Txt = StringCol(length=255,dbName="duty_2_txt")
	Duty1Pnr = StringCol(length=255,dbName="duty_1_pnr")
	Duty2Pnr = StringCol(length=255,dbName="duty_2_pnr")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class Currency(SQLObject):
	class sqlmeta:
		table = 'care_currency'
		idName = 'item_no'

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

	ShortName = StringCol(length=10,dbName="short_name")
	LongName = StringCol(length=20,dbName="long_name")
	Info = StringCol(length=50,dbName="info")
	Status = StringCol(length=5,dbName="status")
	ModifyId = StringCol(length=20,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=20,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class BillingArchive(SQLObject):
	class sqlmeta:
		table = 'care_billing_archive'
		idName = 'id'

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

	BillNo = IntCol(dbName='bill_no')
	EncounterNr = ForeignKey("Encounter",dbName="encounter_nr")
	PatientName = StringCol(length=255,dbName="patient_name")
	Vorname = StringCol(length=35,dbName="vorname")
	BillDateTime = DateTimeCol(default=cur_date_time(),dbName="bill_date_time")
	BillAmt = FloatCol(dbName="bill_amt")
	PaymentDateTime = DateTimeCol(default=cur_date_time(),dbName="payment_date_time")
	PaymentMode = StringCol(length=255,dbName="payment_mode")
	ChequeNo = StringCol(length=10,dbName="cheque_no")
	CreditcardNo = StringCol(length=10,dbName="creditcard_no")
	PaidBy = StringCol(length=15,dbName="paid_by")

class PersonOtherNumber(SQLObject):
	class sqlmeta:
		table = 'care_person_other_number'
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

	Pid = ForeignKey("Person",dbName="pid")
	OtherNr = StringCol(length=30,dbName="other_nr")
	Org = StringCol(length=35,dbName="org")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class DrgQuicklist(SQLObject):
	class sqlmeta:
		table = 'care_drg_quicklist'
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

	Code = StringCol(length=25,dbName="code")
	CodeParent = StringCol(length=25,dbName="code_parent")
	DeptNr = ForeignKey("Department",dbName="dept_nr")
	QlistType = StringCol(length=25,dbName="qlist_type")
	Rank = IntCol(dbName="rank")
	Status = StringCol(length=15,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=25,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=25,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TechRepairJob(SQLObject):
	class sqlmeta:
		table = 'care_tech_repair_job'
		idName = 'batch_nr'

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

	Dept = StringCol(length=15,dbName="dept")
	Job = StringCol(length=255,dbName="job")
	Reporter = StringCol(length=25,dbName="reporter")
	Id = StringCol(length=15,dbName="id")
	Tphone = StringCol(length=30,dbName="tphone")
	Tdate = DateTimeCol(default=cur_date_time(),dbName="tdate")
	Ttime = StringCol(default=str(cur_date_time()).rjust(8),length=8,dbName="ttime")
	Tid = DateTimeCol(default=cur_date_time(),dbName="tid")
	Done = BoolCol(dbName="done")
	Seen = BoolCol(dbName="seen")
	Seenby = StringCol(length=25,dbName="seenby")
	Sstamp = StringCol(length=16,dbName="sstamp")
	Doneby = StringCol(length=25,dbName="doneby")
	Dstamp = StringCol(length=16,dbName="dstamp")
	DIdx = StringCol(length=8,dbName="d_idx")
	Archive = BoolCol(dbName="archive")
	Status = StringCol(length=20,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TypeTest(SQLObject):
	class sqlmeta:
		table = 'care_type_test'
		idName = 'type_nr'

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

	Type = StringCol(length=35,dbName="type")
	Name = StringCol(length=35,dbName="name")
	LdVar = StringCol(length=35,dbName="LD_var")
	Description = StringCol(length=255,dbName="description")
	Status = StringCol(length=25,dbName="status")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TechRepairDone(SQLObject):
	class sqlmeta:
		table = 'care_tech_repair_done'
		idName = 'batch_nr'

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

	Dept = StringCol(length=15,dbName="dept")
	DeptNr = ForeignKey("Department",dbName="dept_nr")
	JobId = StringCol(length=15,dbName="job_id")
	Job = StringCol(length=255,dbName="job")
	Reporter = StringCol(length=25,dbName="reporter")
	Id = StringCol(length=15,dbName="id")
	Tdate = DateTimeCol(default=cur_date_time(),dbName="tdate")
	Ttime = StringCol(default=str(cur_date_time()).rjust(8),length=8,dbName="ttime")
	Tid = DateTimeCol(default=cur_date_time(),dbName="tid")
	Seen = BoolCol(dbName="seen")
	DIdx = StringCol(length=8,dbName="d_idx")
	Status = StringCol(length=15,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TestGroup(SQLObject):
	class sqlmeta:
		table = 'care_test_group'
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

	GroupId = StringCol(length=35,dbName="group_id")
	Name = StringCol(length=35,dbName="name")
	SortNr = IntCol(dbName="sort_nr")
	Status = StringCol(length=25,dbName="status")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class ClassTherapy(SQLObject):
	class sqlmeta:
		table = 'care_class_therapy'
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

	GroupNr = IntCol(dbName="group_nr")
	Class = StringCol(length=35,dbName="class")
	Name = StringCol(length=35,dbName="name")
	LdVar = StringCol(length=25,dbName="LD_var")
	Description = StringCol(length=255,dbName="description")
	Status = StringCol(length=25,dbName="status")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class CafeMenu(SQLObject):
	class sqlmeta:
		table = 'care_cafe_menu'
		idName = 'item'

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

	Lang = StringCol(length=10,dbName="lang")
	Cdate = DateTimeCol(default=cur_date_time(),dbName="cdate")
	Menu = StringCol(length=255,dbName="menu")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class EffectiveDay(SQLObject):
	class sqlmeta:
		table = 'care_effective_day'
		idName = 'eff_day_nr'

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

	Name = StringCol(length=25,dbName="name")
	Description = StringCol(length=255,dbName="description")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TypeTime(SQLObject):
	class sqlmeta:
		table = 'care_type_time'
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

	Type = StringCol(length=35,dbName="type")
	Name = StringCol(length=35,dbName="name")
	LdVar = StringCol(length=35,dbName="LD_var")
	Description = StringCol(length=255,dbName="description")
	Status = StringCol(length=25,dbName="status")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class OpMedDoc(SQLObject):
	class sqlmeta:
		table = 'care_op_med_doc'
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

	OpDate = StringCol(length=12,dbName="op_date")
	Operator = StringCol(length=255,dbName="operator")
	EncounterNr = ForeignKey("Encounter",dbName="encounter_nr")
	DeptNr = ForeignKey("Department",dbName="dept_nr")
	Diagnosis = StringCol(length=255,dbName="diagnosis")
	Localize = StringCol(length=255,dbName="localize")
	Therapy = StringCol(length=255,dbName="therapy")
	Special = StringCol(length=255,dbName="special")
	ClassS = IntCol(dbName="class_s")
	ClassM = IntCol(dbName="class_m")
	ClassL = IntCol(dbName="class_l")
	OpStart = StringCol(length=8,dbName="op_start")
	OpEnd = StringCol(length=8,dbName="op_end")
	ScrubNurse = StringCol(length=70,dbName="scrub_nurse")
	OpRoom = StringCol(length=10,dbName="op_room")
	Status = StringCol(length=15,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class TypeDuty(SQLObject):
	class sqlmeta:
		table = 'care_type_duty'
		idName = 'type_nr'

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

	Type = StringCol(length=35,dbName="type")
	Name = StringCol(length=35,dbName="name")
	LdVar = StringCol(length=35,dbName="LD_var")
	Description = StringCol(length=255,dbName="description")
	Status = StringCol(length=25,dbName="status")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

class Appointment(SQLObject):
	class sqlmeta:
		table = 'care_appointment'
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

	Pid = ForeignKey("Person",dbName="pid")
	Date = DateTimeCol(default=cur_date_time(),dbName="date")
	Time = StringCol(default=str(cur_date_time()).rjust(8),length=8,dbName="time")
	ToDeptId = StringCol(length=25,dbName="to_dept_id")
	ToDeptNr = ForeignKey("Department",dbName="to_dept_nr")
	ToPersonellNr = ForeignKey("Personell",dbName="to_personell_nr")
	ToPersonellName = StringCol(length=60,dbName="to_personell_name")
	Purpose = StringCol(length=255,dbName="purpose")
	Urgency = IntCol(dbName="urgency")
	Remind = BoolCol(dbName="remind")
	RemindEmail = BoolCol(dbName="remind_email")
	RemindMail = BoolCol(dbName="remind_mail")
	RemindPhone = BoolCol(dbName="remind_phone")
	ApptStatus = StringCol(length=35,dbName="appt_status")
	CancelBy = StringCol(length=255,dbName="cancel_by")
	CancelDate = DateTimeCol(default=cur_date_time(),dbName="cancel_date")
	CancelReason = StringCol(length=255,dbName="cancel_reason")
	EncounterClassNr = ForeignKey("ClassEncounter",dbName="encounter_class_nr")
	EncounterNr = ForeignKey("Encounter",dbName="encounter_nr")
	Status = StringCol(length=25,dbName="status")
	History = StringCol(length=255,dbName="history")
	ModifyId = StringCol(length=35,dbName="modify_id")
	ModifyTime = DateTimeCol(default=cur_date_time(),dbName="modify_time")
	CreateId = StringCol(length=35,dbName="create_id")
	CreateTime = DateTimeCol(default=cur_date_time(),dbName="create_time")

