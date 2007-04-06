import sys, os, time, shutil
import StringIO
import Image

# COMMANDS not used
# BITMAP
# BOX
# ERASE
# DMATRIX
# MAXICODE
# PDF417
# REVERSE
#

class TDP643:
	""" 	Creates a command file to be sent to the barcode printer 
		using the TSPL command set used in TSC barcode printers.
		mandatory parameters:
		device_name = (string) the device where commands are sent (e.g. /dev/usblp0) - *** Not mandatory anymore
		Optional parameters:
		continuous = (boolean) True if continuous receipts are the target, false if you're using labels
		cutter = (boolean) True if you use a cutter at the end, false otherwise
		width = (float) The width of the paper used (4.0 inches)
		height = (float) the length of the label (used when continuous is false)
		unit = (string) "inch" or "mm"
		encoding = (string) barcode encoding
		label = (string) the type of label format being used (pre-defined)
	"""
	#Initialized variables
	continuous = True
	cutter = False
	width = 4.0
	height = 0.0
	unit = "inch" #other options: mm
	label = 'book'
	count = 1
	copies = 1
	#Calculation variables
	commands = []
	cur_y = 0 #The y-position where the next line should start
	pics = []
	
	fonts = {'1':{'X':10,'Y':12},
		'2':{'X':14,'Y':20},
		'3':{'X':18,'Y':24},
		'4':{'X':26,'Y':32},
		'5':{'X':34,'Y':48},
		'TST24.BF2':{'X':26,'Y':24},
		'TST16.BF2':{'X':18,'Y':16},
		'TTT24.BF2':{'X':26,'Y':24},
		'TSS24.BF2':{'X':26,'Y':24},
		'TSS16.BF2':{'X':18,'Y':16},
		'K':{'X':26,'Y':24},
		'L':{'X':18,'Y':16},
		'KS':{'X':26,'Y':24},
	}
	labels = {'book':{'GAP_WIDTH':0.1, 'GAP_OFFSET':0, 'BLINE_THICK':0, 'BLINE_FEED':0, 'OFFSET':0.5,
				'REFERENCE_X':5, 'REFERENCE_Y':5, 'WIDTH':4, 'HEIGHT':3},
			'tube':{'GAP_WIDTH':0.1, 'GAP_OFFSET':0, 'BLINE_THICK':0, 'BLINE_FEED':0, 'OFFSET':0.5,
				'REFERENCE_X':5, 'REFERENCE_Y':5, 'WIDTH':4, 'HEIGHT':3},
			'box':{'GAP_WIDTH':0.1, 'GAP_OFFSET':0, 'BLINE_THICK':0, 'BLINE_FEED':0, 'OFFSET':0.5,
				'REFERENCE_X':5, 'REFERENCE_Y':5, 'WIDTH':4, 'HEIGHT':3},
			'jetpack':{'GAP_WIDTH':0.1, 'GAP_OFFSET':0, 'BLINE_THICK':0, 'BLINE_FEED':0, 'OFFSET':0.5,
				'REFERENCE_X':5, 'REFERENCE_Y':5, 'WIDTH':4, 'HEIGHT':3}}
				
	def __init__(self, **kw):
		if kw.has_key("continuous"):
			self.continuous = kw["continuous"]
		if kw.has_key("cutter"):
			self.cutter = kw["cutter"]
		if kw.has_key("width"):
			self.width = kw["width"]
		if kw.has_key("height"):
			self.height = kw["height"]
		if kw.has_key("unit"):
			self.unit = kw["unit"]
		if kw.has_key("encoding"):
			self.encoding = kw["encoding"]
		if kw.has_key("label"):
			self.label = kw["label"]
		self.write_start()

	def calc_width(self):
		#approx 200DPI or 8DPmm
		if self.unit == 'inch':
			return 200*self.width
		if self.unit == 'mm':
			return 8*self.width
					
	def append_reset(self):
		#Reset our variables
		self.cur_y = 0
		self.commands = []
		self.pics = []
		#Clear the image buffer
		#self.commands.append("CLS")
		#Move to the next label
		if not self.continuous:
			self.commands.append("HOME")
			
	def append_final(self):
		self.commands.append("PRINT %s, %s" % (str(self.count), str(self.copies)))
		if self.cutter:
			self.commands.append("CUT")

