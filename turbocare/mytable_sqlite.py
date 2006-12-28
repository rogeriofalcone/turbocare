#
#	mytable.py
#
#	Sort and group my report data using sqlite
#
#	Created a custom aggregate for sqlite
#
#
from pysqlite2 import dbapi2 as sqlite
from datetime import datetime
import logging

log = logging.getLogger("care2x.controllers")	

class MyMerge:
	def __init__(self):
		self.merge = ''
		
	def step(self, value):
		if value != None:
			str = '%r' % value
			if self.merge == '':
				self.merge = str
			else:
				self.merge = '%s,%s' % (self.merge, str)
		
	def finalize(self):
		return self.merge
		
class MyFirst:
	def __init__(self):
		self.val = None
		
	def step(self, value):
		if self.val == None:
			self.val = value
		
	def finalize(self):
		return self.val
		
class MyLast:
	def __init__(self):
		self.val = None
		
	def step(self, value):
		self.val = value
			
	def finalize(self):
		return self.val

class MyTable:
	'''	MyTable class 
		I use this to group and sort data for my reporting
	'''
	data = []	 		# Final result data (a list of lists)
	Totals = []		# This is a totals row which is calculated after grouping is done
	pk = -1			# The column designated as primary key (index number)
	sCols = []			# A list indicating the type of sorting on each column: asc, dec, none
	gCols = []		# A list indicating the type of aggregate on each column: GroupBy, Sum
					# Average, Minimum, Maximum, First, Last, Count, Normal
	tCols = []			# A list indicating the data type of the column: Numeric, DateTime, Boolean, Text
	_keys = []		# A list of key values
	_con = None		# SQLite3 database connection
	_cur = None		# my cursor
	_INSERT = ''		# The Insert statement
	
	def __init__(self, TypeCols=[], GroupingCols=[], SortingCols=[], pkcol=-1, hidden=False):
		'''	TypeCols: list of column types: Numeric, DateTime, Boolean, Text
			GroupingCols: This will be assigned to self.gTypeCol (needs to be the same structure)
			SortingCols: Will be assigned to self.sCols, so it needs to be the same dataype
			pkcol: the column number which has a primary key (-1 for the last column)
			hidden: If the row is to be hidden in the end results, then we'll perform grouping
				on all the data regardless of the grouping settings.
		'''
		self.data = []
		self.Totals = []
		self.count = len(TypeCols)
		self.hidden = hidden 
		# Create our database
		self._con = sqlite.connect(":memory:")
		# Attach our custom aggregates
		self._con.create_aggregate("mymerge", 1, MyMerge)
		self._con.create_aggregate("myfirst", 1, MyFirst)
		self._con.create_aggregate("mylast", 1, MyLast)
		# Create our temp table
		CreateSQL = 'CREATE TABLE homer ('
		for coltype,num in zip(TypeCols,range(self.count)):
			if coltype == 'Numeric':
				CreateSQL += 'c%d REAL,' % num
			elif coltype in ['DateTime','Text']:
				CreateSQL += 'c%d TEXT,' % num
			elif coltype in ['Boolean','Integer']:
				CreateSQL += 'c%d INTEGER,'	% num			
		CreateSQL = CreateSQL[:-1] + ')'
		self._cur = self._con.cursor()
		self._cur.execute(CreateSQL)
		self._con.commit()
		# Create our INSERT statement
		self._INSERT = 'INSERT INTO homer ('
		for num in range(self.count):
			self._INSERT += 'c%d,' % num
		self._INSERT = self._INSERT[:-1] + ') VALUES ('
		self._INSERT += '?,'*self.count
		self._INSERT = self._INSERT[:-1] + ")"
		# Assign other important variables
		if pkcol < 0:
			self.pk = self.count + pkcol
		else:
			self.pk = pkcol
		self.gCols = GroupingCols
		self.sCols = SortingCols
		self.tCols = TypeCols
	
	def AddRow(self, row):
		'''	Add a row of data.  Use this when initializing a the data 
			If you add a row after grouping, you'll need to group again
		'''
		# Create a tuple from our row
		t = tuple(row)
		self._cur.execute(self._INSERT,t)
		self._con.commit()
		
	
	def Compute(self):
		'''	Calculate the groupings, aggregates, sortings and totals '''
		# Create our group by statement
		GroupBy = ''
		if not self.hidden:
			for type,num in zip(self.gCols,range(self.count)):
				if type == 'GroupBy':
					GroupBy += 'c%d,' % num
			GroupBy = GroupBy[:-1]
		# Create our order by statement
		OrderBy = ''
		if not self.hidden:
			for type,num in zip(self.sCols,range(self.count)):
				if type == 'Ascending':
					OrderBy += 'c%d,' % num
				elif type == 'Descending':
					OrderBy += 'c%d DESC,' % num
			OrderBy = OrderBy[:-1]
		# Create our column row
		# GroupBy, Sum, Average, Minimum, Maximum, First, Last, Count, Normal
		Columns = ''
		if self.hidden: # Process the table as one row
			for type,num in zip(self.gCols,range(self.count)):
				Columns += 'mylast(c%d),' % num
			Columns += 'mymerge(c%d)' % self.pk
		elif len(GroupBy) > 0:
			for type,num in zip(self.gCols,range(self.count)):
				if type == 'GroupBy':
					Columns += 'c%d,' % num
				elif type == 'Sum':
					Columns += 'sum(c%d),' % num
				elif type == 'Average':
					Columns += 'avg(c%d),' % num
				elif type == 'Minimum':
					Columns += 'min(c%d),' % num
				elif type == 'Maximum':
					Columns += 'max(c%d),' % num
				elif type == 'First':
					Columns += 'myfirst(c%d),' % num
				elif type in ['Last','Normal']:
					Columns += 'mylast(c%d),' % num
				elif type == 'Count':
					Columns += 'count(c%d),' % num
				else:
					Columns += 'count(c%d),' % num
			Columns += 'mymerge(c%d)' % self.pk
		else:
			for num in range(self.count):
				Columns += 'c%d,' % num
			Columns += 'c%d' % self.pk
		# Create our SQL statement
		DataSQL = 'SELECT %s FROM homer ' % Columns
		if len(GroupBy) > 0:
			DataSQL += 'GROUP BY %s ' % GroupBy
		if len(OrderBy) > 0:
			DataSQL += 'ORDER BY %s ' % OrderBy
		# Create our Totals/Avg/Count SQL
		TotalCols = ''
		for type, num in zip(self.tCols,range(self.count)):
			# Totals and averages only work for numeric columns.  Other columns will do a count
			if type == 'Numeric':
				# If the grouping type of the column is average, then use average, otherwise use sum
				if self.gCols[num] == 'Average':
					TotalCols += 'avg(c%d),' % num
				else:
					TotalCols += 'sum(c%d),' % num
			else:
				TotalCols += 'count(c%d),' % num
		TotalCols = TotalCols[:-1]
		TotalSQL = 'SELECT %s FROM homer' % TotalCols
		#f = open('/home/wesley/devel/care2x/data_mytable.py','a')
		#f.write('======%s======\n' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		#f.write('GroupingCols: %r\n' % self.gCols)
		#f.write('SortingCols: %r\n' % self.sCols)
		#f.write('TypeCols: %r\n' % self.tCols)
		#f.write('DATASQL: \n%s\n' % DataSQL)
		# Run our data sql
		self._cur.execute(DataSQL)
		for row in self._cur:
			#log.debug('my merge: %r' % type(row[-1]))
			if isinstance(row[-1], basestring):
				lrow = list(row[:-1]) + [list([int(x) for x in row[-1].split(',')])]
			else:
				lrow = list(row[:-1]) + [list([row[-1]])]
		#	f.write('%r\n' % lrow)
			self.data.append(lrow)
		# Run our total sql
		#f.write('TotalSQL: \n%s\n' % TotalSQL)
		self._cur.execute(TotalSQL)
		for row in self._cur:
			self.Totals = list(row)
		#	f.write('%r\n' % self.Totals)
			break
		#f.close()
			
	def Close(self):
		'''	Clean up some of my data '''
		self._con.close()
		try:
			del(self.data)
		except:
			pass
		try:
			del(self.Totals)
		except:
			pass
		try:
			del(self.sCols)
		except:
			pass
		try:
			del(self.gCols)
		except:
			pass
		try:
			del(self.tCols)
		except:
			pass
		try:
			del(self._keys)
		except:
			pass
		try:
			del(self._con)
		except:
			pass
		try:
			del(self._cur)
		except:
			pass
		try:
			del(self._INSERT)
		except:
			pass
		

