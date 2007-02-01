#printer_map.py
#This file uses printer_list.py to find the requested printer type for a computer.
import printer_list 
import logging
log = logging.getLogger("turbocare.controllers")

def GetPrinter(computerIP,typeofprinter):
    log.debug("Computer printing " + computerIP)
    try:
      printer = printer_list.printers[printer_list.computers[computerIP][typeofprinter]]
    except:
        return None
    return printer

def ReloadPrinterList():
    reload(printer_list)
