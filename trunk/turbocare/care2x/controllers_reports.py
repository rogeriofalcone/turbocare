import logging
import cherrypy
import turbogears
from turbogears import controllers, expose, validate, redirect
from turbogears import identity
from turbogears.toolbox.catwalk import CatWalk 
import model
from care2x import json
from report_Generic import GenericReport

log = logging.getLogger("care2x.controllers")

class Reports(controllers.RootController):

	@expose(template="care2x.templates.reports_menu")
	def index(self):
		return dict(PageName='Hospital Reports')
		
	@expose(html='care2x.templates.report')
	def CatalogItemsReport(self):
		'''	Report on the Catalog Items
		'''
		items = model.InvCatalogItem.select()
		ColHeaders = ['Name','Description','Type','Qty. In Stock','Value In-Stock']
		ColFormat = ['%s', '%s', '%s', '%d','%0.2f']
		data = []
		for i in items:
			data.append([i.Name,i.Description,i.TypeDescription(),i.QtyAvailable(),i.ValueAvailablePurchase()])
		report = GenericReport(Title="Item Master Listing", Data=data, ColHeaders=ColHeaders, \
			FileName='ItemMasterListing', ColFormat=ColFormat)
		return report.ReportGeneric()
