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
#from div_dialogs.widgets import DialogBoxLink

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

class BedManager(turbogears.controllers.Controller):
	@expose(html='turbocare.templates.programmingerror')
	def idFail(error):
		error= "Not Permited to do operation"
		log.debug(error)
		next_link = "/"
		return dict(error_message = error, next_link=next_link)
	
	@identity.require(identity.has_permission("bed_manager_view"))
	@exception_handler(idFail,"isinstance(tg_exceptions,identity.IdentityFailure)")
	@expose(html='turbocare.templates.bm_Main')
	def index(self, RoomID=None, EncounterID=None, PersonID=None, **kw):
		'''     The main page for bed manager
		        RoomID - The room to highlight first
			EncounterID - The room for the encounter
			PersonID -  the id of the person we want to load (priority)
			If no Id's are given, then the screen shows a default
		'''
		room = None
		if RoomID:
			try:
				room = model.Room.get(int(RoomID))
			except SQLObjectNotFound:
				pass
		elif EncounterID:
			try:
				encounter = model.Encounter.get(int(EncounterID))
				if not encounter.CurrentRoomID():
					room = model.Room.get(encounter.CurrentRoomID())
				else:
					room = None
			except SQLObjectNotFound:
				pass
		elif PersonID:
			room = None
			try:
				person = model.Person.get(int(PersonID))
				if person.GetLatestEncounter():
					encounter = model.Encounter.get(person.GetLatestEncounter())
					if encounter.CurrentRoomID():
						room = model.Room.get(encounter.CurrentRoomID())
			except SQLObjectNotFound:
				pass	
		if room:	
			# Setup the Wards Select
			ward_list = widgets.SingleSelectField(name="ward",attrs={'size':15},
							      options=[(x.id, x.Name) for x in model.Ward.select()],
							      default=[x.id for x in model.Ward.select()].index(room.WardNrID))
			room_list = widgets.SingleSelectField(name="room",attrs={'size':15},
							      options=[(x.id, x.RoomNr) for x in model.Room.select(model.Room.q.WardNrID == room.WardNrID)],
							      default=[x.RoomNr for x in model.Room.select()].index(room.RoomNr))
			bedoptions = [(Num, '%s: Vacant' % Num) for Num in range(0, room.NrOfBeds)]
			usedbeds = model.GetBedActivityInformation(RoomID=room.id)
			usedbedsIndex = [x['BedNr'] for x in usedbeds]
			for bed in range(0,room.NrOfBeds):
				if bed in usedbedsIndex:
					bedoptions[bed] = (bed, '%s: %s' % (bed,usedbeds[usedbedsIndex.index(bed)]['PatientName']))
			bed_list = widgets.SingleSelectField(name="bed",attrs={'size':15},validator=validators.NotEmpty(),
							     options=bedoptions,
							     default=1)
		else:
			ward_list = widgets.SingleSelectField(name="ward",attrs={'size':15},
							      options=[(x.id, x.Name) for x in model.Ward.select()],
							      default=1)
			WardNr = model.Ward.select()[0].id
			room_list = widgets.SingleSelectField(name="room",attrs={'size':15},
							      options=[(x.id, x.RoomNr) for x in model.Room.select(model.Room.q.WardNrID == WardNr)],
							      default=1)
			room = model.Room.select(model.Room.q.WardNrID == WardNr)[0]
			bedoptions = [(Num, '%s: Vacant' % Num) for Num in range(0, room.NrOfBeds)]
			usedbeds = model.GetBedActivityInformation(RoomID=room.id)
			usedbedsIndex = [x['BedNr'] for x in usedbeds]
			for bed in range(0,room.NrOfBeds):
				if bed in usedbedsIndex:
					bedoptions[bed] = (bed, '%s: %s' % (bed,usedbeds[usedbedsIndex.index(bed)]['PatientName']))
			bed_list = widgets.SingleSelectField(name="bed",attrs={'size':15},validator=validators.NotEmpty(),
							     options=bedoptions,
							     default=1)
		return dict(ward_list=ward_list, room_list=room_list, bed_list=bed_list)
	
	@expose(format='json')
	def LoadRooms(self, WardID=None, **kw):
		''' Load the rooms for the specified Ward '''
		rooms = []
		if WardID:
			try:
				ward = model.Ward.get(int(WardID))
				for room in ward.Rooms:
					rooms.append(dict(value=room.id, label=room.RoomNr))
			except SQLObjectNotFound:
				rooms = []
		return dict(rooms=rooms)
		
	@expose(format='json')
	def LoadBeds(self, RoomID=None, **kw):
		''' Load the beds for the specified Room '''
		beds = []
		if RoomID:
			try:
				room = model.Room.get(int(RoomID))
				beds = [dict(value=Num, label='%s: Vacant' % Num) for Num in range(0, room.NrOfBeds)]
				usedbeds = model.GetBedActivityInformation(RoomID=room.id)
				usedbedsIndex = [x['BedNr'] for x in usedbeds]
				for bed in range(0,room.NrOfBeds):
					if bed in usedbedsIndex:
						beds[bed] = dict(value=bed, label='%s: %s' % (bed,usedbeds[usedbedsIndex.index(bed)]['PatientName']))
			except SQLObjectNotFound:
				beds = []
		return dict(beds=beds)
	
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
			
