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


class PurchaseOrderPrintOut:
	'''	Produce the specified PurchaseOrder (using the id)
	'''
	PurchaseOrderID = None
	PAGE_HEIGHT=defaultPageSize[1]
	PAGE_WIDTH=defaultPageSize[0]
	styles = getSampleStyleSheet()
	PAGE_SIZE = 'A4'
	StaticDir = '/home/wesley/devel/care2x/care2x/static/reports/' # Location for static files to be stored
	StaticURL = '/static/reports/'
	
	def __init__(self, PurchaseOrderID, Paper='A4', **kw):
		'''	Initialize the report for printing
		'''
		self.PurchaseOrderID = PurchaseOrderID
		self.PAGE_SIZE = Paper
	
	def FormatData(self):
		'''	Put the data into a list of rows where each column in the row is formatted properly
			This is done according to the ColFormat list (AutoFormat should be run before this)
		'''
		rows = []
		rows.append(self.ColHeaders)
		# Go through every row in the data set
		for row in self.Data:
			cols = []
			# Go through every column in the row
			for data, col in zip(row, range(0,len(self.ColFormat))):
				# In each column, apply the Column format to the column data using the % string format operators
				cols.append(self.ColFormat[col] % data)
			rows.append(cols)
		return rows

	def DocFirstPage(self, canvas, doc):
		canvas.saveState()
		canvas.setFont('Courier',16)
		canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-108, self.Title)
		canvas.setFont('Courier',9)
		canvas.drawString(inch, 0.75 * inch, "First Page / %s" % self.Title)
		canvas.restoreState()

	def DocOtherPage(self, canvas, doc):
		canvas.saveState()
		canvas.setFont('Courier',9)
		canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, self.Title))
		canvas.restoreState()
		
	def GenerateTableStyle(self):
		'''	Go through the ColFormat list and make a table style
			AutoFormat should be run before this routine
		'''
		GenericStyle = [('BACKGROUND',(0,0),(-1,0),colors.lightgrey), # First line gets a gray background
					('ALIGN',(0,0),(-1,0),'CENTER'), # Center the first row (header)
					('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), # make inner line grids for cells
					('BOX', (0,0), (-1,-1), 0.25, colors.black)] # Make a box around the entire table
		# Figure out alignment for each column in the table
		for fmt, col in zip(self.ColFormat,range(0,len(self.ColFormat))):
			if ('s' in fmt): # Left justify strings
				GenericStyle.append(('ALIGN',(col,1),(col,-1),'LEFT'))
			elif ('d' in fmt) or ('f' in fmt): # Right justify numbers
				GenericStyle.append(('ALIGN',(col,1),(col,-1),'RIGHT'))
			else: # Centre other objects
				GenericStyle.append(('ALIGN',(col,1),(col,-1),'CENTER'))
		# Generate and return the style
		return TableStyle(GenericStyle)

	def MakePurchaseOrder(self):
		'''	Produce the PurchaseOrder Print out
		'''
		# Configure the table format
		self.AutoFormat()
		#Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1,repeatRows=0, repeatCols=0)
		# table = Table(self.Data,style=tableStyle,repeatRows=1,colWidths=col_widths, rowHeights=len(results['data'])*[0.3*inch])
		table = Table(self.FormatData(),style=self.GenerateTableStyle(),repeatRows=1,colWidths=None, rowHeights=None)
		#Make the document
		doc = SimpleDocTemplate(self.StaticDir+self.Filename)
		#p = Paragraph(table, styles['Normal'])
		Body = [Spacer(1,2*inch)]
		Body.append(table)
		Body.append(Spacer(1,0.2*inch))
		doc.build(Body, onFirstPage=self.DocFirstPage, onLaterPages=self.DocOtherPage)
		
	def ReportGeneric(self):
		'''	Don't know if I'll use this for displaying the link to the generic report? ... maybe
		'''
		self.MakeGenericReport()
		return dict(next_link=self.StaticURL+self.Filename)