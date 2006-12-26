"""	Manage MySQL schema changes and updates
	Designed for MySQL version 5
	Tested on MySQL version 5.0.22

	1. A pickle file, which contains a pre-defined db structure, is loaded
	2. All defined indexes and keys are dropped
	3. The script compares the currently connected database tables with the definition and:
		a) When a table is missing, it adds it
		b) When fields in a known table are missing, they are appended
		c) When known fields are found with different definitions, they are updated (hopefully without error).  Columns are matched based on position in the table.
		d) Defined indexes and keys are dropped and remade (at the very end)
	4. All the views:
		a) If the view exists, it will be dropped, then recreated
		b) If the view doesn't exist, it will be created
	5. All stored procedures:
		a) If the stored procedure exists, it is dropped and recreated
		b) If the stored procedure doesn't exist, it is created
	6. All defined triggers are dropped and recreated (or created if new)
	7. All indexes and keys are re-applied
	8. The defined data is appended or updated
	
	Missing features:
	1. Doesn't maintain foreign key constraint information
	2. Indexes isn't fully supported
	
	WARNING:
	USING THIS CLASS IS VERY DANGEROUS!!!
	When trying to synchronize schemas to a specific definition it is assumed that:
	1. No modifications to the schema happen apart from your knowledge
	2. When columns are deleted from a table, no columns are appended (and vice-versa)
	3. All new columns are appended to the end (necessary in most situations)
	4. The behaviour of MySQL at the destination (where changes are applied) is the same as your source when it comes to schema modifications
"""

import sys, os, time, pickle, datetime, MySQLdb
from optparse import OptionParser

