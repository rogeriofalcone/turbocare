import sys, os, time, shutil, threading, socket

def get_printer(device='/dev/usblp0'):
	return os.open(device,os.O_RDWR+os.O_APPEND)
	
def print_data(printer, data):
	os.write(printer,data)
	
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
		data = self.sock.recv(1024)
		while data != '':
			prn_data += data
			data = self.sock.recv(1024)
		# Check for device availability (poll every second)
		print "Data received"
		printer = None
		while printer == None:
			try:
				printer = os.open(self.printer,os.O_RDWR+os.O_APPEND)
			except OSError, (errno, strerror): # "[Errno 16] Device or resource busy:" - the message we're looking for
				print "Printer busy (%s)..." % strerror
				time.sleep(2)
		# Send data
		bytes = os.write(printer,prn_data)
		os.close(printer)
		print "%s bytes of data sent to printer" % str(bytes)
		# Notify client that data is sent
		self.sock.send("DATA SENT TO PRINTER")
		#self.sock.flush()
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()
		print "Connection closed"

# Configure server
printer = '/dev/usblp0'
printserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
printserver.bind((socket.gethostname(),3444))
printserver.listen(5)
# Loop forever
while 1:
	(clientprint, address) = printserver.accept()
	print "Connection from %s" % str(address)
	printjob = ClientPrint(clientprint, printer)
	printjob.run()
	

	


	