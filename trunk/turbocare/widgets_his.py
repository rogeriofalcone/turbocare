from turbogears import  validate, widgets, validators


#=====Person=====
personDateReg = widgets.CalendarDatePicker("DateReg",button_text="Pick")
personName_first = widgets.TextField("Name_first",label = "First name")
personName2 = widgets.TextField("Name2",label = "Extra name (2)")
personName3 = widgets.TextField("Name3",label = "Extra name (3)")
personNameMiddle = widgets.TextField("NameMiddle",label = "Middle name")
personNameLast = widgets.TextField("NameLast",label = "Last name")
personNameMaiden = widgets.TextField("NameMaiden",label = "Maiden name")
personNameOthers = widgets.TextField("NameOthers",label = "Other name")
personDateBirth = widgets.CalendarDatePicker("DateBirth",button_text="Calendar",label="Date of birth")
personBloodGroup = widgets.TextField("BloodGroup",label = "Blood group")
personAddrStr = widgets.TextField("AddrStr",label = "Address", attrs={'size':20})
personAddrStrNr = widgets.TextField("AddrStrNr",label = "Street number",  attrs={'size':5})

personAddrZip = widgets.TextField("AddrZip",label = "Address pin code")

personAddrCitytownNr = widgets.HiddenField("AddressCityTown")

personAddrIsValid = widgets.CheckBox(name="AddrIsValid", attrs=dict(checked=True), label="Is address valid", help_text="")
personCitizenship = widgets.TextField("Citizenship",label = "Citizenship")
personPhone1Code = widgets.TextField("Phone1Code",label = "Phone (area code)")
personPhone1Nr = widgets.TextField("Phone1Nr",label = "Phone number")
personPhone2Code = widgets.TextField("Phone2Code",label = "Phone 2 (area code)")
personPhone2Nr = widgets.TextField("Phone2Nr",label = "Phone 2 number")
personCellphone1Nr = widgets.TextField("Cellphone1Nr",label = "Cellphone number")
personCellphone2Nr = widgets.TextField("Cellphone2Nr",label = "Cellphone 2 number")
personFax = widgets.TextField("Fax",label = "Fax")
personEmail = widgets.TextField("Email",label = "E-mail")
personCivilStatus = widgets.TextField("CivilStatus",label = "Civil status")
personSex = widgets.TextField("Sex",label = "Sex (M/F/U)")
personTitle = widgets.SingleSelectField("Title", 
                                   options=[(1,"None"),
                                   			(2, "Mrs."), 
                                            (3, "Mr."), 
                                            (4, "Ms."),
                                            (5, "Dr.")],
                                   default=1,label="Title")
#personPhoto = BLOBCol(dbName='photo')
personPhotoFilename = widgets.FileField("PhotoFilename", attrs=dict(size="30"), label="Photo filename")
#personEthnicOrig = ForeignKey("ClassEthnicOrig", dbName='ethnic_orig')
personOrgId = widgets.TextField("OrgId",label = "Organization id")
personSssNr = widgets.TextField("SssNr",label = "Social security number")
personNatIdNr = widgets.TextField("NatIdNr",label = "National ID number")
personReligion = widgets.TextField("Religion",label = "Religion")
#personMotherPid = ForeignKey("Person", dbName='mother_pid')
#personFatherPid = ForeignKey("Person", dbName='father_pid')
personContactPerson = widgets.TextField("ContactPerson",label = "Contact person")
#personContactPid = ForeignKey("Person",dbName='contact_pid')
personContactRelation = widgets.TextField("ContactRelation",label = "Relation of contact")
personDeathDate = widgets.CalendarDatePicker("DeathDate",button_text="Pick",label="Date of death")
#personDeathEncounterNr = ForeignKey("Encounter", dbName='death_encounter_nr')
personDeathCause = widgets.TextField("DeathCause",label = "Death cause")
personDeathCauseCode = widgets.TextField("DeathCauseCode",label = "Death code")
personDateUpdate = widgets.CalendarDatePicker("DateUpdate",button_text="Pick",label="Date of update")
#=====AddressCityTown=====
addressUneceModifier = widgets.TextField("UneceModifier",label="UN ECE modifier")
addressUneceLocode = widgets.TextField("UneceLocode",label="UN ECE location code")
addressName = widgets.TextField("Name",label="City/town name")
addressZipCode = widgets.TextField("ZipCode",label="Pin code")#char 25
addressIsoCountryId = widgets.TextField("IsoCountryId",label="Country code",attrs={'size':3})
addressUneceLocodeType = widgets.TextField("UneceLocodeType",label="UN ECE location code type")
addressUneceCoordinates = widgets.TextField("UneceCoordinates",label="UN ECE coordinates")
addressInfoUrl = widgets.TextField("InfoUrl",label="Web-site")
addressUseFrequency = widgets.HiddenField("UseFrequency")
addressBlock = widgets.TextField("Block",label="Block")
addressDistrict = widgets.TextField("District",label="District")
addressState = widgets.TextField("State",label="State")

#============FOR ALL OBJECTS====================
Status = widgets.Label("Status",label = "Record status")
History = widgets.HiddenField("History")

                        
