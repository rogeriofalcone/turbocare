import sys, os, time, socket
from printer_tdp643 import TDP643

receipt = TDP643()
receipt.write_hr_single()
receipt.write_barcode(barcode="00000000000000000035")
receipt.write_line("Wesley Penner")
receipt.write_line("Items purchased on Oct. 10th, 2005")
col_width = [50, 20, 30]
text = ["Item", "Qty", "Total"]
col_just = ['C', 'C', 'C']
receipt.write_colText(text, col_width, col_just, font='3')
receipt.write_hr_double()
col_just = ['L', 'R', 'R']
text = [["Registration", "1", "30.00"],
	["Booklet", "1", "20.00"],
	["Hair cut", "1", "60.00"],
	["Internet", "1", "100.00"],
	["Wesley", "4", "100.00"],
	["====================", "====================", "================"],
	["Total", "Rs.", "310.00"]]
for line in text:
	receipt.write_colText(line, col_width, col_just, font='2')

#Make a server connection
HOST = '192.168.11.9'
PORT = 3444
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send(receipt.write_toPrinter())
#sock.flush()
sock.shutdown(socket.SHUT_WR)
reply = ''
data = sock.recv(1024)
while data != '':
	reply += data
	data = sock.recv(1024)
print 'Completed: ' + reply

#f = open('/home/wesley/devel/care2x/testprint.txt','w')
#f.write(receipt.write_toPrinter())
#f.close()