#VARIABLES SET BEFORE MAKING OUR FORM
	def append_SIZE(self):
		if not self.continuous:
			label = self.labels[self.label]
			self.width = label['WIDTH']
			self.height = label['HEIGHT']
			if self.unit == "inch":
				self.commands.append('SIZE %s, %s' % (str(self.width),str(self.height)))
			elif self.unit == "mm":
				self.commands.append('SIZE %s mm, %s mm' % (str(self.width),str(self.height)))
	
	def append_LIMITFEED(self):
		if not self.continuous:
			self.commands.append('LIMITFEED 4')

	def append_GAP(self):
		if self.continuous:
			self.commands.append('GAP 0,0')
		else:
			label = self.labels[self.label]
			if self.unit == 'inch':
				self.commands.append('GAP %s, %s' % (str(label['GAP_WIDTH']),str(label['GAP_OFFSET'])))
			elif self.unit == 'mm':
				self.commands.append('GAP %s mm, %s mm' % (str(label['GAP_WIDTH']),str(label['GAP_OFFSET'])))
				
	def append_BLINE(self):
		label = self.labels[self.label]
		if (not self.continuous) or (label['BLINE_THICK'] > 0):
			if self.unit == 'inch':
				self.commands.append('BLINE %s, %s' % (str(label['BLINE_THICK']),str(label['BLINE_FEED'])))
			elif self.unit == 'mm':
				self.commands.append('BLINE %s mm, %s mm' % (str(label['BLINE_THICK']),str(label['BLINE_FEED'])))
		
	def append_OFFSET(self):
		label = self.labels[self.label]
		if (not self.continuous) or (label['OFFSET'] > 0):
			if self.unit == 'inch':
				self.commands.append('OFFSET %s' % str(label['OFFSET']))
			elif self.unit == 'mm':
				self.commands.append('OFFSET %s mm' % str(label['OFFSET']))
	
	def append_REFERENCE(self):
		label = self.labels[self.label]
		if not self.continuous:
			X = label['REFERENCE_X']
			Y = label['REFERENCE_Y']
		else:
			X = 5
			Y = 5
		self.commands.append('REFERENCE %s, %s' % (str(X), str(Y)))
		
	def append_SPEED(self):
		#currently hardcoded to a single speed of 2
		self.commands.append("SPEED 2.0")

	def append_DENSITY(self):
		#currently hardcoded to a single density of 7
		self.commands.append("DENSITY 7")

	def append_DIRECTION(self):
		#currently hardcoded direction
		self.commands.append("DIRECTION 0")
	
	def append_COUNTRY(self):
		#currently hardcoded
		self.commands.append("COUNTRY 001") #US

	def append_CODEPAGE(self):
		#currently hardcoded
		self.commands.append("CODEPAGE 437") #US English