class MySQLSchema:
	dbname = ''
	conn = None
	tables = [] #Table defs, columns, indexes (custom definition and some sql text)
	views = [] # View definitions (SQL text)
	sp = [] #Stored procedure AND function definitions (SQL text)
	triggers = [] #Trigger definitions (sql text)
	data = [] #data lines by table.  Not a db unload/reload
	
	def __init__(self, dbname='mysql', user='root', passwd='', host='localhost', port='3306'):
		self.dbname = dbname
		self.conn = MySQLdb.connect(db=dbname, user=user, passwd=passwd, host=host, port=int(port))
	
	# Major functions
	def restore_data(self, filename):
		try:
			f = open(filename) #make sure the file exists
			f.close()
			self.delete_all_data()
			self.restore_from_backup(filename)
		except:
			raise
			
	def backup_data(self, filename):
		try:
			self.backup_tables(filename)
		except:
			raise
			
	def schema_update(self, filename):
		try:
			self.load_from_file(filename)
		except:
			raise
			
	def schema_save(self, filename):
		try:
			self.save_to_file(filename)
		except:
			raise
		
	def load_from_file(self, filename):
		f = open(filename)
		db = pickle.load(f)
		f.close()
		self.tables = db['tables']
		self.views = db['views']
		self.sp = db['sp']
		self.triggers = db['triggers']
		self.apply_table_definitions()
		self.apply_view_definitions()
		self.apply_trigger_definitions()
		self.apply_sp_definitions()
		
	def save_to_file(self, filename):
		self.make_table_definitions()
		self.make_view_definitions()
		self.make_stored_procedure_definitions()
		self.make_trigger_definitions()
		db = {}
		db['tables'] = self.tables
		db['views'] = self.views
		db['sp'] = self.sp
		db['triggers'] = self.triggers
		f = open(filename,'w')
		pickle.dump(db,f)
		f.close()
		
	def reset(self):
		tables = []
		views = []
		sp = []
		triggers = []
		data = []
		
	# Internal processing functions
	def delete_all_data(self):
		qry = self.conn.cursor()
		qry.execute(self.sql_table_names())
		tables = [x[0] for x in qry.fetchall()]
		qry.execute(self.sql_flush_lock_tables())
		for table in tables:
			self.sql_truncate_table(table)
		qry.execute(self.sql_unlock_tables())
		qry.close()
		
	def restore_from_backup(self, filename):
		f = open(filename)
		qry = self.conn.cursor()
		qry.execute(f.read())
		qry.close()
		f.close()
	
	def backup_tables(self, filename):
		qry = self.conn.cursor()
		qry.execute(self.sql_table_names())
		f = open(filename, 'w')
		f.write("-- Backup taken by python script on %s \n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		f.write(self.sql_flush_lock_tables() + ";\n")
		tables = [x[0] for x in qry.fetchall()]
		qry.execute(self.sql_flush_lock_tables())
		for table in tables:
			self.write_table_data(table, f)
		qry.execute(self.sql_unlock_tables())
		f.write(self.sql_unlock_tables()+";\n")
		f.close()
		qry.close()
		
	def write_table_data(self, table, f):
		#appends the sql to the file 'f' for the table 'table'
		qry = self.conn.cursor()
		qry.execute("select * from " + table)
		if qry.rowcount > 0:
			col_names = reduce(lambda x, y: x+', '+y, [x[0] for x in qry.description]) #Comma separated column names
			f.write("INSERT INTO %s (%s) VALUES (\n" % (table, col_names))
			row = qry.fetchone()
			while row != None:
				val = ''
				for col in row:
					if col == None:
						val += "Null, "
					elif isinstance(col, (datetime.datetime, datetime.date)):
						if col.year < 1900: #Don't know if this is good or not, maybe I'll figure out what to do later.
							val += "Null, "
						else:
							val += "'"+col.strftime('%Y-%m-%d') + "', "
					elif isinstance(col, (long, int, float)):
						val += str(col) + ', '
					elif isinstance(col, str):
						val += "'%s', " % MySQLdb._mysql.escape_string(col)
					else:
						val += "'%s', " % str(col)
				f.write("(%s)" % val[:-2])
				row = qry.fetchone()
				if row != None:
					f.write(',\n')
				else:
					f.write(');\n\n')
		qry.close()

	def make_table_def(self, table):
		fields = []
		index_list = []
		sql = ''
		#Get all the column definitions: 
		#Get all indexes (including primary keys)
		#Get create statement
		qry = self.conn.cursor()
		qry.execute(self.sql_column_names(table))
		cols = qry.fetchall()
		for col in cols:
			fields.append(dict([(x[1], x[0]) for x in zip(col, map(lambda x: x[0], qry.description))]))
		qry.execute(self.sql_index_names(table))
		indexes = qry.fetchall()
		for index in indexes:
			index_list.append(dict([(x[1], x[0]) for x in zip(index, map(lambda x: x[0], qry.description))]))
		qry.execute(self.sql_create_table(table))
		stmts = qry.fetchall()
		stmt = stmts[0] #should only be one line
		sql = dict([(x[1], x[0]) for x in zip(stmt, map(lambda x: x[0], qry.description))])['Create Table']
		qry.close()
		return dict(name=table, fields=fields, indexes=index_list, sql=sql)

	def make_table_definitions(self):
		qry = self.conn.cursor()
		table_list = []
		qry.execute(self.sql_table_names())
		res = qry.fetchall()
		for rec in res:
			table_list.append(rec[0])
			#table_list.append(dict([(x[1], x[0]) for x in zip(rec, map(lambda x: x[0], qry.description))])['Name'])
		for table in table_list:
			self.tables.append(dict(name=table,defn=self.make_table_def(table)))
		qry.close()
	
	def make_view_definitions(self):
		qry = self.conn.cursor()
		qry.execute(self.sql_view_names())
		views = qry.fetchall()
		for view in views:
			self.views.append(dict(Name=view[0], sql=self.sql_create_view(view[0])[1]))
		qry.close()
		
	def make_stored_procedure_definitions(self):
		functions = []
		procedures = []
		#Get functions
		qry = self.conn.cursor()
		qry.execute(self.sql_function_names())
		res = qry.fetchall()
		for rec in res:
			functions.append(dict([(x[1], x[0]) for x in zip(rec, map(lambda x: x[0], qry.description))])['Name'])
		#get procedures
		qry.execute(self.sql_procedure_names())
		res = qry.fetchall()
		for rec in res:
			procedures.append(dict([(x[1], x[0]) for x in zip(rec, map(lambda x: x[0], qry.description))])['Name'])
		#Get function definitions
		for function in functions:
			qry.execute(self.sql_create_function(function))
			res = qry.fetchall()
			sql = dict([(x[1], x[0]) for x in zip(res[0], map(lambda x: x[0], qry.description))])['Create Function']
			self.sp.append(dict(name=function,sql=sql))
		for procedure in procedures:
			qry.execute(self.sql_create_procedure(procedure))
			res = qry.fetchall()
			sql = dict([(x[1], x[0]) for x in zip(res[0], map(lambda x: x[0], qry.description))])['Create Procedure']
			self.sp.append(dict(name=procedure,sql=sql))
		qry.close()
		
	def make_trigger_definitions(self):
		qry = self.conn.cursor()
		qry.execute(self.sql_trigger_names())
		res = qry.fetchall()
		for rec in res:
			trigger = dict([(x[1], x[0]) for x in zip(rec, map(lambda x: x[0], qry.description))])
			self.triggers.append(dict(name=trigger['Name'],sql=self.sql_exe_add_trigger_dict(trigger)))
		qry.close()
			
	def apply_trigger_definitions(self):
		qry = self.conn.cursor()
		qry.execute(self.sql_trigger_names())
		res = qry.fetchall()
		db_triggers = []
		#Get a list of current triggers
		for rec in res:
			db_triggers.append(dict([(x[1], x[0]) for x in zip(rec, map(lambda x: x[0], qry.description))])['Name'])
		#Drop all triggers which are both in the current db and reference schema
		for trigger in self.triggers:
			if db_triggers.find(trigger['name']) > -1:
				qry.execute(self.sql_exe_drop_trigger(trigger['name']))
		#Create all triggers in the reference schema
		for trigger in self.triggers:
			qry.execute(self.trigger['sql'])
		qry.close()
		
	def apply_view_definitions(self):
		qry = self.conn.cursor()
		qry.execute(self.sql_view_names())
		res = qry.fetchall()
		#Get a listing of all current views
		for rec in res:
			db_views.append(rec[0])
		#Drop all views common both in the current db and the reference
		for view in self.views:
			if db_views.find(view['name']) > -1:
				qry.execute(self.sql_exe_drop_view(view['name']))
		#Create all the views
		for view in self.views:
			qry.execute(view['sql'])
		qry.close()
		
	def apply_sp_definitions(self):
		qry = self.conn.cursor()
		#Drop all stored procedures and functions which we define (using the error free drop syntax)
		for ProcFunc in self.sp:
			qry.execute(self.sql_exe_drop_procedure(ProcFunc['name']))
			qry.execute(self.sql_exe_drop_function(ProcFunc['name']))
		for ProcFunc in self.sp:
			qry.execute(ProcFunc['sql'])
		qry.close()
		
	def apply_table_definitions(self):
		#Tables to create
		#Tables to update
		db_tables = []
		qry = self.conn.cursor()
		qry.execute(self.sql_table_names())
		res = qry.fetchall()
		for rec in res:
			db_tables.append(rec[0])
		dfn_tables = [x['name'] for x in self.tables]
		updt_tables = set(db_tables) & set(dfn_tables) #Tables both in the definition and the current db
		create_tables = set(dfn_tables) - set(db_tables) #Tables in the definition but not in the current db
		for table in create_tables:
			qry.execute(self.tables[table]['defn']['sql'])
		for table in updt_tables:
			self.update_table_def(table)
		qry.close()
		
	def update_table_def(self, tablename):
		#The 'db_' prefix is for variables referencing the current database (which we're updating) while "dfn_" prefixes our reference definition which we want to update to
		qry = self.conn.cursor()
		db_table = self.make_table_def(tablename)
		dfn_table = list(self.table[tablename]['defn'])#create a local copy
		#Drop all keys and indexes
		for index in db_table['indexes']:
			qry.execute(self.sql_exe_drop_index(tablename, index['Key_name']))
		#create a dictionary of column names to field number
		dfn_col_map = dict([(x[0]['Field'], x[1]) for x in zip(dfn_table['fields'],range(0,len(dfn_table['fields'])))])
		#Edit fields with matching names (assuming that same name means same data or an easy conversion)
		db_cols = []
		for i in range(0,len(db_table['fields'])-1):
			db_col = db_table['fields'][i]
			if dfn_col_map.has_key(db_col['Field']): #Same name, so either leave unchanged or modify to new def.
				dfn_col = dfn_table['fields'].pop(dfn_col_map[db_col['Field']])
				if (dfn_col['Type'] != db_col['Type']) or (dfn_col['Null'] != db_col['Null']):
					qry.execute(self.sql_exe_modify_column_dict(tablename, db_col['Field'], dfn_col))
			elif db_col['Type'] == dfn_tabl['fields'][i]['Type']: #Same position, same type, might be a name change
				dfn_col = dfn_table['fields'].pop(i)
				qry.execute(self.sql_exe_modify_column_dict(tablename, db_col['Field'], dfn_col))
			else:
				db_cols.append(db_col)
		#Drop any remaining columns
		for db_col in db_cols: #We need to drop these additional columns
			qry.execute(self.sql_exe_drop_column(tablename,db_col['Field']))
		for dfn_col in dfn_table['fields']: #We need to append additional columns
			qry.execute(self.sql_exe_append_column_dict(tablename,dfn_col))
		#Apply all defined PKs and Indexes
		for index in dfn_table['indexes']:
			if index['Key_name'] == 'PRIMARY':
				qry.execute(self.sql_exe_add_PK(tablename,index['Column_name']))
			else:
				qry.execute(self.sql_exe_add_index(tablename, index['Key_name'], index['Index_type'], index['Column_name']))
		qry.close()
	
	# SQL statement functions
	
	def sql_create_db(self):
		return 'SHOW CREATE DATABASE %s' % self.dbname
	
	def sql_create_table(self, name):
		return 'SHOW CREATE TABLE %s' % name
		
	def sql_table_names(self):
		return "SHOW FULL TABLES WHERE Table_type != 'VIEW'"
		
	def sql_column_names(self, table):
		return 'SHOW FULL COLUMNS FROM %s' % table
		
	def sql_index_names(self, table):
		return 'SHOW INDEX FROM %s' % table
	
	def sql_create_function(self, name):
		return 'SHOW CREATE FUNCTION %s' % name
	
	def sql_function_names(self):
		return 'SHOW FUNCTION STATUS'
		
	def sql_create_procedure(self, name):
		return 'SHOW CREATE PROCEDURE %s' % name
	
	def sql_procedure_names(self):
		return 'SHOW PROCEDURE STATUS'
	
	def sql_create_view(self, name):
		return 'SHOW CREATE VIEW %s' % name
	
	def sql_view_names(self):
		return "SHOW FULL TABLES WHERE Table_type = 'VIEW'"

	def sql_trigger_names(self):
		return 'SHOW TRIGGERS'
	
	def sql_flush_lock_tables(self):
		return 'FLUSH TABLES WITH READ LOCK'
	
	def sql_unlock_tables(self):
		return 'UNLOCK TABLES'
	
	def sql_truncate_table(self, table):
		return 'TRUNCATE TABLE %s' % table
	
	def sql_exe_column_def_dict(col):
		return self.sql_exe_column_def(col['Field'], col['Type'], col['Null']!='NO', col['Default'], 
			col['Extra'].find('auto_increment')>-1, col['Key']=='UNI', col['Key']=='PRI', col['Comment'])
		
	def sql_exe_column_def(name, data_type, is_null=True, default_value='', auto_inc=False, 
			unique=False, primary=False, comment=''):
		if is_null: 	null_val = 'NULL'
		else: null_val = 'NOT NULL'
		if default_value != '': default_value = 'DEFAULT ' + default_value
		if auto_inc: autoinc_val = 'AUTO_INCREMENT'
		else: autoinc_val = ''
		if primary: key_val = 'PRIMARY KEY'
		elif unique: key_val = 'UNIQUE KEY'
		else: key_val = ''
		if comment != '': comment = "COMMENT '%s'" % comment
		return '%s %s %s %s %s %s %s' % (name,data_type, null_val, default_value, autoinc_val, key_val, comment)
	
	def sql_exe_append_column_dict(self, table, col):
		return self.sql_exe_append_column(table, col['Field'], col['Type'], col['Null']!='NO', col['Default'], 
			col['Extra'].find('auto_increment')>-1, col['Key']=='UNI', col['Key']=='PRI', col['Comment'])
		
	def sql_exe_append_column(self,table,name, data_type, is_null=True, default_value='', auto_inc=False, 
			unique=False, primary=False, comment=''):
		col_def = self.sql_exe_column_def(name, data_type, is_null, default_value, auto_inc, unique, primary, comment)
		return 'ALTER TABLE %s ADD COLUMN %s' % (table, col_def)
	
	def sql_exe_modify_column_dict(self,table, old_name, col):
		col_def = self.sql_exe_column_def_dict(col)
		return 'ALTER TABLE %s CHANGE COLUMN %s %s' % (table, old_name, col_def)
		
	def sql_exe_modify_column(self, table, old_name, new_name, name, data_type, is_null=True, default_value='',
			auto_inc=False, unique=False, primary=False, comment=''):
		col_def = self.sql_exe_column_def(name, data_type, is_null, default_value, auto_inc, unique, primary, comment)
		return 'ALTER TABLE %s CHANGE COLUMN %s %s' % (table, old_name, col_def)
	
	def sql_exe_drop_column(self,table,name):
		return 'ALTER TABLE %s DROP COLUMN %s' % (table, name)
		
	def sql_exe_drop_PK(self, table):
		return 'ALTER TABLE %s DROP PRIMARY KEY' % table
		
	def sql_exe_add_PK(self, table, cols):
		if isinstance(cols,(str, unicode)):
			return "ALTER TABLE %s ADD PRIMARY KEY (%s)" % (table, cols)
		else:
			return "ALTER TABLE %s ADD PRIMARY KEY (%s)" % (table, reduce(lambda x, y: x+","+y, cols))
		
	def sql_exe_drop_index(self, table, name):
		return 'ALTER TABLE %s DROP INDEX %s' % (table, name)
		
	def sql_exe_add_index(self, table, name, type, cols):
		if isinstance(cols,(str, unicode)):
			return "ALTER TABLE %s ADD INDEX %s %s (%s)" % (table, name, type, cols)
		else:
			return "ALTER TABLE %s ADD INDEX %s %s (%s)" % (table, name, type, reduce(lambda x, y: x+","+y, cols))
		
	def sql_exe_drop_FK(self, name):
		#Not implemented in all of MySQL's storage engines
		pass
		
	def sql_exe_add_FK(self, table, name):
		#Not implemented in all of MySQL's storage engines
		pass

	def sql_exe_drop_trigger(self, name):
		return 'DROP TRIGGER %s' % name

	def sql_exe_add_trigger_dict(self, trigger):
		return self.sql_exe_add_trigger(trigger['Table'], trigger['Trigger'], trigger['Timing'], trigger['Event'], trigger['Statement'])
		
	def sql_exe_add_trigger(self, table, name, time, event, statement):
		#time = BEFORE/AFTER, event = INSERT/UPDATE/DELETE
		return 'CREATE TRIGGER %s %s %s ON %s FOR EACH ROW %s' % (name, time, event, table, statement) 
		
	def sql_exe_drop_view(self, name):
		return 'DROP VIEW IF EXISTS %s' % name
		
	def sql_exe_drop_procedure(self, name):
		return 'DROP PROCEDURE IF EXISTS %s' % name
		
	def sql_exe_drop_function(self, name):
		return 'DROP FUNCTION IF EXISTS %s' % name
		
	def sql_exe_drop_table(self, name):
		return 'DROP TABLE IF EXISTS %s' % name

def configure_option_parser():
	filename = "backup_%s.sql" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename", default=filename, help="""File to use for the selected operation [backup]:
	backup: 		file to backup your data to
	restore: 		file to restore your data from
	schema_updt:	file that holds current schema information which you want to synchronize with
	schema_save:	file that you want to save the current schema information to""")
	parser.add_option("-o", "--op", dest="op", default="backup",  help="""Operation that you want to run [backup_datetime.sql]:
	backup:		Backup the database data
	restore:		Remove all data from database tables and then restore the data from the file
	schema_updt:	Attempt to synchronize the current database schema with what the file describes
	schema_save:	Save the current database schema to the file""")
	parser.add_option("-H", "--host", dest="host", default="localhost", help="The server host to connect to [localhost]")
	parser.add_option("-P", "--port", dest="port", default=3306, help="The server port to connect to [3306]")
	parser.add_option("-d", "--db", dest="dbname", default="mysql", help="The database to connect to [mysql]")
	parser.add_option("-u", "--user", dest="user", default="root", help="The user to connect as [root]")
	parser.add_option("-p", "--passwd", dest="passwd", default="", help="The password for the user []")
	return parser

if __name__ == "__main__":
	parser = configure_option_parser()
	(options, args) = parser.parse_args()
	db = MySQLSchema(dbname=options.dbname, user=options.user, passwd=options.passwd, host=options.host,
		port=options.port)
	if options.op == "backup":
		db.backup_data(options.filename)
	elif options.op == "restore":
		db.restore_data(options.filename)
	elif options.op == "schema_updt":
		db.schema_update(options.filename)
	else:
		db.schema_save(options.filename)
	
	