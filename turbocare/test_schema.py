from mysql_schema import MySQLSchema

db = MySQLSchema(dbname='care2x')
db.make_table_definitions()
r = db.tables[0]
print "NAME: " + r['name']
print "======================================"
print "INDEXES: %d"  % len(r['defn']['indexes'])
print "--> Index 1: " + repr(r['defn']['indexes'][0])
print "--> Index 2: " + repr(r['defn']['indexes'][1])
print "COLUMNS: %d" % len(r['defn']['fields'])
print "--> Col 1: " +repr( r['defn']['fields'][0])
print "--> Col 2: " +repr( r['defn']['fields'][3])