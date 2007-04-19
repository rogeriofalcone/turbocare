from printer_tdp643 import TDP643
import logging
import sys, os, time, socket
from sqlobject import *
import model
import model_inventory
import inventory_catalogitem
import printer_map

# Standard vars
#HOST_PORT = 3444
log = logging.getLogger("turbocare.controllers")
# Initialize printer

def PrintReceipt(ReceiptID, ClientIP):
	'''     Load a receipt from the database and print to the printer.
	'''
	clientPrinter=printer_map.GetPrinter(ClientIP,'ReceiptPrinter')
	if clientPrinter==None:
		return "No printer found"
	
	#Load the receipt
	receipt = model.InvReceipt.get(ReceiptID)
	#Load Financial information
	#some initial records had receipt not tied to Encounters, so we'll fix that here if we need to.
	if receipt.ExternalId == None:
		encounter = model.Encounter.get(model.Person.get(receipt.Customer.ExternalID).GetLatestEncounter(receipt.CreateTime))
		receipt.ExternalId = encounter.id
	else:
		encounter = model.Encounter.get(receipt.ExternalId)

	EncounterDate = encounter.EncounterDate 
	InsuranceType = encounter.InsuranceClassNr.ClassId #class_id.  e.g. self_pay, private, charity, hospital, common (state run for everyone in the state)
	InsuranceName = encounter.InsuranceClassNr.Name #name
	if InsuranceType == 'private':
		if encounter.InsuranceFirmID != None:
			try:
				firm = model.InsuranceFirm.get(encounter.InsuranceFirmId)
				InsuranceFirm = 'Firm: %s' % firm.Name #People who provide insurance, not valid with self pay
				InsuranceNumber = 'Number: %s' % encounter.InsuranceNr #Policy Number
			except SQLObjectNotFound:
				firm = None
				InsuranceFirm = 'Unknown insurance firm: Probably a registration ERROR'
				InsuranceNumber = 'Unknown insurance number: Check registration!!'
		else:
			firm = None
			InsuranceFirm = 'Unknown insurance firm: Probably a registration ERROR'
			InsuranceNumber = 'Unknown insurance number: Check registration!!'
			
	else:
		InsuranceFirm = 'Firm: Not applicable'
		InsuranceNumber = 'Number: Not applicable'

	#Print the receipt
	printer = TDP643()
	#Receipt header
	printer.write_hr_single()
	barcode = '00000000000000000000' + str(receipt.CustomerID)
	printer.write_barcode(barcode=barcode[-20:]) #Print out a barcode with the leading character filled with zeros
	printer.write_line(receipt.Customer.Name,font='2')
	printer.write_line("Items purchased on %s" % receipt.CreateTime.strftime('%a %b %d, %Y'),font='2')
	printer.write_line(InsuranceName,font='2')
	printer.write_line(InsuranceFirm,font='2')
	printer.write_line(InsuranceNumber,font='2')
	#Print the items column header
	col_width = [40, 10, 25, 25]
	text = ["Item", "Qty", "Unit Price", "Total"]
	col_just = ['C', 'C', 'C', 'C']
	printer.write_colText(text, col_width, col_just, font='2')
	printer.write_hr_double()
	#Print the body
	col_just = ['L', 'R', 'R','R']
	for item in receipt.CatalogItems:
		if len(item.StockItems) > 0:
			description = item.StockItems[0].StockItem.Name
		else:
			description = item.CatalogItem.Name + ' (ctlg)'
		log.debug('Line: %s, %01.02d, %01.02f, %01.02f' % (description, item.Quantity, item.UnitCost, item.Quantity*item.UnitCost))
		line = [description, '%01.02f' % item.Quantity, '%01.02f' % item.UnitCost, '%01.02f' % (item.Quantity*item.UnitCost)]
		printer.write_colText(line, col_width, col_just, font='2')
	#Print the total
	printer.write_hr_double()
	line = ['Total:','','', '%01.02f' % receipt.TotalPayment]
	printer.write_colText(line, col_width, col_just, font='2')
	#Print the footer... the payment made
	col_just = ['R','R']
	col_width = [50, 50]
	line = ['Self pay:', '%01.02f' % receipt.TotalSelfPay]
	printer.write_colText(line, col_width, col_just, font='2')
	line = ['Insurance:', '%01.02f' % receipt.TotalInsurance]
	printer.write_colText(line, col_width, col_just, font='2')
	line = ['','===============']
	printer.write_colText(line, col_width, col_just, font='2')
	line = ['Total payment:','Rs. %01.02f' % receipt.TotalPaid]
	printer.write_colText(line, col_width, col_just, font='2')
	# Print out the stock locations where items are located
	printer.write_hr_single()
	printer.write_line('Locations',font='2')
	printer.write_hr_single()
	for location in receipt.FromLocationList():
			printer.write_line(location,font='2')
	#Make a server connection
	#HOST = PrinterIP
	#PORT = HOST_PORT
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock.connect((HOST, PORT))
	sock.connect((clientPrinter['IP'], int(clientPrinter['PORT'])))
	#Send the data
	sock.send(printer.write_toPrinter())
	#sock.flush()
	sock.shutdown(socket.SHUT_WR)
	reply = ''
	#Read the reply
	data = sock.recv(1024)
	while data != '':
		reply += data
		data = sock.recv(1024)
	return 'Completed: ' + reply

def PrintBookletLabel(ReceiptID, ClientIP):
	'''     Load a receipt from the database and print to the printer.
	'''
	log.debug("printer_inventory.PrintBookletLabel")
	clientPrinter=printer_map.GetPrinter(ClientIP,'LabelPrinter')
	if clientPrinter==None:
		return "No printer found"
	
	#Load the Patient
	patient = model.Person.get(model.InvReceipt.get(ReceiptID).Customer.ExternalID)

	#Receipt header
	#log.debug('HIN: %d  NAME: %s  SEX: %s' % (patient.id, patient.DisplayNameAsContact(), patient.Sex))
	#log.debug('D.O.B.: %s  SERVICE: Unknown  1st VISIT DATE: %s' % (patient.DateBirth.strftime(model.DATE_FORMAT), patient.DateReg.strftime(model.DATE_FORMAT)))
	#log.debug('00000000000000000000' + str(patient.id))
	#Print the receipt
	printer = TDP643() # label="book"
	printer.write_hr_single()
	printer.write_line('HIN: %d  NAME: %s  SEX: %s' % (patient.id, patient.DisplayNameAsContact(), patient.Sex))
	printer.write_line('D.O.B.: %s  SERVICE: Unknown  1st VISIT DATE: %s' % (patient.DateBirth.strftime(model.DATE_FORMAT), patient.DateReg.strftime(model.DATE_FORMAT)))
	barcode = '00000000000000000000' + str(patient.id)
	printer.write_barcode(barcode=barcode[-18:]) #Print out a barcode with the leading character filled with zeros.  PatientIDs (HIN) is 18 characters
	printer.write_hr_single()
	#Make a server connection
	#HOST = PrinterIP
	#PORT = HOST_PORT
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock.connect((HOST, PORT))
	sock.connect((clientPrinter['IP'], int(clientPrinter['PORT'])))
	#Send the data
	sock.send(printer.write_toPrinter())
	#sock.flush()
	sock.shutdown(socket.SHUT_WR)
	reply = ''
	#Read the reply
	data = sock.recv(1024)
	while data != '':
		reply += data
		data = sock.recv(1024)
	return 'Completed: ' + reply
