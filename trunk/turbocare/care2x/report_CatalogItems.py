#Turbogears stuff
import logging
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash, identity
import model
#Reportlab stuff
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import Table, TableStyle, GRID_STYLE
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors
#Initial reportlab vars
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "Catalog Items Report"

def GetCatalogData():
	rows = []
	titles = ['id', 'Name', 'Avg. Cost', 'Qty. Available', 'Total Qty Received', 'Qty. Sold', 'Qty. Consumed']
	rows.append(titles)
	max_col_width = []
	total_col_len = []
	for col in titles:
		max_col_width.append(len(col))
		total_col_len.append(len(col))
	records = model.InvCatalogItem.select()
	for row in records:
		cols = [str(row.id), row.Name, str(row.AvgCost()), str(row.QtyAvailable()), str(row.QtyReceived()), str(row.QtySold()),\
			str(row.QtyConsumed())]
		i = 0
		for col in cols:
			total_col_len[i] += len(col)
			if len(col) > max_col_width[i]:
				max_col_width[i] = len(col)
			i+=1
		rows.append(cols)
	return dict(data=rows, widths=max_col_width, total_widths=total_col_len)

def DocFirstPage(canvas, doc):
	canvas.saveState()
	canvas.setFont('Courier',16)
	canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
	canvas.setFont('Courier',9)
	canvas.drawString(inch, 0.75 * inch, "First Page / %s" % Title)
	canvas.restoreState()

def DocOtherPage(canvas, doc):
	canvas.saveState()
	canvas.setFont('Courier',9)
	canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, Title))
	canvas.restoreState()

def MakeCatalogItemsReport(filename):
	log = logging.getLogger("care2x.controllers")
	#Generate the table style
	tableStyle = TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
		('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
		('BOX', (0,0), (-1,-1), 0.25, colors.black),
		('ALIGN',(0,0),(-1,0),'CENTER'),
		('ALIGN',(0,1),(-1,-1),'RIGHT'),
		('ALIGN',(1,1),(1,-1),'LEFT'),
		('TEXTCOLOR',(0,0),(-1,-1),colors.black),
		])
	#Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1,repeatRows=0, repeatCols=0)
	#Make the table
	results = GetCatalogData()
	#Calculate the column widths that I prefer
	col_widths = []
	total=0
	for col in results['total_widths']:
		total += col
	for col in results['total_widths']:
		col_widths.append((PAGE_WIDTH-inch)*col/total)
	log.debug("Column count: %s" % str(len(col_widths)))#GRID_STYLE
	table = Table(results['data'],style=tableStyle,repeatRows=1,colWidths=col_widths, rowHeights=len(results['data'])*[0.3*inch])
	#Make the document
	doc = SimpleDocTemplate('/home/wesley/devel/care2x/care2x/static/reports/'+filename)
	#p = Paragraph(table, styles['Normal'])
	Body = [Spacer(1,2*inch)]
	Body.append(table)
	Body.append(Spacer(1,0.2*inch))
	doc.build(Body, onFirstPage=DocFirstPage, onLaterPages=DocOtherPage)
	
@expose(html='care2x.templates.report')
def ReportCatalogItems(self):
	filename = model.cur_user_id()+model.cur_date_time().strftime('%Y%m%d%H%M%S')+'_catalogitems.pdf'
	MakeCatalogItemsReport(filename)
	return dict(next_link='/static/reports/'+filename)