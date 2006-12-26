from sqlobject import *
import model
import pkg_resources
#  import time
import os
import struct
import socket
from browse import Browse
import re,datetime
import sidewalk

def cur_date_time():
	return datetime.datetime.now()

def care2x_test():
	schema = sidewalk.SideWalk(model)
	tables = schema.models()
	i = 0
	for table in tables:
		i += 1
		print str(i).rjust(3,'0') + ": " + table
		t_class = schema.load_object(table)
		cols = schema.get_columns_for_object(t_class)
		col_str = ''
		for col in cols:
			if col['columnName'] in ['CreateId','ModifyId']:
				col_str += col['columnName'] + "='Wesley_test',"
			elif col['columnName'] == 'P':
				col_str += "Pid=0,"
			elif col['type'] =='SOStringCol':
				if col.has_key('default'):
					if col['default'] == '':
						col_str += col['columnName'] + "='TeSt',"
					else:
						col_str += col['columnName'] + "='" + col['default'] + "',"
				else:
					col_str += col['columnName'] + "='TeSt',"
			elif col['type'] in ['SODateCol','SODateTimeCol']:
				col_str += col['columnName'] + "=cur_date_time(),"
			elif col['type'] in ['SOIntCol','SOFloatCol','SOCurrencyCol','SOFloatCol']:
				if col.has_key('default'):
					if col['default'] > 0:
						num_val = str(col['default'])
					else:
						num_val = '5'
				else:
					num_val = '5'
				if num_val == '':
					num_val = '5'
				col_str += col['columnName'] + "="+ str(num_val) +","
			elif col['type'] == 'SOBoolCol':
				if col.has_key('default'):
					bool_val = str(col['default'])
				else:
					bool_val = 'True'
				if bool_val == '':
					bool_val = 'True'
				col_str += col['columnName'] + "="+ bool_val +","
			elif col['type'] == 'SOEnumCol':
				if col.has_key('default'):
					enum_val = col['default']
				else:
					enum_val =  col['options'][0]
				if enum_val == '':
					enum_val =  col['options'][0]
				col_str += col['columnName'] + "='" + enum_val + "',"
			elif col['type'] in ['SOMultipleJoin','SORelatedJoin','SOSingleJoin','SOForeignKey']:
				col_str += col['columnName'] + "=0,"
			else:
				col_str += col['columnName'] + "='Empty',"
#				if col.has_key('default'):
#					col_str += col['columnName'] + "='" + col['default'] + "',"
#				else:
#					col_str += col['columnName'] + "=None,"
		cmd_str = 'model.'+table+'('+col_str[:len(col_str)-1]+')'
#		print str(i).rjust(3,'0') + ": " + cmd_str
		if table in ['User','Group','Permission','VisitIdentity']:
			pass
		else:
			test_table = eval(cmd_str)
			test_table.delete(test_table.id)
		del(cols)
		del(col_str)
		del(cmd_str)

def test_model(test_model):
	for m in dir(test_model):
		print m
		if m in ('SQLObject','InheritableSQLObject'): continue	
		c = getattr(test_model,m)
		if isinstance(c, type) and issubclass(c,sqlobject.SQLObject):
			test = c()
		return 1

def get_col_dict(the_model,table_name):
	table = getattr(the_model,table_name)
	col_vals = {}
	cols = []
	for attrib in dir(table):
		try:
			if isinstance(getattr(table,attrib),property):
				cols.append(attrib)
		except AttributeError:
			pass
	for col in cols:
		col_vals[col] = 'TEST'
	return col_vals
	
def test_care2x_model():
	tables = dir(model)
	i = 1
	for table in tables:
		if table in ('SQLObject','InheritableSQLObject'):
			pass
		else:
			c = getattr(model,table)
			if isinstance(c, type) and issubclass(c,SQLObject):
				print str(i) +" "+table
				i = i+1
				col_dict = get_col_dict(model,table)
				# Construct our class call statement
				exec_stmt = 'model.' + table + '('
				for col in col_dict:
					exec_stmt += col + "='" + col_dict[col] + "',"
				exec_stmt = exec_stmt[:len(exec_stmt)-1] + ')'
				tmp_table = eval(exec_stmt)
			else:
				pass
