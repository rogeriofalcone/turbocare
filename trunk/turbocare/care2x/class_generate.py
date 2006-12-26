from sqlobject import *

from turbogears import identity 
from turbogears.database import PackageHub
import sidewalk

class GenerateError(Exception):
	"""Base class for generate errors"""
	pass
	
class Generate:
	
	db_model = None
	table_list = []
	db_table_list = []
	model_table_list = []
	model_class_list = []
	conn = None
	
	def getConnection(self):
		if self.db_model == None:
			raise GenerateError, "Database model is not defined"
		if self.conn == None:
			tables = dir(self.db_model)
			for table in tables:
				if table in ('SQLObject','InheritableSQLObject'):
					pass
				else:
					c = getattr(self.db_model,table)
					if isinstance(c, type) and issubclass(c,SQLObject):
						self.model_table_list.append(c.sqlmeta.table)
						self.model_class_list.append(table)
			if len(self.model_class_list) > 0:
				c = getattr(self.db_model,self.model_class_list[0])
				self.conn = c._connection
			else:
				raise GenerateError, "No tables found in model"
			
	def getTables(self):
		""" Get a list of all the tables in the database and remove
			any tables already existing in the model form our list"""
		if self.conn == None:
			raise GenerateError, "No database connection found"
		else:
			sql = "show tables from care2x"
			tables = self.conn.queryAll(sql)
			self.db_table_list = []
			for table in tables:
				self.db_table_list.append(table[0])
		self.table_list = set(self.db_table_list) - set(self.model_table_list)
		return self.table_list
		
	def getCols(self,table_name):
		""" Return a list of tuples of all the columns in the database for the table and their definition """
		if self.conn == None:
			raise GenerateError, "No database connection found"
		else:
			sql = "show columns from care2x."+table_name
			columns = self.conn.queryAll(sql)
		return columns
		
	def getFunctions(self):
		return """
	def _set_ModifyId(self, value):
		value = cur_user_id()
		self._SO_set_ModifyId(value)	

	def _set_ModifyTime(self, value):
		value = cur_date_time()
		self._SO_set_ModifyTime(value)

	def _set_CreateId(self, value):
		try:
			if self.CreateId == '':
				value = cur_user_id()
			else:
				value = self.CreateId
		except AttributeError:
			value = cur_user_id()
		self._SO_set_CreateId(value)

	def _set_CreateTime(self, value):
		try:
			if self.CreateTime == '':
				value = cur_date_time()
			else:
				value = self.CreateTime
		except AttributeError:
			value = cur_date_time()
		self._SO_set_CreateTime(value)

"""

	def getColString(self,colName, colDef):
		"""Returns a string of the column definition for the model"""
		strCol = ''
		i = 0
		j = 0
		while j < len(colName):
			i = j
			j = colName.find('_',i)
			if j < 0:
				j = len(colName)
			strCol += colName[i:j].capitalize()
			j += 1
		if colDef[0:7] == 'varchar':
			length = colDef[8:colDef.find(')',8)]
			strDef = ' = StringCol(length=' + length + ',dbName="'+colName+'")'
		elif colDef[0:4] == 'char':
			length = colDef[5:colDef.find(')',5)]
			strDef = ' = StringCol(length=' + length + ',dbName="'+colName+'")'
		elif (colDef == 'text') or (colDef == 'tinytext') or (colDef == 'longtext'):
			strDef = ' = StringCol(length=255,dbName="'+colName+'")'
		elif colDef == 'time':
			strDef = ' = StringCol(default=str(cur_date_time()).rjust(8),length=8,dbName="'+colName+'")'
		elif colDef.find('year') >= 0:
			strDef = ' = StringCol(default=str(cur_date_time()).ljust(4),length=4,dbName="'+colName+'")'
		elif (colDef.find('int(1)') >= 0):
			strDef = ' = BoolCol(dbName="'+colName+'")'
		elif colDef.find('int(') >= 0:
			strDef = ' = IntCol(dbName="'+colName+'")'
		elif (colDef[0:8] == 'datetime') or (colDef[0:9] == 'timestamp') or (colDef[0:4] == 'date'):
			strDef = ' = DateTimeCol(default=cur_date_time(),dbName="'+colName+'")'
		elif (colDef[0:5] == 'float') or (colDef.find('double') >= 0):
			strDef = ' = FloatCol(dbName="'+colName+'")'
		elif (colDef[0:4] == 'blob'):
			strDef = ' = BLOBCol(default="",dbName="'+colName+'")'
		else:
			strDef = ' = ?? ' + colDef
		return "	" + strCol + strDef + "\n"
		
	def getIdCol(self,columns):
		pri_count = 0
		pri_col = ''
		for col in columns:
			if col[3] == 'PRI':
				pri_count += 1
				pri_col += col[0]
		if pri_count == 1:
			return pri_col
		else:
			return '??'
		
	def generateText(self,model_name, tables = [], **kw):
		self.db_model = model_name
		self.getConnection()
		output = ''
		if tables == []:
			tables = self.getTables()
		for table in tables:
			className = ''
			i = 0
			j = table.find('_',i) + 1 #remove the "care_" text
			while j < len(table):
				i = j
				j = table.find('_',i)
				if j < 0:
					j = len(table)
				className += table[i:j].capitalize()
				j += 1
			output += "class "+className+"(SQLObject):\n"
			output +=  "	class sqlmeta:\n"
			output +=  "		table = '"+table+"'\n"
			columns = self.getCols(table)
			pri_id = self.getIdCol(columns)
			output += "		idName = '"+ pri_id +"'\n"
			output +=  self.getFunctions()
			for col in columns:
				if col[0] != pri_id:
					output += self.getColString(col[0],col[1])
			output +=  "\n"
		return output
			

