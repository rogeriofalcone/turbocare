import logging
import sys
import os
import stat
import string
import getopt
import time
import os.path
import time
import simplejson
import pprint
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model
from model import DATE_FORMAT
import model_inventory
import inventory_catalogitem
from printer_inventory import *

log = logging.getLogger("care2x.controllers")
ReportBaseDir= "care2x/static/user_reports"

class SavedReport(controllers.RootController):
#===== Inventory App Stuff ====================================================
	@expose(html='care2x.templates.saved')
	@identity.require(identity.not_anonymous())
	def index(self, customer_id='', receipt_id='', **kw):
		usersDir = self.getDirectories(ReportBaseDir)
		usersFiles= {}
		for direc in usersDir:
			log.debug("Directory name " +direc)
			#usersFiles.append(self.getReport(ReportBaseDir,direc))
			usersFiles[direc]=self.getReport(ReportBaseDir,direc)
		log.debug(usersFiles)
		return dict(groups=usersDir,reports=usersFiles, title="Saved Reports")
	
	def getDirectories(self,my_dir):
		try:
			file_list = os.listdir(my_dir)
		except:
			log.debug("No such directory "+ ReportBaseDir)
			return []
		#print file_list
		new_list=[]
		log.debug("Your Groups are " + str(turbogears.identity.current.groups))
		for name in file_list:
			if os.path.isdir(my_dir + "/" +name):
#				log.debug('Dir name is ' + name)
				#Check is user is in write group. 
				if name in turbogears.identity.current.permissions:
					new_list.append(name)
					log.debug('You are allowed ' + name)
		return new_list
		
	def getReport(self,basedir,direcory_name):
		log.debug("In "+direcory_name)
		new_list=[]
		file_list = os.listdir(basedir+"/" + direcory_name)
		for name in file_list:
			if name[0] != '.':
				new_list.append(name)
		return new_list

	


	#Map billing back to the index
	billing = index
	#
	#	External stuff
	#
	CatalogItemSearch = inventory_catalogitem.CatalogItemSearch
	
	#
	#	COMMENTS
	#
	# TESTED:
	#	1. When I have a receipt with un-assigned stock locations, it will add new stock locations
	#	2. When I have a receipt whose transfer is not complete, It will update quantity changes
	#
	# TO TEST:
	#	1. Reject modifications to a completed receipt
	#	2. Adding A new bill
	#	3. Appending new items to a bill
	#	4. Changing the location of an assigned receipt item