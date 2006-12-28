import logging

import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model
from widgets_his import *

log = logging.getLogger("turbocare.controllers")

   
class HIS(controllers.RootController):

	@expose(html="turbocare.templates.form")
	def PersonEdit(self, **kw):
		java_script = "\n\
			function update_form_delay(){\n\
				callLater(1,update_form);\n\
			};\n\
			function update_form(){\n\
				var citydispGood = function(data){\n\
					self.document.PersonEdit.PersonEdit_AddrCitytownFind.value = data.value;\n\
				};\n\
				var  citydispBad = function(err){\n\
					alert(\"The data could not be fetched: \"+err.req+ \" \" + err);\n\
					self.document.PersonEdit.PersonEdit_AddrCitytownFind.value = \"Select\";\n\
				};\n\
				var cityid = self.document.PersonEdit.PersonEdit_AddressCityTown.value;\n\
				var citydisp = loadJSONDoc(\"AddressCityTownDisplay?id=\"+cityid);\n\
				citydisp.addCallbacks(citydispGood,citydispBad);\n\
				return true;\n\
			};\n"
		form_js = widgets.JSSource(java_script)
		personAddrCitytown_find = widgets.Button(default="Select",attrs=dict(id='PersonEdit_AddrCitytownFind',onclick='javascript:doFind("AddressCityTownSearch?CallingForm=PersonEdit&FormField=PersonEdit_AddressCityTown")'),label='City/Town')
		personForm = widgets.TableForm("PersonEdit", fields=[personAddrCitytownNr,personTitle,personName_first,personNameMiddle,personNameLast,personDateBirth,personBloodGroup,personAddrIsValid,personAddrCitytown_find], action="PersonEditsave", submit_text="Add")
		return dict(form=personForm, action='PersonEdit',extra_script=form_js.display(),message="")

	@expose('turbocare.templates.search')
	def AddressCityTownSearch(self, **kw):
		if kw.has_key("CallingForm"):
			ret_form = widgets.HiddenField("CallingForm",attrs={'value':kw["CallingForm"]})
		else:
			ret_form = widgets.HiddenField("CallingForm",attrs={'value':'None'})
		if kw.has_key("FormField"):
			ret_field = widgets.HiddenField("FormField",attrs={'value':kw["FormField"]})
		else:
			ret_field = widgets.HiddenField("FormField",attrs={'value':'None'})
		form = widgets.RemoteForm(fields = [addressName,addressZipCode,addressBlock,addressDistrict,ret_form,ret_field], name="search_form", update = "search_result", action = "AddressCityTownSearchResult",submit_text='Search',method='post')
		return dict(searchform=form)
		
	@expose()
	def AddressCityTownSearchResult(self, **kw):
		qArgs = ""
		if kw.has_key("Name"):
			if kw["Name"] != "":
				qArgs+="model.AddressCityTown.q.Name.contains('"+kw["Name"] + "'),"
		if kw.has_key("ZipCode"):
			if kw["ZipCode"] != "":
				qArgs+="model.AddressCityTown.q.ZipCode.contains('"+kw["ZipCode"] + "'),"
		if kw.has_key("District"):
			if kw["District"] != "":
				qArgs+="model.AddressCityTown.q.District.contains('"+kw["District"] + "'),"
		if kw.has_key("Block"):
			if kw["Block"] != "":
				qArgs+="model.AddressCityTown.q.Block.contains('"+kw["Block"] + "'),"
		if len(qArgs) > 0:
			cities = eval('model.AddressCityTown.select(AND ('+qArgs[0:len(qArgs)-1]+'))')
		else:
			cities = model.AddressCityTown.select()
		results = ''
		lineNum = 0
		for city in list(cities):
			lineNum += 1
			if lineNum == 1:
				results += '<div class="smallstringtop"><br/><a href="javascript:retPick(form=\''+ kw["CallingForm"] +'\',field=\''+kw["FormField"] +'\',id=\''+ str(city.id) +'\')">Pick >></a> '+city.Name + ', (' + city.Block +', '+city.District+', '+city.ZipCode+', '+city.State+', '+city.IsoCountryId+')\n</div>'			
			elif (lineNum % 2) == 0:
				results += '<div class="smallstringeven"><br/><a href="javascript:retPick(form=\''+ kw["CallingForm"] +'\',field=\''+kw["FormField"] +'\',id=\''+ str(city.id) +'\')">Pick >></a> '+city.Name + ', (' + city.Block +', '+city.District+', '+city.ZipCode+', '+city.State+', '+city.IsoCountryId+')\n</div>'
			else:
				results += '<div class="smallstringodd"><br/><a href="javascript:retPick(form=\''+ kw["CallingForm"] +'\',field=\''+kw["FormField"] +'\',id=\''+ str(city.id) +'\')">Pick >></a> '+city.Name + ', (' + city.Block +', '+city.District+', '+city.ZipCode+', '+city.State+', '+city.IsoCountryId+')\n</div>'
		return results 

	@expose(format="json")
	def AddressCityTownDisplay(self, **kw):
		if kw.has_key('id'):
			try:
				city = model.AddressCityTown.get(int(kw['id']))
				return dict(value=city.Name + ", " + city.Block + ", " + city.District + ", " + city.State)
			except ValueError:
				return dict(value="Error: City index is wrong type")
			except SQLObjectNotFound:
				return dict(value="Error: City not found")
		else:
			return dict(value="Error: No value is specified")
