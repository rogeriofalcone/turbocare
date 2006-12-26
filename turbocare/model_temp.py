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

