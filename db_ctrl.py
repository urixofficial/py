import sqlite3

# Connect to DB
db = sqlite3.connect('cartridge.db')

# Create a cursor
c = db.cursor()

def create_table():
	# Create a table
	c.execute('''
		CREATE TABLE cartridges (
			model text,
			count integer
			)
		''')
	# Commit our command
	db.commit()

def insert_value(data):
	# Insert a data into the table
	c.execute('''
		INSERT INTO cartridges VALUES {}
		'''.format(data))
	# Commit our command
	db.commit()

def query_table():
	# Query the DB
	c.execute('SELECT rowid, * FROM cartridges')
	#c.fetchone()
	#c.fetchmany(3)
	items = c.fetchall()

	print('|{:<3}|{:<8}|{:<8}|'.format('ID', 'Model', 'Count'))
	print('|{:-<3}|{:-<8}|{:-<8}|'.format('', '', ''))
	for item in items:
		print('|{:0>3}|{:<8}|{:<8}|'.format(*item))

#insert_value(('53A', 3))

query_table()
# Close our connection
db.close()