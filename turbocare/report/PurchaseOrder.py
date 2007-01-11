# General stuff
from datetime import datetime
import Image
#Turbogears stuff
import logging
import cherrypy
from sqlobject import *
import turbogears
from turbogears import  controllers, expose, validate, redirect, widgets, validators, flash, identity
from turbogears import config
#Reportlab stuff
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
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
	
# image = Image.open('/home/wesley/devel/care2x/care2x/report/logo.png')
# image.load()

class PurchaseOrderPrintOut:
	'''	Produce the specified PurchaseOrder (using the id)
	'''
	PAGE_HEIGHT=defaultPageSize[1]
	PAGE_WIDTH=defaultPageSize[0]
	styles1 = getSampleStyleSheet()
	styles2 = getSampleStyleSheet()
	PAGE_SIZE = 'A4'
	StaticDir = config.get('turbocare.basedir','') + 'turbocare/static/reports/'
	#StaticDir = '/home/wesley/svn/google/turbocare/turbocare/static/reports/' # Location for static files to be stored
	StaticURL = '/static/reports/'
	PO = None
	
	def __init__(self, PO, Paper='A4', PreparedBy='', CheckedBy='', ApprovedBy='', ToAddress='',
	FromAddress='', DeliveryInstructions='', PackingAndForwarding='', **kw):
		'''	Initialize the report for printing
		'''
		self.PO = PO
		self.PAGE_SIZE = Paper
		self.PreparedBy=PreparedBy
		self.CheckedBy=CheckedBy
		self.ApprovedBy=ApprovedBy
		self.ToAddress=ToAddress
		self.FromAddress=FromAddress
		self.DeliveryInstructions=DeliveryInstructions
		self.PackingAndForwarding=PackingAndForwarding
		self.RegularStyle = self.styles1['Normal']
		self.RegularStyle.fontName = 'Times-Roman'
		self.RegularStyle.leftIndent = -0.5*inch
		self.RegularStyle.fontSize = 12
		self.TitleStyle = self.styles2['Normal']
		self.TitleStyle.fontName = 'Courier'
		self.TitleStyle.leftIndent = -0.5*inch
		self.TitleStyle.fontSize = 14
			
			
	def ToAddressBox(self, canvas):
		'''	Create a to address box on the supplied canvas '''
		# Get our data
		if self.ToAddress=='':
			Address = ["To:",str(self.PO.Vendor.Name)]
			Address.append('Attn: %s' % str(self.PO.Vendor.ContactName))
			Address += self.PO.Vendor.AddressLabel.splitlines()
		else:
			Address = self.ToAddress.splitlines()
			Address = ["To:"]+Address
		for line, i in zip(Address, range(0,len(Address))):
			canvas.drawString(0.5*inch, self.PAGE_HEIGHT-1*inch-9*i,line)

	def FromAddressBox(self, canvas):
		'''	Create a from address box on the supplied canvas '''
		# Get our data
		if self.FromAddress=='':
			Address = ["From:","CIHSR","4th Mile, Dimapur, NL", "123321", "Ph: 123123123"]
		else:
			Address = self.FromAddress.splitlines()
			Address = ["From"]+Address
		for line, i in zip(Address, range(0,len(Address))):
			canvas.drawString(2.5*inch, self.PAGE_HEIGHT-1*inch-9*i,line)
	
	def PreparedByBox(self, canvas):
		'''	Create a prepared by box on the supplied canvas '''
		# Get our data
		if self.PreparedBy=='':
			Text = ["Prepared By", "Unknown Person"]
		else:
			Text = ["Prepared By", self.PreparedBy]
		for line, i in zip(Text, range(0,len(Text))):
			canvas.drawString(0.5*inch, 1.5*inch-9*i,line)

	def ApprovedByBox(self, canvas):
		'''	Create a prepared by box on the supplied canvas '''
		# Get our data
		if self.PreparedBy=='':
			Text = ["Approved By", "Unknown Person"]
		else:
			Text = ["Approved By", self.ApprovedBy]
		for line, i in zip(Text, range(0,len(Text))):
			canvas.drawString(6.5*inch, 1.5*inch-9*i,line)
	
	def CheckedByBox(self, canvas):
		'''	Create a prepared by box on the supplied canvas '''
		# Get our data
		if self.CheckedBy=='':
			Text = ["Checked By", "Unknown Person"]
		else:
			Text = ["Checked By", self.CheckedBy]
		for line, i in zip(Text, range(0,len(Text))):
			canvas.drawString(3.5*inch, 1.5*inch-9*i,line)
	
	def PurchaseOrderNoBox(self, canvas):
		'''	Create a from address box on the supplied canvas '''
		# Get our data
		if self.PO.POSentOnDate != None:
			Text = ["Purchase No.: %#08d" % self.PO.id, "Purchase Date: %s" % self.PO.POSentOnDate.strftime('%d/%m/%Y')]
		else:
			Text = ["Purchase No.: %#08d" % self.PO.id, "Purchase Date: Unknown"]
		for line, i in zip(Text, range(0,len(Text))):
			canvas.drawRightString(self.PAGE_WIDTH-1*inch, self.PAGE_HEIGHT-1*inch-9*i,line)

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
		# self.LogoBox(canvas)
		canvas.setFont('Courier',9)
		# Add the Address label
		self.ToAddressBox(canvas)
		self.FromAddressBox(canvas)
		self.PurchaseOrderNoBox(canvas)
		self.PreparedByBox(canvas)
		self.CheckedByBox(canvas)
		self.ApprovedByBox(canvas)
		# Add the date
		canvas.drawString(inch, 0.75 * inch, "Page 1")
		canvas.restoreState()

	def DocOtherPage(self, canvas, doc):
		canvas.saveState()
		# Print the title
		canvas.setFont('Courier',14)
		canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-1*inch, "Purchase Order")
		# Add the letter head/logo
		# self.LogoBox(canvas)
		canvas.setFont('Courier',9)
		# Add the Address label
		self.ToAddressBox(canvas)
		self.FromAddressBox(canvas)
		self.PurchaseOrderNoBox(canvas)
		self.PreparedByBox(canvas)
		self.CheckedByBox(canvas)
		self.ApprovedByBox(canvas)
		# Add the date
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
					('ALIGN',(0,1),(0,-1),'CENTER'),
					('ALIGN',(1,1),(1,-1),'LEFT'),
					('ALIGN',(2,1),(2,-1),'RIGHT'),
					('ALIGN',(3,1),(3,-1),'RIGHT'),
					('ALIGN',(4,1),(4,-1),'RIGHT'),
					('ALIGN',(5,1),(5,-1),'LEFT'),
					('FONT', (0,0),(-1,-1), 'Courier', 10)]
		# Produce our data
		Headers = ['SL No.','Discription','Qty','Unit Price','Total','Notes']
		CUR_WIDTH = self.PAGE_WIDTH-1.5*inch
		Widths = [0.5*inch,CUR_WIDTH*0.25,CUR_WIDTH*0.1,CUR_WIDTH*0.15,CUR_WIDTH*0.25,CUR_WIDTH*0.25]
		Data = []
		Data.append(Headers)
		fmt = '%0.2f'
		Total = 0.0
		for item, sl_no in zip(self.PO.Items,range(len(self.PO.Items))):
			Data.append([sl_no, item.GetQuoteItemName(), '%0.0f' % item.QuantityRequested, FmtNum(item.QuotePrice), \
				FmtNum(item.QuantityRequested*item.QuotePrice), item.Notes])
			Total += item.QuantityRequested*item.QuotePrice
		Data.append(['','Total','','',FmtNum(Total),''])
		return Table(Data,style=GenericStyle,repeatRows=1,colWidths=Widths, rowHeights=None)

	def MakePurchaseOrder(self):
		'''	Produce the PurchaseOrder Print out
		'''
		#Make the document
		doc = SimpleDocTemplate(self.StaticDir+self.Filename)
		#p = Paragraph(table, styles['Normal'])
		Body = [Spacer(1,1*inch)]
		Body.append(self.GenerateTable())
		if self.DeliveryInstructions != '':
			Body.append(Spacer(1,0.2*inch))
			Body.append(Paragraph("Delivery Instructions:",self.TitleStyle))
			Body.append(Paragraph(self.DeliveryInstructions,self.RegularStyle))
		if self.PackingAndForwarding != '':
			Body.append(Spacer(1,0.2*inch))
			Body.append(Paragraph("Packing, Forwarding & Notes:",self.TitleStyle))
			Body.append(Paragraph(self.PackingAndForwarding,self.RegularStyle))
		doc.build(Body, onFirstPage=self.DocFirstPage, onLaterPages=self.DocOtherPage)
		
	def P(self, Filename='PO.pdf'):
		''' Print to PDF '''
		self.Filename = 'purchase_order_%d.pdf' % self.PO.id
		self.MakePurchaseOrder()
		return self.Filename
		
	def ReportGeneric(self):
		'''	Don't know if I'll use this for displaying the link to the generic report? ... maybe
		'''
		self.MakeGenericReport()
		return dict(next_link=self.StaticURL+self.Filename)
