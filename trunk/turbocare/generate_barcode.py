import sys, os, time, shutil

def convert_ps2png(filename):
	""" convert an existing postscript file to a png.  File name should not have the extension included."""
	cmd_str = "convert "+filename+".ps "+filename+".png"
	cmd = os.popen(cmd_str,'r')
	result = cmd.readlines()
	cmd.close()

def convert_ps2pcx(filename):
	""" convert an existing postscript file to a png.  File name should not have the extension included."""
	cmd_str = "convert "+filename+".ps +dither -colors 2 "+filename+".pcx"
	cmd = os.popen(cmd_str,'r')
	result = cmd.readlines()
	cmd.close()

def barcode_ps(start_num, end_num, destination):
	""" in the destination, generate UPC-A codes for numbers between start_num and end_num"""
	cur_num = start_num
	if destination[len(destination)-1] != '/':
		destination += '/'
	while cur_num <= end_num:
		barcode_num = '00000000000000000000' + str(cur_num)
		barcode_num = barcode_num[len(barcode_num)-20:]
		cmd_str = 'barcode -E -u cm -p 9x2 -g 9x2 +0+0 -e "128c" -o '+destination+barcode_num+'.ps -b "' + barcode_num +'"'
		cmd = os.popen(cmd_str,'r')
		result = cmd.readlines()
		cmd.close()
		cur_num += 1
		convert_ps2png(destination+barcode_num)
		convert_ps2pcx(destination+barcode_num)
		
barcode_ps(1,250,'/home/wesley/devel/care2x/care2x/static/images/barcode/9x2')