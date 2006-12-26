from model import *

class Temp:
	def tfunc(self):
		pass

def listing(table):
	if not isinstance(table, str):
		table = table.__name__
		print table
	for col in dir(eval(table)):
		try:
			if isinstance(eval("%s.%s" % (table,col)), property):
				print "property: %s" % col
			elif isinstance(eval("%s.%s" % (table,col)), type(Temp.tfunc)) and (col[0]!='_') and (not col[0].islower()):
				print "function: %s" % col
		except:
			raise
			print "Error: %s" % col
