#
#	mytable.py
#
#	A dictionary key with array columns for the table
#
#	Sorting features
#	Grouping features
#

class MyTable:
	'''	MyTable class 
		I use this to group and sort data for my reporting
	'''
	data = None 		# Original data rows.  A list of lists
					# If grouping is done, the primary key column becomes a list of primary
					# key values contained in the group (needed for counting and average)
	gData = None 	# If the data is grouped, then gData is set.  It is a Dictionary of lists.
	gTypeCol = {		# A dictionary of lists indicating what grouping
		'GroupBy':[],	# operation happens on the associated list
		'Sum':[],		# The lists are column numbers
		'Minimum':[],
		'Maximum':[],
		'First':[],
		'Last':[],
		'Count':[],
		'Normal':[],
		'None':[]}
	pk = -1			# The column designated as primary key (index number)
	sCols = None		# A list of dictionaries, in order of sort indicating "col" number and 
					# "sort" type (Ascending/Descending)
	_gColType = {}	# A dictionary of column numbers and their grouping type
					# This is calculated from the gTypeCol
	_keys = []		# A list of key values
	
	
	def AddRow(self, row):
		'''	Add a row of data.  Use this when initializing a the data 
			If you add a row after grouping, you'll need to group again
		'''
		self.data.append(row)
	
	def MakegColType(self):
		'''	make our _gColType variable from gTypeCol 
			it's just an inverse dictionary
		'''
		for grp in gTypeCol:
			for col in gTypeCol[grp]:
				self._gColType[col] = grp
	
	def GroupData(self):
		'''	Group the data
			Make sure that the gGrpType variable is properly set
			If it isn't, then the grouping will use the primary key field as the key
			During the process of grouping, an additional column is added
			which is a list of primary keys included in the group
		'''
		# Make two short cut variables
		GBcols = self.gTypeCol['GroupBy']
		GB = self.gData
		# Generate our column to type dictionary
		self.MakegColType()
		if len(GBcols) > 0 and (len(self.data)>0) and not (len(GBcols)>=len(self.data[0])):
			for row in data:
				# The key for our dictionary is a comma list of column values
				key = reduce(lambda x,y: "%s,%s" % (x,y), [row[col] for col in GBcols])
				if not GB.has_key(key): # If the key doesn't exist, create a new row
					GB[key] = row
					self._keys.append(key)
				else:
					# Make sure that the primary key field is a list
					if isinstance(GB[key][self.pk], list):
						GB[key][self.pk].append(row[self.pk])
					else:
						GB[key][self.pk] = list([GB[key][self.pk]] + [row[self.pk]])
					# Merge the row with the rest of the group
					for col in range(len(row[0])):
						if not (col in GBcols):
							self.MergeColumn(col, key, row[col])
			# Sort the keys and then place our results into the GroupedResults list
			self._keys.sort()
			# Figure out the count for count columns and the Average for average columns
			for row in GroupedResults:
				for col,num in zip(ShowCols,range(len(ShowCols))):
					ColAggType = self.GetCD(TD,col)['Aggregate']
					if ColAggType == 'Average':
						row[num] = float(row[num])/len(row[-1])
					elif ColAggType == 'Count':
						row[num] = len(row[-1])
			# Calculate totals for Averages (total averages), Sums and counts
			Totals = [0]+[0]*len(ShowCols) # An extra one to store the total count
			for row in GroupedResults:
				for col,num in zip(ShowCols,range(len(ShowCols))):
					ColAggType = self.GetCD(TD,col)['Aggregate']
					if ColAggType == 'Average':
						Totals[num] = float(row[num])*len(row[-1])
					elif ColAggType == 'Count':
						row[num] = len(row[-1])
					elif ColAggType == 'Sum':
						row[num] = float(row[num])
				Totals[-1] += len(row[-1])
			for col,num in zip(ShowCols,range(len(ShowCols))):
				ColAggType = self.GetCD(TD,col)['Aggregate']
				if ColAggType == 'Average':
					Totals[num] = float(Totals[num])/len(Totals[-1])
			GroupedResults.append(Totals)
		else: # return our results as the list of lists (no grouping, summing in this case)
			for row in Results:
				cols = []
				for col in ShowCols: # Go through the columns we're showing
					cols.append(eval("row.%s" % col))
				cols.append(row.id) # always append the row id
				GroupedResults.append(cols)
			# Calculate the totals for numeric columns
			Totals = [0]+[0]*len(ShowCols) # An extra one to store the total count
			for row in GroupedResults:
				for col,num in zip(ShowCols,range(len(ShowCols))):
					ColType = self.GetCD(TD,col)['ColType']
					if ColType == 'Numeric':
						Totals[num] += row[num]
				Totals[-1] += 1
			GroupedResults.append(Totals)			
		return GroupedResults	
		
	def MergeColumn(self, col, key, newdata):
		'''	Merge the newdata to the grouped data which 
			already exists
		'''
		type = self._gColType[col]
		if (type in ['Sum','Average']) and (isinstance(newdata, (int, float))):
			self.gData[key] += newdata
		elif (type in ['Sum','Average']) and not (isinstance(newdata, (int, float))):
			return 0
		elif (type == 'Minimum'):
			if self.gData[key] < newdata:
				return D1
			else:
				return D2
		elif (type == 'Maximum'):
			if D1 > D2:
				return D1
			else:
				return D2
		elif (type in ['First','Count']):
			return D1
		elif (type in ['Normal','Last', 'None']):
			return D2
