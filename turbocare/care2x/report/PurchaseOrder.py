# General stuff
from datetime import datetime
import Image
#Turbogears stuff
import logging
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash, identity
#Reportlab stuff
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import Table, TableStyle, GRID_STYLE
from reportlab.platypus.frames import Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors

DATE_FORMAT='%Y-%m-%d'

def FmtNum(v, minwidth=0, trailing=2):
	V = '%f' % v
	I = V[0:V.find('.')]
	D = V[V.find('.'):]
	f_I = ''
	H = [y for y in I]
	H.reverse()
	for x, i in zip(H,range(0,len(I))):
		if i in [3,5,7,9,11,13,15,17]:
			f_I = x+','+f_I
		else:
			f_I = x+f_I
	if trailing > 0:
		f_D = D[0:trailing+1]
	else:
		f_D = ''
	return f_I+f_D
	
image = Image.open('/home/wesley/devel/care2x/care2x/report/logo.png')
image.load()

signature = "Yours sincerely,\n\n\n\n\nLuke Skywalker\nJedi Knight"

class PurchaseOrderPrintOut:
	'''	Produce the specified PurchaseOrder (using the id)
	'''
	PAGE_HEIGHT=defaultPageSize[1]
	PAGE_WIDTH=defaultPageSize[0]
	styles = getSampleStyleSheet()
	PAGE_SIZE = 'A4'
	StaticDir = '/home/wesley/devel/care2x/care2x/static/reports/' # Location for static files to be stored
	StaticURL = '/static/reports/'
	PO = None
	LogoFile = '/home/wesley/devel/care2x/care2x/report/logo.png'
	
	def __init__(self, PO, Paper='A4', **kw):
		'''	Initialize the report for printing
		'''
		self.PO = PO
		self.PAGE_SIZE = Paper
			
	def AddressBox(self, canvas):
		'''	Create an address box on the supplied canvas '''
		# Get our data
		Address = [str(self.PO.Vendor.Name)]
		Address.append('Attn: %s' % str(self.PO.Vendor.ContactName))
		Address += self.PO.Vendor.AddressLabel.splitlines()
		for line, i in zip(Address, range(0,len(Address))):
			canvas.drawString(0.5*inch, self.PAGE_HEIGHT-1*inch-9*i,line)

	def LogoBox(self, canvas):
		'''	Create a logo on the supplied canvas '''
		canvas.drawInlineImage(image=image, x=self.PAGE_WIDTH - 1.35*inch, y=self.PAGE_HEIGHT-1.75*inch,\
			width=1.2*inch,height=1.7*inch)

	def DocFirstPage(self, canvas, doc):
		canvas.saveState()
		# Print the title
		canvas.setFont('Courier',14)
		canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-2*inch, "Purchase Order")
		# Add the letter head/logo
		self.LogoBox(canvas)
		canvas.setFont('Courier',9)
		# Add the Address label
		self.AddressBox(canvas)
		# Add the date
		canvas.drawString(0.5*inch, self.PAGE_HEIGHT-2*inch-10,self.PO.POSentOnDate.strftime(DATE_FORMAT))
		canvas.drawString(inch, 0.75 * inch, "Page 1")
		canvas.restoreState()

	def DocOtherPage(self, canvas, doc):
		canvas.saveState()
		# Print the title
		canvas.setFont('Courier',14)
		canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-1*inch, "Purchase Order")
		# Add the letter head/logo
		self.LogoBox(canvas)
		canvas.setFont('Courier',9)
		# Add the Address label
		self.AddressBox(canvas)
		# Add the date
		canvas.drawString(0.5*inch, self.PAGE_HEIGHT-2*inch-10,self.PO.POSentOnDate.strftime(DATE_FORMAT))
		canvas.drawString(inch, 0.75 * inch, "Page 1")
		canvas.restoreState()
		
	def GenerateTable(self):
		'''	Go through the ColFormat list and make a table style
			AutoFormat should be run before this routine
		'''
		GenericStyle = [('BACKGROUND',(0,0),(-1,0),colors.lightgrey), # First line gets a gray background
					('ALIGN',(0,0),(-1,0),'CENTER'), # Center the first row (header)
					('LINEABOVE', (0,1), (-1,1), 0.25, colors.black),
					('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black),
					('LINEBEFORE', (0,0), (-1,-1), 0.25, colors.black),
					('BOX', (0,0), (-1,-1), 0.25, colors.black), # Make a box around the entire table
					('ALIGN',(0,1),(0,-1),'LEFT'),
					('ALIGN',(1,1),(1,-1),'RIGHT'),
					('ALIGN',(2,1),(2,-1),'RIGHT'),
					('ALIGN',(3,1),(3,-1),'RIGHT'),
					('ALIGN',(4,1),(4,-1),'LEFT'),
					('FONT', (0,0),(-1,-1), 'Courier', 10)]
		# Produce our data
		Headers = ['Item Name','Quantity','Price','Total','Notes']
		CUR_WIDTH = self.PAGE_WIDTH-1*inch
		Widths = [CUR_WIDTH*0.25,CUR_WIDTH*0.1,CUR_WIDTH*0.15,CUR_WIDTH*0.25,CUR_WIDTH*0.25]
		Data = []
		Data.append(Headers)
		fmt = '%0.2f'
		Total = 0.0
		for item in self.PO.Items:
			Data.append([item.GetQuoteItemName(), '%0.0f' % item.QuantityRequested, FmtNum(item.QuotePrice), \
				FmtNum(item.QuantityRequested*item.QuotePrice), item.Notes])
			Total += item.QuantityRequested*item.QuotePrice
		Data.append(['Total','','',FmtNum(Total),''])
		return Table(Data,style=GenericStyle,repeatRows=1,colWidths=Widths, rowHeights=None)

	def MakePurchaseOrder(self):
		'''	Produce the PurchaseOrder Print out
		'''
		#Make the document
		doc = SimpleDocTemplate(self.StaticDir+self.Filename)
		#p = Paragraph(table, styles['Normal'])
		Body = [Spacer(1,1.75*inch)]
		Body.append(Paragraph(self.PO.Notes,self.styles['Normal']))
		Body.append(Spacer(1,0.2*inch))
		Body.append(self.GenerateTable())
		Body.append(Spacer(1,0.2*inch))
		Body.append(Paragraph('Yours Sincerely,',self.styles['Normal']))
		Body.append(Spacer(1,1*inch))
		Body.append(Paragraph('Homer Simpson',self.styles['Normal']))
		Body.append(Paragraph('Safty Inspector',self.styles['Normal']))
		doc.build(Body, onFirstPage=self.DocFirstPage, onLaterPages=self.DocOtherPage)
		
	def P(self, Filename='PO.pdf'):
		''' Print to PDF '''
		self.Filename = 'purchase_order_%d.pdf' % self.PO.id
		self.MakePurchaseOrder()
		
	def ReportGeneric(self):
		'''	Don't know if I'll use this for displaying the link to the generic report? ... maybe
		'''
		self.MakeGenericReport()
		return dict(next_link=self.StaticURL+self.Filename)