#THE FOLLOWING COMMANDS EDIT THE FORM
	def append_barcode(self, barcode, height=100, show_num=True, **kw):
		"""We will append a 128 encoded barcode, default format"""
		label = self.labels[self.label]
		Y = self.cur_y
		if self.continuous:
			X = 5
		else:
			X = label['REFERENCE_X']
		self.cur_y += height + 50
		if show_num:
			hr = '1'
		else:
			hr = '0'
		self.commands.append('BARCODE %s, %s, "128", %s, %s, 0, 2, 2, "%s"' % (str(X), str(Y), \
			str(height), hr, barcode))
		
	def append_FEED(self, dots=10):
		self.commands.append("FEED %s" % str(dots))
		self.cur_y += dots
		
	def append_FORMFEED(self):
		self.commands.append("FORMFEED")
		self.cur_y = 0
	
	def append_SOUND(self, beep_count=2):
		i =0
		while i < beep_count:
			i +=1
			self.commands.append('SOUND 5,200')
			
	def append_BAR(self, type='custom', X=1, Y=1, width=1, height=1, line_num=0):
		if type == 'custom':
			self.commands.append('BAR %s, %s, %s, %s' %(str(X), str(Y), str(width), str(height)))
		if type == 'double':
			Y = self.cur_y
			X = 5
			height = 2
			width = self.calc_width()-5
			self.commands.append('BAR %s, %s, %s, %s' %(str(X), str(Y), str(width), str(height)))
			self.commands.append('BAR %s, %s, %s, %s' %(str(X), str(Y+3), str(width), str(height)))
			self.cur_y += 9
		if type == 'single':
			Y = self.cur_y
			X = 5
			height = 1
			width = self.calc_width()-5
			self.commands.append('BAR %s, %s, %s, %s' %(str(X), str(Y), str(width), str(height)))
			self.cur_y += 6
			
	def append_PUTPCX(self, filename, position='LEFT'):
		#search for a loaded picture of the filename.  First match is used
		# position = LEFT | CENTER | RIGHT
		label = self.labels[self.label]
		if self.continuous:
			MINX = 5
		else:
			MINX = label['REFERENCE_X']
		for pic in self.pics:
			if pic['filename'] == filename:
				if (position.upper() == 'LEFT'):
					X = MINX
				elif (position.upper() == 'CENTER'):
					X = int((self.calc_width()-pic['width'])/2)
				else:
					X = int((self.calc_width()-pic['width']))
				self.commands.append('PUTPCX %s, %s, "%s"' % (str(X), str(self.cur_y), filename))
				self.cur_y += pic['height'] + 4
				break
		
	def load_image(self, filename):
		#load a file from the computer and generate the necessary statement to load the picture into
		#the printer memory.  The image needs to be transformed before all this
		(file, ext) = os.path.splitext(os.path.basename(filename))
		file = file[-10:]
		image = Image.open(filename)
		(width, height) = image.size
		#transform the image to fit either width or height
		if (self.calc_width()-2) < width:
			image = image.resize((self.calc_width()-2,int((self.calc_width()-2)/width*height)),Image.BICUBIC)
		if (not self.continuous) and (height > self.height):
			image = image.resize((int(self.height/height*width),self.height),Image.BICUBIC)
		if image.mode != '1':
			image.convert(mode='1')
		if image.format.upper() != 'PCX':
			buf = StringIO.StringIO()
			image.save(buf, 'pcx')
			buf.seek(0)
		else:
			buf = open(filename)
		(width, height) = image.size
		#Get the filename without path and extension
		data = buf.read()
		pic = dict(filename=file+'.pcx',filesize=len(data), command='DOWNLOAD "'+file+'.pcx", '+str(len(data)) + ', ' + data,
			height=height, width=width)
		self.pics.append(pic)
			
	def append_TEXT(self, text='', font='1', multiply=1):
		label = self.labels[self.label]
		if self.continuous:
			X = label['REFERENCE_X']
		else:
			X = 5
		self.commands.append('TEXT %s, %s, "%s", 0, %s, %s, "%s"' % (str(X), str(self.cur_y), font,
			str(multiply), str(multiply), text))
		self.cur_y += self.fonts[font]['Y']*multiply
		
	def append_colText(self, text=[], col_width=[], col_just=[], col_buffer=1, font='1', multiply=1):
		"""	text = ["column 1 text", "column 2 text", "column 3 text"]
			col_width = [50, 20, 30] * these are % of the total width of the paper
			col_just = ["L", "C", "R"] * text justification, Left, Center, Right
			NOTE: The script does not verify column width %
			The buffer is added to the right of a column, except the final column
		"""
		label = self.labels[self.label]
		cols = len(text) # number of columns to format for.  Good for receipts....
		if not self.continuous:
			right_margin = label['REFERENCE_X']
		else:
			right_margin = 5
		char_cols = int(float((self.calc_width()-right_margin))/float((self.fonts[font]['X']*multiply))) #the number of characters that can fit across the paper
		line_text = ''
		cur_col = 1
		for line, pct, just in zip(text, col_width, col_just):
			#only the last column doesn't have a buffer to the right, otherwise, we need a buffer to the right
			if cur_col == cols:
				buffer = 0
			else:
				buffer = col_buffer
			cur_col += 1
			#Calculate the num of character columns we have
			num_chars = int(float(pct)/100*float(char_cols)) - buffer
			if len(line) > num_chars:
				line_text += line[0:num_chars] + ' '*buffer
			else:
				if just.upper() == 'L':
					line_text += line.ljust(num_chars) + ' '*buffer
				elif just.upper() == 'C':
					line_text += line.center(num_chars) + ' '*buffer
				else:
					line_text += line.rjust(num_chars) + ' '*buffer
		self.append_TEXT(line_text, font, multiply)
	
	#FUNCTIONS intended for regular use
	def write_start(self):
		self.append_reset()
		self.append_SIZE()
		self.append_LIMITFEED()
		self.append_GAP()
		self.append_BLINE()
		self.append_OFFSET()
		self.append_REFERENCE()
		self.append_SPEED()
		self.append_DENSITY()
		self.append_DIRECTION()
		self.append_COUNTRY()
		self.append_CODEPAGE()
		
	def write_line(self, text, font='1', multiply=1):
		self.append_TEXT(text, font, multiply)
		
	def write_pic(self, filename, position='LEFT'):
		(file, ext) = os.path.splitext(os.path.basename(filename))
		file = file[-10:]
		self.load_image(filename)
		self.append_PUTPCX(file+".pcx", position)
		
	def write_barcode(self, barcode, height=100, show_num=True):
		self.append_barcode(barcode, height, show_num)
		
	def write_hr_single(self):
		self.append_BAR(type='single')

	def write_hr_double(self):
		self.append_BAR(type='double')

	def write_colText(self, text=[], col_width=[], col_just=[], col_buffer=1, font='1', multiply=1):
		self.append_colText(text, col_width, col_just, col_buffer, font, multiply)
		
	def write_toPrinter(self):
		label = self.labels[self.label]
		self.append_final()
		output = StringIO.StringIO()
		#append picture information to our file first.
		output.write("CLS\n")
		output.write('Kill "*.PCX"\n')
		for pic in self.pics:
			output.write(pic['command'] + '\n')
		#prepend a size command if the paper is continuous (if it's a label, it'll already have a size command)
		if self.continuous:
			width = self.width
			if self.unit == 'inch':
				height = float(self.cur_y )/200.0
				output.write('SIZE %s, %s \n' % (str(width),str(height)))
			elif self.unit == 'mm':
				height = float(self.cur_y )/8.0
				output.write('SIZE %s mm, %s mm \n' % (str(width),str(height)))
		#append our commands
		for command in self.commands:
			output.write(command+'\n')
		#reset the pointer
		output.seek(0)
		return output.read()
		
		