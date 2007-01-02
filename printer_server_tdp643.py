#!/usr/bin/python
import sys, os, time, shutil, threading, socket
import platform
from optparse import OptionParser

   
class ClientPrint(threading.Thread):
   sock = None
   printer = None
   def __init__(self, sock, printer):
      threading.Thread.__init__(self)        
      self.sock = sock
      self.printer = printer

   def run(self):
      # Wait for data to come and collect (timeout of ?? seconds)
      prn_data = ''
      self.sock.settimeout(5.0)
      try:
         data = self.sock.recv(1024)
         while data != '':
            prn_data += data
            data = self.sock.recv(1024)
      except socket.timeout:
         print "Client timed out - disconnecting"
         self.sock.close()
         return()
      # Check for device availability (poll every second)
      print "Data received"
      printer = None
      while printer == None:
         try:
            printer = os.open(self.printer,os.O_RDWR)
         except OSError, (errno, strerror): # "[Errno 16] Device or resource busy:" - the message we're looking for
            print "Printer busy (%s)..." % strerror
            time.sleep(2)
      # Send data
      print prn_data
      bytes = os.write(printer,prn_data)
      os.close(printer)
      print "%s bytes of data sent to printer" % str(bytes)
      # Notify client that data is sent
      try:
         self.sock.send("DATA SENT TO PRINTER")
      except socket.timeout:
         print "Client timed out - disconnecting"
         self.sock.close()
         return()
      #self.sock.flush()
      self.sock.shutdown(socket.SHUT_RDWR)
      self.sock.close()
      print "Connection closed"

# Configure server
print "CIHSR TCP PRINT SERVER 20 Sep 2006"
#setup command line arguments
parser = OptionParser()
parser.add_option("-P", "--port", dest="PORT",type="int", default=3444, help="Sets the port number [default: %default")
if platform.system() == "Windows":
        print "Using Windows"
        parser.add_option("-D", "--device", dest="DEVICE",type="string",default="LPT1", help="Sets the device file to use for printing [default: %default")
else:
        print "Not using Windows"
        parser.add_option("-D", "--device", dest="DEVICE",type="string",default="/dev/usblp0", help="Sets the device file to use for printing [default: %default")
(options, args) = parser.parse_args()                                                                                                                             
printer = options.DEVICE
print "Printer device is " + printer
printserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
printserver.bind((socket.gethostname(),options.PORT))
printserver.listen(5)
print "Listening on port " + str(options.PORT)
# Loop forever
while 1:
   (clientprint, address) = printserver.accept()
   print "Connection from %s" % str(address)
   printjob = ClientPrint(clientprint, printer)
   printjob.run()
   

   


   
