"""     By Wesley Penner (Sept.2006)

		Manage MySQL schema changes and updates
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

import sys, os, time, pickle, cPickle, datetime, MySQLdb, MySQLdb.converters
from optparse import OptionParser
import MySQLdb.constants

def timestampConverter(s):
	"""Convert MYSQL TIMESTAMP"""
	try:
		val = datetime.datetime.fromtimestamp(s)
	except:
		val = None
	return val

def BLOBconvert(s):
	"""Convert MySQL BLOB's to unicode strings"""
	return unicode(s)

class MySQLSchema:
		dbname = ''
		conn = None
		tables = [] #Table defs, columns, indexes (custom definition and some sql text)
		views = [] # View definitions (SQL text)
		sp = [] #Stored procedure AND function definitions (SQL text)
		triggers = [] #Trigger definitions (sql text)
		data = [] #data lines by table.  Not a db unload/reload
		logfile = None
		
		def __init__(self, dbname='', user='root', passwd='', host='localhost', port='3306', logfile='logfile.txt'):
				self.dbname = dbname
				conv = MySQLdb.converters.conversions
				conv[7] = timestampConverter
				#del(conv[MySQLdb.constants.FIELD_TYPE.BLOB])
				conv[MySQLdb.constants.FIELD_TYPE.BLOB] = BLOBconvert
				self.conn = MySQLdb.connect(db=dbname, user=user, passwd=passwd, host=host, port=int(port), conv=conv)
				self.logfile = open(logfile, 'a')
				#self.conn.converter[7] = timestampConverter
				
		def log(self,text):
				self.logfile.write('%s: %s\n' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text))

		def log_close(self):
				self.logfile.close()
				
		# Major functions
		def restore_data(self, filename):
				try:
						f = open(filename) #make sure the file exists
						f.close()
						self.delete_all_data()
						#self.restore_from_backup(filename)
						self.log('RESTORE OPERATION BEGINS')
						self.restore_tables_DBAPI(filename)
						self.log('RESTORE OPERATION ENDS')
						self.log_close()
				except:
						raise
						
		def backup_data(self, filename):
				try:
						#self.backup_tables(filename)
						self.log('BACKUP OPERATION BEGINS')
						self.backup_tables_DBAPI(filename)
						self.log('BACKUP OPERATION ENDS')
						self.log_close()
				except:
						raise
						
		def schema_update(self, filename):
				try:
						self.log('SCHEMA UPDATE OPERATION BEGINS')
						self.load_from_file(filename)
						self.log('SCHEMA UPDATE OPERATION ENDS')
						self.log_close()
				except:
						raise
						
		def schema_save(self, filename):
				try:
						self.log('SCHEMA SAVE OPERATION BEGINS')
						self.save_to_file(filename)
						self.log('SCHEMA SAVE OPERATION ENDS')
						self.log_close()
				except:
						raise

		def db_close(self):
				qry = self.conn.cursor()
				qry.execute(self.sql_unlock_tables())
				qry.close()
				self.conn.close()
				
		def load_from_file(self, filename):
				f = open(filename,'rb')
				try:
						db = pickle.load(f)
				except:
						self.log('ERROR: Cannot load file')
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
				f = open(filename,'wb')
				pickle.dump(db,f,2)
				f.close()
				self.log('Schema definition successfully saved to a file.')
				
		def reset(self):
				tables = []
				views = []
				sp = []
				triggers = []
				data = []
				
		# Internal processing functions
		def delete_all_data(self):
				self.log('Deleting all data in db %s' % self.dbname)
				qry = self.conn.cursor()
				qry.execute(self.sql_table_names())
				tables = [x[0] for x in qry.fetchall()]
				try:
						qry.execute(self.sql_disable_FK())
				except:
						self.log('ERROR: (in delete all) Disabling FK constraints: %s' % sys.exc_info()[0])
						raise
				#qry.execute(self.sql_flush_lock_tables())
				for table in tables:
						self.log('Truncating table %s' % table)
						try:
								qry.execute(self.sql_truncate_table(table))
						except MySQLdb.OperationalError, (errorno, strerror):
								if errorno == 1451:
										self.log('ERROR: ForeignKey constraint error: %s' % strerror)
								else:
										self.log('ERROR: Truncating table (# %s) (Msg: %s)' % (errorno, strerror))
						except:      
								self.log('ERROR: Truncating table: %s' % sys.exc_info()[0])
								raise
				#qry.execute(self.sql_unlock_tables())
				try:
						qry.execute(self.sql_enable_FK())
				except:
						self.log('ERROR: (in delete all) Enabling FK constraints: %s' % sys.exc_info()[0])
						raise
				qry.close()
				
		def restore_tables_DBAPI(self, filename):
				f = open(filename,'rb')
				restore_tables = pickle.load(f)
				f.close()
				qry = self.conn.cursor()
				try:
						qry.execute(self.sql_disable_FK())
				except:
						self.log('ERROR: Disabling FK constraints: %s' % sys.exc_info()[0])
						raise
				for table in restore_tables:
						print "Restoring table %s with %d lines of data" % (table, len(restore_tables[table]['data']))
						self.log("Restoring table %s with %d lines of data" % (table, len(restore_tables[table]['data'])))
						try:
								qry.executemany(restore_tables[table]['command'],restore_tables[table]['data'])
						except MySQLdb.OperationalError, (errorno, errorstr):
								self.log("Error restoring table %s (# %s): %s" % (table, errorno, errorstr))
								print "Error restoring table %s (# %s): %s" % (table, errorno, errorstr)
								if errorno == 1136:
										self.log("Error: Command: %s" % restore_tables[table]['command'])
										print "     Command: %s" % restore_tables[table]['command']
										print "     1st Line: %s"
										print restore_tables[table]['data'][0]
										raise
						except ValueError:
								#Some stupid time conversions are not working (bad data) so I'll just skip those rows
								self.log("Error: with table %s" % table)
								print "     Problems with table %s, trying to fix" % table
								for row in restore_tables[table]['data']:
										try:
												qry.execute(restore_tables[table]['command'],row)
										except ValueError, (strerror):
												if (strerror[0][0:24] == 'year=1899 is before 1900') or (strerror[0][0:20] == 'year is out of range'):
														self.fix_date_entry(restore_tables[table]['command'],row)
												else:
														self.log("WARNING: dropped line in table %s: %s" % (table, strerror))
														print "     Dropped line in %s" % table
						self.conn.commit()
				try:
						qry.execute(self.sql_enable_FK())
				except:
						self.log('ERROR: Enabling FK constraints: %s' % sys.exc_info()[0])
						raise
				self.conn.commit()
				qry.close()

		def fix_date_entry(self, command, row):
				qry = self.conn.cursor()
				fixed_row = []
				for col in row:
						if isinstance(col, (datetime.datetime, datetime.date)):
								try:
										tmp = col.strftime('%Y-%m-%d')
										fixed_row.append(col)
								except:
										fixed_row.append(datetime.datetime(1900,1,1))
										self.log('NOTE: Fixed one date column setting it to 1900,1,1')
						else:
								fixed_row.append(col)
				try:
						qry.execute(command,fixed_row)
				except:
						self.log('ERROR: Even after trying to fix a row, it failed: %s' % sys.exc_info()[0])
						print 'ERROR: Even after trying to fix a row, it failed: %s' % sys.exc_info()[0]
				qry.close()

		def backup_tables_DBAPI(self, filename):
				qry = self.conn.cursor()
				qry.execute(self.sql_table_names())
				tables = [x[0] for x in qry.fetchall()]
				qry.execute(self.sql_flush_lock_tables())
				qry.execute(self.sql_unlock_tables())
				bkup_tables = {}
				for table in tables:
						self.log('Backing up table %s' % table)
						bkup_tables[table] = self.write_table_data_DBAPI(table)
				f = open(filename, 'wb')
				pickle.dump(bkup_tables,f,2)
				f.close()
				qry.close()
				
		def write_table_data_DBAPI(self, table):
				#appends the sql to the file 'f' for the table 'table'
				qry = self.conn.cursor()
				qry.execute("select * from " + table)
				command = ''
				data = []
				if qry.rowcount > 0:
						col_names = '`%s`' % reduce(lambda x, y: x+'`, `'+y, [x[0] for x in qry.description]) #Comma separated column names
						command = "INSERT IGNORE INTO %s (%s) VALUES (%s)" % (table, col_names, (" %s,"*len(qry.description))[1:-1])
						data = qry.fetchall()
				qry.close()
				return dict(command=command, data=data)

		def restore_from_backup(self, filename):
				f = open(filename)
				qry = self.conn.cursor()
				qry.execute("SET @@session.FOREIGN_KEY_CHECKS = 0;")
				sql_file = f.read()
				mark = sql_file.find('INSERT INTO')
				mark2 = sql_file.find('INSERT INTO',mark+11)
				while mark != -1:
						sql = sql_file[mark:mark2]
						try:
								qry.execute(sql)
						except:
								print "ERROR trying to insert data"
								print sql
								raise
						mark = sql_file.find('INSERT INTO',mark2)
						mark2 = sql_file.find('INSERT INTO',mark+11)
				qry.execute("SET @@session.FOREIGN_KEY_CHECKS = 1;")
				qry.close()
				f.close()
								
		def backup_tables(self, filename):
				qry = self.conn.cursor()
				qry.execute(self.sql_table_names())
				f = open(filename, 'w')
				f.write("-- Backup taken by python script on %s \n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				f.write(self.sql_flush_lock_tables() + ";\n")
				f.write("SET FOREIGN_KEY_CHECKS = 0;")
				tables = [x[0] for x in qry.fetchall()]
				qry.execute(self.sql_flush_lock_tables())
				for table in tables:
						self.write_table_data(table, f)
				qry.execute(self.sql_unlock_tables())
				f.write("SET FOREIGN_KEY_CHECKS = 1;")
				f.write(self.sql_unlock_tables()+";\n")
				f.close()
				qry.close()
				
		def write_table_data(self, table, f):
				#appends the sql to the file 'f' for the table 'table'
				qry = self.conn.cursor()
				qry.execute("select * from " + table)
				if qry.rowcount > 0:
						col_names = '`%s`' % reduce(lambda x, y: x+'`, `'+y, [x[0] for x in qry.description]) #Comma separated column names
						f.write("INSERT INTO %s (%s) VALUES \n" % (table, col_names))
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
										f.write(';\n\n')
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
						self.log('Saving table %s definition' % table)
						self.tables.append(dict(name=table,defn=self.make_table_def(table)))
				qry.close()
		
		def make_view_definitions(self):
				qry = self.conn.cursor()
				qry.execute(self.sql_view_names())
				views = qry.fetchall()
				for view in views:
						self.log('Saving view %s definition' % view[0])
						qry.execute(self.sql_create_view(view[0]))
						view_sql = qry.fetchall()[0][1]
						self.views.append(dict(name=view[0], sql=view_sql))
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
						self.log('Saving function %s definition' % function)
						qry.execute(self.sql_create_function(function))
						res = qry.fetchall()
						sql = dict([(x[1], x[0]) for x in zip(res[0], map(lambda x: x[0], qry.description))])['Create Function']
						self.sp.append(dict(name=function,sql=sql))
				for procedure in procedures:
						self.log('Saving procedure %s definition' % procedure)
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
						self.log('Saving trigger %s definition' % trigger['Trigger'])
						self.triggers.append(dict(name=trigger['Trigger'],sql=self.sql_exe_add_trigger_dict(trigger)))
				qry.close()
						
		def apply_trigger_definitions(self):
				self.log('Updating Triggers')
				print "Applying Triggers"
				print "================="
				qry = self.conn.cursor()
				qry.execute(self.sql_trigger_names())
				res = qry.fetchall()
				db_triggers = []
				#Get a list of current triggers
				for rec in res:
						db_triggers.append(dict([(x[1], x[0]) for x in zip(rec, map(lambda x: x[0], qry.description))])['Trigger'])
				trigger_set = set(db_triggers)
				#Drop all triggers which are both in the current db and reference schema
				for trigger in self.triggers:
						if trigger['name'] in trigger_set:
								try:
										self.log('Dropping trigger %s' % trigger['name'])
										print "Dropping trigger:    %s" % trigger['name']
										qry.execute(self.sql_exe_drop_trigger(trigger['name']))
								except:
										self.log('Error: Failed to drop trigger')
										print " Failed dropping trigger"
										raise
				#Create all triggers in the reference schema
				for trigger in self.triggers:
						try:
								self.log('Adding trigger %s' % trigger['name'])
								print "Adding trigger:  %s" % trigger['name']
								qry.execute(trigger['sql'])
						except MySQLdb.OperationalError, (errorno, errorstr):
								self.log('Error: Failed to add trigger (No %s) (Str %s)' % (errorno, errorstr))
								print " Failed adding trigger (No %s) (Str %s)" % (errorno, errorstr)
								print trigger['sql']
								raise
				qry.close()
				
		def apply_view_definitions(self):
				self.log('Updating Views')
				print "Applying Views"
				print "=============="
				qry = self.conn.cursor()
				qry.execute(self.sql_view_names())
				res = qry.fetchall()
				#Get a listing of all current views
				db_views = []
				for rec in res:
						db_views.append(rec[0])
				view_map = dict([(x[0], x[1]) for x in zip(db_views,range(0,len(db_views)))])
				#Drop all views common both in the current db and the reference
				for view in self.views:
						if view_map.has_key(view['name']):
								self.log('Dropping view %s' % view['name'])
								qry.execute(self.sql_exe_drop_view(view['name']))
				#Create all the views
				delayed_views = {}
				for view in self.views:
						try:
								self.log('Creating view %s' % view['name'])
								print "Adding view: %s" % view['name']
								qry.execute(view['sql'])
						except MySQLdb.ProgrammingError, (errorno, errorstr):
								if errorno == 1146:
										#In this case, the view depends on other views not created yet
										self.log('Note: Delaying view add (dependency)')
										delayed_views[view['name']] = view['sql']
								else:
										self.log('ERROR adding view. SQL SYNTAX ERROR (# %s): %s' % (errorno, errorstr))
										print "SQL SYNTAX ERROR (# %s): %s" % (errorno, errorstr)
										print view['sql']
										raise
				while len(delayed_views) > 0:
						del_views = dict(delayed_views) #create a copy
						for view in del_views:
								try:
										qry.execute(delayed_views[view])
										del(delayed_views[view])
										self.log('Added view after delay: %s' % view)
								except MySQLdb.ProgrammingError, (errorno, errorstr):
										self.log('Delaying view %s even more' % view)
										print "Retrying %s: %s" % (view, errorstr)
				qry.close()
				
		def apply_sp_definitions(self):
				self.log('Updating stored procedures/functions')
				print "Applying stored procedures/functions"
				print "===================================="
				qry = self.conn.cursor()
				#Drop all stored procedures and functions which we define (using the error free drop syntax)
				for ProcFunc in self.sp:
						self.log('Dropping procedure/function %s' % ProcFunc['name'])
						print "Stored procedure/function drop: %s" % ProcFunc['name']
						qry.execute(self.sql_exe_drop_procedure(ProcFunc['name']))
						qry.execute(self.sql_exe_drop_function(ProcFunc['name']))
				for ProcFunc in self.sp:
						print "Stored procedure/function add: %s" % ProcFunc['name']
						try:
								self.log('Adding procedure/function %s' % ProcFunc['name'])
								qry.execute(ProcFunc['sql'])
						except MySQLdb.OperationalError, (errorno, errorstr):
								if errorno == 1418:
										#This error happens when we have binary logging and the option for non-deterministic functions
										#Fix it by setting an option
										self.log('NOTE: Turning on "log-bin-trust-function-creators" option')
										qry.execute("SET @@global.log_bin_trust_function_creators=1;")
										qry.execute(ProcFunc['sql'])
								else:
										self.log('ERROR: adding proc/func (# %s) (Str %s)' % (errorno, errorstr))
										print "Error adding proc/func (# %s) (Str %s)" % (errorno, errorstr)
										raise
				qry.close()
				
		def apply_table_definitions(self):
				self.log('Updating Tables')
				print "Applying tables"
				print "==============="
				#Tables to create
				#Tables to update
				db_tables = []
				table_map = dict([(x[0]['name'], x[1]) for x in zip(self.tables,range(0,len(self.tables)))])
				qry = self.conn.cursor()
				#qry.execute(self.sql_flush_lock_tables())
				qry.execute(self.sql_table_names())
				res = qry.fetchall()
				for rec in res:
						db_tables.append(rec[0])
				dfn_tables = [x['name'] for x in self.tables]
				updt_tables = set(db_tables) & set(dfn_tables) #Tables both in the definition and the current db
				create_tables = set(dfn_tables) - set(db_tables) #Tables in the definition but not in the current db
				#NOTE: ForeignKey dependencies may force tables to be created in a specific order, so I added the "create_later" list
				while len(create_tables) > 0:
						create_later = []
						for table in create_tables:
								try:
										self.log('Creating table %s' % table)
										qry.execute(self.tables[table_map[table]]['defn']['sql'])
								except MySQLdb.OperationalError, (errorno, strerror):
										if errorno == 1005:
												create_later.append(table) #Couldn't create table now, but maybe later
										else:
												self.log('ERROR creating table %s: %s' % (table, sys.exc_info()[0]))
												print "ERROR creating table"
												print "===================="
												print self.tables[table_map[table]]['defn']['sql']
												raise
								except:
										self.log('ERROR creating table %s: %s' % (table, sys.exc_info()[0]))
										self.log('ERROR creating table %s: %s' % (table, sys.exc_info()[0]))
										print "ERROR creating table"
										print "===================="
										print self.tables[table_map[table]]['defn']['sql']
										raise
						create_tables = set(create_later)
				for table in updt_tables:
						self.log('Updating Table %s' % table)
						self.update_table_def(table)
				#qry.execute(self.sql_unlock_tables())
				qry.close()
				
		def update_table_def(self, tablename):
				#The 'db_' prefix is for variables referencing the current database (which we're updating) while "dfn_" prefixes our reference definition which we want to update to
				qry = self.conn.cursor()
				db_table = self.make_table_def(tablename)
				table_map = dict([(x[0]['name'], x[1]) for x in zip(self.tables,range(0,len(self.tables)))])
				dfn_table = dict(self.tables[table_map[tablename]]['defn'])#create a local copy
				print "Working on table: %s" % tablename
				#Edit fields with matching names (assuming that same name means same data or an easy conversion)
				db_cols = []
				for i in range(0,len(db_table['fields'])):
						db_col = db_table['fields'][i]
						#create a dictionary of column names to field number (needs to be recreated every time)
						dfn_col_map = dict([(x[0]['Field'],x[1]) for x in zip(dfn_table['fields'],range(0,len(dfn_table['fields'])))])
						if dfn_col_map.has_key(db_col['Field']): #Same name, so either leave unchanged or modify to new def.
								dfn_col = dfn_table['fields'].pop(dfn_col_map[db_col['Field']])
								#print "Name: dfn[%s] db[%s] Type: dfn[%s] db[%s].  Null: dfn[%s] db[%s]" % (dfn_col['Field'], db_col['Field'], dfn_col['Type'], db_col['Type'], dfn_col['Null'], db_col['Null'])
								if (dfn_col['Type'] != db_col['Type']) or (dfn_col['Null'] != db_col['Null']):
										print dfn_col
										self.log('Modifying column %s in table %s' % (db_col['Field'], tablename))
										qry.execute(self.sql_exe_modify_column_dict(tablename, db_col['Field'], dfn_col))
						else:
								self.log('Adding column %s to table %s' % (db_col['Field'], tablename))
								#should this line use dfn_col instead?!?!?
								db_cols.append(db_col)
				for i in range(0,min(len(db_cols),len(dfn_table['fields']))-1):
						if db_cols[i]['Type'] == dfn_table['fields'][i]['Type']:
								try:
										self.log('Modifying column %s in table %s' % (db_col['Field'], tablename))
										dfn_col = dfn_table['fields'][i]
										db_col = db_table['fields'][i]
										qry.execute(self.sql_exe_modify_column_dict(tablename, db_col['Field'], dfn_col))
										db_col = db_table['fields'].pop(i)
										dfn_col = dfn_table['fields'].pop(i)
								except MySQLdb.OperationalError:
										self.log('ERROR: Modifying column %s in table %s faild' % (db_col['Field'], tablename))
										print "     Failed modifying column %s" % db_col['Field']
				#Drop all keys and indexes -- sometimes the primary key can't be removed if the column defn. doesn't allow it
				# So, if we are changing the primary key to another column, then we need to first modify the original column, then
				# we'll be allowed to drop the primary key
				for index in db_table['indexes']:
						try:
								if index['Key_name'] == 'PRIMARY':
										try:
												self.log('Dropping PK in %s' % tablename)
												qry.execute(self.sql_exe_drop_PK(tablename))
										except MySQLdb.OperationalError:
												self.log('WARNING: failed to drop primary key... a common problem')
												pass #Skip over any operational errors.  Normally just stopping me from dropping a primary key
								else:
										#print "Deleting Index: %s" % index['Key_name']
										self.log('Dropping index %s' % index['Key_name'])
										qry.execute(self.sql_exe_drop_index(tablename, index['Key_name']))
						except MySQLdb.OperationalError:
								self.log('WARNING: failed to drop index %s' % index['Key_name'])
								print "     Failed dropping index %s" % index['Key_name'] # Innodb is giving me problems?  Some indexes refuse to be removed
				#Drop any remaining columns
				for db_col in db_cols: #We need to drop these additional columns
						self.log('Dropping column %s from table %s' % (db_col['Field'], tablename))
						qry.execute(self.sql_exe_drop_column(tablename,db_col['Field']))
				for dfn_col in dfn_table['fields']: #We need to append additional columns
						self.log('Appending column %s to table %s' % (dfn_col['Field'], tablename))
						print dfn_col
						qry.execute(self.sql_exe_append_column_dict(tablename,dfn_col))
				#Check for a multi-column PK
				tmp_PK = []
				for index in dfn_table['indexes']:
						if index['Key_name'] == 'PRIMARY':
								tmp_PK.append(index['Column_name'])
				if len(tmp_PK) > 1:
						self.log('Adding PK to table %s' % tablename)
						try:
								self.log('Adding PK to table %s' % tablename)
								qry.execute(self.sql_exe_add_PK(tablename,tmp_PK))
						except MySQLdb.OperationalError, (errorno, strerror):
								if errorno == 1068:
										self.log('WARNING: failed to add primary key to %s.  It already exists' % tablename)
										print "     Failed adding primary key %s" % index['Column_name'] #encountered when a primary key we hoped to drop... didin't
								else:
										self.log('WARNING: failed to add primary key to %s #%s: %s' % (tablename, errorno, strerror))
										print "     Failed adding primary key %s" % index['Column_name'] #encountered when a primary key we hoped to drop... didin't
						except:
								self.log('WARNING: failed to add primary key to %s.  Probably already exists' % tablename)
								print "     Failed adding primary key %s" % index['Column_name'] #encountered when a primary key we hoped to drop... didin't
								raise
				#Apply all defined PKs (unless we already added the PK) and Indexes
				for index in dfn_table['indexes']:
						if (index['Key_name'] == 'PRIMARY'):
								try:
										if len(tmp_PK) <= 1:
												self.log('Adding PK to table %s' % tablename)
												qry.execute(self.sql_exe_add_PK(tablename,index['Column_name']))
								except MySQLdb.OperationalError:
										self.log('WARNING: failed to add primary key to %s.  Probably already exists' % tablename)
										print "     Failed adding primary key %s" % index['Column_name'] #encountered when a primary key we hoped to drop... didin't
						else:
								try:
										self.log('Adding index %s to table %s' % (index['Key_name'], tablename))                                
										qry.execute(self.sql_exe_add_index(tablename, index['Key_name'], index['Index_type'], index['Column_name']))
								except MySQLdb.OperationalError:
										self.log('WARNING: failed to add index %s to table %s.  Probably already exists' % (index['Key_name'], tablename))  
										print "     Failed adding index %s" % index['Key_name'] #again, some keys which are not labelled primary key but can't be removed earlier
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
				return "SHOW FUNCTION STATUS WHERE Db='%s'" % self.dbname
				
		def sql_create_procedure(self, name):
				return 'SHOW CREATE PROCEDURE %s' % name
		
		def sql_procedure_names(self):
				return "SHOW PROCEDURE STATUS WHERE Db='%s'" % self.dbname
		
		def sql_create_view(self, name):
				return 'SHOW CREATE VIEW %s' % name
		
		def sql_view_names(self):
				return "SHOW FULL TABLES WHERE Table_type = 'VIEW'"

		def sql_trigger_names(self):
				return 'SHOW TRIGGERS'

		def sql_enable_FK(self):
				return 'SET @@session.FOREIGN_KEY_CHECKS = 1;'
		
		def sql_disable_FK(self):
				return 'SET @@session.FOREIGN_KEY_CHECKS = 0;'

		def sql_flush_lock_tables(self):
				return 'FLUSH TABLES WITH READ LOCK'
		
		def sql_unlock_tables(self):
				return 'UNLOCK TABLES'
		
		def sql_truncate_table(self, table):
				return 'TRUNCATE TABLE %s' % table
		
		def sql_exe_column_def_dict(self, col):
				return self.sql_exe_column_def(col['Field'], col['Type'], col['Null']!='NO', col['Default'], 
						col['Extra'].find('auto_increment')>-1, col['Key']=='UNI', col['Key']=='PRI', col['Comment'])
				
		def sql_exe_column_def(self, name, data_type, is_null=True, default_value='', auto_inc=False, 
						unique=False, primary=False, comment=''):
				quotevar = ('CHAR','VARBINARY','BLOB','TEXT','DATE','TIME','YEAR')
				if is_null:     null_val = 'NULL'
				else: null_val = 'NOT NULL'
				if default_value == None: default_value = 'NULL'
				elif (default_value == '') and (not is_null) and (not (True in map(lambda x: data_type.upper().find(x)>-1, quotevar))):
						default_value = '0'
				elif default_value == 'CURRENT_TIMESTAMP': default_value = 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
				elif not default_value.isdigit(): default_value = "'%s'" % default_value
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
				
		def sql_exe_add_index(self, table, name, itype, cols):
				if isinstance(cols,(str, unicode)):
						return "ALTER TABLE %s ADD INDEX %s (%s)" % (table, name, cols)
				else:
						return "ALTER TABLE %s ADD INDEX %s (%s)" % (table, name, reduce(lambda x, y: x+","+y, cols))
				
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
		backup:                 file to backup your data to
		restore:                file to restore your data from
		schema_updt:    file that holds current schema information which you want to synchronize with
		schema_save:    file that you want to save the current schema information to""")
		parser.add_option("-o", "--op", dest="op", default="backup",  help="""Operation that you want to run [backup_datetime.sql]:
		backup:         Backup the database data
		restore:                Remove all data from database tables and then restore the data from the file
		schema_updt:    Attempt to synchronize the current database schema with what the file describes
		schema_save:    Save the current database schema to the file""")
		parser.add_option("-H", "--host", dest="host", default="localhost", help="The server host to connect to [localhost]")
		parser.add_option("-P", "--port", dest="port", default=3306, help="The server port to connect to [3306]")
		parser.add_option("-d", "--db", dest="dbname", default="mysql", help="The database to connect to [mysql]")
		parser.add_option("-u", "--user", dest="user", default="root", help="The user to connect as [root]")
		parser.add_option("-p", "--passwd", dest="passwd", default="", help="The password for the user []")
		parser.add_option("-l", "--logfile", dest="logfile", default="logfile.txt", help="File where the script writes out logging information")
		return parser

if __name__ == "__main__":
		parser = configure_option_parser()
		(options, args) = parser.parse_args()
		if options.op in ["backup", "restore", "schema_updt", "schema_save"]:
			db = MySQLSchema(dbname=options.dbname, user=options.user, passwd=options.passwd, host=options.host,
				port=options.port)
		try:
				if options.op == "backup":
						db.backup_data(options.filename)
				elif options.op == "restore":
						db.restore_data(options.filename)
				elif options.op == "schema_updt":
						db.schema_update(options.filename)
				elif options.op == "schema_save":
						db.schema_save(options.filename)
				else:
					print parser.print_help()
		finally:
			if 'db' in dir():
				db.db_close()
			else:
				print "Done"
		
		
