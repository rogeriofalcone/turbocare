from printer_tdp643 import TDP643

receipt = TDP643()
receipt.write_hr_double()
receipt.write_line("BARCODE TEST")
path = '/home/wesley/devel/care2x/care2x/static/images/barcode/9x2/'
for i in range(1,5):
	barcode = '00000000000000000000' + str(i)
	barcode = barcode[-20:]
	receipt.write_barcode(barcode=barcode)
	receipt.write_pic(path+barcode+'.pcx','CENTER')
receipt.write_hr_double()

f = open('/home/wesley/devel/care2x/testprint.txt','w')
f.write(receipt.write_toPrinter())
f.close()